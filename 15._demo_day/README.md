# Exam — Feature Presentation & Defense

**Week 50 | Python Elective 2026 Fall**

> The final exam. Each student individually presents and defends their group's feature: a 10-minute presentation followed by 15 minutes of examiner questions. This is an individual oral exam, not a group session — it runs as a scheduled exam period across the week, roughly 25 minutes per student, not a single class slot.

---

## Format at a glance

- **Group hand-in (before the exam):** the group PR — your feature branch → `v2026-base` (still pinned at `v2.14.1`). One PR per group.
- **Initial evaluation:** before the orals, the examiner merges each group's PR and checks that it merges cleanly, runs, is tested, and does what it claims. This is the shared starting point for the group's feature.
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

- The group PR is handed in and merges cleanly into `v2026-base`; tests pass and the linter is clean
- You can run the feature live from a terminal, including at least one edge case or error path
- You can open and explain *any* part of the feature — not only the parts you personally wrote. Walk your teammates' code before exam day
- Bring your individual AI reflection notes

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

The examiner will probe your individual understanding of the feature and the surrounding codebase. Expect questions like:
- "Why did you use *this* approach here instead of an alternative?"
- "What happens if this file doesn't exist / this input is empty / this call fails?"
- "Walk me through what happens, step by step, when a user triggers this."
- "Where does this connect to the rest of mistral-vibe?"
- "Your teammate wrote this part — explain what it does and why."

There is no way to prepare for this except to actually understand your group's feature and the code it touches. That is the point.

---

## What you have built this semester

By reaching this exam you have:
- Forked and extended a real Python project used by developers worldwide
- Learned modern Python: `uv`, `ruff`, type hints, async, pathlib, httpx, pytest
- Practiced open source contribution workflows end to end
- Used AI tools as a professional force multiplier — and learned to take responsibility for the code you ship

---

*End of Python Elective 2026 Fall — well done.*
