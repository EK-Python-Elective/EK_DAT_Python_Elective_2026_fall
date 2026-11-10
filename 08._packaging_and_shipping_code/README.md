# 08. Packaging and Shipping Code

Det er svært at få kode til at virke efter hensigten; det er ofte endnu sværere at få den samme kode til at køre på en anden maskine end din egen.

At *shippe* kode betyder at tage den kode, du har skrevet, og omdanne den til en brugbar form, som andre kan køre uden at have præcis samme opsætning som din computer.
Shipping af kode kan tage mange former og afhænger blandt mange andre faktorer af valget af programmeringssprog, system libraries og operativsystem.
Det afhænger også af, hvad du bygger: et software library, et command line tool og en web service har alle forskellige krav og deployment-trin.
Uanset hvad er der et fælles mønster i alle disse scenarier: vi skal definere, hvad leverancen er — også kaldet _artifact_ — og hvilke antagelser den gør om miljøet omkring den.

I denne lektion gennemgår vi:

- [Dependencies & Environments](#dependencies--environments)
- [Artifacts & Packaging](#artifacts--packaging)
- [Releases & Versioning](#releases--versioning)
- [Reproducibility](#reproducibility)
- [VMs & Containers](#vms--containers)
- [Configuration](#configuration)
- [Services & Orchestration](#services--orchestration)
- [Publishing](#publishing)

Vi forklarer begreberne gennem eksempler fra Python-økosystemet, da konkrete eksempler gør det lettere at forstå. Selvom værktøjerne er anderledes i andre sprogs økosystemer, er begreberne stort set de samme.

# Dependencies & Environments

I moderne softwareudvikling er lag af abstraktion overalt.
Programmer overlader naturligt logik til andre libraries eller services.
Det skaber dog en _dependency_-relation mellem dit program og de libraries, det kræver for at fungere.
I Python henter vi for eksempel ofte indholdet af en hjemmeside sådan her:

```python
import requests

response = requests.get("https://missing.csail.mit.edu")
```

Men `requests`-library'et følger ikke med Python runtime, så hvis vi prøver at køre koden uden at have `requests` installeret, giver Python en fejl:

```console
$ python fetch.py
Traceback (most recent call last):
  File "fetch.py", line 1, in <module>
    import requests
ModuleNotFoundError: No module named 'requests'
```

For at gøre library'et tilgængeligt skal vi først køre `pip install requests` for at installere det.
`pip` er det command line tool, som Python stiller til rådighed til at installere packages.
`pip install requests` udfører følgende trin:

1. Søger efter requests i Python Package Index ([PyPI](https://pypi.org/))
1. Søger efter det passende artifact til den platform, vi kører på
1. Resolver dependencies — `requests`-library'et afhænger selv af andre packages, så installeren skal finde kompatible versioner af alle transitive dependencies og installere dem først
1. Downloader artifacts og pakker dem ud og kopierer filerne de rigtige steder hen i vores filsystem

```console
$ pip install requests
Collecting requests
  Downloading requests-2.32.3-py3-none-any.whl (64 kB)
Collecting charset-normalizer<4,>=2
  Downloading charset_normalizer-3.4.0-cp311-cp311-manylinux_x86_64.whl (142 kB)
Collecting idna<4,>=2.5
  Downloading idna-3.10-py3-none-any.whl (70 kB)
Collecting urllib3<3,>=1.21.1
  Downloading urllib3-2.2.3-py3-none-any.whl (126 kB)
Collecting certifi>=2017.4.17
  Downloading certifi-2024.8.30-py3-none-any.whl (167 kB)
Installing collected packages: urllib3, idna, charset-normalizer, certifi, requests
Successfully installed certifi-2024.8.30 charset-normalizer-3.4.0 idna-3.10 requests-2.32.3 urllib3-2.2.3
```

Her kan vi se, at `requests` har sine egne dependencies, såsom `certifi` eller `charset-normalizer`, og at de skal installeres, før `requests` kan installeres.
Når det er installeret, kan Python runtime finde library'et, når det importeres.

```console
$ python -c 'import requests; print(requests.__path__)'
['/usr/local/lib/python3.11/dist-packages/requests']

$ pip list | grep requests
requests        2.32.3
```

Programmeringssprog har forskellige værktøjer, konventioner og praksisser for at installere og publicere libraries.
I nogle sprog som Rust er toolchain'en samlet — `cargo` håndterer building, testing, dependency management og publishing.
I andre, som Python, sker samlingen på specifikationsniveau — i stedet for ét værktøj findes der standardiserede specifikationer, der definerer, hvordan packaging fungerer, hvilket giver plads til flere konkurrerende værktøjer til hver opgave (`pip` vs [`uv`](https://docs.astral.sh/uv/), `setuptools` vs [`hatch`](https://hatch.pypa.io/) vs [`poetry`](https://python-poetry.org/)).
Og i nogle økosystemer som LaTeX kommer distributioner som TeX Live eller MacTeX med tusindvis af packages forudinstalleret.

Når man introducerer dependencies, introducerer man også dependency conflicts.
Konflikter opstår, når programmer kræver inkompatible versioner af den samme dependency.
Hvis `tensorflow==2.3.0` for eksempel kræver `numpy>=1.16.0,<1.19.0`, og `pandas==1.2.0` kræver `numpy>=1.16.5`, så er enhver version, der opfylder `numpy>=1.16.5,<1.19.0`, gyldig.
Men hvis en anden package i dit projekt kræver `numpy>=1.19`, har du en konflikt, hvor ingen version opfylder alle constraints.

Denne situation — hvor flere packages kræver indbyrdes inkompatible versioner af fælles dependencies — kaldes ofte _dependency hell_.
En måde at håndtere konflikter på er at isolere hvert programs dependencies i deres eget _environment_.
I Python opretter vi et virtual environment ved at køre:

```console
$ which python
/usr/bin/python
$ pwd
/home/missingsemester
$ python -m venv venv
$ source venv/bin/activate
$ which python
/home/missingsemester/venv/bin/python
$ which pip
/home/missingsemester/venv/bin/pip
$ python -c 'import requests; print(requests.__path__)'
['/home/missingsemester/venv/lib/python3.11/site-packages/requests']

$ pip list
Package Version
------- -------
pip     24.0
```

Du kan tænke på et environment som en komplet, selvstændig udgave af sprogets runtime med sit eget sæt installerede packages.
Dette virtual environment, eller venv, isolerer de installerede dependencies fra den globale Python-installation.
Det er god praksis at have et virtual environment til hvert projekt, som indeholder de dependencies, projektet kræver.

> Selvom mange moderne operativsystemer leveres med installationer af runtimes som Python, er det uklogt at ændre i dem, da OS'et kan være afhængigt af dem til sin egen funktionalitet. Brug hellere separate environments.

I nogle sprog er installationsprotokollen ikke defineret af et værktøj, men af en specifikation.
I Python definerer [PEP 517](https://peps.python.org/pep-0517/) build system-interfacet, og [PEP 621](https://peps.python.org/pep-0621/) specificerer, hvordan projektets metadata gemmes i `pyproject.toml`.
Det har gjort det muligt for udviklere at forbedre `pip` og lave mere optimerede værktøjer som `uv`. For at installere `uv` er det nok at køre `pip install uv`.

`uv` i stedet for `pip` har samme interface, men er markant hurtigere:

```console
$ uv pip install requests
Resolved 5 packages in 12ms
Prepared 5 packages in 0.45ms
Installed 5 packages in 8ms
 + certifi==2024.8.30
 + charset-normalizer==3.4.0
 + idna==3.10
 + requests==2.32.3
 + urllib3==2.2.3
```

> Vi anbefaler kraftigt at bruge `uv pip` i stedet for `pip`, når det er muligt, da det reducerer installationstiden dramatisk.

Udover at isolere dependencies gør environments det også muligt at have forskellige versioner af sprogets runtime.

```console
$ uv venv --python 3.12 venv312
Using CPython 3.12.7
Creating virtual environment at: venv312

$ source venv312/bin/activate && python --version
Python 3.12.7

$ uv venv --python 3.11 venv311
Using CPython 3.11.10
Creating virtual environment at: venv311

$ source venv311/bin/activate && python --version
Python 3.11.10
```

Det er nyttigt, når du skal teste din kode på tværs af flere Python-versioner, eller når et projekt kræver en bestemt version.

> I nogle programmeringssprog får hvert projekt automatisk sit eget environment til sine dependencies, i stedet for at du opretter det manuelt, men princippet er det samme. De fleste sprog har i dag også en mekanisme til at håndtere flere versioner af sproget på samme system og angive, hvilken version det enkelte projekt skal bruge.

# Artifacts & Packaging

I softwareudvikling skelner vi mellem source code og artifacts. Udviklere skriver og læser source code, mens artifacts er de pakkede, distribuerbare outputs, der produceres ud fra source code'en — klar til at blive installeret eller deployet.
Et artifact kan være så simpelt som en kodefil, vi kører, og så komplekst som en hel Virtual Machine, der indeholder alle de dele, en applikation har brug for.
Se dette eksempel, hvor vi har en Python-fil `greet.py` i den aktuelle mappe:

```console
$ cat greet.py
def greet(name):
    print(f"Hello, {name}!")

$ python -c "from greet import greet; greet('World')"
Hello, World!

$ cd /tmp
$ python -c "from greet import greet; greet('World')"
ModuleNotFoundError: No module named 'greet'
```

Importen fejler, så snart vi skifter til en anden mappe, fordi Python kun leder efter modules bestemte steder (den aktuelle mappe, installerede packages og stierne i `PYTHONPATH`). Packaging løser dette ved at installere koden et kendt sted.

I Python handler packaging af et library om at producere et artifact, som package installers som `pip` eller `uv` kan bruge til at installere de relevante filer.
Python-artifacts kaldes _wheels_ og indeholder al den information, der skal til for at installere en package: kodefilerne, metadata om package'en (navn, version, dependencies) og instruktioner om, hvor filerne skal placeres i environment'et.
For at bygge et artifact skal vi skrive en projektfil (ofte også kaldet et manifest), der beskriver projektets detaljer, de nødvendige dependencies, package'ens version og anden information. I Python bruger vi `pyproject.toml` til det formål.

> `pyproject.toml` er den moderne og anbefalede måde. Selvom ældre packaging-metoder som `requirements.txt` eller `setup.py` stadig understøttes, bør du foretrække `pyproject.toml`, når det er muligt.

Her er en minimal `pyproject.toml` til et library, der også leverer et command-line tool:

```toml
[project]
name = "greeting"
version = "0.1.0"
description = "A simple greeting library"
dependencies = ["typer>=0.9"]

[project.scripts]
greet = "greeting:cli"

[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"
```

`typer`-library'et er en populær Python package til at lave command-line interfaces med minimal boilerplate.

Og den tilhørende `greeting.py`:

```python
import typer


def greet(name: str) -> None:
    print(f"Hello, {name}!")


def cli() -> None:
    typer.run(greet)


if __name__ == "__main__":
    cli()
```

Med denne fil kan vi nu bygge wheel'et:

```console
$ uv build
Building source distribution...
Building wheel from source distribution...
Successfully built dist/greeting-0.1.0.tar.gz
Successfully built dist/greeting-0.1.0-py3-none-any.whl

$ ls dist/
greeting-0.1.0-py3-none-any.whl
greeting-0.1.0.tar.gz
```

`.whl`-filen er wheel'et (et zip-arkiv med en bestemt struktur), og `.tar.gz` er en source distribution til systemer, der skal bygge fra source.

Du kan inspicere indholdet af et wheel for at se, hvad der bliver pakket:

```console
$ unzip -l dist/greeting-0.1.0-py3-none-any.whl
Archive:  dist/greeting-0.1.0-py3-none-any.whl
  Length      Date    Time    Name
---------  ---------- -----   ----
      150  2024-01-15 10:30   greeting.py
      312  2024-01-15 10:30   greeting-0.1.0.dist-info/METADATA
       92  2024-01-15 10:30   greeting-0.1.0.dist-info/WHEEL
        9  2024-01-15 10:30   greeting-0.1.0.dist-info/top_level.txt
      435  2024-01-15 10:30   greeting-0.1.0.dist-info/RECORD
---------                     -------
      998                     5 files
```

Hvis vi nu gav dette wheel til en anden, kunne vedkommende installere det ved at køre:

```console
$ uv pip install ./greeting-0.1.0-py3-none-any.whl
$ greet Alice
Hello, Alice!
```

Det installerer det library, vi byggede tidligere, i deres environment — inklusive `greet` CLI-værktøjet.

Denne tilgang har begrænsninger. Især hvis vores library afhænger af platformspecifikke libraries, f.eks. CUDA til GPU-acceleration, så virker vores artifact kun på systemer, hvor de specifikke libraries er installeret, og vi kan blive nødt til at bygge separate wheels til forskellige platforme (Linux, macOS, Windows) og arkitekturer (x86, ARM).

Når man installerer software, er der en vigtig forskel på at installere fra source og at installere en prebuilt binary. At installere fra source betyder at downloade den originale kode og kompilere den på din maskine — det kræver, at du har en compiler og build tools installeret, og det kan tage lang tid for store projekter.

At installere en prebuilt binary betyder at downloade et artifact, som allerede er kompileret af en anden — hurtigere og enklere, men binary'en skal matche din platform og arkitektur.
For eksempel viser [ripgreps releases-side](https://github.com/BurntSushi/ripgrep/releases) prebuilt binaries til Linux (x86_64, ARM), macOS (Intel, Apple Silicon) og Windows.

# Releases & Versioning

Kode bygges i en kontinuerlig proces, men releases i diskrete trin.
I softwareudvikling er der en klar skelnen mellem development- og production-environments.
Kode skal have bevist, at den virker i et dev-environment, før den bliver _shippet_ til prod.
Release-processen består af mange trin, herunder testing, dependency management, versioning, configuration, deployment og publishing.

Software libraries er ikke statiske; de udvikler sig over tid med fejlrettelser og nye features.
Vi følger denne udvikling med diskrete versions-identifiers, der svarer til library'ets tilstand på et bestemt tidspunkt.
Ændringer i et library's opførsel kan spænde fra patches, der retter ikke-kritisk funktionalitet, over nye features, der udvider funktionaliteten, til ændringer, der bryder bagudkompatibiliteten.
Changelogs dokumenterer, hvilke ændringer en version introducerer — det er dokumenter, som udviklere bruger til at kommunikere ændringerne i en ny release.

Det er dog upraktisk at holde styr på de løbende ændringer i hver eneste dependency, og endnu mere når vi tager de transitive dependencies med — altså vores dependencies' dependencies.

> Du kan visualisere hele dit projekts dependency tree med `uv tree`, som viser alle packages og deres transitive dependencies i en træstruktur.

For at forenkle problemet findes der konventioner for, hvordan man versionerer software, og en af de mest udbredte er [Semantic Versioning](https://semver.org/), eller SemVer.
Under Semantic Versioning har en version en identifier på formen MAJOR.MINOR.PATCH, hvor hver værdi er et heltal. Kort fortalt gælder det ved en opgradering af:

- PATCH (f.eks. 1.2.3 → 1.2.4), at den kun bør indeholde fejlrettelser og være fuldt bagudkompatibel
- MINOR (f.eks. 1.2.3 → 1.3.0), at den tilføjer ny funktionalitet på en bagudkompatibel måde
- MAJOR (f.eks. 1.2.3 → 2.0.0), at den indeholder breaking changes, som kan kræve ændringer i koden

> Dette er en forenkling, og vi opfordrer til at læse hele SemVer-specifikationen for f.eks. at forstå, hvorfor et skift fra 0.1.3 til 0.2.0 kan give breaking changes, eller hvad 1.0.0-rc.1 betyder.

Python packaging understøtter standardiserede version specifiers defineret af [PEP 440](https://peps.python.org/pep-0440/), så når vi angiver versionerne af vores dependencies, kan vi bruge forskellige constraints.

I `pyproject.toml` har vi forskellige måder at afgrænse intervallet af kompatible versioner for vores dependencies:

```toml
[project]
dependencies = [
    "requests==2.32.3",  # Exact version - only this specific version
    "click>=8.0",        # Minimum version - 8.0 or newer
    "numpy>=1.24,<2.0",  # Range - at least 1.24 but less than 2.0
    "pandas~=2.1.0",     # Compatible release - >=2.1.0 and <2.2.0
]
```

Version specifiers findes i mange package managers (npm, cargo osv.) med lidt forskellig præcis semantik. `~=`-operatoren er Pythons "compatible release"-operator — `~=2.1.0` betyder "enhver version, der er kompatibel med 2.1.0", hvilket svarer til `>=2.1.0` og `<2.2.0`. Det svarer nogenlunde til caret-operatoren (`^`) i npm og cargo, som følger SemVers idé om kompatibilitet.

Ikke al software bruger semantic versioning. Et almindeligt alternativ er Calendar Versioning (CalVer), hvor versioner er baseret på udgivelsesdatoer i stedet for semantisk betydning. Ubuntu bruger for eksempel versioner som `24.04` (april 2024) og `24.10` (oktober 2024). CalVer gør det let at se, hvor gammel en release er, men siger ikke noget om kompatibilitet. Endelig er semantic versioning ikke ufejlbarlig, og nogle gange kommer maintainers utilsigtet til at introducere breaking changes i minor- eller patch-releases.

# Reproducibility

I moderne softwareudvikling ligger den kode, du skriver, oven på et betydeligt antal lag af abstraktion.
Det omfatter ting som sprogets runtime, third party libraries, operativsystemet eller endda selve hardwaren.
Enhver forskel i et af disse lag kan ændre din kodes opførsel eller endda forhindre den i at virke efter hensigten.
Desuden påvirker selv forskelle i den underliggende hardware din evne til at shippe software.

At *pinne* et library betyder at angive en eksakt version i stedet for et interval, f.eks. `requests==2.32.3` i stedet for `requests>=2.0`.

En del af en package managers job er at tage højde for alle de constraints, der stilles af dependencies — og transitive dependencies — og derefter producere en gyldig liste af versioner, der opfylder dem alle.
Den konkrete liste af versioner kan så gemmes i en fil af hensyn til reproducibility; sådanne filer kaldes _lock files_.

```console
$ uv lock
Resolved 12 packages in 45ms

$ cat uv.lock | head -20
version = 1
requires-python = ">=3.11"

[[package]]
name = "certifi"
version = "2024.8.30"
source = { registry = "https://pypi.org/simple" }
sdist = { url = "https://files.pythonhosted.org/...", hash = "sha256:..." }
wheels = [
    { url = "https://files.pythonhosted.org/...", hash = "sha256:..." },
]
...
```

En afgørende skelnen, når det gælder dependency-versionering og reproducibility, er forskellen mellem libraries og applications/services.
Et library er beregnet til at blive importeret og brugt af anden kode, som kan have sine egne dependencies, så alt for stramme version constraints kan skabe konflikter med brugerens andre dependencies.
Applications eller services er derimod slutforbrugere af softwaren og eksponerer typisk deres funktionalitet gennem en brugerflade eller en API, ikke gennem et programmeringsinterface.
For libraries er det god praksis at angive versionsintervaller for at maksimere kompatibiliteten med resten af package-økosystemet. For applications sikrer pinning af eksakte versioner reproducibility — alle, der kører applikationen, bruger præcis de samme dependencies.

For projekter, der kræver maksimal reproducibility, tilbyder værktøjer som [Nix](https://nixos.org/) og [Bazel](https://bazel.build/) _hermetic_ builds — hvor ethvert input, inklusive compilere, system libraries og selve build-environment'et, er pinnet og content-addressed. Det garanterer bit-for-bit identiske outputs, uanset hvornår eller hvor buildet kører.

> Du kan endda bruge NixOS til at styre hele din computerinstallation, så du nemt kan starte nye kopier af din opsætning og styre hele dens konfiguration via versionsstyrede konfigurationsfiler.

En evig spænding i softwareudvikling er, at nye softwareversioner introducerer fejl — enten bevidst eller ubevidst — mens gamle softwareversioner med tiden bliver kompromitteret af sikkerhedshuller.
Vi kan håndtere dette ved at bruge continuous integration pipelines (mere om det i lektionen [Code Quality and CI](https://missing.csail.mit.edu/2026/code-quality/)), der tester vores applikation mod nye softwareversioner, og ved at have automatisering, der opdager, når der udkommer nye versioner af vores dependencies, såsom [Dependabot](https://github.com/dependabot).

Selv med CI-tests på plads opstår der stadig problemer ved opgradering af softwareversioner, ofte på grund af den uundgåelige forskel mellem dev- og prod-environments.
I de situationer er det bedste at have en _rollback_-plan, hvor versionsopgraderingen rulles tilbage, og en kendt fungerende version deployes i stedet.

# VMs & Containers

Når du begynder at afhænge af mere komplekse dependencies, vil din kodes dependencies sandsynligvis række ud over, hvad package manageren kan håndtere.
En almindelig årsag er behovet for at interagere med bestemte system libraries eller hardware drivers.
Inden for scientific computing og AI har programmer for eksempel ofte brug for specialiserede libraries og drivers for at udnytte GPU-hardware.
Mange dependencies på systemniveau (GPU drivers, bestemte compiler-versioner, shared libraries som OpenSSL) kræver stadig en systemdækkende installation.

Traditionelt blev dette bredere dependency-problem løst med Virtual Machines (VMs).
VMs abstraherer hele computeren og giver et fuldstændigt isoleret environment med sit eget dedikerede operativsystem.
En mere moderne tilgang er containers, som pakker en applikation sammen med dens dependencies, libraries og filsystem, men deler værtens operating system kernel i stedet for at virtualisere en hel computer.
Containers er lettere end VMs, fordi de deler kernel'en, hvilket gør dem hurtigere at starte og mere effektive at køre.

Den mest populære container-platform er [Docker](https://www.docker.com/). Docker introducerede en standardiseret måde at bygge, distribuere og køre containers på. Under motorhjelmen bruger Docker containerd som container runtime — en industristandard, som også andre værktøjer som Kubernetes bruger.

Det er ligetil at køre en container. For eksempel bruger vi `docker run` til at køre en Python-interpreter inde i en container (flagene `-it` gør containeren interaktiv med en terminal. Når du afslutter, stopper containeren.).

```console
$ docker run -it python:3.12 python
Python 3.12.7 (main, Nov  5 2024, 02:53:25) [GCC 12.2.0] on linux
>>> print("Hello from inside a container!")
Hello from inside a container!
```

I praksis kan dit program afhænge af hele filsystemet.
For at løse det kan vi bruge container images, som shipper applikationens fulde filsystem som artifact.
Container images oprettes programmatisk. Med Docker angiver vi præcist imagets dependencies, system libraries og konfiguration med Dockerfile-syntaks:

```dockerfile
FROM python:3.12
RUN apt-get update
RUN apt-get install -y gcc
RUN apt-get install -y libpq-dev
RUN pip install numpy
RUN pip install pandas
COPY . /app
WORKDIR /app
RUN pip install .
```

En vigtig skelnen: et Docker **image** er det pakkede artifact (som en skabelon), mens en **container** er en kørende instans af det image. Du kan køre flere containers fra det samme image. Images bygges i lag (layers), hvor hver instruktion (`FROM`, `RUN`, `COPY` osv.) i en Dockerfile skaber et nyt layer. Docker cacher disse layers, så hvis du ændrer en linje i din Dockerfile, skal kun det layer og de efterfølgende layers bygges igen.

Den forrige Dockerfile har flere problemer: den bruger det fulde Python-image i stedet for en slim-variant, kører separate `RUN`-kommandoer, der skaber unødvendige layers, versioner er ikke pinnet, og den rydder ikke op i package managerens caches, så der shippes unødvendige filer. Andre hyppige fejl er at køre containers usikkert som root og ved et uheld at indlejre secrets i layers.

Her er en forbedret version:

```dockerfile
FROM python:3.12-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc libpq-dev && \
    rm -rf /var/lib/apt/lists/*
WORKDIR /app
ENV PATH="/app/.venv/bin:$PATH"
COPY pyproject.toml uv.lock ./
RUN uv sync --locked --no-dev --no-install-project
COPY . .
RUN uv sync --locked --no-dev
```

I eksemplet ovenfor ser vi, at i stedet for at installere `uv` fra source kopierer vi den prebuilt binary fra `ghcr.io/astral-sh/uv:latest`-imaget. Det kaldes _builder_ pattern. Med dette pattern behøver vi ikke at shippe alle de værktøjer, der skal til for at kompilere vores kode — kun den endelige binary, der skal til for at køre applikationen (`uv` i dette tilfælde).

Docker har vigtige begrænsninger, man skal være opmærksom på. For det første er container images ofte platformspecifikke — et image bygget til `linux/amd64` kører ikke native på `linux/arm64` (Apple Silicon Macs) uden emulering, hvilket er langsomt. For det andet kræver Docker-containers en Linux kernel, så på macOS og Windows kører Docker faktisk en letvægts Linux-VM under motorhjelmen, hvilket giver ekstra overhead. For det tredje er Dockers isolation svagere end VMs — containers deler værtens kernel, hvilket er et sikkerhedsproblem i multi-tenant-environments.

> I dag bruger flere og flere projekter også Nix til at styre selv "systemdækkende" libraries og applikationer per projekt via [nix flakes](https://serokell.io/blog/practical-nix-flakes).

# Configuration

Software er i sagens natur konfigurerbar. I lektionen [Command-line Environment](https://missing.csail.mit.edu/2026/command-line-environment/) så vi programmer, der modtager options via flags, environment variables eller endda konfigurationsfiler, også kaldet dotfiles. Det gælder også for mere komplekse applikationer, og der findes etablerede patterns til at håndtere konfiguration i stor skala.
Softwarekonfiguration bør ikke være indlejret i koden, men leveres ved runtime.
To almindelige måder er environment variables og config files.

Her er et eksempel på en applikation, der konfigureres via environment variables:

```python
import os

DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///local.db")
DEBUG = os.environ.get("DEBUG", "false").lower() == "true"
API_KEY = os.environ["API_KEY"]  # Required - will raise if not set
```

En applikation kan også konfigureres via en konfigurationsfil (f.eks. et Python-program, der indlæser en config via `yaml.load`), `config.yaml`:

```yaml
database:
  url: "postgresql://localhost/myapp"
  pool_size: 5
server:
  host: "0.0.0.0"
  port: 8080
  debug: false
```

En god tommelfingerregel for konfiguration er, at den samme codebase skal kunne deployes til forskellige environments (development, staging, production) udelukkende med ændringer i konfigurationen — aldrig ændringer i koden.

Blandt de mange konfigurationsmuligheder er der ofte følsomme data som API keys.
Secrets skal håndteres varsomt, så de ikke eksponeres ved et uheld, og de må ikke komme med i version control.

# Services & Orchestration

Moderne applikationer eksisterer sjældent isoleret. En typisk webapplikation kan have brug for en database til persistent storage, en cache for performance, en message queue til baggrundsopgaver og diverse andre understøttende services. I stedet for at samle alt i én monolitisk applikation opdeler moderne arkitekturer ofte funktionaliteten i separate services, der kan udvikles, deployes og skaleres uafhængigt af hinanden.

Hvis vi for eksempel vurderer, at vores applikation kunne have gavn af en cache, kan vi i stedet for at lave vores egen bruge eksisterende, gennemtestede løsninger som [Redis](https://redis.io/) eller [Memcached](https://memcached.org/).
Vi kunne indlejre Redis i vores applikations dependencies ved at bygge den som en del af containeren, men så skal alle dependencies mellem Redis og vores applikation harmoniseres, hvilket kan være svært eller endda umuligt.
I stedet kan vi deploye hver applikation separat i sin egen container.
Det kaldes ofte en microservice-arkitektur, hvor hver komponent kører som en selvstændig service, der kommunikerer over netværket, typisk via HTTP APIs.

[Docker Compose](https://docs.docker.com/compose/) er et værktøj til at definere og køre multi-container-applikationer. I stedet for at håndtere containers enkeltvis deklarerer du alle services i én YAML-fil og orkestrerer dem samlet. Nu består vores samlede applikation af mere end én container:

```yaml
# docker-compose.yml
services:
  web:
    build: .
    ports:
      - "8080:8080"
    environment:
      - REDIS_URL=redis://cache:6379
    depends_on:
      - cache

  cache:
    image: redis:7-alpine
    volumes:
      - redis_data:/data

volumes:
  redis_data:
```

Med `docker compose up` starter begge services sammen, og webapplikationen kan forbinde til Redis via hostname'et `cache` (Dockers interne DNS resolver automatisk service-navne).
Docker Compose lader os deklarere, hvordan vi vil deploye en eller flere services, og håndterer orkestreringen: at starte dem sammen, sætte netværk op mellem dem og håndtere delte volumes til data persistence.

Ved production deployments vil du ofte have, at dine docker compose services starter automatisk ved boot og genstarter ved fejl. En almindelig tilgang er at bruge systemd til at styre docker compose-deploymentet:

```ini
# /etc/systemd/system/myapp.service
[Unit]
Description=My Application
Requires=docker.service
After=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=/opt/myapp
ExecStart=/usr/bin/docker compose up -d
ExecStop=/usr/bin/docker compose down

[Install]
WantedBy=multi-user.target
```

Denne systemd unit file sikrer, at din applikation starter, når systemet booter (efter Docker er klar), og giver standardkommandoer som `systemctl start myapp`, `systemctl stop myapp` og `systemctl status myapp`.

Efterhånden som deployment-kravene bliver mere komplekse — skalerbarhed på tværs af flere maskiner, fault tolerance når services crasher, og garantier for high availability — vender organisationer sig mod avancerede container orchestration-platforme som Kubernetes (k8s), der kan håndtere tusindvis af containers på tværs af clusters af maskiner. Når det er sagt, har Kubernetes en stejl læringskurve og betydeligt driftsmæssigt overhead, så det er ofte overkill til mindre projekter.

Denne multi-container-opsætning er delvist mulig, fordi moderne services kommunikerer med hinanden via standardiserede APIs, typisk HTTP REST APIs. Når et program for eksempel interagerer med en LLM-udbyder som OpenAI eller Anthropic, sender det under motorhjelmen en HTTP request til deres servere og parser svaret:

```console
$ curl https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "content-type: application/json" \
    -H "anthropic-version: 2023-06-01" \
    -d '{"model": "claude-sonnet-4-20250514", "max_tokens": 256,
         "messages": [{"role": "user", "content": "Explain containers vs VMs in one sentence."}]}'
```

# Publishing

Når du har vist, at din kode virker, vil du måske distribuere den, så andre kan downloade og installere den.
Distribution kan tage mange former og hænger uløseligt sammen med det programmeringssprog og de environments, du arbejder med.

Den simpleste form for distribution er at uploade artifacts, som folk kan downloade og installere lokalt.
Det er stadig udbredt og ses f.eks. i [Ubuntus package archive](http://archive.ubuntu.com/ubuntu/pool/main/), som i bund og grund er en HTTP-mappeoversigt over `.deb`-filer.

I dag er GitHub blevet de facto-platformen til at publicere source code og artifacts.
Mens source code'en ofte er offentligt tilgængelig, giver GitHub Releases maintainers mulighed for at vedhæfte prebuilt binaries og andre artifacts til taggede versioner.

Package managers understøtter nogle gange installation direkte fra GitHub, enten fra source eller fra et prebuilt wheel:

```console
# Install from source (will clone and build)
$ pip install git+https://github.com/psf/requests.git

# Install from a specific tag/branch
$ pip install git+https://github.com/psf/requests.git@v2.32.3

# Install a wheel directly from a GitHub release
$ pip install https://github.com/user/repo/releases/download/v1.0/package-1.0-py3-none-any.whl
```

Nogle sprog som Go bruger faktisk en decentral distributionsmodel — i stedet for et centralt package repository distribueres Go modules direkte fra deres source code repositories.
Module paths som `github.com/gorilla/mux` angiver, hvor koden ligger, og `go get` henter direkte derfra. De fleste package managers som `pip`, `cargo` eller `brew` har dog centrale indexes over færdigpakkede projekter, så distribution og installation bliver nemmere. Hvis vi kører

```console
$ uv pip install requests --verbose --no-cache 2>&1 | grep -F '.whl'
DEBUG Selecting: requests==2.32.5 [compatible] (requests-2.32.5-py3-none-any.whl)
DEBUG No cache entry for: https://files.pythonhosted.org/packages/1e/db/4254e3eabe8020b458f1a747140d32277ec7a271daf1d235b70dc0b4e6e3/requests-2.32.5-py3-none-any.whl.metadata
DEBUG No cache entry for: https://files.pythonhosted.org/packages/1e/db/4254e3eabe8020b458f1a747140d32277ec7a271daf1d235b70dc0b4e6e3/requests-2.32.5-py3-none-any.whl
```

kan vi se, hvorfra vi henter `requests`-wheel'et. Læg mærke til `py3-none-any` i filnavnet — det betyder, at wheel'et virker med enhver Python 3-version, på ethvert OS og på enhver arkitektur. For packages med kompileret kode er wheel'et platformspecifikt:

```console
$ uv pip install numpy --verbose --no-cache 2>&1 | grep -F '.whl'
DEBUG Selecting: numpy==2.2.1 [compatible] (numpy-2.2.1-cp312-cp312-macosx_14_0_arm64.whl)
```

Her angiver `cp312-cp312-macosx_14_0_arm64`, at dette wheel specifikt er til CPython 3.12 på macOS 14+ til ARM64 (Apple Silicon). Er du på en anden platform, downloader `pip` et andet wheel eller bygger fra source.

Omvendt: for at andre kan finde en package, vi har lavet, skal vi publicere den til et af disse registries.
I Python er det primære registry [Python Package Index (PyPI)](https://pypi.org).
Ligesom ved installation er der flere måder at publicere packages på. Kommandoen `uv publish` giver et moderne interface til at uploade packages til PyPI:

```console
$ uv publish --publish-url https://test.pypi.org/legacy/
Publishing greeting-0.1.0.tar.gz
Publishing greeting-0.1.0-py3-none-any.whl
```

Her bruger vi [TestPyPI](https://test.pypi.org) — et separat package registry beregnet til at teste dit publishing-workflow uden at forurene det rigtige PyPI. Når den er uploadet, kan du installere fra TestPyPI:

```console
$ uv pip install --index-url https://test.pypi.org/simple/ greeting
```

En central overvejelse ved publicering af software er tillid (trust). Hvordan kan brugere verificere, at den package, de downloader, faktisk kommer fra dig og ikke er blevet manipuleret? Package registries bruger checksums til at verificere integriteten, og nogle økosystemer understøtter package signing for at give kryptografisk bevis for forfatterskab.

Forskellige sprog har deres egne package registries: [crates.io](https://crates.io) til Rust, [npm](https://www.npmjs.com) til JavaScript, [RubyGems](https://rubygems.org) til Ruby og [Docker Hub](https://hub.docker.com) til container images. Til private eller interne packages deployer organisationer ofte deres egne package repositories (såsom en privat PyPI-server eller et privat Docker registry) eller bruger managed løsninger fra cloud-udbydere.

At deploye en web service på internettet kræver yderligere infrastruktur: registrering af et domænenavn, DNS-konfiguration, der peger dit domæne på din server, og ofte en reverse proxy som nginx til at håndtere HTTPS og route trafik. Til simplere formål som dokumentation eller statiske sites tilbyder [GitHub Pages](https://pages.github.com/) gratis hosting direkte fra et repository.

# Øvelser

1. Gem dit environment med `printenv` i en fil, opret et venv, aktivér det, kør `printenv` til en anden fil og `diff before.txt after.txt`. Hvad ændrede sig i environment'et? Hvorfor foretrækker shell'en venv'et? (Hint: se på `$PATH` før og efter aktivering.) Kør `which deactivate` og ræsonnér over, hvad bash-funktionen `deactivate` gør.
1. Opret en Python package med en `pyproject.toml` og installér den i et virtual environment. Opret en lockfile og inspicér den.
1. Installér Docker og brug det til at bygge Missing Semester-kursets hjemmeside lokalt med docker compose.
1. Skriv en Dockerfile til en simpel Python-applikation. Skriv derefter en `docker-compose.yml`, der kører din applikation sammen med en Redis-cache.
1. Publicér en Python package til TestPyPI (publicér ikke til det rigtige PyPI, medmindre den er værd at dele!). Byg derefter et Docker image med den package og push det til `ghcr.io`.
1. Lav en hjemmeside med [GitHub Pages](https://docs.github.com/en/pages/quickstart). Ekstra (ikke-)point: konfigurér den med et custom domain.

---

> 📚 **Kilde:** Dansk oversættelse af lektionen [*Packaging and Shipping Code*](https://missing.csail.mit.edu/2026/shipping-code/) fra MIT's kursus [The Missing Semester of Your CS Education](https://missing.csail.mit.edu/) (2026). Originalen er udgivet under [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/), og denne oversættelse deles under samme licens. Tekniske termer er bevidst bevaret på engelsk.
>
> 🎥 **Video (engelsk):** [youtube.com/watch?v=KBMiB-8P4Ns](https://www.youtube.com/watch?v=KBMiB-8P4Ns)
