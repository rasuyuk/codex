# Repository Guidelines
The Codex agents repository is still being scaffolded, so use this guide to keep new work consistent and ready for collaboration.

## Project Structure & Module Organization
- Place all runnable code under `src/` and keep module paths importable (add an empty `__init__.py` when creating a new package).
- Store individual agent logic in `src/agents/<agent_name>/`, shared utilities in `src/shared/`, and CLI orchestration in `src/cli/`.
- Check configuration and prompt assets into `configs/` and `assets/` respectively; document pipelines that cross module boundaries in `docs/`.
- Mirror the module layout inside `tests/` (e.g., `tests/agents/test_researcher.py`) to make ownership obvious.

## Build, Test, and Development Commands
- `python -m venv .venv` — create a local virtual environment; commit only the activation scripts in `.gitignore`.
- `source .venv/bin/activate` — enable the environment for all development commands.
- `pip install -r requirements.txt` (or `pip install -e .` once `pyproject.toml` lands) — install runtime and tooling dependencies.
- `pytest tests` — run the full test suite before pushing.
- `ruff check src tests` and `black src tests` — lint and format; run both until they exit cleanly.

## Coding Style & Naming Conventions
Use four-space indentation, prefer f-strings for formatting, and type-annotate public functions. Agent packages follow snake_case module names while class names stay in PascalCase (`ResearchAgent`). Keep functions focused: short orchestration helpers in `src/cli/` and longer running loops in the agent package. Run `ruff` and `black` prior to every commit so reviewers only see intentional diffs.

## Testing Guidelines
Author tests with `pytest`; name files `test_<module>.py` and test functions `test_<behavior>`. Target 85% coverage or higher for new code and include regression tests whenever a bug is fixed. For async behaviors, lean on `pytest.mark.asyncio`. Provide fixtures in `tests/conftest.py` instead of repeating setup in multiple modules.

## Commit & Pull Request Guidelines
Follow Conventional Commits (`feat`, `fix`, `chore`, etc.) and keep the subject <= 72 characters (e.g., `feat(agent): add planning loop`). Each pull request needs: a concise summary, linked issue or ticket, test evidence (`pytest` output or screenshots for manual flows), and callouts for TODOs or follow-up work. Request at least one reviewer familiar with the touched agent before merging.

## Security & Configuration Tips
Store secrets in local `.env` files that mirror `configs/example.env` and exclude them from commits. Document any new external integrations under `docs/security.md` with scopes, tokens, and rotation plans so the team can audit changes quickly.
