# Session 5: Byg en API med Flask

**Uge 40 | Python Elective 2026 Fall**

---

## Læringsmål

- Du kan bygge en simpel API i Flask
- Du kan kalde og teste din API
- Du kan forklare, hvad en route, en HTTP-metode og en statuskode er
- Du kan dokumentere din API med Swagger

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

Det andet hold har ikke adgang til jeres kode — de skal kunne bruge API'en alene ud fra jeres dokumentation. Lever derfor også en **`swagger.json`**, der beskriver præcis de endpoints, I har lavet. Om I skriver den selv eller får den genereret, bestemmer I.

---

## Kom i gang

Installér [Postman](https://www.postman.com/downloads/), [Insomnia](https://insomnia.rest/download) eller lign. før undervisningen.

Kør startfilen [`hello_api.py`](hello_api.py):

```bash
uv run --with flask python hello_api.py
```

Lav en `GET`-request i Postman til `http://127.0.0.1:5000/`.

Byg videre derfra.

---

## Undervejs dukker der nye problemer op

Tag dem, når I når dertil:

- Hvad skal der ske, hvis nogen prøver at hente en bog, der ikke findes?
- Hvad hvis nogen tilføjer en bog uden titel?
- Genstart serveren. Hvor blev bøgerne af?
- Hvordan beviser I, at API'en virker — uden at klikke rundt i Postman hver gang?
- I har ændret et endpoint. Passer `swagger.json` stadig? Tjek det ved at åbne filen i [Swagger Editor](https://editor.swagger.io/) eller importere den i Postman.

---

## Afslutning

Hver gruppe viser på 2 minutter:

- Ét kald til jeres API, der virker
- Jeres `swagger.json` åbnet i Swagger Editor
- Ét problem, I løb ind i, og hvordan I løste det
