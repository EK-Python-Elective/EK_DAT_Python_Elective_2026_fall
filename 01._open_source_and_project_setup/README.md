# Session 1: Kickoff — Open Source Culture & Project Setup

**Week 35 | Python Elective 2026 Fall**

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

  | | Use in proprietary/closed-source product | Must share your source code | Patent protection |
  |---|---|---|---|
  | MIT | Yes | No | No |
  | Apache 2.0 | Yes | No | Yes |
  | GPL | No | Yes | Yes |

- The open source contribution lifecycle:

  ```mermaid
  flowchart LR
      A[Issue] --> B[Fork]
      B --> C[Branch]
      C --> D[Pull Request]
      D --> E[Merge]
  ```
- Why companies open source their tools (and why Mistral AI did — see [Mistral AI's own reasoning](https://mistral.ai/about))

### Forking and cloning
1. Fork the course repo, **`EK-Python-Elective/mistral-vibe-ek-python-elective`**, to your own GitHub account.
2. Clone your fork locally: `git clone git@github.com:<you>/mistral-vibe-ek-python-elective.git`
3. That's it. Your clone is on `main` — the course's pinned base: mistral-vibe at release `v2.24.0`, plus the course's CI checks and a `tests/exam/` folder. Everyone starts on identical code, so the file and line references in later sessions match what you see on screen.

> The course repo is itself a fork of the original [`mistralai/mistral-vibe`](https://github.com/mistralai/mistral-vibe). You don't need to touch the original at all this semester — but if you later want to contribute your feature back to it, that's an optional path covered in [session 13](../13._pr_preparation/README.md).

### Working on a branch — always
**Never commit to `main`.** It's your stable base — the pinned release everyone shares, and the branch your exam feature is reviewed against. Keep it clean.

All your actual work — exercises, experiments, your feature — happens on branches off `main`:

```bash
git checkout -b exercise/session-04   # one branch per exercise or experiment
git checkout -b feature/my-experiment
```

When an exercise is ready, open a pull request from your branch into your own `main` — **but do not merge it.** Opening the PR is a rehearsal for session 11, where this same motion happens for real: it gives you GitHub's diff view to review your own change, and it triggers the course's CI checks (ruff, pyright, pytest) automatically. Once you've looked it over, leave it open or close it — either way, don't click Merge. Because your work lives on its own branches and none of these PRs get merged, `main` stays pristine at the pinned release all semester, and can always be restored without touching anything you wrote.

#### If `main` ever gets messed up
You forked a pinned repo and you don't pull from anywhere else, so `main` shouldn't drift. If it ever does — a stray commit, a bad merge — reset it to the version you forked:

```bash
git checkout main
git fetch origin
git reset --hard origin/main   # your exercise/feature branches are untouched
```

If it's truly tangled, the simplest fix is to delete your fork and fork again. Sanity check anytime with `git describe --tags` — it should start with `v2.24.0`.

### Installing with uv

**Step 1 — install globally** so the `vibe` command is available anywhere in your terminal:
```bash
uv tool install mistral-vibe
vibe --help
```
This installs the published version from PyPI. Use this when you just want to *use* the tool.

**Step 2 — set up your local dev environment** inside your cloned fork so you can read, run, and modify the source code:
```bash
cd mistral-vibe-ek-python-elective   # your cloned fork
uv sync                              # creates a local virtual environment and installs all dependencies
uv run vibe --help                   # runs *your local version* of the tool
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
- Re-read "Working on a branch — always" until you can answer these without looking: why do you never commit to `main`, and what *is* `main` (where did it come from)? Where does your own work live instead? How do you restore `main` if it gets messed up? Why do you open a PR for an exercise if you're never going to merge it? This branch model is the foundation for the whole semester — every session starts from it, and getting it wrong is the #1 way to lose an afternoon to git archaeology
- Write 3-5 bullet points in your own words: what does mistral-vibe do, and how does it work at a high level?
- Browse the source files — don't read deeply yet, just get a feel for the shape of the codebase
- Think about what feature you might want to add this semester — come to next class with at least one idea

---

## Optional

For students who want to go further. None of this is required — pick whatever looks interesting.

- [optional] *Pro Git* (Chacon & Straub), chapters 2–3 — free at [git-scm.com/book](https://git-scm.com/book/en/v2). Branches, `reset --hard`, and the object model behind "never commit to `main`".
- [optional] [choosealicense.com](https://choosealicense.com) and [tldrlegal.com](https://tldrlegal.com) — plain-language breakdowns of MIT vs Apache 2.0 vs GPL, the same comparison as the licence table above.
- [optional] *Producing Open Source Software* (Karl Fogel) — free at [producingoss.com](https://producingoss.com). How real open-source projects are actually run, governed, and funded.
- [optional] *Working in Public* (Nadia Eghbal) — a book on the social and economic dynamics of maintaining open source; good if the "why do companies do this?" question stuck with you.
- [optional] [uv — Features](https://docs.astral.sh/uv/getting-started/features/) — the full list of what uv replaces (pip, pipx, pyenv, virtualenv, poetry) and the command for each.
