# Session 10: The Skills/Plugin System — Extensibility Patterns

**Week 44 | Python Elective 2026 Fall**

> Deep dive into `SKILL.md` and how skills extend the tool. Learn plugin architecture patterns in Python. Students implement a new skill.

---

## Learning Goals

- Understand what a plugin/skills architecture is and why it is useful
- Read and understand the `SKILL.md` format used in mistral-vibe
- Know common Python patterns for building extensible systems
- Implement a new skill for mistral-vibe
- Understand how the agent picks and calls the right skill at runtime

---

## Before Class

- Read the **Skills System** section in the mistral-vibe `README.md` (search for `## Skills System`) — this explains the `SKILL.md` format, discovery rules, and configuration
- Browse `vibe/core/skills/` in the repo — `models.py` defines the skill schema, `manager.py` shows how skills are discovered and loaded
- Think of one skill you would find genuinely useful — bring the idea to class

---

## Today's Teachings

### What is a plugin system?
- Core app + extensions that follow a contract
- Examples: VS Code extensions, pytest plugins, browser add-ons
- Benefits: add features without modifying core code; community contributions

### The mistral-vibe skills model
- A skill is a Markdown file describing a capability the agent can invoke
- The file defines: name, description, trigger conditions, and instructions
- The LLM decides which skill to use based on the user's input
- Skills can invoke shell commands, call APIs, read files, etc.

### Anatomy of a skill file

Each skill lives in its own directory with a `SKILL.md` file. The file has YAML frontmatter followed by freeform Markdown instructions. Example: `~/.vibe/skills/web-search/SKILL.md`:

```markdown
---
name: web-search
description: Search the web for up-to-date information when the user asks about recent events.
license: MIT
compatibility: Python 3.12+
user-invocable: true
allowed-tools:
  - bash
---

# Web Search Skill

Search the web for up-to-date information.

## Instructions
1. Extract the search query from the user's message
2. Run the search and retrieve results
3. Summarise the top results for the user
```

**Frontmatter fields** (defined in `vibe/core/skills/models.py`):

| Field | Required | Notes |
|-------|----------|-------|
| `name` | yes | Lowercase, hyphens only. Must match the directory name. |
| `description` | yes | What the skill does and when to use it (up to 1024 chars). |
| `user-invocable` | no | `true` by default — makes the skill appear as a `/slash` command. |
| `allowed-tools` | no | List of tools the skill is pre-approved to use. |
| `license` | no | License name or path to a bundled license file. |
| `compatibility` | no | Environment requirements. |

### Python extensibility patterns

**Registration pattern:**
```python
SKILLS: dict[str, Callable] = {}

def register_skill(name: str):
    def decorator(fn: Callable) -> Callable:
        SKILLS[name] = fn
        return fn
    return decorator

@register_skill("web-search")
def web_search(query: str) -> str:
    ...
```

**Discovery pattern (load from directory):**
```python
import importlib
from pathlib import Path

for skill_file in Path("skills/").glob("*.py"):
    module_name = skill_file.stem
    importlib.import_module(f"skills.{module_name}")
```

### How mistral-vibe loads and calls skills
- Walk through `vibe/core/skills/manager.py`: `SkillManager._discover_skills()` walks the search paths, finds `SKILL.md` files, and builds a registry
- Walk through `vibe/core/skills/models.py`: `SkillMetadata` (Pydantic) validates the frontmatter; `SkillInfo` is the runtime representation
- **Discovery order**: custom `skill_paths` from `config.toml` → `.agents/skills/` → `.vibe/skills/` (both project-local, trusted folders only) → `~/.vibe/skills/` (global)
- The skill name **must match the directory name** — the manager warns if they differ
- How does the LLM "call" a skill? (tool use / function calling)
- Mistral function calling format: name, description, parameters schema

### Exercise: implement a new skill
Ideas:
- A skill that reads the current git log and summarises recent changes
- A skill that looks up a Python package on PyPI and returns its description
- A skill that converts a file from one format to another (JSON ↔ TOML)

---

## After Class

- On a branch off `main`, add at least one new skill file (`.vibe/skills/<your-skill-name>/SKILL.md` at the project root) — keep `main` clean
- Test your skill: prompt `vibe` in a way that triggers the skill and verify it works
- Think about your main feature for the sprint: does it fit naturally as a skill, or does it require changes to the core?

> **Note:** Adding a skill to your fork is a great way to learn the system, but `.vibe/skills/` is user/project configuration — not source code. A PR to the upstream mistral-vibe repo would not include this folder. If you want to contribute upstream, you need to extend the Python source code itself (e.g. a new tool, a CLI flag, an improvement to the core). Keep this in mind when planning your feature for sessions 12–14.
