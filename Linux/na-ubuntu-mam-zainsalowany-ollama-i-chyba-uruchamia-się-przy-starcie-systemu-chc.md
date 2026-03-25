# Na ubuntu mam zainsalowany ollama i  chyba uruchamia się przy starcie systemu. C

**Data:** 19 lis 2025, 17:38:13 CET

---

**User:**

Na ubuntu mam zainsalowany ollama i  chyba uruchamia się przy starcie systemu. Chciałbym żeby uruchamiała się tylko gdy ją wywołam.

---

**Gemini:**

Rozumiem, chcesz wyłączyć automatyczne uruchamianie usługi `ollama` przy starcie systemu i zarządzać nią ręcznie.

Poniższe instrukcje używają `systemctl`, standardowego narzędzia do zarządzania usługami systemowymi w nowoczesnych systemach Linux, takich jak Ubuntu, które używają `systemd`.

### Wyłączenie automatycznego startu usługi Ollama

Aby wyłączyć automatyczne uruchamianie usługi `ollama` przy starcie systemu, użyj polecenia `disable`:

```
sudo systemctl disable ollama
```

- **`sudo`**: Używane do wykonywania polecenia z uprawnieniami administratora (wymagane do zarządzania usługami systemowymi).
- **`systemctl`**: Narzędzie do kontrolowania systemu inicjowania systemd.
- **`disable`**: Wyłącza jednostkę usługi (service unit) z automatycznego uruchamiania podczas kolejnych rozruchów systemu. Spowoduje to usunięcie symbolicznego linku w katalogu startowym (np. w `/etc/systemd/system/multi-user.target.wants/`).

### Zatrzymanie aktualnie uruchomionej usługi

Po wyłączeniu automatycznego startu, usługa może nadal działać w obecnej sesji. Aby ją natychmiast zatrzymać, użyj polecenia `stop`:

```
sudo systemctl stop ollama
```

### Ręczne uruchamianie usługi Ollama (w razie potrzeby)

Gdy usługa jest wyłączona, będziesz musiał ją uruchomić ręcznie, gdy będziesz chciał jej użyć:

```
sudo systemctl start ollama
```

### Sprawdzenie statusu usługi

Aby sprawdzić, czy usługa jest aktywna i czy jest włączona do automatycznego startu:

```
systemctl status ollama
```

- W linii zaczynającej się od **`Active:`** zobaczysz, czy usługa jest uruchomiona (`active (running)`).
- W linii zaczynającej się od **`Loaded:`** zobaczysz, czy usługa jest włączona (`enabled`) czy wyłączona (`disabled`) dla automatycznego startu.

---

**Podsumowanie kroków, które powinieneś wykonać:**

1. **Wyłącz automatyczny start:** `sudo systemctl disable ollama`
2. **Zatrzymaj aktualną instancję (opcjonalnie, jeśli chcesz natychmiast zwolnić zasoby):** `sudo systemctl stop ollama`

Od tej pory `ollama` będzie uruchamiana tylko wtedy, gdy wydasz polecenie `sudo systemctl start ollama`.

Chciałbyś, abym sprawdził, czy istnieje jakaś specyficzna konfiguracja dla użytkownika, pod którym instalowałeś Ollama, która może powodować jej uruchamianie poza systemd?