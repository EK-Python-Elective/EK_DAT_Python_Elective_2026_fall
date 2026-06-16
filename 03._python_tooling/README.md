# Session 3: Python Tooling — uv, ruff, and the Modern Ecosystem

**Week 37 | Python Elective 2026 Fall**

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

- Make sure `uv` is installed: `uv --version`. Then verify ruff is available in the project: `uv run ruff --version`
- Run `uv run ruff check .` inside your fork — what does it report?
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

### Type checking with pyright
- Python is dynamically typed — but type hints + a checker catch bugs at "compile time"
- `pyright` / `pylance`: fast, used by VS Code by default — and what mistral-vibe uses
- `mypy`: the classic alternative, worth knowing about
```bash
uv run pyright
```
- How to read type errors and what they mean

### Configuring your fork's tooling
- Students add or adjust `[tool.ruff]` and `[tool.pyright]` sections in their `pyproject.toml`
- Run a full lint pass and fix all warnings

### Pre-commit hooks (preview)
- Brief intro to `pre-commit` — automatically run ruff before every commit
- We will use this properly in a later session on testing and CI

---

## After Class

- Run `uv run ruff check --fix .` and `uv run ruff format .` on your entire fork — commit the result
- Inspect the existing `[tool.ruff]` section in `pyproject.toml` — find at least 3 configured rules and write a short comment (in your notes, not the file) explaining what each one does, then extend the ruff configuration with one new rule of your own
- Try to introduce a deliberate type error and confirm that `pyright` catches it
- Optional: set up the `ruff` VS Code extension (or equivalent for your editor)
