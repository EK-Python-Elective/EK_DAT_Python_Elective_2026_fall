# Session 3: Python Fundamentals — Variables, Collections & Classes

**Week 38 | Python Elective 2026 Fall**

> No mistral-vibe today, no live-demo project — just a blank editor. Variables and basic types, functions (your own and Python's built-in ones), lists, tuples, dictionaries, and a first real Python `class`. Every idea gets built on the board, then you rebuild it yourself in a small exercise before we move on. Repetition, not coverage.

---

## Learning Goals

- Set up and use a Jupyter notebook in VS Code
- Read and write variables of the basic types (`str`, `int`, `float`, `bool`, `None`) confidently
- Write and call a function with parameters, a default value, and a return value
- Reach for the right built-in function (`len`, `type`, `round`, `min`/`max`, and later `sorted`/`sum`) instead of writing one yourself
- Build, index, slice, and mutate `list`s
- Explain what makes a `tuple` different from a `list`, and when that difference matters
- Build, look up, and iterate `dict`s; know `.get()` vs `[]`
- Write a plain Python `class`: `__init__`, `self`, attributes, methods, creating instances
- Choose the right structure — list, tuple, dict, or class — for a small piece of data

---

## Before Class

- Nothing new to install — your editor and Python from session 1 is all you need
- Optional, saves a few minutes in class: install the **Python** and **Jupyter** extensions for VS Code (Extensions panel, `Ctrl/Cmd+Shift+X`, search each, both published by *Microsoft*)
- Come ready to type along on your own machine while we build things on the board

---

## Intro — Get Jupyter running in VS Code

The first thing we do, before any Python content: set up a notebook. From here on today, you work in it — one cell per idea, one cell per exercise — instead of a plain `.py` file. Code, output, and quick notes side by side.

### What you need
- **VS Code**, with the **Python** and **Jupyter** extensions (Microsoft) — install from the Extensions panel if you skipped the Before Class step
- **`uv`**, from session 1 (check with `uv --version`)

### Step 1 — make a project with a notebook kernel

A notebook runs Python through a "kernel." The kernel needs the `ipykernel` package available in the environment VS Code points at — we make a small `uv` project for that:

```bash
mkdir python-fundamentals && cd python-fundamentals
uv init               # creates pyproject.toml
uv add ipykernel      # the package that lets a notebook run in this environment
```

`uv` creates a `.venv` folder in the project — that's the environment (and kernel) VS Code will use.

### Step 2 — create a notebook

Open the project in VS Code (`code .` from the project folder, or File → Open Folder). Then either:

- Command Palette (`Ctrl/Cmd+Shift+P`) → **"Create: New Jupyter Notebook"**, or
- create a new file ending in `.ipynb` (e.g. `fundamentals.ipynb`) and open it

### Step 3 — select the kernel

Top-right of the notebook, click **"Select Kernel"** → **Python Environments** → choose the interpreter inside your project's `.venv` (it shows the project path). If VS Code offers to install `ipykernel`, say yes — though `uv add ipykernel` already handled it.

### Step 4 — run a cell

Type into a cell and press **`Shift+Enter`** to run it and move to the next:

```python
students = ["Ada", "Grace", "Alan"]
students.append("Katherine")
students        # the cell shows the repr: ['Ada', 'Grace', 'Alan', 'Katherine']
```

Useful basics:
- **`Shift+Enter`** run cell and go to next; **`Ctrl/Cmd+Enter`** run cell and stay
- The **`+ Code`** / **`+ Markdown`** buttons add cells — use a Markdown cell to label which exercise a code cell belongs to
- **Restart** (circular arrow) clears all variables and starts the kernel fresh — do this whenever state gets confusing, which will happen
- The **Variables** panel shows everything currently defined — useful all session, since today is mostly about inspecting what a list/dict/instance actually holds

From here on: one cell per **Try it** below, a short Markdown cell above each labelling which one it is. By the end of class this notebook is your record of the whole session.

### A note on `.ipynb` files and git

A notebook is a JSON file that stores your code **and its output** — that makes it noisy in git diffs and not a good home for real project source code. Fine for today's exploration and exercises; once you're back working in the mistral-vibe fork, code goes in `.py` files as usual.

---

## Today's Teachings

Each block is **short explanation → live demo on the board → your turn**. Don't skip ahead — the point of this session is that everyone's hands have typed every construct at least once before class ends. Build each demo and each "Try it" in your notebook.

### 1. Variables & basic types

```python
name = "Ada"          # str
age = 28               # int
gpa = 9.7               # float
is_enrolled = True      # bool
advisor = None           # the absence of a value
```

- Variables are just names bound to values — no declaration keyword, no fixed type
- `type(x)` tells you what you're holding; reassignment can change it (and usually shouldn't)
- `f"{name} is {age}"` — f-strings, the normal way to build a string from variables

