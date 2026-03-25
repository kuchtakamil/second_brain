# Instalacja psycopg2 w Ansible

**Data:** 2025-04-17

---

**User:**

Dostałem taki błąd
FAILED! => {"changed": false, "msg": "Failed to import the required Python library (psycopg2) on HAHAHA-M's Python /Users/kamil/homebrew/Cellar/ansible/11.4.0/libexec/bin/python. Please read the module documentation and install it in the appropriate location. If the required library is installed, but Ansible is using the wrong Python interpreter, please consult the documentation on ansible_python_interpreter"}

---

**Assistant:**

Ten błąd oznacza, że Ansible próbuje wykonać zadanie, które wymaga biblioteki `psycopg2` (czyli klienta PostgreSQL dla Pythona), ale ta biblioteka **nie jest zainstalowana** w interpreterze Pythona, którego używa Ansible.

Oto, jak możesz to rozwiązać:

---

### 🔍 1. Sprawdź, którego Pythona używa Ansible

Z komunikatu:
```
/Users/kamil/homebrew/Cellar/ansible/11.4.0/libexec/bin/python
```
To wygląda na *wbudowanego Pythona w Homebrewową instalację Ansible*.

---

### 💡 2. Zainstaluj `psycopg2` dla tego Pythona

Spróbuj ręcznie zainstalować bibliotekę `psycopg2` dla tego interpretera:

```bash
/Users/kamil/homebrew/Cellar/ansible/11.4.0/libexec/bin/python -m pip install psycopg2-binary
```

> Używamy `psycopg2-binary`, bo jest łatwiejszy w instalacji (nie wymaga kompilacji).

---

### 🛠️ 3. Alternatywnie: Ustaw własnego Pythona

Jeśli chcesz, żeby Ansible używał innego interpretera, możesz ustawić go w `ansible.cfg` lub bezpośrednio w playbooku/inventory:

#### W `ansible.cfg`:
```ini
[defaults]
ansible_python_interpreter = /usr/bin/python3
```

#### Lub w inventory:
```ini
[db_servers]
db1 ansible_python_interpreter=/usr/bin/python3
```

---

### ✅ 4. Sprawdzenie

Po zainstalowaniu, sprawdź czy działa:

```bash
/Users/kamil/homebrew/Cellar/ansible/11.4.0/libexec/bin/python -c "import psycopg2; print('OK')"
```

---

Jeśli chcesz, możemy przejść razem przez konfigurację `ansible.cfg`, inventory albo spróbować z wirtualnym środowiskiem (venv), żeby mieć pełną kontrolę nad zależnościami. Chcesz?

---

**User:**

Mam następny problem 
An exception occurred during task execution. To see the full traceback, use -vvv. The error was: . unexpected '.'
bo w pliku j2 jest
PERMISSIONS_SCHEMA={{ .Values.OTHER_PERMISSIONS | default false }}

---

**Assistant:**

Okej, ten błąd wynika z tego, że składnia, której używasz w pliku `.j2` (`{{ .Values.OTHER_PERMISSIONS }}`), to **składnia Helm/Go templates**, a nie **Jinja2**, której używa Ansible.

---

### 🧠 TL;DR
Ansible używa **Jinja2**, więc nie rozumie notacji `{{ .Values.foo }}`. Musisz użyć `{{ variable_name }}` zamiast tego.

---

### 🔧 Jak naprawić

Zamień:

```jinja2
PERMISSIONS_SCHEMA={{ .Values.OTHER_PERMISSIONS | default false }}
```

na:

```jinja2
PERMISSIONS_SCHEMA={{ OTHER_PERMISSIONS | default(false) }}
```

lub jeśli `OTHER_PERMISSIONS` to część jakiegoś większego obiektu (np. `Values`), to:

```jinja2
PERMISSIONS_SCHEMA={{ Values.OTHER_PERMISSIONS | default(false) }}
```

Ale to **ty musisz wiedzieć**, jaka dokładnie zmienna przychodzi z Ansible do tego szablonu. Możesz to łatwo sprawdzić debugując:

---

### 🕵️ Jak sprawdzić dostępne zmienne

Dodaj w playbooku tymczasowo:

```yaml
- name: Debug all variables
  debug:
    var: vars
```

Albo:

```yaml
- name: Show all variables
  debug:
    msg: "{{ vars | to_nice_json }}"
```

---

### 🧪 Testowy przykład

Załóżmy, że masz w playbooku:

```yaml
vars:
  OTHER_PERMISSIONS: true
```

A w Jinja2 `.j2` robisz:

```jinja2
PERMISSIONS_SCHEMA={{ OTHER_PERMISSIONS | default(false) }}
```

To powinno działać.

---

Daj znać, skąd pochodzi ta zmienna (`.Values.OTHER_PERMISSIONS`) — czy to fragment Helmowego `values.yaml`, czy próbujesz użyć tego samego templatu z Helm i Ansible? Bo jeśli tak, mogę pokazać, jak zrobić wersję zgodną z jednym i drugim.