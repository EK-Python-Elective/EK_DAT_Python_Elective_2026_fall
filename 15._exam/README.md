# Exam — Feature Presentation & Defense

**Exam period | Python Elective 2026 Fall**

> The final exam. Each student individually presents and defends their group's feature: a 10-minute presentation followed by 15 minutes of examiner questions. This is an individual oral exam, not a group session — it runs as a scheduled exam period across the week, roughly 25 minutes per student, not a single class slot.

---

## Format at a glance

- **Group hand-in (before the exam):** the group PR — your feature branch → `main` (still pinned at `v2.24.0`). One PR per group.
- **Initial evaluation:** before the orals, the examiner evaluates each group's PR *as an artifact* — the PR is reviewed and run, **not merged**. The examiner reads the diff, checks out the feature branch and runs it (`uv sync`, runs the feature, `uv run pytest`, `uv run ruff check .`), and confirms GitHub reports no conflicts with `main`. This is the shared starting point for the group's feature.
- **Individual oral (≈25 min per student):** 10-minute presentation + 15-minute Q&A. You present your group's *whole* feature; the questions establish *your individual* understanding.
- **Grading is individual.** Two students from the same group can receive different grades — the Q&A is what separates "I understand this code" from "the group built it."

---

## Learning Goals

- Present technical work clearly and defend the decisions behind it
- Explain the Python concepts used in your group's feature implementation
- Demonstrate genuine, individual understanding of code you helped ship — including code AI tools helped write
- Reflect critically on the use of AI tools in a development process

---

## Before the Exam

- The group PR is handed in against `main` and is **mergeable** (GitHub reports no conflicts) — the examiner does not merge it, but it must be in a state that *could* be merged
- `uv run pytest` passes and `uv run ruff check .` is clean on the feature branch
- You can run the feature live from a terminal, including at least one edge case or error path
- You can open and explain *any* part of the feature — not only the parts you personally wrote. Walk your teammates' code before exam day
- Bring your individual AI reflection notes

### How the PR is evaluated

The examiner does not merge your PR — it is reviewed and run as an artifact. The bar (and the spine of the Q&A) is:
- **Runs:** checks out cleanly and the feature works when launched
- **Tested:** `uv run pytest` passes
- **Clean:** `uv run ruff check .` is clean
- **Mergeable:** GitHub reports no conflicts with `main`
- **Coherent:** the PR description matches the diff
- **Yours to defend:** every group member can explain and justify the code in the oral

Most of this is checked automatically: opening the PR runs the **Exam checks** workflow (`ruff`, `pyright`, `pytest tests/exam`), so a green check already covers *tested* and *clean*. The examiner still checks out and runs the feature, and the oral is where *yours to defend* is decided.

---

## Your 10-minute presentation

Keep the structure simple — no slides required, just a working terminal and the codebase.

1. **Show it working** (3–4 min)
   - Live terminal demo — start `vibe`, trigger the feature, show the result
   - Show at least one edge case or error path

2. **Explain the code** (3–4 min)
   - Open the most interesting file in the feature
   - Walk through 10–20 lines and explain what they do and why
   - Name the Python concepts in play (async, pathlib, type hints, etc.)

3. **Reflect on AI** (2–3 min)
   - Where did AI tools help, and where did they mislead you?
   - How did you make sure you understood and took responsibility for what you shipped?

## The 15-minute Q&A

The examiner will probe your individual understanding of the feature and the surrounding codebase. Your feature is the main focus, but questions aren't limited to it — the examiner may also ask about other parts of mistral-vibe and Python concepts covered earlier in the semester, to check your understanding of the codebase you've been working in all along. Expect questions like:
- "Why did you use *this* approach here instead of an alternative?"
- "What happens if this file doesn't exist / this input is empty / this call fails?"
- "Walk me through what happens, step by step, when a user triggers this."
- "Where does this connect to the rest of mistral-vibe?"
- "Your teammate wrote this part — explain what it does and why."
- "How does this compare to how [some earlier session's topic] was handled elsewhere in the codebase?"

There is no way to prepare for this except to actually understand your group's feature, the code it touches, and the mistral-vibe codebase more broadly. That is the point.

---

## What you have built this semester

By reaching this exam you have:
- Forked and extended a real Python project used by developers worldwide
- Learned modern Python: `uv`, `ruff`, type hints, async, pathlib, httpx, pytest
- Practiced open source contribution workflows end to end
- Used AI tools as a professional force multiplier — and learned to take responsibility for the code you ship

---

## Optional

For students who want to go further. None of this is required — pick whatever looks interesting.

- [optional] Simon Peyton Jones, ["How to give a great research talk"](https://www.microsoft.com/en-us/research/academic-program/give-great-research-talk/) — video and slides; the structure advice transfers straight to the 10-minute feature demo.
- [optional] Julia Evans, ["How to ask good questions"](https://jvns.ca/blog/good-questions/) — framing for the Q&A: how to reason out loud when you're not certain.
- [optional] [Pro Git — Viewing the Commit History](https://git-scm.com/book/en/v2/Git-Basics-Viewing-the-Commit-History) — `git log`, `git blame`, `git show` for walking a teammate's code before exam day.

---

*End of Python Elective 2026 Fall — well done.*
