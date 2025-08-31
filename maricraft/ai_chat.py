import os
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Literal, Optional

from pydantic import BaseModel, Field, confloat, conint


@dataclass
class AIConfig:
    model: str
    base_url: str = "https://openrouter.ai/api/v1"
    require_parameters: bool = True
    temperature: float = 0.2
    attach_log: bool = False
    log_path: str = "log.txt"
    log_tail_lines: int = 250


def _load_env():
    try:
        from dotenv import load_dotenv

        load_dotenv()
    except Exception:
        pass


def _get_api_key() -> Optional[str]:
    _load_env()
    return os.getenv("OPENROUTER_API_KEY")


def _provider_prefs(require_parameters: bool):
    prefs = {"require_parameters": bool(require_parameters)}
    return prefs


def _response_format(schema_name: str, schema: dict) -> dict:
    return {
        "type": "json_schema",
        "json_schema": {
            "name": schema_name,
            "strict": True,
            "schema": schema,
        },
    }


def _tail_file(path: Path, max_lines: int = 250) -> str:
    try:
        if not path.exists():
            return ""
        # Efficient line tail
        with path.open("rb") as f:
            # Read last ~64KB chunk and tail lines from it
            f.seek(0, os.SEEK_END)
            size = f.tell()
            read_size = min(65536, size)
            f.seek(size - read_size)
            data = f.read().decode("utf-8", errors="ignore")
        lines = data.splitlines()[-max_lines:]
        return "\n".join(lines)
    except Exception:
        return ""


def _schema_create() -> tuple[str, dict]:
    return (
        "minecraft_command_plan",
        {
            "type": "object",
            "properties": {
                "commands": {
                    "type": "array",
                    "items": {"type": "string"},
                    "minItems": 1,
                    "description": "One command per line, ready for Minecraft chat.",
                },
                "explanation": {"type": "string"},
                "chat_key": {"type": "string", "enum": ["t", "/"]},
                "delay_ms": {
                    "type": "integer",
                    "minimum": 50,
                    "maximum": 2000,
                    "default": 150,
                },
                "tags": {"type": "array", "items": {"type": "string"}, "uniqueItems": True},
            },
            "required": ["commands"],
            "additionalProperties": False,
        },
    )


def _schema_debug() -> tuple[str, dict]:
    return (
        "minecraft_command_fix",
        {
            "type": "object",
            "properties": {
                "corrected_commands": {
                    "type": "array",
                    "items": {"type": "string"},
                    "minItems": 1,
                },
                "explanation": {"type": "string"},
                "confidence": {"type": "number", "minimum": 0, "maximum": 1},
                "chat_key": {"type": "string", "enum": ["t", "/"]},
                "delay_ms": {"type": "integer", "minimum": 50, "maximum": 2000},
                "follow_up": {"type": "array", "items": {"type": "string"}},
            },
            "required": ["corrected_commands"],
            "additionalProperties": False,
        },
    )


Mode = Literal["create", "debug"]