**Try it:** make four variables describing yourself (name, age, a float, a bool), print one sentence that uses all four with an f-string.

### 2. Functions — reusable blocks of code

```python
def greet(name: str) -> str:
    return f"Hello, {name}!"

greet("Ada")            # "Hello, Ada!"

def add(a, b=0):         # b has a default value
    return a + b

add(3, 4)                # 7
add(3)                   # 3 — b falls back to its default
```

- `def name(params):` defines it; call it by name with `()`
- `return` sends a value back to the caller — no `return` means the function returns `None`
- Parameters can have default values (`b=0`); call with positional args (`add(3, 4)`) or keyword args (`add(a=3, b=4)`)
- A function is just a name bound to a reusable block of code — the same "name bound to a thing" idea as a variable, applied to behaviour instead of data

**Try it:** write a function `is_even(n)` that returns whether `n` is even, and a function `shout(text)` that returns `text` upper-cased with an exclamation mark. Call each a few times and print the results.

### 3. Built-in functions — Python's ready-made toolbox

```python
name = "Ada Lovelace"
gpa = 9.7

len(name)                            # 19
type(gpa)                             # <class 'float'>
round(gpa)                             # 10 — nearest int
round(gpa, 0)                           # 10.0 — 0 decimals, stays a float
min(4, 9, 2), max(4, 9, 2)               # (2, 9) — any number of arguments
str(42), int("42"), float("3.14")         # "42", 42, 3.14 — converting between types
```

- Same call syntax as the functions you just wrote yourself — `name(args)` — except Python already wrote these for you, no `import` needed
- `type()`, `str()`, `int()`, `float()` share their name with the type itself — calling one converts a value to that type
- `min`/`max` take any number of arguments directly; `len`/`round` take one
- `help(round)` in a cell shows what any built-in expects, if you forget
- More built-ins — `sorted`, `sum`, `range` — become genuinely useful once there's a collection to point them at; you'll meet those over the next few sections

**Try it:** using your `name`, `age`, and `gpa` variables from section 1, print: the length of your name, your `gpa` rounded to a whole number, and the larger of `age` and any other number you pick.

### 4. Lists — ordered, mutable

```python
students = ["Ada", "Grace", "Alan"]
students.append("Katherine")
students[0]                 # "Ada"
students[-1]                # last element
students[1:3]                # slice — ["Grace", "Alan"]
len(students)
"Grace" in students
for s in students:
    print(s)
```

