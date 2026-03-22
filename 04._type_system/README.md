# Session 4: The Type System — Type Hints, Dataclasses, and Pydantic

**Week 39 | Python Elective 2026 Fall**

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