class AIChatController:
    """High-level interface for AI chat operations with structured outputs.

    Uses OpenAI Agents SDK with LiteLLM + OpenRouter under the hood.
    """

    def __init__(self, logger=None):
        self.logger = logger
        self._agent = None
        self._session = None
        self._mode: Mode | None = None
        self._model_id: str | None = None
        self._api_key: Optional[str] = None

    def _log(self, msg: str):
        try:
            if self.logger is not None:
                self.logger.log(msg)
        except Exception:
            pass

    def _ensure_agent(self, mode: Mode, cfg: AIConfig):
        if self._agent and self._mode == mode and self._model_id == cfg.model:
            return

        self._mode = mode
        self._model_id = cfg.model
        self._api_key = _get_api_key()
        if not self._api_key:
            raise RuntimeError("OPENROUTER_API_KEY is not set (check your .env)")

        # Import here to avoid hard dependency for non-AI usage
        from agents import Agent, SQLiteSession, ModelSettings, set_tracing_disabled
        from agents.extensions.models.litellm_model import LitellmModel

        set_tracing_disabled(True)

        # Per-mode persistent session id
        session_id = f"maricraft_{mode}"
        self._session = SQLiteSession(session_id)

        # Attribution headers (optional but recommended by OpenRouter)
        extra_headers = {}
        if os.getenv("OR_SITE_URL"):
            extra_headers["HTTP-Referer"] = os.getenv("OR_SITE_URL")
        if os.getenv("OR_APP_NAME"):
            extra_headers["X-Title"] = os.getenv("OR_APP_NAME")

        self._model_settings = ModelSettings(
            temperature=cfg.temperature,
            extra_args={
                # OpenRouter structured outputs
                # Will be updated per-call with schema
                # Provider routing
                "provider": _provider_prefs(cfg.require_parameters),
                # Optional attribution
                **({"extra_headers": extra_headers} if extra_headers else {}),
            },
        )

        # Define typed output models for structured outputs
        class CreateOutput(BaseModel):
            commands: list[str]
            explanation: Optional[str] = None
            chat_key: Optional[Literal["t", "/"]] = None
            delay_ms: Optional[conint(ge=50, le=2000)] = None
            tags: Optional[list[str]] = None

        class DebugOutput(BaseModel):
            corrected_commands: list[str]
            explanation: Optional[str] = None
            confidence: Optional[confloat(ge=0.0, le=1.0)] = None
            chat_key: Optional[Literal["t", "/"]] = None
            delay_ms: Optional[conint(ge=50, le=2000)] = None
            follow_up: Optional[list[str]] = None

        instructions = (
            "You are a Minecraft command assistant. Respond using structured outputs only. "
            "Commands must be valid for Minecraft chat; one command per array item. "
            "No extra commentary outside the structured output."
        )

        self._agent = Agent(
            name="Maricraft AI",
            instructions=instructions,
            model=LitellmModel(
                model=cfg.model,
                base_url=cfg.base_url,
                api_key=self._api_key,
            ),
            model_settings=self._model_settings,
            output_type=CreateOutput if mode == "create" else DebugOutput,
        )

        self._Runner = None
        # Lazy import Runner to keep surface small
        from agents import Runner as _Runner

        self._Runner = _Runner

    def _build_prompt(self, mode: Mode, user_message: str, attach_log: bool, log_path: str, tail_lines: int) -> str:
        base = []
        if mode == "create":
            base.append(
                "Task: Generate Minecraft chat commands for the user's goal. "
                "Do not include comments or explanations in the commands themselves."
            )
        else:
            base.append(
                "Task: Correct the provided Minecraft command(s). If an error is present in the logs, "
                "propose corrected commands."
            )
        base.append(f"User: {user_message}")
        if mode == "debug":
            # Let the user paste the failing command into the message; we also attach logs below
            if attach_log:
                excerpt = _tail_file(Path(log_path), max_lines=tail_lines)
                if excerpt:
                    base.append("Recent log excerpt:\n" + excerpt)
        return "\n\n".join(base)

    def _schema_for_mode(self, mode: Mode) -> tuple[str, dict]:
        return _schema_create() if mode == "create" else _schema_debug()

    def send(self, mode: Mode, cfg: AIConfig, user_message: str) -> dict:
        """Send a message and return a dict:
        {
          "parsed": dict | None,
          "raw": str,
          "error": str | None,
        }
        """

        self._ensure_agent(mode, cfg)
        # Rely on Agents SDK output_type to enable structured outputs.
        # Provider routing is already set via model_settings.extra_args.

        prompt = self._build_prompt(
            mode,
            user_message=user_message,
            attach_log=cfg.attach_log,
            log_path=cfg.log_path,
            tail_lines=cfg.log_tail_lines,
        )

        self._log(f"AI request mode={mode} model={cfg.model} require_parameters={cfg.require_parameters}")
        self._log(f"AI prompt: {user_message[:2000]}")

        try:
            result = self._Runner.run_sync(
                self._agent,
                prompt,
                session=self._session,
                # The SDK's Runner uses the agent's model_settings, but many versions allow
                # passing a per-call override via Agent.model_settings. To keep compatibility,
                # we temporarily swap the settings.
            )
        except Exception as e:
            return {"parsed": None, "raw": "", "error": str(e)}

        out = getattr(result, "final_output", None)
        parsed, raw, err = None, None, None
        try:
            if isinstance(out, str):
                raw = out
                parsed = json.loads(out)
            elif hasattr(out, "model_dump"):
                parsed = out.model_dump()
                raw = json.dumps(parsed)
            elif isinstance(out, dict):
                parsed = out
                raw = json.dumps(out)
            else:
                raw = str(out)
                parsed = None
        except Exception as ex:
            err = f"Failed to parse output: {ex}"
        if err:
            self._log(f"AI response (raw): {str(out)[:4000]}")
            self._log(err)
        return {"parsed": parsed, "raw": raw, "error": err}
