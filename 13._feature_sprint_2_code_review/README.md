# Session 13: Feature Sprint II & Code Review

**Week 48 | Python Elective 2026 Fall**

> Continue implementation. Peer code review between groups. Discuss what makes a good PR: small commits, clear descriptions, tests, docs.

---

## Learning Goals

- Complete or significantly advance your feature implementation
- Give and receive structured code review feedback
- Understand what makes a good PR: small commits, clear description, tests, docs
- Know how to respond to review comments constructively
- Understand the difference between code style feedback and structural feedback

---

## Before Class

- Your draft PR from last session should be up on GitHub with at least some code
- Read through another group's PR and prepare 2-3 comments (constructive, specific)
- Make sure your own code runs — no broken imports, no obvious crashes
- Optional: read [Google's code review guidelines](https://google.github.io/eng-practices/review/)

---

## Today's Teachings

### What is a code review?
- A structured process where someone else reads your code before it is merged
- Goals: catch bugs, share knowledge, maintain consistency, improve design
- Not: a personal critique, a gatekeeping exercise, or a style war

### How to give good review feedback

**Too vague:**
> "This doesn't look right."

**Too aggressive:**
> "Why would you do it this way? This is wrong."

**Good:**
> "This will fail if `config.toml` doesn't exist yet — consider using `Path.exists()` before reading, or wrapping in a try/except with a helpful error message."

Structure: **observation + reason + suggestion**

### Categories of feedback
- **Must fix**: bug, security issue, broken behaviour
- **Should fix**: code smell, poor naming, missing test
- **Nice to have**: style preference, minor improvement — mark with `nit:`
- **Question**: genuinely unclear — ask, don't assume

### How to respond to review comments
- Address every comment — either fix it or explain why you disagree
- Don't take it personally
- If you disagree: explain your reasoning, then defer to the reviewer if still unsure
- Use "Resolve conversation" only after the issue is actually resolved

### What a good PR looks like
- **Title**: short, describes what changes (`feat: add session memory persistence`)
- **Description**: why this feature, how it works, how to test it
- **Size**: ideally under 400 lines changed — easier to review
- **Tests**: new behaviour has tests
- **No unrelated changes**: don't fix unrelated things in the same PR

### Code review checklist
- [ ] Does the code do what the PR description says?
- [ ] Are there tests for the new behaviour?
- [ ] Are error cases handled?
- [ ] Are there any obvious performance issues?
- [ ] Is the code readable without comments?
- [ ] Does it follow the style of the rest of the codebase?

### Today's working session
- 30 min: structured peer review — swap PRs with another group, leave written comments on GitHub
- Remaining time: continue implementation and address review feedback

---

## After Class

- Respond to all review comments on your PR
- Update your implementation based on feedback
- Run the full test suite: `uv run pytest`
- Run the linter: `uv run ruff check .`
- Your feature should be functionally complete by end of next session (PR Preparation)
