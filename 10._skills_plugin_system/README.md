# Session 10: The Skills/Plugin System — Extensibility Patterns

**Week 45 | Python Elective 2026 Fall**

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

- Read the `SKILL.md` file in the mistral-vibe repo carefully
- Look at any existing example skills in the `skills/` directory
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
```markdown
# Skill: web-search

## Description
Search the web for up-to-date information when the user asks about recent events.

## When to use
Use this skill when the user asks about news, current events, or anything that
might have changed after your training cutoff.

## Instructions
1. Extract the search query from the user's message
2. Run: `curl "https://api.search.example.com?q={query}"`
3. Summarise the top 3 results for the user
```

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
- Walk through the skill loading and dispatch code
- How does the LLM "call" a skill? (tool use / function calling)
- Mistral function calling format: name, description, parameters schema

### Exercise: implement a new skill
Ideas:
- A skill that reads the current git log and summarises recent changes
- A skill that looks up a Python package on PyPI and returns its description
- A skill that converts a file from one format to another (JSON ↔ TOML)

---

## After Class

- Your fork should have at least one new skill file committed
- Test your skill: prompt `vibe` in a way that triggers the skill and verify it works
- Think about your main feature for the sprint: does it fit naturally as a skill, or does it require changes to the core?
