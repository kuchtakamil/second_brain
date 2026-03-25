# Iterable Class in Python

**Data:** 2026-02-02

---

**User:**

in python how to create a new class which is iterable

---

**Assistant:**

In Python, a class becomes **iterable** when it implements the **iterator protocol**:

- `__iter__(self)` → returns an **iterator**
- The iterator implements `__next__(self)` → returns next item or raises `StopIteration`

There are **two clean patterns** depending on what you want.

---

## ✅ Pattern 1 — The class itself is the iterator (simplest)

Use this when:
- The object has a **single, linear traversal**
- You don’t need multiple independent iterations at the same time

```python
class Counter:
    def __init__(self, start, end):
        self.current = start
        self.end = end

    def __iter__(self):
        return self

    def __next__(self):
        if self.current > self.end:
            raise StopIteration
        value = self.current
        self.current += 1
        return value
```

Usage:

```python
for x in Counter(1, 5):
    print(x)
```

⚠️ Problem: you **cannot iterate twice** because state is consumed.

---

## ✅ Pattern 2 — Proper iterable with a separate iterator (correct design)

Use this when:
- You want **fresh iteration every time**
- This is how lists, sets, etc. behave

```python
class Counter:
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def __iter__(self):
        return CounterIterator(self.start, self.end)


class CounterIterator:
    def __init__(self, start, end):
        self.current = start
        self.end = end

    def __iter__(self):
        return self

    def __next__(self):
        if self.current > self.end:
            raise StopIteration
        value = self.current
        self.current += 1
        return value
```

Now this works correctly:

```python
c = Counter(1, 3)

for x in c:
    print(x)

for x in c:   # works again
    print(x)
```

---

## ✅ Pattern 3 — Pythonic way: use a generator (best in 95% cases)

You almost never need the previous patterns.

```python
class Counter:
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def __iter__(self):
        for i in range(self.start, self.end + 1):
            yield i
```

This automatically creates a proper iterator every time.

This is how **production Python code** is typically written.

---

## 🔎 What Python actually does in `for x in obj`

Equivalent to:

```python
it = obj.__iter__()
while True:
    try:
        x = it.__next__()
    except StopIteration:
        break
```

That’s the whole protocol.

---

## Rule of thumb

| Situation | Use |
|---|---|
| Simple sequential iteration | Generator in `__iter__` |
| Complex iterator state machine | Separate iterator class |
| One-shot streaming object | Object is its own iterator |

---

## Example closer to real use-case

```python
class LogFile:
    def __init__(self, path):
        self.path = path

    def __iter__(self):
        with open(self.path) as f:
            for line in f:
                yield line.strip()
```

Usage:

```python
for line in LogFile("app.log"):
    print(line)
```

Clean, lazy, memory-safe, idiomatic.

---

**User:**

is iterator in python's list implemented with generator?

---

**Assistant:**

No.

`list` iteration in CPython is **not** implemented with a generator.

It is implemented as a **dedicated C iterator type**.

---

## What actually happens in `for x in my_list`

When you do:

```python
for x in my_list:
    ...
```

Python does roughly:

```python
it = my_list.__iter__()
x = it.__next__()
```

For lists:

```python
type(my_list.__iter__())
# <class 'list_iterator'>
```

That `list_iterator` is a **C struct**, not a generator, not Python code.

---

## Why it is not a generator

A generator:

- is a Python frame object
- stores execution state, locals, stack
- is relatively heavy
- requires bytecode execution on every `next()`

A list iterator:

- is a tiny C object:
  
  ```c
  typedef struct {
      PyObject_HEAD
      PyListObject *list;
      Py_ssize_t index;
  } listiterobject;
  ```

- just holds:
  - pointer to the list
  - current index

And `__next__` is literally:

```c
return list->ob_item[index++];
```

No Python frame. No yield. No bytecode. No overhead.

---

## Performance reason

If lists used generators, iteration over lists would be **much slower**.

List iteration is one of the most performance-critical paths in Python, so CPython uses a specialized iterator type for:

- list
- tuple
- dict
- set
- range
- str
- bytes

All of them have custom C iterators.

---

## You can see this yourself

```python
lst = [1, 2, 3]
it = iter(lst)

print(type(it))
# <class 'list_iterator'>
```

Compare with generator:

```python
def gen():
    yield 1

print(type(gen()))
# <class 'generator'>
```

Totally different objects.

---

## Key insight

When you write:

```python
def __iter__(self):
    yield ...
```

Python creates a **generator iterator**.

But built-in containers do **not** use this mechanism. They use **specialized iterator types** written in C for speed.

---

## Mental model

| Thing | Implementation |
|---|---|
| Your iterable with `yield` | generator iterator |
| `list`, `tuple`, `dict`, `set`, `range` | custom C iterator |
| Generator function | Python frame-based iterator |

---

## Why this matters

This is why:

```python
for x in list_obj:     # very fast
for x in my_generator: # slower
```

even if both yield the same values.

Because one is pointer arithmetic in C, the other is Python bytecode execution.