# Session 14: PR Preparation — Finalizing Your Hand-In

**Week 48 | Python Elective 2026 Fall**

> Polish the feature to production quality and finalize the group PR — this PR (your feature branch → `main`) is your **exam hand-in**. Then, optionally, evaluate whether the feature is also worth contributing upstream to `mistralai/mistral-vibe`.

---

## Learning Goals

- Polish a feature branch to production-ready quality
- Write a high-quality PR description suitable for an open source project
- Produce the clean group PR that serves as your exam hand-in
- Evaluate whether a feature is *also* suitable for upstream contribution (optional, beyond the exam)
- Understand upstream contribution etiquette and expectations

---

## Before Class

- Your feature should be functionally complete and tested
- All review comments from last session should be addressed
- Run `ruff check .`, `ruff format .`, and `pytest` — fix any remaining issues
- Read mistral-vibe's `CONTRIBUTING.md` (if it exists) or their PR template

---

## Today's Teachings

### What makes a PR ready to hand in?

Your group PR is evaluated. Before the oral exam your instructor reviews it *as an artifact* — reviewing the diff and checking out the branch to run it — **without merging it** (see [the exam](../15._exam/README.md)). So aim for the same bar a real maintainer would apply:
- Does this feature do something clear and useful?
- Is it well-tested? (`uv run pytest` passes)
- Does it follow the project's code style? (`ruff check .` and `ruff format .` clean)
- Is the PR description clear enough to review without asking questions?
- Does it add unnecessary complexity?
- Is it mergeable into `main`? (GitHub reports no conflicts — even though the instructor won't actually merge it)

**CI runs the checks for you.** When you open the PR, the repo's **Exam checks** workflow automatically runs `ruff`, `pyright`, and your tests (`pytest tests/exam`) and shows a green or red mark on the PR. Put your feature's tests in `tests/exam/` so they're picked up. Getting that check green is part of the bar — do it before the exam.

### Writing a great PR description

When you open the PR, the repo's PR template pre-fills the description with the sections below and a hand-in checklist — fill it in, don't delete it.

Here is a worked example for a small, realistic feature: an `/export` command that saves the conversation to a Markdown file. **It is illustrative — your feature and the exact files will differ — but notice the structure** (Summary / Motivation / Changes / How to test / Notes) and how the *Changes* section points at the real files the feature touches.

```markdown
## Summary
Add an `/export` command that writes the current conversation to a Markdown
file, so a user can save a session transcript for notes or sharing.

## Motivation
`/copy` puts the last agent message on the clipboard, but there is no way to
save a whole conversation. A transcript is useful for keeping a record of a
debugging session or sharing what the agent did.

## Changes
- `vibe/cli/commands.py`: register a new `export` command (alias `/export`),
  alongside the existing `copy` command
- `vibe/cli/textual_ui/app.py`: add the `_export_conversation` handler, next
  to the existing `_copy_last_agent_message`
- `tests/cli/test_export.py`: cover the handler, including the empty-conversation case

## How to test
1. Start a session: `vibe`
2. Ask a few questions
3. Run `/export`
4. Confirm a Markdown file is written and contains the conversation

## Notes
- Written with `pathlib` to the working directory as `vibe-export-<timestamp>.md`
- An empty conversation prints a friendly message instead of writing an empty file
```

### Squashing and cleaning up commits
```bash
# Interactive rebase to clean up messy commits before handing in
# (main is what your feature branched from)
git rebase -i main

# Combine all feature commits into one clean commit
# (pick the first, squash the rest)
```

### Optional: is your feature also suitable for upstream?
Your exam hand-in is the PR against `main`. Contributing upstream is an optional stretch goal *on top of that* — and because the course pin (`v2.14.1`) now sits behind upstream's latest release, a real upstream PR means first rebasing your feature onto upstream's current `main`, then opening the PR against `mistralai/mistral-vibe`. Worth it if your feature is genuinely broadly useful.

Criteria for upstream contribution:
- General usefulness (not just for your specific use case)
- Follows the project's design philosophy
- Adds minimal complexity to the core
- Has tests
- Does not break existing behaviour

If in doubt: open an issue first, ask if the feature is wanted before spending time on a PR.

### The contribution conversation
- Be patient — maintainers are often volunteers
- Be responsive — reply to feedback within a few days
- Be gracious — if rejected, the learnings were still valuable

### Today's working session
- Polish your PR: fix last issues, clean up commits, finalize the description
- Make sure the PR is mergeable into `main` (no conflicts), tests pass, and the linter is clean
- Optional: decide whether your group also wants to contribute upstream (rebase onto upstream `main`, open against `mistralai/mistral-vibe`)

---

## After Class

- **Hand in the group PR** (feature branch → `main`) by the exam deadline — this is your exam deliverable
- Your PR should be in a state you are proud of — clean, tested, documented
- Optional: if contributing upstream, rebase onto upstream `main` and open the PR there
- Write a short individual reflection (half a page): what was the hardest part of this feature? What would you do differently? How did AI tools help or mislead you?
- **Prepare for the exam:** every group member must be able to present *and defend the whole feature individually* — 10-minute presentation + 15-minute Q&A (see [the exam](../15._exam/README.md))
