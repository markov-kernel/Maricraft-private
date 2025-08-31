# Design Polish Gate

This repo includes a lightweight, repeatable flow to keep visual quality high and consistent across pages.

## Inputs: `polish_goal/`
- Drop 5–10 screenshots of world‑class sites into `polish_goal/` at repo root.
- On `dev`, `build`, and `test`, these images are synced to `public/polish_goal/` and ingested by the app.

## Review: `/design-review`
- Visit `/design-review` while developing to see a gallery of the target screenshots.
- Each tile extracts a simple color palette. Click a swatch to apply it as the live `--accent` token.
- Use the component preview to ensure buttons, inputs, and blocks feel balanced with the chosen accent.
- Accent selection persists locally (via `localStorage`) during development.

### QA Overlay
- Append `?qa=1` to any route to display a non-interactive overlay showing 24px baseline rhythm and a 12‑column container grid. Example: `/neural-ledger?qa=1`.
- Helpful for aligning hero copy, media, and card grids to the same rhythm.

## Tokens & Tailwind
- Core design tokens live in `src/styles/globals.css` and are mapped into Tailwind via `tailwind.config.js`.
- Variables include color roles (background, foreground, primary, secondary, accent), radius, shadows, and container spacing.

## Guardrails
- Playwright specs attach console and request failure handlers to catch regressions early.
- `tests/home.spec.ts` includes a screenshot gate for `/` to keep changes intentional.
- `tests/design-review.spec.ts` validates the design review page loads and the accent can be applied.
- `tests/a11y.spec.ts` runs Axe on `/`, `/neural-ledger`, and `/contact` and fails on serious/critical issues.

## Working Mode
- Keep changes to tokens deliberate and tested; when updating the home hero visually, run `npm run test:update` to refresh baselines.
- If a page introduces a new flow or a significant visual component, add a small spec to cover it.
