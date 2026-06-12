# Session 1: Kickoff — Open Source Culture & Project Setup

**Week 36 | Python Elective 2026 Fall**

> Fork `mistral-vibe`, clone locally, install with `uv`, run it. Read the README, CONTRIBUTING, and LICENSE. Discuss what open source means.

---

## Learning Goals

- Understand what open source software is and why it matters
- Know how to fork a GitHub repository and set up a local development environment
- Create a development branch and understand why you should never work directly on `main`
- Be able to install and run `mistral-vibe` using `uv`
- Read and interpret a project's README, LICENSE, and CONTRIBUTING files
- Have a basic mental model of how the mistral-vibe project is organised

---

## Before Class

- Create a [GitHub](https://github.com) account if you don't have one
- Install [uv](https://docs.astral.sh/uv/getting-started/installation/) on your machine — uv will automatically download and manage Python 3.12+ for you, so you do not need to install Python separately
- Install [Git](https://git-scm.com/) if not already installed
- Install a code editor — [VS Code](https://code.visualstudio.com/) is recommended. After installing, add these extensions:
  - [Python](https://marketplace.visualstudio.com/items?itemName=ms-python.python) — language support, debugging, venv integration
  - [Ruff](https://marketplace.visualstudio.com/items?itemName=charliermarsh.ruff) — linting and formatting on save
- Get a [Mistral API key](https://console.mistral.ai/) — free tier is sufficient
- Read the mistral-vibe README: [https://github.com/mistralai/mistral-vibe](https://github.com/mistralai/mistral-vibe)

---

## Today's Teachings

### What is open source?
- Licences: MIT, Apache 2.0, GPL — what they allow and restrict
- The open source contribution lifecycle: issues → fork → branch → PR → merge
- Why companies open source their tools (and why Mistral AI did)

### Forking and cloning
- Fork `mistralai/mistral-vibe` to your own GitHub account
- Clone your fork locally: `git clone git@github.com:<you>/mistral-vibe.git`
- Add the upstream remote: `git remote add upstream https://github.com/mistralai/mistral-vibe`

### Working on a branch — always
Never commit directly to `main`. It stays clean and in sync with upstream, making it easy to pull in future updates from the original project.

We all pin to the **same release** for the whole semester: mistral-vibe ships new releases weekly, and the course materials point at specific files and line numbers — if everyone runs a different version, those references won't match what you see. Create a `v2026-base` branch based on this semester's tag:

```bash
cd mistral-vibe
git fetch upstream --tags
git checkout -b v2026-base v2.14.1   # your stable base for the whole semester
```

**`v2026-base` is a base, not a workbench — never commit to it either.** All actual work — exercises, experiments, features — happens on branches off `v2026-base`:

```bash
git checkout -b exercise/session-04   # one branch per exercise or experiment
git checkout -b feature/my-experiment
```

So you have two branches you never commit to, each mirroring something stable: `main` mirrors upstream, `v2026-base` mirrors the course release. Everything you write lives on your own branches off `v2026-base`. The payoff: if your `v2026-base` ever drifts from the course release, it can be reset in seconds without touching a single line of your work (see below).

#### Out of sync? Reset in four commands

At the start of each session we all run `git describe --tags` on our `v2026-base` branch — the output should start with `v2.14.1`. If yours shows something else (you updated by accident, cloned late, ended up somewhere strange), don't try to repair the branch. Rename it out of the way and create a fresh one from the tag:

```bash
git fetch upstream --tags                    # make sure the course tag is available locally
git branch -m v2026-base v2026-base-old     # park your current base under a backup name
git checkout -b v2026-base v2.14.1          # fresh base from the course release
git describe --tags                          # check: should print v2.14.1
```

Nothing is deleted, and none of your work is touched: your exercise and feature branches are separate from `v2026-base`, so they survive this reset completely unchanged — there is nothing to move over. The old branch is kept as `v2026-base-old` just in case; once the new one checks out fine, you can delete it (`git branch -D v2026-base-old`). If git refuses the checkout because of uncommitted changes, run `git stash` first.

### Installing with uv

**Step 1 — install globally** so the `vibe` command is available anywhere in your terminal:
```bash
uv tool install mistral-vibe
vibe --help
```
This installs the published version from PyPI. Use this when you just want to *use* the tool.

**Step 2 — set up your local dev environment** inside your cloned fork so you can read, run, and modify the source code:
```bash
cd mistral-vibe       # your cloned fork
uv sync               # creates a local virtual environment and installs all dependencies
uv run vibe --help    # runs *your local version* of the tool
```
`uv run` always uses the local virtual environment, so changes you make to the source code are reflected immediately — no reinstall needed.

### First run
- Set your `MISTRAL_API_KEY` in `.env`
- Run `vibe` against a small Python file in your fork
- Try asking it: *"What does this project do?"*

### Reading the repo
- `README.md` — what is it, how to install, how to use
- `LICENSE` — what you can and cannot do with the code
- `CONTRIBUTING.md` — how to submit changes back upstream

### Exercise

[Your First Prompt to Vibe](exercise_first_prompt.md)

---

## After Class

- Make sure your fork is running and you can invoke `vibe` from the terminal
- Write 3-5 bullet points in your own words: what does mistral-vibe do, and how does it work at a high level?
- Browse the source files — don't read deeply yet, just get a feel for the shape of the codebase
- Think about what feature you might want to add this semester — come to next class with at least one idea
