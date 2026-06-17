# Teacher Notes — Session 1: Kickoff

---

## Tone for this session

This is day one. Energy matters more than content depth. Students are forming first impressions of the course and of each other. Keep it relaxed, practical, and concrete. Avoid long monologues — get them hands-on as fast as possible.

---

## Opening (10–15 min)

**What to say:**
- Welcome, brief intro of yourself and the course premise: "We are going to spend the semester contributing to a real open source project built by Mistral AI. Not toy exercises — real code."
- Ask: "Who has used an AI coding assistant before?" — show of hands, brief discussion. This sets the tone that AI is expected and welcome.
- Explain the exam in one sentence: "At the end you will demo a feature or improvement you made, and explain what you learned."

---

## Open source culture (15 min)

**What to explain:**
- What open source actually means in practice — not just "free software" but a contribution workflow. The cycle: someone files an issue → someone forks → makes a branch → opens a PR → maintainer reviews → merges.
- Why Mistral AI open sourced mistral-vibe: visibility, community trust, free QA. This is a business decision, not pure altruism.
- Licences — keep it brief. MIT means "do what you want, keep the copyright notice." Apache 2.0 adds patent protection. GPL means derivatives must also be open source. mistral-vibe uses Apache 2.0.
- Point out CONTRIBUTING.md and LICENSE in the repo. Students should read these — they are the rules of the house.

**Good question to pose to the class:** "If you improve mistral-vibe, who owns that improvement?" (Answer: you do, but you grant Mistral AI a licence to use it by submitting a PR.)

---

## Fork, clone, remote setup (20 min)

**What to explain:**
- The difference between the upstream repo (`mistralai/mistral-vibe`) and their fork (`<student>/mistral-vibe`). Upstream is the source of truth; their fork is their playground.
- Why you add `upstream` as a remote: so you can pull in future changes from the original project without going through GitHub's UI.
- Walk through the commands live on your machine. Students follow along.

**Common issue to watch for:** students who clone with HTTPS instead of SSH may hit auth problems later when pushing. If you see this, help them set up SSH keys or switch to HTTPS with a token.

---

## Branching strategy (10 min)

**What to explain:**
- `main` stays clean and in sync with upstream. This is the rule, not a suggestion.
- They create a `dev` branch now and work from there all semester. For each new feature, they branch off `dev`.
- Draw this on the whiteboard: `main` ← `dev` ← `feature/my-thing`
- Explain *why*: if upstream releases a fix, they can pull it into `main` and rebase `dev` without conflicts destroying their work.

---

## Installing and running (15 min)

**What to explain:**
- `uv tool install mistral-vibe` — installs the published version globally. This is for *using* the tool.
- `uv sync` inside the cloned fork — sets up a local venv for *developing* the tool. `uv run vibe` always uses this local version.
- The `.env` file with `MISTRAL_API_KEY` — never commit this. It is already in `.gitignore` in the mistral-vibe repo.

**What to demo:** run `vibe` in the terminal, ask it something simple. Show that it works before students attempt the exercise.

---

## Exercise (20 min)

Students do the [exercise](../exercise_first_prompt.md) individually, then compare with a neighbour. Walk around and help with setup issues — this is where most time gets lost on day one.

**What to watch for:**
- Students who haven't set their API key yet
- Students who are running the PyPI version instead of their local fork (`vibe` vs `uv run vibe`)
- Students who haven't created a branch yet

---

## Wrap-up (5 min)

- Recap: fork → clone → branch → run. This is the loop they will repeat all semester.
- After Class task: write 3–5 bullet points about what mistral-vibe does. This is a low-stakes way to check that they have actually looked at the code.
- Preview session 2: "Next week we go inside the project — how is it structured, how does `pyproject.toml` work, how does typing `vibe` in the terminal end up calling Python code?"
