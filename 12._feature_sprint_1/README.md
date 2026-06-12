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
- Skim upstream's `CHANGELOG.md` and open issues/PRs since `v2.14.1`: has your feature (or part of it) already shipped, or is someone building it right now?
- Do **not** create your feature branch yet — we do that together in class, and it does *not* start from your pinned `dev` (see "Rejoining upstream" below)

---

## Today's Teachings

### Rejoining upstream

All semester you have worked on the pinned `v2.14.1` release so that the course materials match the code in front of you. A pull request, however, is a request to merge into upstream's `main` *as it is today* — so from this session on, feature work is built against the live project, not the pin.

First, see how far the project has moved while we were learning:

```bash
git fetch upstream --tags
git log --oneline v2.14.1..upstream/main | wc -l    # number of commits since our pin
git diff v2.14.1..upstream/main -- CHANGELOG.md     # what shipped, in the project's own words
```

Read that CHANGELOG diff as a team before locking in your feature plan. You are checking two things:
- **Has your feature already shipped?** Projects that release weekly implement ideas fast — finding yours in the CHANGELOG now costs five minutes; finding it after a two-week sprint costs the sprint.
- **Did the code you plan to touch change?** If your feature extends a subsystem that was just rewritten, your design doc should describe the new shape, not the v2.14.1 shape.

Then create your feature branch **from upstream's `main`**, not from `dev`:

```bash
git checkout -b feature/<your-feature-name> upstream/main
git push -u origin feature/<your-feature-name>
```

Your `dev` branch stays pinned at `v2.14.1` — it is still your learning base, and every file/line reference from sessions 1–11 still matches it. The mental model: `dev` lives on the stable snapshot, feature branches live on the moving stream. This split — the version you studied vs. the version you contribute to — is exactly how professionals work against fast-moving open source projects.

During the sprint, keep your drift from upstream small so the final rebase before your PR (session 14) is trivial:

```bash
git fetch upstream
git rebase upstream/main
```

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
- 15 min: rejoin upstream together — CHANGELOG diff, feature-still-novel check, create feature branches from `upstream/main`
- 20 min: present your feature plan to another group, get feedback
- Remaining time: implement — teacher circulates to help unblock

---

## After Class

- At least the skeleton of your feature should be committed to your feature branch
- Open a draft PR on GitHub from your feature branch — even if it is not done yet
- Write the PR description: what does this feature do, how do you test it, what is left to do?
- Be ready to show progress next session
