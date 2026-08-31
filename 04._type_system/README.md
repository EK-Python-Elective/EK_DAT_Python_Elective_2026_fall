# Session 4: The Type System — Type Hints, Dataclasses, and Pydantic

**Week 38 | Python Elective 2026 Fall**

> Find and read all type annotations in mistral-vibe. Learn `TypedDict`, `dataclass`, `Optional`, `Union`. Students add type hints to an untyped part of the code.

---

## Learning Goals

- Read and write Python type annotations confidently
- Understand the most common types: `str`, `int`, `list`, `dict`, `Optional`, `Union`, `Any`
- Use `TypedDict` and `dataclass` to define structured data
- Understand when and why to use Pydantic for data validation
- Find all type annotations in mistral-vibe and understand what they express

---

## Before Class

- Search your fork for `from __future__ import annotations` — what does it do?
- Find one function in mistral-vibe that has full type annotations and one that has none
- Optional: read [PEP 526 – Variable Annotations](https://peps.python.org/pep-0526/)

---

## Today's Teachings

### Basic type hints
```python
def greet(name: str) -> str:
    return f"Hello, {name}"

age: int = 25
items: list[str] = []
lookup: dict[str, int] = {}
```

### Optional and Union
```python
from typing import Optional, Union

def find(name: str) -> Optional[str]:   # returns str or None
    ...

def process(value: str | int) -> None:  # Python 3.10+ union syntax
    ...
```

### A quick primer: reading `class` syntax

This course does not teach object-oriented programming from scratch, but the three constructs below all use Python's `class` keyword — so here is the minimum you need to *read* them. A plain class bundles some data together with the functions that work on it:

```python
class Counter:
    def __init__(self, start: int = 0):   # runs when you create an instance of the class
        self.value = start                 # an attribute, stored on the instance

    def increment(self) -> None:           # a method; `self` is the instance
        self.value += 1

c = Counter(10)        # create an instance
c.increment()          # call a method
print(c.value)         # read an attribute -> 11
```

Two more pieces of syntax you will see in this session:
- **Inheritance** — `class Config(BaseModel):` means `Config` *is a* `BaseModel` and inherits its behaviour. The name in parentheses is the parent class.
- **Decorators** — `@dataclass` on the line above a class transforms it. `@dataclass` writes the `__init__` for you, which is why the dataclass below has no visible `__init__`. The `@` marks a decorator.

You will rarely write a plain class like `Counter` in this course — mistral-vibe leans on `dataclass` and Pydantic instead — but you need to recognise the shape to read what follows.

### TypedDict — typed dictionaries
```python
from typing import TypedDict

class Config(TypedDict):
    model: str
    temperature: float
    max_tokens: int
```

### Dataclasses — lightweight data containers
```python
from dataclasses import dataclass, field

@dataclass
class Message:
    role: str
    content: str
    tokens: int = 0
    metadata: dict = field(default_factory=dict)
```

### Pydantic — runtime validation
```python
from pydantic import BaseModel

class Config(BaseModel):
    model: str = "mistral-small"
    temperature: float = 0.7

cfg = Config(model="mistral-large", temperature=1.2)
# Pydantic validates types and raises errors on bad input
```

### Reading types in mistral-vibe
- Walk through the data structures used in the codebase
- Identify where `TypedDict`, `dataclass`, or Pydantic is used
- Discuss: why would you choose one over another?

### Exercise: add type hints
- Write a new helper function and add complete type annotations to it
- Verify it with `pyright` — make sure it passes clean

---

## After Class

- Add a new typed function or small module to your fork — annotate it fully from the start
- Run `pyright` and fix any errors
- Write a short explanation (as a comment or in your notes): when would you use `TypedDict` vs `dataclass` vs `Pydantic`?

---

## Optional

For students who want to go further. None of this is required — pick whatever looks interesting.

- [optional] [mypy type-hints cheat sheet](https://mypy.readthedocs.io/en/stable/cheat_sheet_py3.html) — a compact one-page reference for annotation syntax; applies to pyright too.
- [optional] [Python docs — `typing`](https://docs.python.org/3/library/typing.html) — the fuller vocabulary: `Literal`, `Protocol`, `TypeAlias`, generics, `cast`.
- [optional] [Pydantic docs — Models](https://docs.pydantic.dev/latest/concepts/models/) — validation, type coercion, and how `BaseModel` differs from a plain `dataclass`.
- [optional] [PEP 557 — Data Classes](https://peps.python.org/pep-0557/) and [PEP 589 — TypedDict](https://peps.python.org/pep-0589/) — the rationale for each and when to reach for which.
