# CLAUDE.md — Python Elective 2026 Fall

This file gives you context for working in this repository as a teaching assistant.

---

## About the Course

This course focuses on contributing to an open-source Python project, [mistral-vibe](https://github.com/mistralai/mistral-vibe). Students will learn to analyze, improve, and extend the project using AI and CLI tools. Along the way, they will become familiar with Python syntax and programming concepts.

## Exam

The exam will involve presenting a feature or improvement made to the mistral-vibe project, demonstrating understanding of the codebase, and reflecting on the use of AI in the development process.

---

## What this repo is

This is the **teacher's repository** for a 4th semester university elective course called **Python Elective 2026 Fall**, taught at KEA (Copenhagen School of Design and Technology).

The course runs from **August to November 2026**, approximately 14 sessions, weekly on Thursdays.

---

## The course red thread

The entire semester revolves around one open source project:
**[mistral-vibe](https://github.com/mistralai/mistral-vibe)** — an AI-powered Python CLI coding assistant made by Mistral AI.

Students will:
- **Fork** mistral-vibe into their own GitHub repo
- **Analyse** it to learn Python language features and ecosystem tooling
- **Extend** it with new features across the semester
- **Optionally submit a PR** back to the original upstream repo

The goal is for students to experience real open source contribution workflows, not just toy exercises.

---

## AI policy

**AI tools are 100% allowed for everything.** Students are encouraged to use:
- Claude Code (this tool)
- mistral-vibe itself (the project they are working on)
- GitHub Copilot, Cursor, ChatGPT, or any other AI assistant

The teacher also uses Claude Code to prepare course material, lesson plans, and code examples. When you help in this repo, you are primarily helping the **teacher**, not students.

---

## Repository structure

```
/
├── CLAUDE.md                          # This file
├── README.md                          # Public-facing course overview and semester plan
└── teacher/
    ├── agenda/                        # Per-session lesson plans (teacher-facing)
    └── claude/
        ├── README.md                  # Prior Claude-generated content (ITA course ref)
        └── python_elective_2026_fall.md  # Detailed 15-session course plan (Claude-generated)
```

> Student-facing session folders (e.g. `01._introduction/`) will be added as the course progresses.

---

## Semester overview

Approximate start: **week 36, 2026** (September). 15 teaching sessions.

| # | Week | Topic | What students do |
|:-:|:----:|-------|-----------------|
| 1 | 36 | **Kickoff: Open Source Culture & Project Setup** | Fork `mistral-vibe`, clone locally, install with `uv`, run it. Read the README, CONTRIBUTING, and LICENSE. Discuss what open source means. |
| 2 | 37 | **Reading Code: Project Structure & Python Packaging** | Explore `pyproject.toml`, `uv.lock`, folder layout, entry points. Understand how a Python package is installed and run. Compare to `pip`/`requirements.txt`. |
| 3 | 38 | **Python Tooling: uv, ruff, and the Modern Ecosystem** | Deep dive into `uv` as package manager, `ruff` for linting/formatting, `mypy`/`pyright` for type checking. Students configure their fork's tooling. |
| 4 | 39 | **Type System: Type Hints, Dataclasses, and Pydantic** | Find and read all type annotations in mistral-vibe. Learn `TypedDict`, `dataclass`, `Optional`, `Union`. Students add type hints to an untyped part of the code. |
| 5 | 40 | **CLI Development: How the CLI Works** | Understand how mistral-vibe builds its CLI (argument parsing, REPL loop, prompts). Students extend the CLI with a new flag or subcommand. |
| 6 | 41 | **File I/O and pathlib** | Study all file read/write in the codebase (config, prompts, agents, skills). Learn `pathlib.Path`, context managers, JSON/TOML parsing. Students add a feature that persists something new to disk. |
| 7 | 42 | **APIs and HTTP Clients: Talking to Mistral AI** | Find where the API calls happen. Learn `httpx`/`requests`, async HTTP, API keys, `.env` files, error handling. Students swap or extend the API integration. |
| 8 | 43 | **Async Python** | Understand `async`/`await` in mistral-vibe. Learn the event loop, `asyncio`, async generators, streaming responses. Students refactor or extend an async part. |
| 9 | 44 | **Configuration Management: TOML, ENV, and Profiles** | Study `config.toml` and `.env` patterns. Learn `tomllib`/`tomli`, `python-dotenv`, environment variable best practices. Students add a new configurable feature. |
| 10 | 45 | **The Skills/Plugin System: Extensibility Patterns** | Deep dive into `SKILL.md` and how skills extend the tool. Learn plugin architecture patterns in Python. Students implement a new skill. |
| 11 | 46 | **Testing: pytest and How to Test CLI Tools** | Add tests to the fork. Learn `pytest`, `pytest-asyncio`, mocking, fixtures, testing CLI tools with `click.testing` or subprocess. |
| 12 | 47 | **Feature Sprint I** | Teams plan and start implementing their chosen feature. AI tools in full swing. Focus: feature design, branching strategy, code review within team. |
| 13 | 48 | **Feature Sprint II + Code Review** | Continue implementation. Peer code review between groups. Discuss what makes a good PR: small commits, clear descriptions, tests, docs. |
| 14 | 49 | **PR Preparation: Contributing Back** | Polish the fork. Write a proper PR description. Evaluate whether the feature is suitable to submit upstream. Optional: open the PR against `mistralai/mistral-vibe`. |
| 15 | 50 | **Demo Day & Reflection** | Each group demos their fork. Discussion: what did you learn? What was hard? What would you do differently? What is Python good at? |

---

## Key Python topics covered through mistral-vibe

These are the Python concepts students learn by reading and extending the codebase:

- Modern Python packaging: `pyproject.toml`, `uv`, entry points
- Tooling: `ruff` (lint/format), `mypy`/`pyright` (type checking), `pytest`
- Type system: type hints, `TypedDict`, `dataclass`, `Optional`, generics
- CLI development: argument parsing, REPL loops, rich terminal output
- File I/O: `pathlib`, context managers, TOML/JSON parsing
- API clients: `httpx`, async HTTP, streaming responses, `.env` secrets
- Async Python: `async`/`await`, `asyncio`, async generators
- Plugin/skills architecture: extensibility patterns
- Testing: `pytest`, `pytest-asyncio`, mocking, CLI testing
- OSS workflows: forking, branching, code review, PR etiquette

---

## How to help the teacher

When asked to help in this repo, typical tasks include:

- **Drafting lesson plans** for a specific session — save these in `teacher/agenda/` or `teacher/claude/`
- **Writing student-facing README files** for session folders
- **Creating code examples** that illustrate a Python concept visible in mistral-vibe
- **Suggesting exercises** that students can do using AI tools
- **Reviewing and improving course material** already in the repo

When creating course content, keep the mistral-vibe codebase as the anchor. Exercises and examples should connect back to patterns visible in that project.

---

## Tone and audience

- **Teacher audience**: direct, concise, practical. The teacher is experienced and does not need hand-holding.
- **Student audience**: 4th semester CS students. Comfortable with basic programming, but not necessarily with Python or open source workflows. Assume they will use AI tools heavily.
- **Language**: course material can be in **English or Danish** — follow whatever the existing file uses, or ask if unclear.

---

## Pending decisions

### Publishing to PyPI — not yet added to the plan
The teacher wants to add a "publish to PyPI" topic somewhere in the semester. The agreed direction so far:

- **Where**: Session 2 (Project Structure & Python Packaging) is the preferred slot — packaging is already the topic, so publishing is a natural conclusion
- **How**: a standalone exercise unrelated to mistral-vibe — students build a small simple CLI tool from scratch and publish it to TestPyPI (sandbox) and optionally the real PyPI
- **Why standalone**: easier to learn the mechanics without the complexity of a large codebase; students get a real PyPI page with their name on it which is motivating
- **Open question**: session 2 may become too dense — consider whether to move the mistral-vibe structure analysis to Before Class reading to free up time for the hands-on exercise

When the teacher returns to this topic, update `02._project_structure_and_packaging/README.md` with the exercise and add PyPI/TestPyPI to the learning goals.

---

## Notes

- The `teacher/claude/` directory is where Claude saves its own generated suggestions and plans.
- The existing `teacher/claude/README.md` is from a different course (ITA Spring 2026) — ignore it for this course.
- When in doubt about scope or direction, refer to `teacher/claude/python_elective_2026_fall.md` as the canonical plan.
