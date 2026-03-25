# Sprawdzanie Pythona przez Brew

**Data:** 2025-04-17

---

**User:**

jak się dowiedzieć czy na macos python mam zainstalowany przy pomocy homebrew?

---

**Assistant:**

Żeby sprawdzić, czy Python na macOS został zainstalowany przy pomocy Homebrew, masz kilka sposobów:

---

### 🔍 1. **Sprawdzenie ścieżki do Pythona**
W terminalu wpisz:

```bash
which python3
```

lub

```bash
type -a python3
```

Jeśli zwrócona ścieżka zaczyna się od:

```
/opt/homebrew/bin/python3
```

albo

```
/usr/local/bin/python3
```

to bardzo prawdopodobne, że to wersja z Homebrew (na M1/M2 `/opt/homebrew`, na Intel `/usr/local`).

---

### 🔍 2. **Sprawdzenie listy zainstalowanych pakietów Homebrew**

```bash
brew list | grep python
```

Jeśli pojawi się `python@3.x`, to oznacza, że masz zainstalowanego Pythona przez Homebrew.

---

### 🔍 3. **Sprawdzenie wersji z Homebrew**

```bash
brew info python
```

Zobaczysz ścieżkę instalacji oraz inne informacje. Jeśli Python jest zainstalowany, zobaczysz coś takiego:

```
/opt/homebrew/Cellar/python@3.12/3.12.2
...
```

---

### 🔍 4. **Sprawdzenie wersji Pythona**

```bash
python3 --version
```

Choć to nie da 100% pewności, możesz to zestawić z informacjami z `brew info python`.

---

Jeśli chcesz mogę pomóc Ci też rozkminić, który interpreter dokładnie jest używany w Twoim terminalu czy np. w VSCode. Daj znać :)