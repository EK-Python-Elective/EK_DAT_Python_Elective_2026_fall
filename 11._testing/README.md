# Session 11: Testing — pytest and How to Test CLI Tools

**Week 46 | Python Elective 2026 Fall**

> Add tests to the fork. Learn `pytest`, `pytest-asyncio`, mocking, fixtures, testing CLI tools with `click.testing` or subprocess.

---

## Learning Goals

- Write tests using `pytest` for real Python code
- Test async functions with `pytest-asyncio`
- Mock external dependencies (API calls, file system) in tests
- Test CLI tools by invoking them as subprocesses or via a test runner
- Add a meaningful test suite to your fork

---

## Before Class

- Check if mistral-vibe has any existing tests — where are they, what do they cover?
- Install pytest in your fork: `uv add --dev pytest pytest-asyncio`
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

Configure in `pyproject.toml`:
```toml
[tool.pytest.ini_options]
asyncio_mode = "auto"
```

### Mocking — isolating external dependencies
```python
from unittest.mock import patch, AsyncMock

def test_api_call_uses_correct_model():
    with patch("mistral_vibe.api.httpx.AsyncClient") as mock_client:
        mock_client.return_value.__aenter__.return_value.post = AsyncMock(
            return_value=mock_response(model="mistral-large")
        )
        result = call_api(model="mistral-large", prompt="test")
    assert result.model == "mistral-large"
```

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

- Add at least 5 meaningful tests to your fork
- At least one test should use a fixture with `tmp_path`
- At least one test should mock an external dependency
- Run `uv run pytest -v` and make sure all tests pass
- Optional: add a `pytest` step to your repo's CI (GitHub Actions) so tests run on every push