- Ordered, indexed from 0, can hold mixed types (usually don't), grows/shrinks in place
- Common methods: `.append()`, `.remove()`, `.sort()`, `.pop()`

**Try it:** build a list of 5 course topics, print the third one, add a 6th, remove the first, print the final list.

### 5. Tuples — ordered, immutable

```python
point = (3, 7)
x, y = point                # unpacking
point[0]                     # 3
# point[0] = 9               # TypeError — tuples don't allow this
```

- Same ordering/indexing as lists, but **cannot be changed** after creation
- Use a tuple when the shape is fixed and shouldn't be edited by accident — coordinates, RGB values, a `(name, age)` pair
- Unpacking (`x, y = point`) is the move you'll use constantly, including in `for` loops over `dict.items()` (coming up)

**Try it:** make a tuple for a `(latitude, longitude)`, unpack it into two variables, print them. Then try to mutate the tuple and read the error.

### 6. Dictionaries — key/value lookup

```python
student = {"name": "Ada", "age": 28, "enrolled": True}
student["name"]              # "Ada"
student.get("email")          # None — no KeyError
student.get("email", "n/a")    # "n/a" — default if missing
student["email"] = "ada@kea.dk"
for key, value in student.items():
    print(key, value)
```

- Unordered-by-meaning key → value lookup; keys are usually strings
- `[]` raises `KeyError` on a missing key; `.get()` doesn't — use `.get()` when the key might not be there
- `.items()`, `.keys()`, `.values()` for iterating

**Try it:** build a dict for a course session (title, week, topic list), look up one field with `[]`, look up a field that doesn't exist with `.get(..., default)`, then loop over `.items()` and print each pair.

### 7. Classes — bundling data with behaviour

```python
class Counter:
    def __init__(self, start: int = 0):   # runs when you create an instance
        self.value = start                 # an attribute, stored on the instance

    def increment(self) -> None:           # a method; `self` is the instance
        self.value += 1

c = Counter(10)        # create an instance
c.increment()          # call a method
print(c.value)         # read an attribute -> 11
```

- A class is a blueprint; an instance is one concrete thing built from it
- `__init__` runs once, when the instance is created — it's where you set up starting attributes
- `self` is just the instance itself — every method takes it as the first parameter, Python passes it automatically
- Attributes (`self.value`) are per-instance state; methods are shared behaviour defined once on the class

**Try it:** write a `BankAccount` class with `__init__(self, owner, balance=0)`, a `deposit(self, amount)` method, and a `withdraw(self, amount)` method. Create two accounts, deposit into one, withdraw from the other, print both balances.

### 8. Putting it together

A class's attributes can be a list, a tuple, or a dict — everything from today combines:

```python
class Classroom:
    def __init__(self, name: str):
        self.name = name
        self.students: list[str] = []

    def enroll(self, student: str) -> None:
        self.students.append(student)

room = Classroom("Python Elective")
room.enroll("Ada")
room.enroll("Grace")
print(f"{room.name}: {room.students}")
```

**Try it:** extend `Classroom` with a `grades: dict[str, float]` attribute and a `record_grade(self, student, grade)` method. Enroll two students, record a grade for each, print the dict.

---

## Exercises

Small, done in-class, in order — each builds on the section just taught:

1. **Contact card** — a `dict` with name/phone/email, printed with an f-string
2. **Top 3** — a `list` of numbers, sorted, sliced to the top 3
3. **RGB tuple** — a function that takes an `(r, g, b)` tuple and returns whether it's "light" or "dark" (average > 128)
4. **Word count** — loop over a sentence's words into a `dict` counting occurrences
5. **`Pet` class** — `__init__(self, name, species)`, a `speak(self)` method returning a species-specific string, create two pets and call `speak()` on both

---

## After Class

- Extend the `Classroom` exercise: add a `average_grade(self)` method that computes the mean of `self.grades.values()`
- Write a short paragraph (in your notes): when would you reach for a `list` vs a `tuple`? A `dict` vs a `class`?
- Optional: open your mistral-vibe fork and find one real `list`, one real `dict`, and one real `class` in the codebase — you don't need to understand them yet, just recognise the shape

---

## Optional

For students who want to go further. None of this is required — pick whatever looks interesting.

- [optional] [Python docs — Defining Functions](https://docs.python.org/3/tutorial/controlflow.html#defining-functions) — the official tutorial section on `def`, default values, and keyword arguments, going a bit further than today (`*args`, `**kwargs`, docstrings).
- [optional] [Python docs — Built-in Functions](https://docs.python.org/3/library/functions.html) — the full A–Z reference: every built-in, `len` and `sorted` included, in one page.
- [optional] [Python docs — Data Structures](https://docs.python.org/3/tutorial/datastructures.html) — the official tutorial chapter on lists, tuples, dicts, sets, and comprehensions.
- [optional] [Python docs — Classes](https://docs.python.org/3/tutorial/classes.html) — the official tutorial chapter on `class`, going further than today's session (inheritance, class vs instance variables).
- [optional] [Real Python — Python Lists and Tuples](https://realpython.com/python-lists-tuples/) — a friendlier walkthrough with more examples.
- [optional] [Real Python — Dictionaries in Python](https://realpython.com/python-dicts/) — deeper dict methods and patterns.
- [optional] [VS Code docs — Jupyter Notebooks in VS Code](https://code.visualstudio.com/docs/datascience/jupyter-notebooks) — the full reference behind today's intro: variable explorer, debugging cells, exporting a notebook to a script, and more.
