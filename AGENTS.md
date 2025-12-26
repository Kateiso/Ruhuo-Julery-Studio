# Repository Guidelines

## Current Direction & Scope (UI-First)
- Primary goal: rewrite the UI as a desktop app using **Flet (Python)**; keep business logic in Python services.
- **Scope right now: UI only.** Do not change `services/` or business logic unless explicitly requested.
- The existing Streamlit UI (`gui.py`, `pages/`) is **legacy**. Avoid editing it unless asked.
- UX target: Creator Tool / Dark Mode, app-style layout (left nav, center workspace, right config panel).
- Settings (API keys, model choices) should live in a separate Settings view; avoid showing keys on the main screen.
- New feature “script + shooting guidance” is **planned** but **not in scope** until requested.

## Project Structure & Module Organization
- `gui.py` is the legacy Streamlit entry point; `pages/` contains the legacy multi-page UI flows.
- Core business logic lives in `main.py` and `services/` (audio, video, captioning, LLM providers, publishing, resources).
- If adding a new Flet UI, place it under a new `app/` directory (e.g., `app/main.py`) and keep it independent of Streamlit.
- Shared utilities are in `tools/`, constants in `const/`, and configuration in `config/` (see `config/config.example.yml`).
- Assets and models are kept in folders such as `fonts/`, `bgmusic/`, `chattts/`, `fasterwhisper/`, and `sensevoice/`.
- Docs live in `docs/` (English/Japanese) and `doc/` (project notes).

## Build, Test, and Development Commands
- `pip install -r requirements.txt` installs Python dependencies.
- `streamlit run gui.py` runs the web UI locally.
- If/when Flet UI is added, run it via `flet run app/main.py` (or the chosen entry file).
- `bash setup.sh` (macOS/Linux) or `setup.bat` (Windows) performs automatic setup.
- `bash start.sh` (macOS/Linux) or `start.bat` (Windows) starts the app after setup.

## Coding Style & Naming Conventions
- Python code uses 4-space indentation; keep functions small and focused.
- Prefer descriptive, lowercase module names (`*_service.py`) and snake_case for functions/variables.
- No enforced formatter/linter is configured; keep changes consistent with existing style.

## Testing Guidelines
- There is no dedicated `tests/` directory or test runner configured.
- When adding logic, include a simple manual verification note in PRs (e.g., “ran `streamlit run gui.py` and verified page X” or “ran `flet run app/main.py` and verified view Y”).

## Commit & Pull Request Guidelines
- Commit history shows short, descriptive messages (often Chinese), e.g., “修复sensevoice”, “add docker file”. Keep messages concise and specific.
- PRs should include: purpose, key changes, how to test (commands or UI flow), and screenshots/GIFs for UI changes in `app/` (Flet) or legacy `pages/`/`gui.py`.
- Link related issues and call out config changes (new keys in `config/config.example.yml`).

## Security & Configuration Tips
- API keys for LLM, TTS, and resource providers belong in local config only; do not commit secrets.
- If adding new providers, update `config/config.example.yml` and document defaults in `docs/en/README.md`.
