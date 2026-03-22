# Session 2: Reading Code — Project Structure & Python Packaging

**Week 37 | Python Elective 2026 Fall**

> Explore `pyproject.toml`, `uv.lock`, folder layout, entry points. Understand how a Python package is installed and run. Compare to `pip`/`requirements.txt`.

---

## Learning Goals

- Understand how a modern Python project is structured on disk
- Read and interpret a `pyproject.toml` file
- Know what entry points are and how they make a CLI command available after install
- Understand the difference between `uv`, `pip`, and `requirements.txt` workflows
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
- Compare with the old `setup.py` / `requirements.txt` approach

### Entry points
- How does typing `vibe` in the terminal call Python code?
- Trace the call: shell → entry point → `__main__` or `main()` function

### uv vs pip
| | `uv` | `pip` |
|---|---|---|
| Speed | Very fast (Rust) | Slower |
| Lock file | `uv.lock` | `requirements.txt` (manual) |
| Virtualenv | Automatic | Manual |
| Editable install | `uv pip install -e .` | `pip install -e .` |

### Exploring the module structure
- Walk through the top-level modules in mistral-vibe together
- Identify: where is the CLI defined? Where are API calls made? Where is config loaded?

---

## After Class

- Draw a simple diagram of the mistral-vibe module structure (boxes and arrows is fine)
- Find the function that is called first when you run `vibe` — trace it from the entry point
- Add one dependency to your fork using `uv add <package>` and observe what changes in `pyproject.toml` and `uv.lock`
- Come to next class ready to explain what `uv sync` does and why it matters
