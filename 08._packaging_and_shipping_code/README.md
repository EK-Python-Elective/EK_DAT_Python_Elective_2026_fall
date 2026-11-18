# Session 8: Packaging and Shipping Code

**Uge 44 | Python Elective 2026 Fall**

> Jeres kode virker på jeres egen maskine. I dag får I den ud til andre: som en pakke på TestPyPI, som et Docker-image på Docker Hub og med *secrets*, der bliver hjemme.

---

## Dagens spørgsmål

**Hvem skal bruge jeres kode, og hvordan får de fat i den?**

---

## Læringsmål

Efter i dag kan du:

- pakke et Python-projekt med `pyproject.toml` og `uv build`
- læse og skrive version specifiers (`==`, `>=`, `~=`)
- konfigurere en applikation via environment variables og holde *secrets* ude af Git
- skrive en `Dockerfile` og en `docker-compose.yml` til en Python-applikation
- pushe et image til Docker Hub
- publicere en pakke på TestPyPI

---

## Før timen

- Læs [Packaging and Shipping Code](https://missing.csail.mit.edu/2026/shipping-code/) hos MIT. I skal ikke kunne det hele, bare have et overblik.
- Installér [Docker Desktop](https://www.docker.com/products/docker-desktop/), og tjek at `docker run hello-world` virker.
- Opret en bruger på [TestPyPI](https://test.pypi.org/account/register/) og på [Docker Hub](https://hub.docker.com/signup).
- Hav jeres **bogreols-API** fra [session 5](../05._flask_api/README.md) klar. Virker jeres ikke, så brug [`hello_api.py`](../05._flask_api/hello_api.py).

---

## Program

1. Intro · Hvordan kommer kode ud til andre?
2. Runde 1 · Pak et projekt
3. Runde 2 · Publicér på TestPyPI
4. Runde 3 · Version specifiers
5. Runde 4 · Config og *secrets*
6. Runde 5 · Dockerfile
7. Runde 6 · Docker Compose
8. Runde 7 · Push til Docker Hub
9. Ekstra · Redis som ekstra service
10. Opsamling

---

## Intro · Hvordan kommer kode ud til andre?

Der findes mange måder at publicere en applikation på, og hver retter sig mod en bestemt slags modtager.

| Måde | Eksempel | Hvem er modtageren? | Hvad skal modtageren have? |
|------|----------|--------------------|-----------------------------|
| Kildekode på GitHub | `git clone` + `uv sync` | Udviklere, bidragydere | Git, Python, uv og tålmodighed |
| Pakke på PyPI (library) | `uv add requests` | Python-udviklere, der bygger videre | Et Python-projekt |
| Pakke på PyPI (CLI-værktøj) | `uvx mistral-vibe`, `uv tool install ruff` | Tekniske brugere | Python og uv/pipx |
| System-pakkemanager | `brew install`, `apt install`, `choco install` / `winget install` | Tekniske brugere, sysadmins | Den rigtige pakkemanager |
| Container-image | `docker run …` fra Docker Hub/GHCR | Drift, DevOps, servere | Docker, men ikke Python |
| Executable/installer, app store | `.exe`, `.dmg`, App Store | Almindelige brugere | Ingenting |
| Web app / SaaS | En URL | Almindelige brugere | En browser |

**Tænk over:** Hvor ligger mistral-vibe i tabellen? Hvor ligger jeres bogreols-API? Og jeres fredagsbar-system fra den obligatoriske opgave: hvem skal bruge det, og hvordan får de fat i det?

I dag prøver vi to af dem: **PyPI** (til udviklere og tekniske brugere) og **Docker Hub** (til drift og servere).

---

## Runde 1 · Pak et projekt

**Demo:** Vi laver et lille CLI-værktøj, der printer et tilfældigt citat, og gør det installerbart.

**I gør det samme:**

1. Lav et projekt. Brug jeres navn, så navnet er unikt på TestPyPI:

   ```bash
   uv init --package <navn>-quote
   cd <navn>-quote
   ```

2. Skriv `main()` i `src/<navn>_quote/__init__.py`, så den printer et tilfældigt citat fra en liste (`random.choice`).
3. Kig i `pyproject.toml`. Find `[project.scripts]`. Hvad betyder `<navn>-quote = "<navn>_quote:main"`? (Sammenlign med `vibe` i mistral-vibes `pyproject.toml`.)
4. Byg pakken, og kig ind i wheel'et:

   ```bash
   uv build
   unzip -l dist/*.whl                       # hvilke filer er med?
   unzip -p dist/*.whl '*/METADATA'          # navn, version og dependencies
   unzip -p dist/*.whl '*/entry_points.txt'  # [project.scripts]
   ```

   Hvor i `pyproject.toml` kommer indholdet af `METADATA` og `entry_points.txt` fra? Hvilke filer fra projektet er **ikke** med?

5. Installér wheel'et som et værktøj, og kør det fra en **anden mappe**:

   ```bash
   uv tool install dist/*.whl
   cd ~ && <navn>-quote
   ```

**Færdig når:** `<navn>-quote` virker i en hvilken som helst mappe.

**Prøv bagefter:** Del pakken via GitHub. Push projektet til et offentligt repo, og prøv to måder at installere sidemandens pakke på:

```bash
# 1. Direkte fra repoet (uv bygger selv wheel'et)
uvx --from git+https://github.com/<sidemand>/<sidemand>-quote <sidemand>-quote

# 2. Som færdigt wheel i en GitHub Release
gh release create v0.1.0 dist/*          # sidemanden kører denne i sit repo
uv tool install https://github.com/<sidemand>/<sidemand>-quote/releases/download/v0.1.0/<sidemand>_quote-0.1.0-py3-none-any.whl
```

Bemærk: Wheel-filnavnet bruger `_`, ikke `-`.

**Tænk over:** Hvad skal modtageren vide og have installeret i hvert tilfælde?

---

## Runde 2 · Publicér på TestPyPI

**Demo:** Vi publicerer citat-værktøjet på [TestPyPI](https://test.pypi.org/), PyPI's sandkasse.

**I gør det samme:**

1. Lav et API-token på TestPyPI under *Account settings → API tokens*.
2. Læg tokenet i en environment variable, så det ikke står i jeres shell-historik eller kode:

   ```bash
   export UV_PUBLISH_TOKEN=pypi-...
   uv publish --publish-url https://test.pypi.org/legacy/
   ```

3. Find jeres pakke på `https://test.pypi.org/project/<navn>-quote/`.
4. Kør sidemandens pakke uden at installere den:

   ```bash
   uvx --index-url https://test.pypi.org/simple/ <sidemand>-quote
   ```

**Færdig når:** I har kørt sidemandens værktøj fra TestPyPI.

**Prøv bagefter:** Kør `uv publish` igen uden at ændre noget. Hvorfor bliver den afvist?

**Tænk over:** Sammenlign med GitHub i Runde 1. Hvad skulle sidemanden vide for at installere jeres pakke dengang, og hvad skal de vide nu?

---

## Runde 3 · Version specifiers

**Demo:** `uv add`, `pyproject.toml`, `uv tree` og `uv.lock`.

| Specifier | Betyder | Typisk brug |
|-----------|---------|-------------|
| `==2.31.0` | præcis den version | lock files, applikationer |
| `>=2.31` | den eller nyere | libraries |
| `~=2.31` | `>=2.31, <3.0` | "nye features, men ingen breaking changes" |
| `>=2.31,<3` | interval | det samme, skrevet ud |

SemVer: `MAJOR.MINOR.PATCH`. Breaking change → MAJOR, ny feature → MINOR, bugfix → PATCH.

**I gør det samme** i citat-projektet:

1. Tilføj `rich`, og brug den til at printe citatet i farver:

   ```bash
   uv add rich
   ```

   Hvilken specifier skrev `uv` i `pyproject.toml`? Hvilken eksakt version står der i `uv.lock`?
2. Kør `uv tree`. Hvor mange pakker fik I i alt, selv om I kun bad om én?
3. Skriv en specifier for hvert krav, og prøv dem med `uv add`:
   - `rich` version 13, men ikke 14
   - mindst `httpx` 0.27
   - præcis `typer` 0.12.5
4. Hvilket nyt versionsnummer skal jeres pakke have, hvis I: (a) retter en stavefejl i et citat, (b) tilføjer et `--author`-flag, (c) omdøber kommandoen?

**Færdig når:** I kan forklare forskellen på det, der står i `pyproject.toml`, og det, der står i `uv.lock`.

**Prøv bagefter:** Bump versionen i `pyproject.toml`, byg og publicér den nye version på TestPyPI.

---

## Runde 4 · Config og *secrets*

**Demo:** Vi flytter hardcodede værdier ud af `hello_api.py` og ind i environment variables og en `.env`-fil.

**I gør det samme** i jeres bogreols-API:

1. Har API'en ikke en `pyproject.toml`, så lav en: `uv init --app`, og `uv add flask python-dotenv`.
2. Læs config fra environment variables:

   ```python
   import os
   from dotenv import load_dotenv

   load_dotenv()

   HOST = os.environ.get("HOST", "127.0.0.1")
   PORT = int(os.environ.get("PORT", "5000"))
   API_KEY = os.environ["API_KEY"]  # ingen default: crash, hvis den mangler
   ```

   Brug `app.run(host=HOST, port=PORT)`.
3. Kræv headeren `X-API-Key` på `POST`, `PUT` og `DELETE`, og svar `401`, hvis den er forkert.
4. Lav en `.env`:

   ```
   API_KEY=et-langt-tilfældigt-password
   ```

   Lav en tilfældig værdi med `python -c "import secrets; print(secrets.token_hex(32))"`.
5. Tilføj `.env` til `.gitignore`. Lav en `.env.example` med `API_KEY=` uden værdi, og commit den.

**Færdig når:** `git status` ikke viser `.env`, og `DELETE` giver `401` uden header og virker med den.

**Tænk over:** mistral-vibe skal bruge `MISTRAL_API_KEY`. Hvor leder den efter den?

---

## Runde 5 · Dockerfile

**Demo:** Vi bygger et image af API'en og kører det som en container.

**I gør det samme:**

1. Lav en `Dockerfile` ved siden af `pyproject.toml`:

   ```dockerfile
   FROM python:3.12-slim
   COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

   WORKDIR /app
   COPY pyproject.toml uv.lock ./
   RUN uv sync --frozen --no-install-project
   COPY . .

   ENV PATH="/app/.venv/bin:$PATH" HOST=0.0.0.0
   EXPOSE 5000
   CMD ["python", "app.py"]
   ```

   Hedder jeres fil noget andet end `app.py`, så ret det i `CMD`.

2. Lav en `.dockerignore`:

   ```
   .venv
   .env
   ```

3. Byg og kør:

   ```bash
   docker build -t bookshelf-api .
   docker run -p 5000:5000 -e API_KEY=hemmelig bookshelf-api
   ```

**Færdig når:** I kan kalde API'en på `http://localhost:5000` fra Postman.

**Prøv bagefter:** Ret en linje i jeres Python-kode, og byg igen. Hvilke trin står der `CACHED` ved? Hvorfor kopierer vi `pyproject.toml` før resten?

**Tænk over:** Hvad var der sket uden `.env` i `.dockerignore`?

---

## Runde 6 · Docker Compose

**Demo:** Den lange `docker run`-kommando bliver til en fil.

**I gør det samme:**

1. Lav en `docker-compose.yml`:

   ```yaml
   services:
     api:
       build: .
       ports:
         - "5000:5000"
       env_file: .env
   ```

2. Start og stop:

   ```bash
   docker compose up --build
   docker compose down
   ```

**Færdig når:** API'en kører med `docker compose up`, og `API_KEY` kommer fra `.env`.

**Prøv bagefter:** `docker compose config`. Hvem kan læse jeres *secret* nu?

---

## Runde 7 · Push til Docker Hub

**Demo:** Vi pusher et image og kører det på en anden maskine.

**I gør det samme:**

```bash
docker login
docker build -t <dockerhub-bruger>/bookshelf-api:0.1.0 .
docker push <dockerhub-bruger>/bookshelf-api:0.1.0
```

Giv sidemanden navnet på jeres image, og kør sidemandens:

```bash
docker run -p 5000:5000 -e API_KEY=test <sidemand>/bookshelf-api:0.1.0
```

> Har I en Mac med Apple Silicon og sidemanden en Windows-PC? Byg til begge:
> `docker buildx build --platform linux/amd64,linux/arm64 -t <bruger>/bookshelf-api:0.1.0 --push .`

**Færdig når:** I har kørt sidemandens API uden at have deres kode.

**Tænk over:** Sammenlign med Runde 2. Hvad skal modtageren have installeret i hvert tilfælde?

---

## Ekstra · Redis som ekstra service

1. Tilføj et endpoint `/stats`, der tæller requests i Redis (`uv add redis`, og læs forbindelsen fra `REDIS_URL`).
2. Tilføj en service mere i `docker-compose.yml`:

   ```yaml
     cache:
       image: redis:7-alpine
   ```

   og `REDIS_URL=redis://cache:6379` i `.env`.

**Færdig når:** Tælleren stiger, og overlever `docker compose restart api`. Hvad med `docker compose down`?

---

## Opsamling

Tilbage til dagens spørgsmål: **Hvem skal bruge jeres kode, og hvordan får de fat i den?** Hvilken måde passer til den feature, I bygger i mistral-vibe?

---

## Optional

- [optional] MIT: [Packaging and Shipping Code](https://missing.csail.mit.edu/2026/shipping-code/)
- [optional] uv docs: [Building and publishing a package](https://docs.astral.sh/uv/guides/package/)
- [optional] uv docs: [Using uv in Docker](https://docs.astral.sh/uv/guides/integration/docker/)
- [optional] Python Packaging: [Version specifiers](https://packaging.python.org/en/latest/specifications/version-specifiers/)

---

## Kilde

Lektionen bygger på [Packaging and Shipping Code](https://missing.csail.mit.edu/2026/shipping-code/) fra MIT's [The Missing Semester of Your CS Education](https://missing.csail.mit.edu/) (2026), udgivet under [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/).
