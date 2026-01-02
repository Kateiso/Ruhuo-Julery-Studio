# Repository Guidelines

## 如获珠宝·智能视频工坊

本项目是基于 MoneyPrinterPlus 的二次开发版本，专为珠宝行业定制。

### 主要改造
- **UI 品牌化**：爱马仕风格配色、自定义 Logo
- **拍摄脚本生成器**：支持多轮对话优化脚本
- **演示模式**：视频生成演示功能

### 环境配置
- **虚拟环境**：使用 `venv/` 目录
- **启动命令**：`bash start.sh`
- **配置文件**：`config/config.yml`

详细配置请参考 [docs/如获珠宝环境配置指南.md](docs/如获珠宝环境配置指南.md)

---

## Project Structure & Module Organization
- `gui.py` is the Streamlit entry point; `pages/` contains the multi-page UI.
- Core business logic lives in `main.py` and `services/`.
- `.app` 应用包位于 `app/` 目录，双击可启动应用。
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
