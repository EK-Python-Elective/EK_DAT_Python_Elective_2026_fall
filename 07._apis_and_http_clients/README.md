# Session 7: APIs and HTTP Clients — Talking to Mistral AI

**Week 42 | Python Elective 2026 Fall**

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

---

## After Class

- Make sure you understand every line of the API call in mistral-vibe
- Experiment: change the `temperature` or `max_tokens` parameter and observe the difference in responses
- Add your API key to `.env` and verify `.env` is in `.gitignore` in your fork
- Optional: read about [rate limiting](https://docs.mistral.ai/api/) and add basic retry logic on a branch off `main` (the `.env` work above is fine on `main` — it's gitignored, never committed)
