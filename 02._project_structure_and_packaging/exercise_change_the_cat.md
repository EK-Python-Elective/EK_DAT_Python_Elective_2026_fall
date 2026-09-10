# Exercise: Change the Cat, Keep It Clean

**Type:** Individual — pair up if you get stuck

**Motivation:** Two skills in one — navigating an unfamiliar codebase to find
the thing you want to change, and using `ruff` + `pyright` to prove your change
is still clean Python *before* you run the app.

---

When you start `vibe`, the welcome banner shows a small animated cat, drawn with
braille dots. It also shows up on the first-run setup screens. Your job: turn it
into an **elephant**. (Or a dog, a spaceship, a mistral — whatever. It does not
have to be a masterpiece.)

Do all of this **on a branch** (`git checkout -b exercise/change-the-cat`), and
don't open a PR — this is a throwaway change.

### 1. Find it

You've never seen this code before. Find the file without being told the path:

- It's a Textual widget — look under `vibe/cli/textual_ui/widgets/`.
- `grep` (or your editor's search) for something the banner would mention —
  `PetitChat`, `banner`, `braille`.
- When you find the widget, read the `render_braille()` docstring in the file
  next to it. It tells you the coordinate convention (origin top-left, `x`
  right, `y` down).

### 2. Change it

- `STARTING_DOTS` is the cat's resting shape — a list of sets, one set per row,
  each number a lit dot in that row. Edit these to draw your elephant.
- The animation (`TRANSITIONS`) makes the head turn and the eyes blink. You can
  leave it alone (the elephant just won't animate quite right), or edit those
  frames too if you're enjoying yourself.
- Run `uv run vibe` and look at the banner. Iterate.

### 3. Prove it's clean

This is the actual point of the exercise. On your branch, from the fork root:

```bash
uv run ruff check .        # style + lint — a stray comma, bad spacing, an unused import
uv run ruff format .       # then re-check that nothing needs reformatting
uv run pyright             # types — a mistyped name, a wrong argument, a broken import
```

Both must come back clean. Then, to see the checkers actually *bite*: mistype
one of the constant names (`STARTING_DOT` instead of `STARTING_DOTS`), or add
`import os` at the top and don't use it — re-run `ruff check` and `pyright` and
read what they say. Undo it before you finish.

### Hand in

Nothing to submit. Be ready to show: your elephant in the banner, and a clean
`ruff check` + `pyright` on the file you edited.
