# Session 5: Byg en REST API med Flask

**Uge 40 | Python Elective 2026 Fall**

> 100 % hands-on: vi bygger, kører og tester en REST API i Flask — først sammen via live demos, derefter selv via øvelserne. Ingen slides.

---

## Læringsmål

- Starte en Flask-app med `uv` uden at sætte et helt projekt op
- Definere routes med path-parametre (`/todos/<int:id>`) og query-parametre (`?a=2`)
- Håndtere de fire HTTP-metoder `GET`, `POST`, `PUT`, `DELETE` og returnere JSON
- Returnere de rigtige statuskoder (`200`, `201`, `204`, `400`, `404`)
- Kalde en API fra terminalen med `curl`
- Teste en Flask API med `pytest` og `app.test_client()`

---

## Før undervisningen

- Tjek at `uv` virker: `uv --version`
- Tjek at `curl` virker: `curl --version`
  - **Windows:** brug **Git Bash** til `curl`-kommandoerne i dag — PowerShell håndterer JSON-anførselstegn anderledes, og kommandoerne herunder virker ikke 1:1 der.

---

## Demos

Alle demos ligger i denne mappe og kan køres direkte. Åbn **to terminaler**: én til serveren og én til `curl`.

### Demo 1 — Hello API ([`hello_api.py`](hello_api.py))

```bash
uv run --with flask python hello_api.py
```

```bash
curl http://127.0.0.1:5000/
curl http://127.0.0.1:5000/hello/Alice
curl "http://127.0.0.1:5000/add?a=2&b=3"
curl -i "http://127.0.0.1:5000/add?a=2&b=x"    # -i viser statuskoden: 400
```

Det vi ser på undervejs:
- `@app.get("/")` — en decorator kobler en URL til en funktion
- En `dict` returneret fra en route bliver automatisk til JSON
- `return {...}, 400` — body og statuskode i én tuple
- `debug=True` — ret i filen, gem, og serveren genstarter af sig selv

### Demo 2 — Todo CRUD API ([`todo_api.py`](todo_api.py))

```bash
uv run --with flask python todo_api.py
```

```bash
curl http://127.0.0.1:5000/todos
curl -X POST http://127.0.0.1:5000/todos -H "Content-Type: application/json" -d '{"title": "Lær Flask"}'
curl http://127.0.0.1:5000/todos/1
curl -X PUT http://127.0.0.1:5000/todos/1 -H "Content-Type: application/json" -d '{"done": true}'
curl -X DELETE http://127.0.0.1:5000/todos/1
curl -i http://127.0.0.1:5000/todos/99
```

Det vi ser på undervejs:

| Metode | URL | Gør | Status |
|--------|-----|-----|:------:|
| `GET` | `/todos` | Hent alle | 200 |
| `GET` | `/todos/<id>` | Hent én | 200 / 404 |
| `POST` | `/todos` | Opret | 201 / 400 |
| `PUT` | `/todos/<id>` | Opdatér | 200 / 404 |
| `DELETE` | `/todos/<id>` | Slet | 204 / 404 |

- `request.get_json()` — læs JSON-body fra klienten
- `abort(404)` + `@app.errorhandler(404)` — JSON-fejl i stedet for en HTML-side
- Data ligger i en `dict` i hukommelsen — genstart serveren, og alt er væk

### Demo 3 — Test API'en ([`test_todo_api.py`](test_todo_api.py))

```bash
uv run --with flask --with pytest pytest test_todo_api.py -v
```

- `app.test_client()` kalder routes direkte — ingen server, ingen `curl`
- En `pytest`-fixture nulstiller data før hver test

---

## Øvelser

Byg en **Bog-API** fra bunden i en ny fil, `book_api.py`. Brug gerne AI — men kør og test hvert trin selv med `curl`, før du går videre.

1. **Hent bøger.** Start med en hardkodet liste af 3 bøger (`id`, `title`, `author`, `year`). Lav `GET /books` og `GET /books/<id>`. Ukendt id skal give `404` med en JSON-fejl.
2. **Opret en bog.** Lav `POST /books`. Returnér `201` og den nye bog. Mangler `title` eller `author`, så returnér `400`.
3. **Opdatér og slet.** Lav `PUT /books/<id>` og `DELETE /books/<id>` med de rigtige statuskoder.
4. **Søg og filtrér.** Understøt query-parametre på `GET /books`, fx `?author=Tolkien` og `?after=2000`.
5. **Validering.** `year` skal være et heltal mellem 0 og indeværende år — ellers `400` med en fejlbesked, der siger hvad der er galt.
6. **Test det.** Skriv mindst 5 `pytest`-tests med `app.test_client()` — én for hver statuskode du bruger.
7. **Gem på disk.** Gem bøgerne i en `books.json`-fil, så de overlever en genstart af serveren. Brug `pathlib.Path` og `json`.

---

## Valgfrit

For dem der vil videre. Intet af det er påkrævet.

- [valgfri] Lav en lille klient i Python (`client.py`), der kalder din API med `httpx` eller `requests` i stedet for `curl`.
- [valgfri] Pak din CLI fra session 4 ind i en API: et endpoint, der tager input som JSON og returnerer det, dit script ville have printet.
- [valgfri] Byg den samme Bog-API i [FastAPI](https://fastapi.tiangolo.com/) og sammenlign: hvad giver type hints dig gratis (validering, `/docs`)?
- [valgfri] [Flask Quickstart](https://flask.palletsprojects.com/en/stable/quickstart/) — den officielle gennemgang af routing, requests og responses.
