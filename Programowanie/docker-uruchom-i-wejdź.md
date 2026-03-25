# Docker: uruchom i wejdź.

**Data:** 2023-05-07

---

**User:**

Istnieje kontener docker który jest wyłączony. Jak w jednym poleceniu uruchomić kontener i wejść do niego do powłoki bash?

---

**Assistant:**

Tak, można uruchomić wyłączony kontener Docker i wejść do niego do powłoki bash za pomocą jednego polecenia.

Najpierw musisz znaleźć ID lub nazwę kontenera, który chcesz uruchomić. Można to zrobić za pomocą polecenia `docker ps -a`, które wyświetli listę wszystkich kontenerów, włącznie z tymi, które są wyłączone.

Następnie użyj polecenia `docker start` i `docker exec` w jednym poleceniu, aby uruchomić kontener i wejść do niego do powłoki bash. Oto przykładowe polecenie:

```
docker start <ID lub nazwa kontenera> && docker exec -it <ID lub nazwa kontenera> bash
```

Gdzie `<ID lub nazwa kontenera>` to identyfikator lub nazwa kontenera, który chcesz uruchomić i wejść do niego do powłoki bash.

Polecenie `docker start` uruchamia kontener, a polecenie `docker exec` umożliwia wejście do niego do powłoki bash z opcją `-it`, która umożliwia interaktywny tryb wejścia/wyjścia.