# Gode råd til eksamensprojekt og eksamen

> Byg en app, der løser et rigtigt problem, og som virker. Og kend den ud og ind.

---

## Mens du laver projektet

- **Vælg et problem, der er værd at løse.** Find noget, der ikke findes i forvejen, eller som du kan løse bedre end det, der findes. Vær klar til at fortælle, hvad der allerede findes, og hvad din app gør anderledes.
- **Start småt, og få det til at virke.** Lav den mindste version, der virker hele vejen igennem, før du bygger mere på.
- **Commit ofte, med gode beskeder.** Din git-historik viser, hvordan projektet er blevet til, og hjælper dig med at huske dine valg.
- **Hold styr på dine værktøjer.** `uv`, `pyproject.toml`, `uv.lock` og `ruff` skal være i orden. Et projekt, der ikke kan køre på en anden maskine, er ikke færdigt.
- **Skriv en README**, der siger, hvad projektet er, hvordan man kører det, og hvordan det er bygget op.
- **Ingen hemmeligheder i git.** Brug `.env` og `.env.example`.
- **Test fra en ren mappe.** Klon dit repo et nyt sted og følg din egen README. Virker det uden ekstra trin?
- **Fravælg ting med vilje.** Hellere få features, der virker og som du forstår, end mange halve.
- **Byg til production, ikke til en demo.** Du skal aflevere en færdig applikation, som en potentiel bruger kan tage i brug, uden at den fejler. Tænk som en bruger: hvad sker der ved forkert input, et tomt felt, en API, der ikke svarer, eller en database uden data? Applikationen skal give en forståelig besked, ikke crashe.
- **Lad en anden prøve den.** Giv appen til en ven eller medstuderende uden at forklare noget. Hvor går de i stå, og hvad får den til at fejle?

## AI

- AI må bruges til alt, men **du står inde for hver linje**.
- Når AI skriver kode for dig: læs den, kør den, og spørg dig selv "hvorfor sådan?". Kan du ikke svare, så spørg AI'en eller skriv det om, indtil du kan.
- Brug AI til at øve dig: "Stil mig fem eksamensspørgsmål om denne fil."
- Slet kode, du ikke bruger eller ikke forstår. Død kode giver spørgsmål, du ikke kan svare på.

## Forberedelse til eksamen

- **Kend din kode.** Gå hver fil igennem og forklar den højt for dig selv: hvad gør den, og hvorfor er den bygget sådan?
- **Kend dine valg.** Hvorfor Flask/Streamlit/httpx/Docker (eller det, du har valgt)? Hvad var alternativet?
- **Kend dine svagheder.** Hvad ville du lave om med mere tid? Det er et godt svar at have klar.
- **Øv demoen.** Hav projektet kørende og klar, før eksamen starter. Hav en plan B (skærmbilleder eller en optagelse), hvis noget driller.
- **Kobl til pensum.** Kunne forklare de begreber, du bruger: type hints, HTTP-metoder og statuskoder, `st.session_state`, Docker-images vs. containere, SemVer, osv.
- **Tag tid.** Du har 10 minutter til præsentationen. Øv den, så den holder sig inden for tiden.

## Til eksamen

- **Vis, mens du forklarer.** Åbn koden og peg, i stedet for at tale abstrakt.
- **Det er okay at tænke højt.** Ved du ikke svaret med det samme, så ræsonnér dig frem til det. Det tæller mere end et hurtigt gæt.
- **Sig "det ved jeg ikke", hvis det er sandt**, og fortæl så, hvordan du ville finde ud af det.
- **Vær ærlig om AI.** Det er tilladt. Fortæl, hvordan du brugte det, og hvad du selv har ændret.

## Tjekliste før aflevering

- [ ] Projektet kan klones og køres med instruktionerne i README
- [ ] Applikationen er færdig og klar til production: en ny bruger kan bruge den, uden at den fejler
- [ ] `ruff check` og `ruff format --check` er grønne
- [ ] Ingen hemmeligheder eller `.env` i repoet
- [ ] README forklarer, hvad, hvordan og hvorfor
- [ ] Jeg kan forklare hver fil i projektet
