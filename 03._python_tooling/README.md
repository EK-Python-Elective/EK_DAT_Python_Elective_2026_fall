# Session 3: Python Tooling — uv, ruff, and the Modern Ecosystem

**Week 38 | Python Elective 2026 Fall**

> Deep dive into `uv` as package manager, `ruff` for linting/formatting, `mypy`/`pyright` for type checking. Students configure their fork's tooling.

---

## Learning Goals

- Use `uv` confidently for dependency management and virtual environments
- Use `ruff` to lint and auto-format Python code
- Understand what static type checking is and how to run `mypy` or `pyright`
- Configure these tools in `pyproject.toml` for your fork
- Understand why consistent tooling matters in a team and open source project

---

## Before Class

- Make sure `uv` and `ruff` are installed: `uv --version` and `ruff --version`
- Run `ruff check .` inside your fork — what does it report?
- Optional: read the [ruff docs](https://docs.astral.sh/ruff/) introduction

---

## Today's Teachings

### uv — beyond basic install
```bash
uv sync                        # install all deps from uv.lock
uv add httpx                   # add a dependency
uv add --dev pytest            # add a dev-only dependency
uv run python script.py        # run a script in the project venv
uv run vibe                    # run the CLI from source
uv tool install ruff           # install a tool globally
```

### ruff — linting and formatting in one
- Replaces: `flake8`, `isort`, `black`, `pyupgrade` and more
- Extremely fast (written in Rust)
- Run linting: `ruff check .`
- Auto-fix: `ruff check --fix .`
- Format: `ruff format .`
- Configure in `pyproject.toml`:
```toml
[tool.ruff]
line-length = 100
target-version = "py312"

[tool.ruff.lint]
select = ["E", "F", "I", "UP"]
```

### Type checking with mypy / pyright
- Python is dynamically typed — but type hints + a checker catch bugs at "compile time"
- `mypy`: the classic checker
- `pyright` / `pylance`: faster, used by VS Code by default
```bash
uv run mypy src/
```
- How to read type errors and what they mean

### Configuring your fork's tooling
- Students add or adjust `[tool.ruff]` and `[tool.mypy]` sections in their `pyproject.toml`
- Run a full lint pass and fix all warnings

### Pre-commit hooks (preview)
- Brief intro to `pre-commit` — automatically run ruff before every commit
- We will use this properly in a later session on testing and CI

---

## After Class

- Run `ruff check --fix .` and `ruff format .` on your entire fork — commit the result
- Add a `[tool.ruff]` section to your `pyproject.toml` with at least 3 configured rules
- Try to introduce a deliberate type error and confirm that `mypy` catches it
- Optional: set up the `ruff` VS Code extension (or equivalent for your editor)
