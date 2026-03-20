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
Never commit directly to `main`. From the moment you clone your fork, create a development branch and do all your work there. This keeps `main` clean and in sync with upstream, making it easy to pull in future updates from the original project.

```bash
cd mistral-vibe
git checkout -b dev   # a personal development branch you use throughout the course
```

For each new feature or experiment, branch off from there:
```bash
git checkout -b feature/my-experiment
```

`main` should only ever receive changes via a PR or a deliberate merge — never a direct commit.

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

---

## After Class

- Make sure your fork is running and you can invoke `vibe` from the terminal
- Write 3-5 bullet points in your own words: what does mistral-vibe do, and how does it work at a high level?
- Browse the source files — don't read deeply yet, just get a feel for the shape of the codebase
- Think about what feature you might want to add this semester — come to next class with at least one idea
