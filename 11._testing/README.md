# Session 11: Testing — pytest and How to Test CLI Tools

**Week 46 | Python Elective 2026 Fall**

> Add tests to the fork. Learn `pytest`, `pytest-asyncio`, mocking, fixtures, testing CLI tools with subprocess.

---

## Learning Goals

- Write tests using `pytest` for real Python code
- Test async functions with `pytest-asyncio`
- Mock external dependencies (API calls, file system) in tests
- Test CLI tools by invoking them as subprocesses
- Add a meaningful test suite to your fork

---

## Before Class

- Check the `tests/` directory in mistral-vibe — where are the tests, what do they cover?
- Dev dependencies (`pytest`, `pytest-asyncio`, `pytest-xdist`, `respx`, etc.) are already in `pyproject.toml` — run `uv sync` to make sure they are installed
- Run `uv run pytest` — what happens?
- Optional: read [pytest getting started](https://docs.pytest.org/en/stable/getting-started.html)

---

## Today's Teachings

### pytest basics
```python
# tests/test_config.py

def test_default_model():
    config = load_config()
    assert config.model == "mistral-small"

def test_config_from_toml(tmp_path):
    config_file = tmp_path / "config.toml"
    config_file.write_text('[model]\nname = "mistral-large"')
    config = load_config(config_file)
    assert config.model == "mistral-large"
```

### Fixtures — reusable test setup
```python
import pytest
from pathlib import Path

@pytest.fixture
def config_dir(tmp_path: Path) -> Path:
    d = tmp_path / ".config" / "vibe"
    d.mkdir(parents=True)
    return d

def test_something(config_dir: Path):
    # config_dir is a fresh temp directory for each test
    ...
```

### Testing async code
```python
import pytest

@pytest.mark.asyncio
async def test_stream_response():
    chunks = []
    async for chunk in stream_tokens("Hello"):
        chunks.append(chunk)
    assert len(chunks) > 0
```

Configure in `pyproject.toml` (you will need to add this to your fork):
```toml
[tool.pytest.ini_options]
asyncio_mode = "auto"
```

### Mocking — isolating external dependencies
```python
from unittest.mock import patch, AsyncMock

def test_api_call_uses_correct_model():
    with patch("vibe.core.llm.backend.mistral.Mistral") as mock_client:
        mock_client.return_value.chat.stream_async = AsyncMock(
            return_value=mock_stream_response(model="mistral-large")
        )
        result = call_api(model="mistral-large", prompt="test")
    assert result.model == "mistral-large"
```

The project also uses `respx` (already in dev deps) for mocking HTTP requests at the transport layer — look at `tests/` for examples.

### Testing CLI tools
```python
import subprocess

def test_cli_help():
    result = subprocess.run(["vibe", "--help"], capture_output=True, text=True)
    assert result.returncode == 0
    assert "Usage" in result.stdout

def test_cli_version():
    result = subprocess.run(["vibe", "--version"], capture_output=True, text=True)
    assert "0." in result.stdout
```

### What to test in mistral-vibe
- Config loading with various inputs (missing file, bad TOML, missing keys)
- Skill loading from a directory
- CLI argument parsing
- Any pure functions (formatters, parsers, validators)
- Do NOT try to test actual API calls — mock those

---

## After Class

- On a branch off `main`, add at least 5 meaningful tests — keep `main` clean
- At least one test should use a fixture with `tmp_path`
- At least one test should mock an external dependency
- Run `uv run pytest -v` and make sure all tests pass
- Optional: your fork already runs `ruff`/`pyright`/`pytest tests/exam` on pull requests via the **Exam checks** workflow — open `.github/workflows/exam-checks.yml` to see how CI works

---

## Optional

For students who want to go further. None of this is required — pick whatever looks interesting.

- [optional] [pytest — How-to guides](https://docs.pytest.org/en/stable/how-to/index.html) — fixtures, `parametrize`, `monkeypatch`, and temporary directories, in task-sized pieces.
- [optional] [Python docs — `unittest.mock`](https://docs.python.org/3/library/unittest.mock.html) — `patch`, `MagicMock`, `AsyncMock`, and the "Where to patch" section (the #1 mocking gotcha).
- [optional] [respx docs](https://lundberg.github.io/respx/) — mocking httpx at the transport layer, the way mistral-vibe's own tests do it.
- [optional] [pytest-asyncio docs](https://pytest-asyncio.readthedocs.io/) — `asyncio_mode = "auto"` and how to test coroutines and async fixtures.
- [optional] Brian Okken, *Python Testing with pytest* (2nd ed.) — the standard practical book if you want depth.
