# Session 8: Async Python

**Week 43 | Python Elective 2026 Fall**

> Understand `async`/`await` in mistral-vibe. Learn the event loop, `asyncio`, async generators, streaming responses. Students refactor or extend an async part.

---

## Learning Goals

- Understand why async programming exists and when to use it
- Read and write `async`/`await` code confidently
- Understand `asyncio`, the event loop, and async generators
- Understand how mistral-vibe uses async for streaming API responses
- Refactor or extend an async part of the codebase

---

## Before Class

- Find all `async def` functions in mistral-vibe — how many are there?
- Find where `asyncio.run()` is called — this is where async code enters the program
- Optional: read [Python asyncio docs](https://docs.python.org/3/library/asyncio.html) — just the overview section

---

## Today's Teachings

### Why async?
- Problem: waiting for I/O (network, disk) blocks the entire program
- Solution: while waiting, do something else
- Perfect for: API calls, file streaming, web servers — anything that waits
- Not for: CPU-heavy work (use multiprocessing instead)

### async / await basics
```python
import asyncio

async def fetch_data() -> str:
    await asyncio.sleep(1)   # simulates a network call
    return "result"

async def main():
    result = await fetch_data()
    print(result)

asyncio.run(main())   # entry point into async world
```

### Running tasks concurrently
```python
async def main():
    # Sequential — slow
    a = await fetch_data()
    b = await fetch_data()

    # Concurrent — fast
    a, b = await asyncio.gather(fetch_data(), fetch_data())
```

### Async generators — streaming token by token
```python
async def stream_tokens(prompt: str):
    async with httpx.AsyncClient() as client:
        async with client.stream("POST", url, json=payload) as response:
            async for chunk in response.aiter_text():
                yield chunk

async def main():
    async for token in stream_tokens("Hello"):
        print(token, end="", flush=True)
```

### How mistral-vibe uses async
- The **agent loop** (`vibe/core/agent_loop.py`) is async — this is the core of the program
- The interactive UI is Textual, which manages its own event loop internally
- API streaming uses async generators (look in `vibe/core/llm/backend/mistral.py`)
- `asyncio.run()` is the entry point into async code — find it in `vibe/core/programmatic.py` and `vibe/core/utils.py`
- Walk through the event loop lifecycle in the codebase

### Common async pitfalls
- Calling `await` inside a non-async function (syntax error)
- Using `time.sleep()` instead of `await asyncio.sleep()` — blocks the event loop
- Forgetting to `await` a coroutine — creates it but never runs it

### Exercise

**Option A — `asyncio.gather`: two API calls in parallel**

The update notifier has two async gateways that each check a different source for the latest version:
- `vibe/cli/update_notifier/adapters/github_update_gateway.py` — `GitHubUpdateGateway.fetch_update()` hits the GitHub Releases API
- `vibe/cli/update_notifier/adapters/pypi_update_gateway.py` — `PyPIUpdateGateway.fetch_update()` hits the PyPI Simple API

In `vibe/cli/update_notifier/update.py:96`, only one gateway is used. Write a function that queries **both in parallel** using `asyncio.gather` and compares timing vs. sequential awaits.

For a production example of the same pattern, read `vibe/core/tools/mcp/registry.py:55-72` — `MCPRegistry._discover_all()` uses `asyncio.gather` to discover multiple MCP servers concurrently.

**Option B — Refactor sync → async**

Find a synchronous function in your fork that does I/O (file read, subprocess call, etc.) and refactor it to be async using `anyio` or `asyncio`. Compare the before/after.

---

## After Class

- Find one place in your feature implementation where async would improve performance and apply it
- Write a short note: in your own words, what is the event loop and why does it matter?
- Optional: read about `asyncio.TaskGroup` (Python 3.11+) — the modern way to run concurrent tasks
