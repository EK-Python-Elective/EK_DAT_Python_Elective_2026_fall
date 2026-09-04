# Session 2: Project Structure, Packaging & Tooling

**Week 37 | Python Elective 2026 Fall**

> Build a tiny Python project from scratch — `pyproject.toml`, a package folder, a dependency, an entry point — then open the mistral-vibe fork and recognise the exact same anatomy at full scale. Then configure that fork's tooling: `uv` beyond the basics, `ruff` for linting/formatting, `pyright` for type checking.

---

## Learning Goals

- Build a minimal installable Python project from an empty folder using `uv`
- Read and interpret a `pyproject.toml` file: `[project]`, `[project.scripts]`, `[build-system]`, `[tool.*]`
- Know what entry points are and how they make a CLI command available after install
- Understand what a lock file (`uv.lock`) is and why it isn't written by hand
- Navigate a real codebase (mistral-vibe) without getting lost
- Use `uv` confidently beyond install: dev dependencies, running scripts, global tools
- Use `ruff` to lint and auto-format Python code
- Understand what static type checking is and how to run `pyright`
- Configure these tools in your fork's `pyproject.toml`, and understand why consistent tooling matters in a team and open source project

---

## Before Class

- Your fork of mistral-vibe must be cloned and running locally (from session 1)
- Skim the `pyproject.toml` in your fork — note any fields you don't understand yet; bring questions
- Make sure `uv` is installed (`uv --version`)
- Optional: read [Python Packaging User Guide — pyproject.toml](https://packaging.python.org/en/latest/guides/writing-pyproject-toml/) and/or the [ruff docs](https://docs.astral.sh/ruff/) introduction

---

## Today's Teachings

### Part 1 — Build a project from scratch (live demo, then you follow)

We build a one-command CLI called `qr` from an empty folder. It prints a QR
code for whatever text you give it, right in the terminal (scan it with your
phone). No network, no files — the whole app is one call to a library. The
point is everything around it.

Demo project and full walkthrough:
[demos_from_teachings / 02._project_structure_and_packaging](https://github.com/EK-Python-Elective/demos_from_teachings/tree/session-2-packaging-demo/02._project_structure_and_packaging)

The build, step by step:

1. `uv init --python 3.12 qr` — what did `uv` create? (`pyproject.toml`, `README.md`, `.python-version`, a package folder)
2. Reshape to a **flat layout** (package folder next to `pyproject.toml`, no `src/`) — the same layout mistral-vibe uses
3. Write `main()` — three lines: read the text from `sys.argv`, hand it to the `segno` library, print the code
4. Wire up `pyproject.toml` by hand:
   - `[project]` — name, version, `requires-python`, `dependencies`
   - `[project.scripts]` — `qr = "qr.cli:main"` — this is what makes `qr` a terminal command
   - `[build-system]` — the build backend (we use `hatchling`, like mistral-vibe)
5. `uv add segno` — watch `pyproject.toml`, `uv.lock`, and `.venv/` change
6. `uv run qr "https://kea.dk"` — the entry point runs
7. Optional: `uv build` — see the `.whl` that `pip install` would download

By the end, every field we're about to see in mistral-vibe's `pyproject.toml`
has already appeared in miniature.

### Part 2 — The same anatomy in mistral-vibe

Open your fork's `pyproject.toml` next to `qr`'s and map it field by field:

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

| In `qr` | In mistral-vibe |
|---|---|
| `qr/` next to `pyproject.toml` | `vibe/` next to `pyproject.toml` (same flat layout) |
| 1 dependency (`segno`), nothing under it | ~60 dependencies, all `==`-pinned, hundreds of transitive |
| `qr = "qr.cli:main"` | `vibe = "vibe.cli.entrypoint:main"` (+ `vibe-acp`, `vibe-app-server`) |
| `[build-system]` → hatchling | hatchling + hatch-vcs (version from git tags) |
| no tool config yet | `[tool.ruff]`, `[tool.pyright]`, … (part 3, below) |

Pick a dependency in the fork's list that you'll actually meet later — `httpx`
(session 6), `pydantic` (session 3) — and note it got there the same way you
just added `segno`: `uv add`, then it's pinned in `uv.lock`.

- Aside: `setup.py` is the legacy predecessor of `pyproject.toml` — you'll see it in older repos, but new projects declare everything in `pyproject.toml`.

### Entry points — the one trick

- How does typing `vibe` (or `qr`) in the terminal call Python code?
- `<command> = "<module>:<function>"` in `[project.scripts]`. At install time the build backend writes a launcher script onto your `PATH` that imports the module and calls the function.
- Trace it: shell → launcher script → `main()`.

### Exploring the module structure

- Walk through the top-level modules in mistral-vibe together
- Identify: where is the CLI defined? Where are API calls made? Where is config loaded?

### Part 3 — Configure the tooling: uv, ruff, pyright

**Everything from here on is about your mistral-vibe fork — not `qr`.** `cd` into your fork before running anything below. It's the same `pyproject.toml` you had open in Part 2; now it's the `[tool.*]` sections.

> ⚠️ **Branch first.** Parts 1 and 2 didn't change any files. Some of what follows does (`ruff --fix`, `ruff format`, adding a dependency) — so before you run any of it, make sure you're on a branch off `main` in your fork, not `main` itself (see session 1, "Working on a branch — always"): `git checkout -b exercise/session-02`.

#### uv — beyond basic install

```bash
uv sync                        # install all deps from uv.lock
uv add httpx                   # add a dependency
uv add --dev pytest            # add a dev-only dependency
uv run python script.py        # run a script in the project venv
uv run vibe                    # run the CLI from source
uv tool install ruff           # install a tool globally (outside any project)
```

#### ruff — linting and formatting in one

- Replaces: `flake8`, `isort`, `black`, `pyupgrade` and more
- Extremely fast (written in Rust)
- Run linting: `uv run ruff check .`
- Auto-fix: `uv run ruff check --fix .`
- Format: `uv run ruff format .`
- Configure in `pyproject.toml`:
```toml
[tool.ruff]
line-length = 100
target-version = "py312"

[tool.ruff.lint]
select = ["E", "F", "I", "UP"]
```

#### Type checking with pyright

- Python is dynamically typed — but type hints + a checker catch bugs at "compile time"
- `pyright` / `pylance`: fast, used by VS Code by default — and what mistral-vibe uses
- `mypy`: the classic alternative, worth knowing about
```bash
uv run pyright
```
- How to read type errors and what they mean

#### Configuring your fork's tooling

- Add or adjust the `[tool.ruff]` and `[tool.pyright]` sections in your fork's `pyproject.toml`
- Run a full lint pass and fix all warnings

#### Pre-commit hooks (preview)

- Brief intro to `pre-commit` — automatically run ruff before every commit
- We will use this properly in a later session on testing and CI

### Exercise

[Scavenger Hunt in pyproject.toml](exercise_scavenger_hunt.md) — you now know what `[project.scripts]` *is*, so "what function does `vibe` call?" is a lookup, not a mystery.

---

## After Class

- Draw a simple diagram of the mistral-vibe module structure (boxes and arrows is fine)
- Find the function that is called first when you run `vibe` — trace it from the entry point
- Add one dependency to your fork using `uv add <package>` and observe what changes in `pyproject.toml` and `uv.lock`
- Come to next class ready to explain what `uv sync` does and why it matters
- Run `uv run ruff check --fix .` and `uv run ruff format .` on your entire fork — commit the result
- Inspect the existing `[tool.ruff]` section in `pyproject.toml` — find at least 3 configured rules and write a short comment (in your notes, not the file) explaining what each one does, then extend the ruff configuration with one new rule of your own
- Try to introduce a deliberate type error and confirm that `pyright` catches it
- Optional: set up the `ruff` VS Code extension (or equivalent for your editor)

---

## Optional

For students who want to go further. None of this is required — pick whatever looks interesting.

- [optional] [Python Packaging User Guide — Packaging Python Projects](https://packaging.python.org/en/latest/tutorials/packaging-projects/) — the end-to-end tutorial: turn a folder of code into a built package and install it back.
- [optional] [PEP 621](https://peps.python.org/pep-0621/) — the spec for the `[project]` table in `pyproject.toml`. Short, and it's the source of truth for every field in the scavenger hunt.
- [optional] [PEP 517 / PEP 518](https://peps.python.org/pep-0518/) — why `pyproject.toml` exists at all, and what a "build backend" is.
- [optional] [Entry points specification](https://packaging.python.org/en/latest/specifications/entry-points/) — the mechanism behind `[project.scripts]` and how typing `vibe` ends up calling Python code.
- [optional] [Astral — uv blog post](https://astral.sh/blog/uv) — the design rationale for uv and how it compares to pip and Poetry.
- [optional] [Ruff — Rules reference](https://docs.astral.sh/ruff/rules/) — every lint rule with a rationale and a before/after example; the menu you pick a `select` set from.
- [optional] [uv — Concepts](https://docs.astral.sh/uv/concepts/) — projects, the lockfile, the resolver, and tools vs. project dependencies.
- [optional] [pyright — Configuration](https://microsoft.github.io/pyright/#/configuration) — every `[tool.pyright]` setting and what each strictness level turns on.
- [optional] [pre-commit.com](https://pre-commit.com/) — the hook framework we preview in class; the quickstart gets ruff running on every commit in a few minutes.
