# Session 6: API'er og HTTP-klienter — Byg en klient til din API

**Uge 41 | Python Elective 2026 Fall**

> Skriv en Python-klient til jeres bog-API fra session 5. Lær `httpx`, asynkron HTTP, API-nøgler, `.env`-filer og fejlhåndtering.

---

## Læringsmål

- Du forstår, hvordan HTTP-API'er virker (request/response, headers, JSON-body)
- Du kan bruge `httpx` til at lave synkrone og asynkrone HTTP-requests i Python
- Du ved, hvordan man håndterer API-nøgler sikkert med `.env`-filer
- Du kan håndtere fejl, når du kalder en API: fejl-statuskoder, en server der ikke kører, og timeouts
- Du forstår streaming-svar, og hvordan man læser dem bid for bid
- Du kan skrive en Python-klient til en API, du selv har bygget

---

## Før undervisningen

- Sørg for, at din bogreols-API fra session 5 kører, og at alle endpoints virker i Postman eller Insomnia. Hvis den ikke virker, så ret den eller aftal at bruge en medstuderendes. Dagens opgave bygger videre på den.
- Vælg én request i Postman, og notér, hvad der sendes afsted (metode, URL, headers, body), og hvad der kommer tilbage (statuskode, headers, body). I dag skriver du den samme request i Python.
- Valgfrit: skim [HTTPX quickstart](https://www.python-httpx.org/quickstart/)

---

## Dagens undervisning

### HTTP-grundbegreber
- Request: metode (GET/POST), URL, headers, body
- Response: statuskode, headers, body (JSON)
- REST API'er: ressourcer, endpoints, autentificering

### httpx — den moderne HTTP-klient
```python
import httpx

# Synkront
response = httpx.get("https://api.example.com/data", headers={"Authorization": "Bearer TOKEN"})
data = response.json()

# POST med JSON-body
response = httpx.post(
    "https://api.mistral.ai/v1/chat/completions",
    headers={"Authorization": f"Bearer {api_key}"},
    json={"model": "mistral-small", "messages": [{"role": "user", "content": "Hello"}]},
)
```

### Hold hemmeligheder ude af koden
```python
# .env-fil (commit den aldrig!)
# MISTRAL_API_KEY=sk-...

from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.environ["MISTRAL_API_KEY"]
```
- `.env` skal i `.gitignore`
- Brug `.env.example` til at dokumentere, hvilke variabler der skal bruges

### Streaming-svar
```python
with httpx.stream("POST", url, json=payload, headers=headers) as response:
    for chunk in response.iter_text():
        print(chunk, end="", flush=True)
```
- Hvorfor streaming? Oplevet hastighed — de første tokens dukker op med det samme
- Server-Sent Events (SSE)-formatet: `data: {...}\n\n`

### Opgave: en Python-klient til din bog-API

Sidste gang byggede du bogreols-API'en i Flask og testede den med Postman. Nu skal du skrive **det andet holds side**: et Python-program, der taler med den via `httpx`. Kør din API fra session 5 i én terminal og klienten i en anden. Hvis din API ikke virker, så brug en medstuderendes, eller få AI til at generere en ud fra jeres `swagger.json`.

```bash
uv run --with flask python app.py                         # terminal 1: din API fra session 5
uv run --with httpx --with python-dotenv library_client.py  # terminal 2: klienten
```

1. **Tal med den.** Skriv `library_client.py`, så den viser alle bøger, tilføjer en bog, låner den ud, afleverer den og sletter den. Print statuskoden og JSON for hvert kald. Brug én `httpx.Client(base_url=...)` i stedet for at gentage hele URL'en.
2. **Når det går galt.** Få klienten til at håndtere hvert tilfælde med en tydelig besked i stedet for en stack trace:
   - en bog, der ikke findes (404)
   - en bog uden titel (400)
   - serveren kører ikke (`httpx.ConnectError`)
   - serveren er for langsom: tilføj `time.sleep(5)` til én route, og kald den med `timeout=2`

   Prøv `response.raise_for_status()`, og fang `httpx.HTTPStatusError`. Hvornår er det bedre end selv at tjekke `response.status_code`?
3. **Tilføj en API-nøgle.** Beskyt de endpoints, der ændrer data. Flask-API'en læser `LIBRARY_API_KEY` fra `.env` og returnerer `401`, hvis requestens `X-API-Key`-header ikke matcher. Klienten læser den samme nøgle fra sin egen `.env` og sender den med. Tilføj en `.env.example`, tjek at `.env` er i `.gitignore`, og bekræft at en request uden nøglen får `401`.
4. **Ekstra — async.** Tilføj 20 bøger, og hent derefter hver bog ud fra dens id: først i et almindeligt loop, derefter med `httpx.AsyncClient` og `asyncio.gather`. Tilføj `time.sleep(0.3)` til routen, der henter én bog, og tag tid på begge versioner. Hvorfor er den ene så meget hurtigere? (Det er en forsmag på session 7.)
5. **Ekstra — streaming.** Tilføj et `GET /books/stream`-endpoint, der returnerer én JSON-linje pr. bog med en kort pause imellem (en Flask-generator, `mimetype="application/x-ndjson"`). Læs det med `httpx.stream(...)` og `response.iter_lines()`, så hver bog bliver printet, efterhånden som den kommer. Det er samme idé, som når en AI-chat skriver sit svar ord for ord.

---

## Efter undervisningen

- Sørg for, at du kan forklare hver linje i din `library_client.py`: hvad hver request sender (metode, URL, headers, body), og hvad der kommer tilbage
- Eksperimentér: ændr `timeout`, send en forkert API-nøgle, eller send en ugyldig JSON-body, og se, hvilken statuskode og fejl du får
- Sørg for, at din `LIBRARY_API_KEY` kun står i `.env`, at `.env` er i `.gitignore`, og at `.env.example` dokumenterer variablen
- Valgfrit: læs om [retries i HTTPX](https://www.python-httpx.org/advanced/transports/#http-transport), og få klienten til at prøve igen, når serveren ikke kan nås, og vente lidt længere hver gang

---

## Valgfrit

Til dig, der vil videre. Intet af det her er påkrævet — vælg det, der ser interessant ud.

- [valgfrit] [MDN — An overview of HTTP](https://developer.mozilla.org/en-US/docs/Web/HTTP/Overview) — metoder, headers og statuskoder fra bunden.
- [valgfrit] [HTTPX-dokumentationen](https://www.python-httpx.org/) — synkrone vs. asynkrone klienter, streaming, timeouts og connection pooling.
- [valgfrit] [MDN — Using server-sent events](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events) — `data: {...}`-formatet bag streaming bid for bid.
- [valgfrit] [`python-dotenv`](https://pypi.org/project/python-dotenv/) — `.env`-prioritetsregler og `.env.example`-konventioner.
