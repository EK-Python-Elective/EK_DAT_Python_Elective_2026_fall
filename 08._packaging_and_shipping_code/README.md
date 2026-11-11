# Session 8: Packaging and Shipping Code

**Uge 44 | Python Elective 2026 Fall**

> Din kode virker på din maskine — men virker den på alle andres? I dag ser vi på, hvordan man får Python-kode fra "det kører hos mig" til noget, andre kan installere, køre og deploye.

---

## Om dagens lektion

I dag gennemgår vi udvalgte elementer fra lektionen **[Packaging and Shipping Code](https://missing.csail.mit.edu/2026/shipping-code/)** fra MIT's kursus *The Missing Semester of Your CS Education* (2026). Lektionen bruger Python-økosystemet som eksempel, så den passer direkte ind i vores kursus.

Læs lektionen hos MIT før eller under undervisningen — den indeholder alle forklaringer og kodeeksempler, som øvelserne nedenfor bygger på.

Vi kommer omkring:

- **Dependencies & Environments** — dependency conflicts, *dependency hell* og virtual environments med `uv venv`
- **Artifacts & Packaging** — `pyproject.toml`, `[project.scripts]`, wheels og `uv build`
- **Releases & Versioning** — Semantic Versioning (SemVer), version specifiers (`==`, `>=`, `~=`) og `uv tree`
- **Reproducibility** — pinning, lock files (`uv.lock`) og forskellen på libraries og applications
- **VMs & Containers** — Docker images vs. containers, layers, Dockerfiles og builder pattern
- **Configuration** — environment variables, config files og secrets uden for version control
- **Services & Orchestration** — Docker Compose og multi-container-applikationer
- **Publishing** — PyPI, TestPyPI og `uv publish`

---

## Læringsmål

- Du kan forklare, hvad et virtual environment er, og hvorfor hvert projekt bør have sit eget
- Du kan pakke et Python-projekt med `pyproject.toml` og bygge et wheel med `uv build`
- Du kan læse og skrive version specifiers og forklare SemVer
- Du forstår, hvad en lock file er, og hvornår man pinner versioner
- Du kan konfigurere en applikation via environment variables og holde secrets ude af Git
- Du kan skrive en Dockerfile og en `docker-compose.yml` til en Python-applikation

---

## Før undervisningen

- Læs [Packaging and Shipping Code](https://missing.csail.mit.edu/2026/shipping-code/) hos MIT.
- Installér [Docker Desktop](https://www.docker.com/products/docker-desktop/) (eller Docker Engine på Linux), og tjek at `docker run hello-world` virker.
- Opret en bruger på [TestPyPI](https://test.pypi.org/account/register/) (bruges i øvelse 2).

---

## Øvelser

> 💡 Brug gerne AI-værktøjer (mistral-vibe, Claude Code, Copilot …) til øvelserne — men sørg for, at du kan forklare hvert trin bagefter.

### Øvelse 1 — Hvor kommer `python` fra?

Målet er at forstå, hvad der *faktisk* sker, når du aktiverer et virtual environment.

1. Skriv et lille script `where_am_i.py`, der printer:
   - `sys.executable` (hvilken Python-fortolker kører?)
   - `sys.prefix` og `sys.base_prefix` (er vi i et venv?)
   - `sys.path` (hvor leder Python efter modules?)
   - `sys.version`
2. Kør scriptet med systemets Python.
3. Opret to environments med forskellige Python-versioner:
   ```console
   $ uv venv --python 3.12 venv312
   $ uv venv --python 3.13 venv313
   ```
4. Aktivér hvert environment på skift og kør scriptet igen. Hvad ændrer sig?
5. Gem output fra `printenv` før og efter `source venv312/bin/activate` i to filer og kør `diff before.txt after.txt`. Hvilke variabler har ændret sig, og hvorfor betyder det, at shell'en finder venv'ets `python`?
6. Udvid scriptet, så det printer `"Du kører i et virtual environment"` eller `"Du kører med systemets Python"` ud fra `sys.prefix != sys.base_prefix`.

### Øvelse 2 — Byg og ship dit eget CLI-værktøj

Lav et lille command-line tool fra bunden og gør det installerbart.

1. Opret et nyt projekt med `uv init --package <dit-navn>-quote` (brug dit navn, så package-navnet er unikt på TestPyPI).
2. Lav et CLI-værktøj med [`typer`](https://typer.tiangolo.com/), der printer et tilfældigt citat — fx `quote` og `quote --author "Ada Lovelace"`.
3. Registrér kommandoen under `[project.scripts]` i `pyproject.toml`, ligesom `greet` i MIT-lektionen. (Kig også i mistral-vibes `pyproject.toml` — hvordan bliver kommandoen `vibe` defineret?)
4. Byg projektet med `uv build` og inspicér wheel'et med `unzip -l dist/*.whl`. Hvilke filer er med? Hvad står der i `METADATA`?
5. Opret et helt nyt venv i en **anden mappe**, installér wheel'et med `uv pip install sti/til/dit.whl`, og kør din kommando derfra.
6. Publicér til TestPyPI med `uv publish --publish-url https://test.pypi.org/legacy/` og installér den igen fra TestPyPI:
   ```console
   $ uv pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ <dit-navn>-quote
   ```
   (Hvorfor skal vi bruge `--extra-index-url` her? Tip: hvor ligger `typer`?)

### Øvelse 3 — Versioner, lock files og dependency hell

1. Tilføj `requests`, `rich` og `httpx` til dit projekt fra øvelse 2 med `uv add`. Kig i `pyproject.toml` — hvilke version specifiers har `uv` valgt?
2. Kør `uv tree`. Hvor mange **transitive** dependencies har du fået? Hvilke packages deles af flere af dine dependencies?
3. Åbn `uv.lock` og find `certifi`. Hvilken eksakt version er låst, og hvad bruges `hash`-feltet til?
4. Fremprovokér en dependency conflict: tilføj to constraints, der ikke kan opfyldes samtidig (fx `uv add "httpx<0.20" "httpx>=0.27"` eller en package, der kræver en nyere version end en anden tillader). Læs fejlbeskeden fra `uv` og forklar den med dine egne ord.
5. Ret versionsnummeret på dit projekt efter SemVer for hver af disse ændringer, og skriv et kort `CHANGELOG.md`:
   - du retter en stavefejl i et citat
   - du tilføjer et `--count`-flag
   - du omdøber kommandoen fra `quote` til `quotes`
6. Kig i mistral-vibes `pyproject.toml` og `uv.lock`. Bruger projektet eksakte versioner (`==`) eller intervaller (`>=`) i `pyproject.toml`? Er mistral-vibe et *library* eller en *application* — og passer valget til MIT-lektionens anbefaling?

### Øvelse 4 — Configuration og secrets

Gør din bogreols-API fra session 5 konfigurerbar uden at ændre i koden.

1. Flyt alle hardcodede værdier (port, debug-mode, database-sti/filnavn …) ud i environment variables, som i MIT-eksemplet:
   ```python
   import os

   PORT = int(os.environ.get("PORT", "5000"))
   DEBUG = os.environ.get("DEBUG", "false").lower() == "true"
   ```
2. Tilføj en "hemmelig" API key, som klienter skal sende i en header (`X-API-Key`). Læs den med `os.environ["API_KEY"]`, så applikationen fejler tydeligt ved opstart, hvis den mangler.
3. Læg dine lokale værdier i en `.env`-fil og indlæs dem med [`python-dotenv`](https://pypi.org/project/python-dotenv/). Tilføj `.env` til `.gitignore`, og lav en `.env.example` uden rigtige secrets, som *må* committes.
4. Supplér med en `config.toml`, der læses med standardbiblioteket `tomllib`. Beslut en rækkefølge: hvad vinder, hvis samme værdi står både i `config.toml` og som environment variable? Implementér det.
5. Sammenlign med mistral-vibe: hvor gemmer den sin `config.toml`, og hvordan finder den din `MISTRAL_API_KEY`?

### Øvelse 5 — Containerize din API med Docker og Redis

1. Skriv en `Dockerfile` til bogreols-API'en fra øvelse 4. Brug det forbedrede eksempel fra MIT-lektionen som udgangspunkt:
   - `python:3.12-slim` som base image
   - kopiér `uv` ind med builder pattern (`COPY --from=ghcr.io/astral-sh/uv:latest ...`)
   - kopiér `pyproject.toml` og `uv.lock` **før** resten af koden, så dependency-laget caches
2. Byg og kør imaget:
   ```console
   $ docker build -t bookshelf-api .
   $ docker run -p 5000:5000 -e API_KEY=hemmelig bookshelf-api
   ```
   > ⚠️ Inde i en container skal Flask lytte på `0.0.0.0` og ikke kun `127.0.0.1` — ellers kan du ikke nå API'en fra din egen maskine. Gør `HOST` konfigurerbar ligesom `PORT`.

   Ændr en linje i din Python-kode og byg igen. Hvilke layers bliver genbrugt fra cachen?
3. Tilføj et endpoint `/stats`, der tæller antal requests i [Redis](https://redis.io/) via [`redis`](https://pypi.org/project/redis/)-package'en. Læs forbindelsen fra `REDIS_URL`.
4. Skriv en `docker-compose.yml` med to services, `web` og `cache` (`redis:7-alpine`), og start det hele med `docker compose up`. Bekræft, at tælleren overlever en genstart af `web`-containeren — men hvad med en genstart af `cache`? Tilføj et volume, så data overlever.
5. **Ekstra:** Push dit image til GitHub Container Registry (`ghcr.io/<dit-github-navn>/bookshelf-api`), og få din Streamlit-app fra session 7 til at køre som en tredje service i samme `docker-compose.yml`.

---

## Kilde

Lektionen bygger på [Packaging and Shipping Code](https://missing.csail.mit.edu/2026/shipping-code/) fra MIT's [The Missing Semester of Your CS Education](https://missing.csail.mit.edu/) (2026), udgivet under [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/).
