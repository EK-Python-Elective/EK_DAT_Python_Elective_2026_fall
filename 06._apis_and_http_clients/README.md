# Session 6: APIs and HTTP Clients — Talking to Mistral AI

**Week 41 | Python Elective 2026 Fall**

> Find where the API calls happen. Learn `httpx`/`requests`, async HTTP, API keys, `.env` files, error handling. Students swap or extend the API integration.

---

## Learning Goals

- Understand how HTTP APIs work (request/response, headers, JSON body)
- Use `httpx` to make synchronous and asynchronous HTTP requests in Python
- Know how to handle API keys securely using `.env` files
- Understand streaming responses and how to consume them token by token
- Find and understand all API calls in mistral-vibe

---

## Before Class

- Find the code in mistral-vibe that sends a request to the Mistral API
- Note: what URL is called, what headers are sent, what is in the request body?
- Optional: read the [Mistral API docs](https://docs.mistral.ai/api/) for the chat completions endpoint

---

## Today's Teachings

### HTTP basics
- Request: method (GET/POST), URL, headers, body
- Response: status code, headers, body (JSON)
- REST APIs: resources, endpoints, authentication

### httpx — the modern HTTP client
```python
import httpx

# Synchronous
response = httpx.get("https://api.example.com/data", headers={"Authorization": "Bearer TOKEN"})
data = response.json()

# POST with JSON body
response = httpx.post(
    "https://api.mistral.ai/v1/chat/completions",
    headers={"Authorization": f"Bearer {api_key}"},
    json={"model": "mistral-small", "messages": [{"role": "user", "content": "Hello"}]},
)
```

### Keeping secrets out of code
```python
# .env file (never commit this!)
# MISTRAL_API_KEY=sk-...

from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.environ["MISTRAL_API_KEY"]
```
- `.env` goes in `.gitignore`
- Use `.env.example` to document what variables are needed

### Streaming responses
```python
with httpx.stream("POST", url, json=payload, headers=headers) as response:
    for chunk in response.iter_text():
        print(chunk, end="", flush=True)
```
- Why streaming? Perceived speed — first tokens appear immediately
- Server-Sent Events (SSE) format: `data: {...}\n\n`

### How mistral-vibe handles the API
- The project uses the **`mistralai` Python SDK** (`from mistralai.client import Mistral`) — not raw `httpx` calls. The SDK wraps the HTTP layer for you.
- `httpx` is still a direct dependency (used for error handling and lower-level HTTP in some places), which is why it is worth knowing.
- Walk through `vibe/core/llm/backend/mistral.py` together: where is the SDK client created? How is a streaming request sent? How are chunks yielded back?
- **Bonus:** the backend supports multiple providers — `vibe/core/llm/backend/` has separate files for Mistral, a generic OpenAI-compatible API, and others. This is a good example of an abstraction layer.
- Identify: where is the API key loaded? How is the request built? How is the stream consumed?

### Exercise: extend the API integration
- Add support for a second model (e.g. `mistral-large`) selectable via a CLI flag
- Or: add a cost estimator that counts tokens and prints estimated cost after each response

### Exercise: a Python client for your book API (no Mistral key needed)

Last session you built the bookshelf API in Flask and tested it with Postman. Now write the **other team's side**: a Python program that talks to it with `httpx`. Run your session 5 API in one terminal and the client in another. If your API isn't working, use a classmate's, or have AI generate one from your `swagger.json`.

```bash
uv run --with flask python app.py                         # terminal 1: your session 5 API
uv run --with httpx --with python-dotenv library_client.py  # terminal 2: the client
```

1. **Talk to it.** Write `library_client.py` so it lists all books, adds a book, borrows it, returns it, and deletes it. Print the status code and JSON for each call. Use a single `httpx.Client(base_url=...)` instead of repeating the full URL.
2. **When things go wrong.** Make the client handle each case with a clear message, not a stack trace:
   - a book that doesn't exist (404)
   - a book with no title (400)
   - the server isn't running (`httpx.ConnectError`)
   - the server is too slow: add `time.sleep(5)` to one route and call it with `timeout=2`

   Try `response.raise_for_status()` and catch `httpx.HTTPStatusError`. When is that better than checking `response.status_code` yourself?
3. **Add an API key.** Protect the endpoints that change data. The Flask API reads `LIBRARY_API_KEY` from `.env` and returns `401` if the request's `X-API-Key` header doesn't match. The client reads the same key from its own `.env` and sends it. Add a `.env.example`, check that `.env` is in `.gitignore`, and confirm that a request without the key gets `401`.
4. **Stretch — async.** Add 20 books, then fetch each one by id: first in a normal loop, then with `httpx.AsyncClient` and `asyncio.gather`. Add `time.sleep(0.3)` to the "get one book" route and time both versions. Why is one so much faster? (This is a preview of session 7.)
5. **Stretch — streaming.** Add a `GET /books/stream` endpoint that returns one JSON line per book with a short pause between them (a Flask generator, `mimetype="application/x-ndjson"`). Consume it with `httpx.stream(...)` and `response.iter_lines()` so each book prints as it arrives. This is the same idea as token streaming in mistral-vibe.

**Connect it back:** open `vibe/core/llm/backend/mistral.py` again and find where mistral-vibe does each of steps 2–5: error handling, the API key, async calls, and consuming a stream.

---

## After Class

- Make sure you understand every line of the API call in mistral-vibe
- Experiment: change the `temperature` or `max_tokens` parameter and observe the difference in responses
- Add your API key to `.env` and verify `.env` is in `.gitignore` in your fork
- Optional: read about [rate limiting](https://docs.mistral.ai/api/) and add basic retry logic on a branch off `main` (the `.env` work above is fine on `main` — it's gitignored, never committed)

---

## Optional

For students who want to go further. None of this is required — pick whatever looks interesting.

- [optional] [MDN — An overview of HTTP](https://developer.mozilla.org/en-US/docs/Web/HTTP/Overview) — methods, headers, and status codes from the ground up.
- [optional] [HTTPX docs](https://www.python-httpx.org/) — sync vs. async clients, streaming, timeouts, and connection pooling.
- [optional] [MDN — Using server-sent events](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events) — the `data: {...}` wire format behind token-by-token streaming.
- [optional] [Mistral API reference](https://docs.mistral.ai/api/) — the chat completions endpoint the SDK wraps; skim the request and response schema.
- [optional] [`python-dotenv`](https://pypi.org/project/python-dotenv/) — `.env` precedence rules and `.env.example` conventions.
