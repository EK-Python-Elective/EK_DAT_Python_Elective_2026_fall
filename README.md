# EK_DAT Python Elective 2026 Fall

> 📌 **Course release: `v2.14.1`** — all materials this semester are written against mistral-vibe at release `v2.14.1`, and the whole semester stays on it: the feature sprint and the exam are all built on this release. You fork the course repo and work on its `main` branch, which is pinned to this tag; see [session 1](01._open_source_and_project_setup/README.md) for setup. (Contributing your feature back to the original [`mistralai/mistral-vibe`](https://github.com/mistralai/mistral-vibe) is an optional stretch goal — see [session 14](14._pr_preparation/README.md).)

## Semester Plan: Fork of mistral-vibe

| # | Week | Topic |
|:-:|:----:|-------|
| 1 | 35 | [Kickoff: Open Source Culture & Project Setup](01._open_source_and_project_setup/README.md) |
| 2 | 36 | [Reading Code: Project Structure & Python Packaging](02._project_structure_and_packaging/README.md) |
| 3 | 37 | [Python Tooling: uv, ruff, and the Modern Ecosystem](03._python_tooling/README.md) |
| 4 | 38 | [Type System: Type Hints, Dataclasses, and Pydantic](04._type_system/README.md) |
| 5 | 39 | [CLI Development: How the CLI Works](05._cli_development/README.md) |
| 6 | 40 | [File I/O and pathlib](06._file_io_and_pathlib/README.md) |
| 7 | 41 | [APIs and HTTP Clients: Talking to Mistral AI](07._apis_and_http_clients/README.md) |
|  | 42 | _Easter break — no session_ |
| 8 | 43 | [Async Python](08._async_python/README.md) |
| 9 | 44 | [Configuration Management: TOML, ENV, and Profiles](09._configuration_management/README.md) |
| 10 | 45 | [The Skills/Plugin System: Extensibility Patterns](10._skills_plugin_system/README.md) |
| 11 | 46 | [Testing: pytest and How to Test CLI Tools](11._testing/README.md) |
| 12 | 47 | [Feature Sprint I](12._feature_sprint_1/README.md) |
| 13 | 48 | [Feature Sprint II + Code Review](13._feature_sprint_2_code_review/README.md) |
| 14 | 49 | [PR Preparation: Contributing Back](14._pr_preparation/README.md) |
| 15 | — | [Exam — Feature Presentation & Defense](15._exam/README.md) |


---

## About the Course

This course focuses on contributing to an open-source Python project, [mistral-vibe](https://github.com/mistralai/mistral-vibe). Students will learn to analyze, improve, and extend the project using AI and CLI tools. Along the way, they will become familiar with Python syntax and programming concepts.

## AI Policy

**AI tools are 100% allowed — and actively encouraged.**

This course is built around the reality that professional developers use AI tools every day. You are expected to use them too.

We will use [mistral-vibe](https://github.com/mistralai/mistral-vibe) as the course's primary AI coding assistant — it is also the project you are studying, so you get to learn from it and with it at the same time. That said, you are free to use whichever AI tools you prefer. Other popular CLI-based AI coding assistants include [Claude Code](https://claude.ai/claude-code), [GitHub Copilot CLI](https://githubnext.com/projects/copilot-cli), and [Cursor](https://www.cursor.com/) — or any other tool you find useful.

Using AI is not cheating. It is a skill. The goal is to learn how to use these tools effectively and critically — knowing when to trust them, when to question them, and how to take responsibility for the code you ship.

You will be asked to reflect on your use of AI at the end of the semester: what helped, what misled you, and what you learned about working alongside these tools.

## Exam

The exam is an **individual oral examination** built on a **group feature**:

- **Group hand-in:** each group submits one PR — their feature branch → their fork's `main` (pinned at `v2.14.1`). A CI workflow runs the checks on the PR, and the examiner evaluates it beforehand by checking it out and running it (it is reviewed, not merged).
- **Individual oral (≈25 min per student):** a 10-minute presentation (live demo + code walkthrough + reflection on AI use) followed by 15 minutes of examiner questions. You present your group's whole feature; the Q&A establishes your individual understanding, so students from the same group can be graded differently.

The work is collaborative (sessions 12–14), but the grade is individual. See [the exam page](15._exam/README.md) for the full format. The binding exam regulations live in the course's official study programme (studieordning).
