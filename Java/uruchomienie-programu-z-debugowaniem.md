# Uruchomienie programu z debugowaniem

**Data:** 2025-08-02

---

**User:**

Czy mogę z konsoli uruchomić program java np. java TempMaster w taki sposób żeby móc podpiąć się debugerem z intellij?

---

**Assistant:**

Tak, możesz uruchomić program Java z konsoli tak, aby umożliwić podłączenie debugera z IntelliJ IDEA. W tym celu musisz dodać odpowiednie opcje JVM do polecenia `java`, aby JVM nasłuchiwała połączeń debuggera z zewnątrz. Przykładowe polecenie:

```bash
java -agentlib:jdwp=transport=dt_socket,server=y,suspend=y,address=*:5005 TempMaster
```

### Opis opcji:

- `-agentlib:jdwp=...` – uruchamia agent JDWP (Java Debug Wire Protocol).
- `transport=dt_socket` – używa gniazd TCP/IP do komunikacji.
- `server=y` – JVM działa jako serwer debugowania (czeka na połączenie).
- `suspend=y` – JVM **zatrzyma się przed wykonaniem main()**, dopóki debuger się nie podłączy. Zmień na `n`, jeśli chcesz, żeby program od razu ruszył.
- `address=*:5005` – nasłuchuje na porcie 5005 na wszystkich interfejsach. Na starszym JDK może być wymagany inny format, np. tylko `address=5005`.

### IntelliJ IDEA – jak się podpiąć:
1. W IntelliJ: Run → **Edit Configurations...**
2. Dodaj nową konfigurację typu **Remote JVM Debug**.
3. Ustaw:
   - Host: `localhost`
   - Port: `5005` (taki jak w poleceniu)
4. Kliknij „Debug”.

Po podłączeniu debugera JVM ruszy (jeśli `suspend=y`).

Daj znać, jeśli chcesz przykład dla starszego JDK (<9) lub przez `-Xdebug` (starsza metoda).