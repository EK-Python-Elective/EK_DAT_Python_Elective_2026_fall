# Session 2: Reading Code — Project Structure & Python Packaging

**Week 36 | Python Elective 2026 Fall**

> Explore `pyproject.toml`, `uv.lock`, folder layout, entry points. Understand how a Python package is installed and run. Compare to `pip`/`requirements.txt`.

---

## Learning Goals

- Understand how a modern Python project is structured on disk
- Read and interpret a `pyproject.toml` file
- Know what entry points are and how they make a CLI command available after install
- Recognise `pip`, `requirements.txt`, and manual virtual environments when you meet them in other projects, and explain what problems `uv` solves over them
- Be able to navigate a real codebase without getting lost

---

## Before Class

- Your fork of mistral-vibe must be cloned and running locally (from session 1)
- Skim the `pyproject.toml` in your fork — note any fields you don't understand yet; bring questions
- Optional: read [Python Packaging User Guide — pyproject.toml](https://packaging.python.org/en/latest/guides/writing-pyproject-toml/)

---

## Today's Teachings

### Anatomy of a Python project
```
mistral-vibe/
├── pyproject.toml       # project metadata, dependencies, tool config
├── uv.lock              # locked dependency tree
├── vibe/                # flat layout — the main package
│   ├── cli/             # CLI entry point, argument parsing, Textual UI
│   ├── core/            # agent loop, tools, config, LLM backend
│   ├── acp/             # Agent Client Protocol (IDE integration)
│   └── setup/           # first-run setup wizard
└── tests/
```

### pyproject.toml deep dive
- `[project]` — name, version, requires-python, dependencies
- `[project.scripts]` — how `vibe` becomes a terminal command after install
- `[tool.ruff]`, `[tool.pyright]` — tool configuration lives here too
- Aside: `setup.py` is the legacy predecessor — you'll see it in older repos, but new projects declare everything in `pyproject.toml`

### Entry points
- How does typing `vibe` in the terminal call Python code?
- Trace the call: shell → entry point → `__main__` or `main()` function

### uv vs pip

You won't use `pip` in this course — we use `uv` everywhere. This section is so you can read the many projects (and tutorials, Dockerfiles, CI configs) that still use `pip` and `requirements.txt`, and so you can see *why* uv exists: every row below is a pip pain point that uv removes.

| | `uv` | `pip` |
|---|---|---|
| Speed | Very fast (Rust) | Slower |
| Lock file | `uv.lock` (automatic, exact) | `requirements.txt` (hand-maintained) |
| Virtualenv | Created and used automatically | You create and activate it yourself (`python -m venv .venv`, then `source .venv/bin/activate`) |
| Install from lock | `uv sync` | `pip install -r requirements.txt` |
| Add a dependency | `uv add httpx` (updates `pyproject.toml` + lock) | `pip install httpx`, then remember to edit `requirements.txt` |
| Editable install | `uv pip install -e .` | `pip install -e .` |

### Exploring the module structure
- Walk through the top-level modules in mistral-vibe together
- Identify: where is the CLI defined? Where are API calls made? Where is config loaded?

### Exercise

[Scavenger Hunt in pyproject.toml](exercise_scavenger_hunt.md)

---

## After Class

- Draw a simple diagram of the mistral-vibe module structure (boxes and arrows is fine)
- Find the function that is called first when you run `vibe` — trace it from the entry point
- Add one dependency to your fork using `uv add <package>` and observe what changes in `pyproject.toml` and `uv.lock`
- Come to next class ready to explain what `uv sync` does and why it matters

---

## Optional

For students who want to go further. None of this is required — pick whatever looks interesting.

- [optional] [Python Packaging User Guide — Packaging Python Projects](https://packaging.python.org/en/latest/tutorials/packaging-projects/) — the end-to-end tutorial: turn a folder of code into a built package and install it back.
- [optional] [PEP 621](https://peps.python.org/pep-0621/) — the spec for the `[project]` table in `pyproject.toml`. Short, and it's the source of truth for every field in the scavenger hunt.
- [optional] [PEP 517 / PEP 518](https://peps.python.org/pep-0518/) — why `pyproject.toml` exists at all, and what a "build backend" is.
- [optional] [Entry points specification](https://packaging.python.org/en/latest/specifications/entry-points/) — the mechanism behind `[project.scripts]` and how typing `vibe` ends up calling Python code.
- [optional] [Astral — uv blog post](https://astral.sh/blog/uv) — the design rationale for uv and how it compares to pip and Poetry.
