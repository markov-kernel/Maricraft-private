# Polish Gate: Visual Quality System

This repo ships a repeatable system to raise and verify visual polish against a clear bar, using both artifacts and runtime checks.

## What it includes

- Design artifacts under `design/`:
  - `design/polish_map.json`: brand palette, spacing, radii, shadows, typography scales (OKLCH-based).
  - `design/design_tokens.json`: enforceable tokens that map to CSS variables (see `src/styles/globals.css`).
  - `design/components/*.json`: specs for key primitives (Button, Card, GlassPanel, Input).
  - `design/visual_qa_plan.json`: viewports, pages, interactions for visual captures.
- Goal gallery: drop 5–10 reference screenshots in `polish_goal/`; they auto-sync to `/polish_goal/` and render at `/design-review` where you can live-pick an accent from a sampled palette.
- Playwright polish score: `tests/polish.spec.ts` computes a heuristic score and writes `test-results/polish_score.json` with a breakdown aligned to a professional rubric (typography, whitespace, grid, color, imagery, motion, components, responsive, performance).

## How to use

- Update targets: place polished goal screenshots in `polish_goal/` and run `npm run dev` (sync runs in `predev`). Visit `/design-review` to calibrate accent.
- Run the suite: `npm test` runs E2E across mobile/tablet/desktop and writes `test-results/polish_score.json`.
- Optional strict mode: gate merges on polish by setting `POLISH_STRICT=1` when invoking Playwright, e.g. `POLISH_STRICT=1 npm test`. This enforces:
  - Overall score ≥ 90
  - Category scores (typography, whitespace, grid, color, imagery, components, motion) ≥ 85

## Raising the bar over time

- Iterate tokens: adjust `globals.css` CSS variables in lockstep with `design/design_tokens.json`.
- Enrich specs: add/adjust `design/components/*.json` to reflect new primitives or state/variant rules.
- Expand checks: evolve `tests/polish.spec.ts` with additional heuristics (e.g., line-length caps, density guards) as patterns stabilize.

## Notes

- Accessibility and performance have dedicated specs (`tests/a11y.spec.ts`, `tests/perf.spec.ts`). The polish score complements them with aesthetic and compositional signals.
- The goal is not to “clone Apple”, but to consistently achieve the same level of discipline: clear hierarchy, calm whitespace, restrained motion, crisp imagery, and confident components.

