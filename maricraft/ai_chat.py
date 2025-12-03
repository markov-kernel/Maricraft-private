"""AI chat assistant for Minecraft command generation and debugging."""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Literal, Optional

from pydantic import BaseModel, confloat, conint

from .logger import LoggerProtocol


@dataclass
class AIConfig:
    """Configuration for AI chat operations."""
    model: str
    base_url: str = "https://openrouter.ai/api/v1"
    require_parameters: bool = True
    temperature: float = 0.2
    attach_log: bool = False
    log_path: str = "log.txt"
    log_tail_lines: int = 250


Mode = Literal["create", "debug"]


def _load_env() -> None:
    """Load environment variables from .env file if available."""
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except Exception:
        pass


def _get_api_key() -> Optional[str]:
    """Get the OpenRouter API key from environment."""
    _load_env()
    return os.getenv("OPENROUTER_API_KEY")


def _provider_prefs(require_parameters: bool) -> Dict[str, bool]:
    """Build provider preferences dict for OpenRouter."""
    return {"require_parameters": bool(require_parameters)}


def _tail_file(path: Path, max_lines: int = 250) -> str:
    """Read the last N lines from a file efficiently."""
    try:
        if not path.exists():
            return ""
        # Efficient line tail: read last ~64KB chunk
        with path.open("rb") as f:
            f.seek(0, os.SEEK_END)
            size = f.tell()
            read_size = min(65536, size)
            f.seek(size - read_size)
            data = f.read().decode("utf-8", errors="ignore")
        lines = data.splitlines()[-max_lines:]
        return "\n".join(lines)
    except Exception:
        return ""


class AIChatController:
    """High-level interface for AI chat operations with structured outputs.

    Uses OpenAI Agents SDK with LiteLLM + OpenRouter under the hood.
    """

    def __init__(self, logger: Optional[LoggerProtocol] = None) -> None:
        self.logger = logger
        self._agent: Any = None
        self._session: Any = None
        self._mode: Optional[Mode] = None
        self._model_id: Optional[str] = None
        self._api_key: Optional[str] = None
        self._model_settings: Any = None
        self._Runner: Any = None

    def _log(self, msg: str) -> None:
        """Log a message if logger is available."""
        try:
            if self.logger is not None:
                self.logger.log(msg)
        except Exception:
            pass

    def _ensure_agent(self, mode: Mode, cfg: AIConfig) -> None:
        """Initialize or reinitialize the AI agent if needed."""
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
        extra_headers: Dict[str, str] = {}
        if os.getenv("OR_SITE_URL"):
            extra_headers["HTTP-Referer"] = os.getenv("OR_SITE_URL")
        if os.getenv("OR_APP_NAME"):
            extra_headers["X-Title"] = os.getenv("OR_APP_NAME")

        self._model_settings = ModelSettings(
            temperature=cfg.temperature,
            extra_args={
                "provider": _provider_prefs(cfg.require_parameters),
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

        # Lazy import Runner to keep surface small
        from agents import Runner as _Runner
        self._Runner = _Runner

    def _build_prompt(
        self,
        mode: Mode,
        user_message: str,
        attach_log: bool,
        log_path: str,
        tail_lines: int,
    ) -> str:
        """Build the prompt for the AI based on mode and context."""
        base: list[str] = []
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
        if mode == "debug" and attach_log:
            excerpt = _tail_file(Path(log_path), max_lines=tail_lines)
            if excerpt:
                base.append("Recent log excerpt:\n" + excerpt)
        return "\n\n".join(base)

    def send(self, mode: Mode, cfg: AIConfig, user_message: str) -> Dict[str, Any]:
        """Send a message to the AI and return the response.

        Args:
            mode: Either "create" for new commands or "debug" for fixing commands
            cfg: AI configuration settings
            user_message: The user's message/request

        Returns:
            Dict with keys:
                - parsed: Parsed structured output as dict, or None
                - raw: Raw string response
                - error: Error message if any, or None
        """
        self._ensure_agent(mode, cfg)

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
            )
        except Exception as e:
            return {"parsed": None, "raw": "", "error": str(e)}

        out = getattr(result, "final_output", None)
        parsed: Optional[Dict[str, Any]] = None
        raw: Optional[str] = None
        err: Optional[str] = None

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
