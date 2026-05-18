# Exercise: Scavenger Hunt in pyproject.toml

**Type:** Individual — discuss in pairs

**Motivation:** Helps you read and navigate project configuration files — a skill you will need every time you pick up an unfamiliar Python project.

---

Answer these questions using only `pyproject.toml` and `uv.lock` — no googling, no AI:

1. What is the minimum Python version required?
2. Which dependency handles the terminal UI? (hint: look for something UI-related in the dependencies list)
3. What function does typing `vibe` in the terminal actually call? (hint: `[project.scripts]`)
4. How many direct dependencies does the project have?
5. Pick any one package from `uv.lock` — how many packages does it depend on? How many packages does its dependencies depend on? (Hint: create a dependency graph and count)
