# Session 5: CLI Development — How the CLI Works

**Week 39 | Python Elective 2026 Fall**

> Understand how mistral-vibe builds its CLI (argument parsing, REPL loop, prompts). Students extend the CLI with a new flag or subcommand.

---

## Learning Goals

- Understand how a Python CLI application is structured
- Read and understand argument parsing in mistral-vibe
- Know the difference between `argparse`, `click`, and `typer`
- Understand how a REPL (Read-Eval-Print Loop) works
- Be able to add a new flag or subcommand to the mistral-vibe CLI

---

## Before Class

- Run `vibe --help` and read the output carefully
- Find the source code that produces that help text
- Optional: read the [argparse docs](https://docs.python.org/3/library/argparse.html) introduction

---

## Today's Teachings

### What is a CLI?
- Arguments vs options vs subcommands
- `sys.argv` — the raw input
- Parsing libraries: `argparse` (stdlib), `click` (popular), `typer` (type-hint based)

### How mistral-vibe parses arguments
- Trace the CLI entry point to where arguments are parsed
- Identify: which flags exist, what are their types, which have defaults?
- How does the `--agent` flag affect program behaviour? What built-in agent names are available?

### The interactive loop
mistral-vibe uses **Textual** — a full TUI (terminal UI) framework — rather than a simple `input()` loop. The entry point calls `run_textual_ui()` in `vibe/cli/textual_ui/`. A simple REPL looks like this for reference:
```python
while True:
    user_input = input("> ")
    if user_input in ("exit", "quit"):
        break
    response = process(user_input)
    print(response)
```
- Explore `vibe/cli/textual_ui/` to see how Textual handles user input
- How does it handle Ctrl+C and Ctrl+D gracefully? (look in `vibe/cli/cli.py`)
- How does it stream responses token by token?

### Rich terminal output
- mistral-vibe uses `rich` for colours, markdown rendering, and spinners
- Brief intro: `Console`, `Markdown`, `Panel`, `Progress`

### Exercise: add a new CLI flag
- Add a `--verbose` flag that prints extra debug information during a session
- Or add a `--no-color` flag that disables rich formatting
- Make it configurable via `config.toml` as well

---

## After Class

- On a branch off `main` (e.g. `exercise/session-05`), add at least one new CLI flag or option you wrote yourself — keep `main` clean, as always
- Write a short description of the flag: what it does, how to use it, what code you changed
- Try building a minimal standalone CLI tool from scratch using `argparse` or `typer` — it helps to understand the pattern outside of a large codebase

---

## Optional

For students who want to go further. None of this is required — pick whatever looks interesting.

- [optional] [argparse tutorial](https://docs.python.org/3/howto/argparse.html) — the stdlib parser, end to end.
- [optional] [Typer docs](https://typer.tiangolo.com/) — building a CLI from type hints; a useful contrast with how mistral-vibe does it.
- [optional] [Click docs](https://click.palletsprojects.com/) — the library Typer builds on; the "Why Click?" page is a good short read on CLI design tradeoffs.
- [optional] [Textual tutorial](https://textual.textualize.io/tutorial/) — build a small TUI step by step; demystifies `vibe/cli/textual_ui/`.
- [optional] [Rich docs](https://rich.readthedocs.io/en/stable/) — `Console`, `Markdown`, `Panel`, `Progress`, with runnable examples.
