# Problemy z wirtualnym środowiskiem

**Data:** 2025-07-07

---

**User:**

Wywołałem python -m venv rag_env
a później sudo apt install python3.12-venv
teraz ls rag_env/bin pokazuje
lrwxrwxrwx 1 kamil kamil   15 lip  7 20:23  python -> /usr/bin/python
lrwxrwxrwx 1 kamil kamil    6 lip  7 20:23 python3 -> python
lrwxrwxrwx 1 kamil kamil    6 lip  7 20:23 python3.12 -> python
więc nie mogę zrobić
source rag_env/bin/activate

---

**Assistant:**

Problem wynika z tego, że stworzyłeś środowisko wirtualne **`rag_env`** przed zainstalowaniem pakietu `python3.12-venv`, więc `venv` utworzyło środowisko z niepełną lub błędną strukturą — szczególnie bez skryptów aktywujących.

Symlinki w `rag_env/bin` wskazują, że `python`, `python3` i `python3.12` są tylko symbolicznymi linkami, nie zawierają skryptów aktywujących (`activate`, `activate.csh`, `activate.fish`, itd.), które powinny się tam znaleźć.

---

### Rozwiązanie

Usuń uszkodzone środowisko i stwórz je ponownie, tym razem już po zainstalowaniu `python3.12-venv`.

```bash
rm -rf rag_env
python3.12 -m venv rag_env
```

Następnie aktywuj środowisko:

```bash
source rag_env/bin/activate
```

---

### Sprawdzenie

Po poprawnym utworzeniu środowiska w katalogu `rag_env/bin` powinieneś zobaczyć m.in. pliki:

- `activate`
- `activate.csh`
- `activate.fish`
- `python`
- `python3`
- `python3.12`
- `pip`

Jeśli nadal nie pojawią się skrypty aktywujące, sprawdź:

```bash
dpkg -L python3.12-venv
```

lub spróbuj:

```bash
sudo apt install --reinstall python3.12-venv
```

Daj znać, jeśli problem się powtórzy — można też sprawdzić alternatywne wersje Pythona lub utworzyć środowisko przy pomocy `virtualenv`.