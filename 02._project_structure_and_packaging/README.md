# Session 2: Project Structure & Python Packaging

**Week 36 | Python Elective 2026 Fall**

> Build a tiny Python project from scratch — `pyproject.toml`, a package folder, a dependency, an entry point — then open the mistral-vibe fork and recognise the exact same anatomy at full scale.

---

## Learning Goals

- Build a minimal installable Python project from an empty folder using `uv`
- Read and interpret a `pyproject.toml` file: `[project]`, `[project.scripts]`, `[build-system]`
- Know what entry points are and how they make a CLI command available after install
- Understand what a lock file (`uv.lock`) is and why it isn't written by hand
- Recognise `pip`, `requirements.txt`, and manual virtual environments when you meet them in other projects, and explain what problems `uv` solves over them
- Navigate a real codebase (mistral-vibe) without getting lost

---

## Before Class

- Your fork of mistral-vibe must be cloned and running locally (from session 1)
- Skim the `pyproject.toml` in your fork — note any fields you don't understand yet; bring questions
- Optional: read [Python Packaging User Guide — pyproject.toml](https://packaging.python.org/en/latest/guides/writing-pyproject-toml/)

---

## Today's Teachings

### Part 1 — Build a project from scratch (live demo, then you follow)

We build a one-command CLI called `milspend` from an empty folder. It reports a
country's military expenditure as a share of GDP, pulled live from the World
Bank's open-data API (source: SIPRI). The app logic is a few lines; the point
is everything around it.

Demo project and full walkthrough:
[demos_from_teachings / 02._project_structure_and_packaging](https://github.com/EK-Python-Elective/demos_from_teachings/tree/session-2-packaging-demo/02._project_structure_and_packaging)

The build, step by step:

1. `uv init --python 3.12 milspend` — what did `uv` create? (`pyproject.toml`, `README.md`, `.python-version`, a package folder)
2. Reshape to a **flat layout** (package folder next to `pyproject.toml`, no `src/`) — the same layout mistral-vibe uses
3. Write `main()` — a small function that fetches JSON over HTTP and prints a table
4. Wire up `pyproject.toml` by hand:
   - `[project]` — name, version, `requires-python`, `dependencies`
   - `[project.scripts]` — `milspend = "milspend.cli:main"` — this is what makes `milspend` a terminal command
   - `[build-system]` — the build backend (we use `hatchling`, like mistral-vibe)
5. `uv add httpx` — watch `pyproject.toml`, `uv.lock`, and `.venv/` change
6. `uv run milspend UKR` — the entry point runs (try `DNK`, `SWE`, `USA`, `RUS`)
7. Optional: `uv build` — see the `.whl` that `pip install` would download

By the end, every field we're about to see in mistral-vibe's `pyproject.toml`
has already appeared in miniature.

### Part 2 — The same anatomy in mistral-vibe

Open your fork's `pyproject.toml` next to `milspend`'s and map it field by field:

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

| In `milspend` | In mistral-vibe |
|---|---|
| `milspend/` next to `pyproject.toml` | `vibe/` next to `pyproject.toml` (same flat layout) |
| 1 dependency (`httpx`) | ~60 dependencies, all `==`-pinned (`httpx` is one of them) |
| `milspend = "milspend.cli:main"` | `vibe = "vibe.cli.entrypoint:main"` (+ `vibe-acp`, `vibe-app-server`) |
| `[build-system]` → hatchling | hatchling + hatch-vcs (version from git tags) |
| no tool config yet | `[tool.ruff]`, `[tool.pyright]`, … (session 3) |

- Aside: `setup.py` is the legacy predecessor of `pyproject.toml` — you'll see it in older repos, but new projects declare everything in `pyproject.toml`.

### Entry points — the one trick

- How does typing `vibe` (or `milspend`) in the terminal call Python code?
- `<command> = "<module>:<function>"` in `[project.scripts]`. At install time the build backend writes a launcher script onto your `PATH` that imports the module and calls the function.
- Trace it: shell → launcher script → `main()`.

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

[Scavenger Hunt in pyproject.toml](exercise_scavenger_hunt.md) — you now know what `[project.scripts]` *is*, so "what function does `vibe` call?" is a lookup, not a mystery.

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
