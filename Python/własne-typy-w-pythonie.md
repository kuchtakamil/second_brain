# Własne typy w Pythonie

**Data:** 2025-07-14

---

**User:**

rozumiem potrzebę używania typing w Python. Ale gdy tworzę swoje typy to czy mogę ich po prostu używać bez importowania biblioteki typing?

---

**Assistant:**

Tak, jeśli tworzysz własne typy w Pythonie, to możesz ich używać bez konieczności importowania biblioteki `typing`, **o ile nie używasz żadnych złożonych konstrukcji typów z tej biblioteki** (np. `List`, `Dict`, `Union`, `Optional`, `Callable`, itp.).

Przykład – możesz zdefiniować własny typ i używać go bez `typing`:

```python
class User:
    def __init__(self, name: str):
        self.name = name

def greet(user: User) -> str:
    return f"Hello, {user.name}"
```

W powyższym kodzie `User` jest twoim własnym typem (klasą), nie musisz nic importować z `typing`.

Natomiast jeśli chcesz wyrazić np. „lista obiektów typu `User`” albo „może być `User` albo `None`”, to wtedy potrzebujesz `typing` (lub od Pythona 3.9+ możesz użyć wbudowanej składni `list[User]`, `User | None`, itd.).

Przykład z `typing`:

```python
from typing import List, Optional

def greet_all(users: List[User]) -> None:
    for user in users:
        print(f"Hello, {user.name}")

def maybe_get_user(name: str) -> Optional[User]:
    ...
```

Od Pythona 3.10 wzwyż możesz używać operatora `|` zamiast `Union` i `Optional`:

```python
def maybe_get_user(name: str) -> User | None:
    ...
```

Podsumowując:

- własne typy (np. klasy) możesz używać w adnotacjach bez `typing`,
- `typing` potrzebne jest tylko do wyrażania bardziej złożonych typów.