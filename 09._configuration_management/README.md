# Session 9: Configuration Management — TOML, ENV, and Profiles

**Week 44 | Python Elective 2026 Fall**

> Study `config.toml` and `.env` patterns. Learn `tomllib`/`tomli`, `python-dotenv`, environment variable best practices. Students add a new configurable feature.

---

## Learning Goals

- Understand the different layers of configuration: defaults, config files, environment variables, CLI flags
- Read and write TOML files using Python's `tomllib` (stdlib) and `tomli-w`
- Use `python-dotenv` to load environment variables from `.env`
- Understand how mistral-vibe loads and merges its configuration
- Add a new configurable feature to your fork

---

## Before Class

- Open the `config.toml` in your mistral-vibe fork and read through every field
- Find the Python code that loads and parses that file
- Optional: read the [TOML specification](https://toml.io/en/) — it is short and readable

---

## Today's Teachings

### Configuration layers (priority order, highest to lowest)
1. CLI flags (`--model mistral-large`)
2. Environment variables (`MISTRAL_MODEL=mistral-large`)
3. User config file (`~/.config/vibe/config.toml`)
4. Project config file (`./config.toml`)
5. Built-in defaults (hardcoded in Python)

### TOML — Tom's Obvious Minimal Language
```toml
[model]
name = "mistral-small"
temperature = 0.7
max_tokens = 4096

[ui]
theme = "dark"
stream = true

[profiles.coding]
name = "mistral-large"
temperature = 0.2
```

### Reading TOML in Python
```python
import tomllib  # Python 3.11+ stdlib

with open("config.toml", "rb") as f:   # must be binary mode
    config = tomllib.load(f)

model_name = config.get("model", {}).get("name", "mistral-small")
```

### Writing TOML
```python
import tomli_w  # third-party, not in stdlib

config = {"model": {"name": "mistral-large", "temperature": 0.5}}
with open("config.toml", "wb") as f:
    tomli_w.dump(config, f)
```

### Environment variables
```python
import os
from dotenv import load_dotenv

load_dotenv()   # loads .env into os.environ

api_key = os.environ["MISTRAL_API_KEY"]          # raises if missing
debug = os.environ.get("DEBUG", "false") == "true"  # with default
```

### Configuration loading in mistral-vibe
- The config system is a **layered merge**: `ConfigOrchestrator` combines `ConfigLayer`s in priority order (lowest → highest) — schema defaults, GrowthBook experiments, user TOML, project TOML, `VIBE_*` env vars, runtime overrides, agent-profile overrides. Walk through `vibe/core/config/default_orchestrator.py` to see the stack assembled
- TOML loading is plain `tomllib` (`vibe/core/config/layers/_base.py`, used by `layers/user.py` and `layers/project.py`); env vars go through **`pydantic_settings`** (`BaseSettings`, prefix `VIBE_`) in `vibe/core/config/layers/environment.py` — Pydantic only handles env-var parsing/coercion here, not the whole system
- How does `--agent` change the behaviour? (there is no `--profile` flag — agents serve a similar purpose)
- Design principle: one config schema (`VibeConfigSchema`), populated by merging multiple layers in priority order — same idea as before, different mechanism than a single `BaseSettings` class

### Exercise: add a configurable feature
- Add a new section to `config.toml` for a feature you are building
- Load it in Python and use the value to alter behaviour
- Make sure the CLI flag overrides the config file value

---

## After Class

- On a branch off `main` (e.g. `exercise/session-09`), add at least one new config key in `config.toml` that controls a real behaviour — keep `main` clean
- Document the new config key in your fork's README
- Think about: what happens if the user has an old config file that is missing your new key? Handle it gracefully with a default
