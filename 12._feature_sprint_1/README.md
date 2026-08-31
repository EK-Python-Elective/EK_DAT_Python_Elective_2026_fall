# Session 12: Feature Sprint I

**Week 47 | Python Elective 2026 Fall**

> Teams plan and start implementing their chosen feature. AI tools in full swing. Focus: feature design, branching strategy, code review within team.

---

## Learning Goals

- Plan and scope a feature for your fork clearly and realistically
- Set up a proper Git branching strategy for collaborative feature development
- Start implementing your chosen feature using AI tools effectively
- Apply all previously learned Python skills in a real feature context
- Give and receive constructive feedback on technical design

---

## Before Class

- Decide as a group which feature you are building — be specific about scope
- Write a one-paragraph feature description and bring it to class
- Make sure your fork is clean, tests pass, and tooling is configured
- Skim the CHANGELOG and open issues/PRs at [github.com/mistralai/mistral-vibe](https://github.com/mistralai/mistral-vibe): has your feature (or part of it) already shipped, or is someone building it right now?
- Decide your feature scope as a group; we create the feature branch off `main` together in class (see "Starting your feature" below)

---

## Today's Teachings

### Starting your feature

Your feature is built on the **same pinned `main` you have used all semester** (mistral-vibe at `v2.24.0`). Keeping every group on one base is deliberate: the file/line references from sessions 1–11 still apply, your group's PR sits on a known state, and the exam evaluation is uniform across groups (see [the exam](../15._exam/README.md)).

**First, due diligence — check the original project for prior art.** Before you lock your plan, look at what the live project is doing: browse the CHANGELOG and the open issues/pull requests at [github.com/mistralai/mistral-vibe](https://github.com/mistralai/mistral-vibe). You are checking one thing: **has your feature (or part of it) already shipped, or is someone building it right now?** Projects that release weekly implement ideas fast — finding yours now costs five minutes; finding it after a two-week sprint costs the sprint.

**Then create your feature branch off `main`:**

```bash
git checkout -b feature/<your-feature-name> main
git push -u origin feature/<your-feature-name>
```

Each team member works on their own branch off `main` and merges into the group's shared feature branch as you go. That group branch, opened as a PR into `main`, is your **exam hand-in** — see [the exam](../15._exam/README.md).

> **Going further (optional, beyond the exam):** contributing your feature to the real `mistralai/mistral-vibe` means adding it as an `upstream` remote, rebasing your work onto upstream's *current* release (mistral-vibe releases often, so it will typically have moved past the course pin, `v2.24.0`, by the time you do this), and opening a PR there. A genuine open-source contribution and a great stretch goal — but not required, and separate from your exam hand-in. Session 14 covers what that takes.

### Feature planning
Before writing code, answer these questions:
- What does the feature do? (one sentence)
- How will a user invoke it? (CLI flag, command, automatic behaviour?)
- What files will you create or modify?
- What new dependencies (if any) will you add?
- How will you test it?

Write this as a short design doc — even a few bullet points in your PR description later.

### Git branching for teams
```bash
# Each team member works on a sub-branch
git checkout -b feature/session-memory
git push -u origin feature/session-memory

# Sync with your team's main branch regularly
git fetch origin
git rebase origin/main

# Small, focused commits
git add vibe/memory.py
git commit -m "add SessionMemory class with JSON persistence"
```

Good commit message structure:
```
<type>: <short description>

<optional body explaining why, not what>
```
Types: `feat`, `fix`, `refactor`, `test`, `docs`, `chore`

### Using AI tools for feature development
- Use `vibe` or Claude Code to explore the codebase: *"Where should I add session memory to this project?"*
- Use AI to generate a first draft, then review it critically
- Use AI to explain code you don't understand: *"What does this async generator do?"*
- Always read and understand AI-generated code before committing it

### Scope management
- A feature that works for the common case is better than one that handles every edge case but is half-finished
- Cut scope early: what is the MVP (minimum viable feature)?
- Nice-to-haves go in a follow-up issue, not the first PR

### Today's working session
- 15 min: due diligence + branch — check the original project for prior art (CHANGELOG, issues/PRs on GitHub), then create feature branches off `main`
- 20 min: present your feature plan to another group, get feedback
- Remaining time: implement — teacher circulates to help unblock

---

## After Class

- At least the skeleton of your feature should be committed to your feature branch
- Open a draft PR on GitHub from your feature branch — even if it is not done yet
- Write the PR description: what does this feature do, how do you test it, what is left to do?
- Be ready to show progress next session

---

## Optional

For students who want to go further. None of this is required — pick whatever looks interesting.

- [optional] [Conventional Commits](https://www.conventionalcommits.org/) — the `feat:` / `fix:` / `refactor:` commit convention used in class, specified precisely.
- [optional] [GitHub Flow](https://docs.github.com/en/get-started/using-github/github-flow) — the lightweight branch-and-PR model this sprint follows.
- [optional] [Pro Git — Rebasing](https://git-scm.com/book/en/v2/Git-Branching-Rebasing) — what `git rebase origin/main` actually does to a feature branch (previews session 14).
- [optional] Simon Willison's [ai-assisted-programming](https://simonwillison.net/tags/ai-assisted-programming/) blog tag — an ongoing, practical record of what works and what breaks when coding with LLMs.
