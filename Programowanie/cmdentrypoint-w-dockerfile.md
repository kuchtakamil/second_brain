# CMD/ENTRYPOINT w Dockerfile

**Data:** 2023-05-08

---

**User:**

Czy CMD lub ENTRYPOINT są obowiązkowe w każdym Dockerfile?

---

**Assistant:**

Nie, CMD lub ENTRYPOINT nie są obowiązkowe w każdym Dockerfile. 

CMD lub ENTRYPOINT służą do definiowania komendy, która zostanie wykonana po uruchomieniu kontenera. Jednak istnieją przypadki, gdy nie są potrzebne lub pożądane. 

Jeśli nie określimy ani CMD, ani ENTRYPOINT w Dockerfile, domyślnie zostanie użyta komenda /bin/sh -c, ale w praktyce zależy to od ustawień konfiguracyjnych Docker Engine.

Niektóre aplikacje, takie jak bazy danych, mogą wymagać tylko obrazu bez dodatkowej komendy, ponieważ w trakcie uruchamiania automatycznie wywołują swoje wewnętrzne polecenia.

W przypadku, gdy nie chcemy korzystać z domyślnych ustawień /bin/sh -c, możemy zdefiniować wartość ENTRYPOINT lub CMD w Dockerfile jako pusta wartość (np. ENTRYPOINT []). W ten sposób zostanie zignorowana domyślna komenda i kontener uruchomi się bez wykonywania dodatkowych komend.

---

**User:**

Czy można wywołać CMD w docker compose zamiast w DOckerfile?

---

**Assistant:**

Tak, można wywołać komendę CMD w pliku docker-compose.yml zamiast definiować ją bezpośrednio w Dockerfile.

W pliku docker-compose.yml możemy zdefiniować wartość pola `command` w ramach definicji usługi, aby określić komendę, która zostanie wywołana po uruchomieniu kontenera. Wartość ta zostanie przekazana do `CMD` w Dockerfile.

Na przykład, jeśli w pliku Dockerfile zdefiniowano polecenie `CMD ["python", "app.py"]`, w pliku docker-compose.yml można zastąpić to polecenie, wpisując:

```
version: '3'
services:
  myapp:
    build: .
    command: python my_script.py
```

W tym przykładzie, zamiast `CMD ["python", "app.py"]` w Dockerfile, wywoływane będzie polecenie `python my_script.py`, które zostanie przekazane przez pole `command` w pliku docker-compose.yml.

Warto jednak pamiętać, że pole `command` w docker-compose.yml zawsze zastąpi wartość `CMD` z Dockerfile, nawet jeśli wartość `CMD` została zdefiniowana w Dockerfile.

---

**User:**

w docker-compose wywołując 
command: sbt "sensor-simulator / run"
podaję komendę sbt, nazwę modułu sensor-simulator oraz komendę run. Chciałbym jeszcze do tego przekazać parametr dla aplikacji

---

**Assistant:**

Aby przekazać parametry dla aplikacji uruchamianej w kontenerze Docker, możesz dodać je po nazwie komendy, oddzielając je spacją. Na przykład, aby przekazać parametr `param1` dla aplikacji, którą uruchamiasz wraz z komendą `sbt`, użyj następującej składni:

```
command: sbt "sensor-simulator / run" param1
```

Jeśli chcesz przekazać więcej niż jeden parametr, oddziel je spacją, np:

```
command: sbt "sensor-simulator / run" param1 param2 param3
```

Warto jednak pamiętać, że niektóre parametry wymagają użycia cudzysłowów lub znaków ucieczki. W przypadku, gdy parametry zawierają znaki specjalne, wartość komendy powinna być zapisana w sposób umożliwiający poprawne przekazanie parametrów do aplikacji wewnątrz kontenera.

---

**User:**

Nie. Ma być tak command: sbt "sensor-simulator / run param1"

---

**Assistant:**

Jeśli chcesz przekazać parametr `param1` jako argument wywołania komendy `run` dla aplikacji uruchamianej za pomocą komendy `sbt`, to możesz dodać ten parametr bezpośrednio do polecenia `run`. W tym celu możesz połączyć nazwę komendy `run` i wartość parametru `param1` w ramach argumentu przekazywanego do `sbt`.

W takim przypadku, polecenie `command` w pliku `docker-compose.yml` powinno wyglądać następująco:

```
command: sbt "sensor-simulator / run param1"
```

To spowoduje, że polecenie `sbt` zostanie wykonane z argumentem `"sensor-simulator / run param1"`, co przekaże parametr `param1` do aplikacji uruchamianej w kontenerze.