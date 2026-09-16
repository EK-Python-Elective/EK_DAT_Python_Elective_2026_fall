# Session 3: Python Fundamentals — Variables, Collections & Classes

**Week 38 | Python Elective 2026 Fall**

> No mistral-vibe today, no live-demo project — just a blank editor. Variables and basic types, lists, tuples, dictionaries, and a first real Python `class`. Every idea gets built on the board, then you rebuild it yourself in a small exercise before we move on. Repetition, not coverage.

---

## Learning Goals

- Read and write variables of the basic types (`str`, `int`, `float`, `bool`, `None`) confidently
- Build, index, slice, and mutate `list`s
- Explain what makes a `tuple` different from a `list`, and when that difference matters
- Build, look up, and iterate `dict`s; know `.get()` vs `[]`
- Write a plain Python `class`: `__init__`, `self`, attributes, methods, creating instances
- Choose the right structure — list, tuple, dict, or class — for a small piece of data

---

## Before Class

- Nothing new to install — your editor and Python from session 1 is all you need
- Come ready to type along on your own machine while we build things on the board

---

## Today's Teachings

Each block is **short explanation → live demo on the board → your turn**. Don't skip ahead — the point of this session is that everyone's hands have typed every construct at least once before class ends.

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

### 2. Lists — ordered, mutable

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

### 3. Tuples — ordered, immutable

```python
point = (3, 7)
x, y = point                # unpacking
point[0]                     # 3
# point[0] = 9               # TypeError — tuples don't allow this
```

- Same ordering/indexing as lists, but **cannot be changed** after creation
- Use a tuple when the shape is fixed and shouldn't be edited by accident — coordinates, RGB values, a `(name, age)` pair
- Unpacking (`x, y = point`) is the move you'll use constantly, including in `for` loops over `dict.items()` (next section)

**Try it:** make a tuple for a `(latitude, longitude)`, unpack it into two variables, print them. Then try to mutate the tuple and read the error.

### 4. Dictionaries — key/value lookup

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

### 5. Classes — bundling data with behaviour

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

### 6. Putting it together

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

- [optional] [Python docs — Data Structures](https://docs.python.org/3/tutorial/datastructures.html) — the official tutorial chapter on lists, tuples, dicts, sets, and comprehensions.
- [optional] [Python docs — Classes](https://docs.python.org/3/tutorial/classes.html) — the official tutorial chapter on `class`, going further than today's session (inheritance, class vs instance variables).
- [optional] [Real Python — Python Lists and Tuples](https://realpython.com/python-lists-tuples/) — a friendlier walkthrough with more examples.
- [optional] [Real Python — Dictionaries in Python](https://realpython.com/python-dicts/) — deeper dict methods and patterns.
