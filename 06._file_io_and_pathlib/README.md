# Session 6: File I/O and pathlib

**Week 40 | Python Elective 2026 Fall**

> Study all file read/write in the codebase (config, prompts, agents, skills). Learn `pathlib.Path`, context managers, JSON/TOML parsing. Students add a feature that persists something new to disk.

---

## Learning Goals

- Use `pathlib.Path` to work with files and directories in a platform-safe way
- Read and write text files, JSON files, and TOML files in Python
- Use context managers (`with` statements) correctly for file operations
- Understand how mistral-vibe reads config, prompts, skills, and agent definitions from disk
- Add a feature to your fork that persists something new to disk

---

## Before Class

- Find all the places in mistral-vibe where files are read from or written to disk
- Note: what formats are used? (TOML, JSON, plain text, Markdown?)
- Optional: read [pathlib docs](https://docs.python.org/3/library/pathlib.html)

---

## Today's Teachings

### pathlib.Path — the modern way
```python
from pathlib import Path

config_dir = Path.home() / ".config" / "vibe"
config_file = config_dir / "config.toml"

config_dir.mkdir(parents=True, exist_ok=True)

# Check existence
if config_file.exists():
    text = config_file.read_text()

# Write
config_file.write_text("model = 'mistral-small'")

# Iterate directory
for skill_file in Path("skills/").glob("*.md"):
    print(skill_file.name)
```

### Context managers for files
```python
# Always prefer this over open() without with
with open("data.json", "r") as f:
    data = json.load(f)

# pathlib equivalent
text = Path("data.json").read_text(encoding="utf-8")
```

### Reading TOML
```python
import tomllib  # stdlib in Python 3.11+

with open("config.toml", "rb") as f:
    config = tomllib.load(f)
```

### Reading and writing JSON
```python
import json

data = json.loads(Path("history.json").read_text())
Path("history.json").write_text(json.dumps(data, indent=2))
```

### How mistral-vibe uses the filesystem
- `config.toml` — user configuration
- `prompts/` directory — custom system prompts
- `agents/` directory — agent profiles
- `skills/` directory — skill definitions in Markdown

### Exercise: persist something new
- Add a feature that saves conversation history to a JSON file after each session
- Or: add a feature that reads a user-defined list of "banned words" from a text file and filters them from responses
- Use `pathlib` throughout — no raw string paths

---

## After Class

- On a branch off `main` (e.g. `exercise/session-06`), add a small feature that reads from or writes to disk — keep `main` clean
- Make sure file paths use `pathlib.Path`, not string concatenation
- Handle the case where the file does not yet exist (create it or show a helpful error)
- Test your feature manually: does it work on a fresh machine where the file doesn't exist yet?
