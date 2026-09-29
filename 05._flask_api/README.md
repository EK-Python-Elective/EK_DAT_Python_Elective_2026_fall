# Session 5: Byg en API med Flask

**Uge 40 | Python Elective 2026 Fall**

---

## Læringsmål

- Du kan bygge en simpel API i Flask
- Du kan kalde og teste din API
- Du kan forklare, hvad en route, en HTTP-metode og en statuskode er

---

## Problemet

Studieforeningen har en bogreol, som alle kan låne fra — men ingen ved, hvilke bøger der er der, eller hvem der har lånt hvad. Et andet hold bygger en app til det, men de mangler en **API** at hente data fra.

**Jeres opgave: byg den API.**

Appen skal kunne:

1. Vise alle bøger på reolen
2. Tilføje en ny bog
3. Markere en bog som udlånt — og som afleveret igen
4. Fjerne en bog

Hvordan URL'erne ser ud, og hvad der sendes frem og tilbage, bestemmer I selv. Brug AI så meget I vil.

---

## Kom i gang

Kør startfilen [`hello_api.py`](hello_api.py) og kald den fra en anden terminal:

```bash
uv run --with flask python hello_api.py
```

```bash
curl http://127.0.0.1:5000/
```

Byg videre derfra.

> **Windows:** brug Git Bash til `curl`.

---

## Undervejs dukker der nye problemer op

Tag dem, når I når dertil:

- Hvad skal der ske, hvis nogen prøver at hente en bog, der ikke findes?
- Hvad hvis nogen tilføjer en bog uden titel?
- Genstart serveren. Hvor blev bøgerne af?
- Hvordan beviser I, at API'en virker — uden at køre `curl` i hånden hver gang?

---

## Afslutning

Hver gruppe viser på 2 minutter:

- Ét kald til jeres API, der virker
- Ét problem, I løb ind i, og hvordan I løste det
