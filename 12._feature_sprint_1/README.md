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
- Create a feature branch: `git checkout -b feature/<your-feature-name>`

---

## Today's Teachings

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
- 20 min: present your feature plan to another group, get feedback
- Remaining time: implement — teacher circulates to help unblock

---

## After Class

- At least the skeleton of your feature should be committed to your feature branch
- Open a draft PR on GitHub from your feature branch — even if it is not done yet
- Write the PR description: what does this feature do, how do you test it, what is left to do?
- Be ready to show progress next session
