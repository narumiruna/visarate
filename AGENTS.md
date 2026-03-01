# Repository Guidelines

## Project Structure & Module Organization
The package lives in `src/visarate/` and exposes exchange-rate querying logic (`rate.py`) plus package exports (`__init__.py`).
Tests are in `tests/` (currently `test_rates.py`), and should mirror module behavior rather than internal implementation details.
Project-level tooling is defined in `pyproject.toml`, task shortcuts in `justfile`, and dependency resolution in `uv.lock`.

## Build, Test, and Development Commands
Use `uv` for all local workflows.

- `uv sync --all-groups`: create/update the local environment with runtime and dev dependencies.
- `just format`: run `ruff format`.
- `just lint`: run `ruff check --fix`.
- `just type`: run `ty check`.
- `just test`: run `pytest -v -s --cov=src tests`.
- `just all`: run format, lint, type, and test in sequence.
- `prek run -a`: run required pre-commit checks before submitting changes.

## Coding Style & Naming Conventions
Write Python 3.12+ code with 4-space indentation and explicit type annotations.
Follow Ruff settings in `pyproject.toml` (line length `120`, import sorting, bugbear/simplify/perf checks, and PEP 8 naming).
Use `snake_case` for functions/variables/modules, `PascalCase` for classes, and clear domain names such as `from_curr`, `to_curr`, and `converted_amount`.
Keep modules focused: add abstractions only when a current, concrete need exists.

## Testing Guidelines
Use `pytest` with `pytest-cov`; keep tests under `tests/test_*.py`.
Prefer deterministic unit tests around request construction, response parsing, retries, and edge-case validation.
Run `just test` locally and ensure coverage remains meaningful for touched paths in `src/`.

## Commit & Pull Request Guidelines
Recent history favors short, imperative commit messages (for example, `rename function`, `migrate to uv`) with optional conventional prefixes for maintenance work (for example, `chore(deps): ...`).
Keep each commit focused on one change.
PRs should include:

- What changed and why.
- Test evidence (command + outcome, e.g., `just all`).
- Any behavior/API impact and migration notes.
- Linked issue/PR context when applicable.
