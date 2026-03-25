# Python Poetry Windows Installation

**Data:** 2023-11-01

---

**User:**

Przekształć polecenie tak aby można było je wykonać w Windows
curl -sSL https://install.python-poetry.org | python3 -

---

**Assistant:**

Aby przekształcić to polecenie tak, aby można je było wykonać w systemie Windows, należy zastąpić polecenie `curl` poleceniem `Invoke-WebRequest` w PowerShell, a także skorygować polecenie Pythona, aby działało zgodnie z konwencją Windows. Oto przekształcone polecenie:

```powershell
Invoke-WebRequest -Uri https://install.python-poetry.org -OutFile get-poetry.py; python get-poetry.py
```

Powyższe polecenie pobiera skrypt instalacyjny `get-poetry.py` z adresu URL https://install.python-poetry.org, a następnie uruchamia go za pomocą `python`. Upewnij się, że masz zainstalowanego Pythona i PowerShell na swoim systemie Windows.

---

**User:**

Nie, curl jest zainstalowany i działa dobrze. Ale to curl pod Windows. Użyj curl

---

**Assistant:**

Jeśli curl jest zainstalowany i działa poprawnie, możesz użyć tej samej komendy. W systemie Windows możesz uruchomić tę komendę bezpośrednio w wierszu poleceń. Oto komenda:

```bash
curl -sSL https://install.python-poetry.org | python -
```

Upewnij się, że masz zainstalowanego Pythona, który jest dostępny w wierszu poleceń. Jeśli Python nie jest dostępny w zmiennej środowiskowej PATH, może być konieczne określenie ścieżki bezwzględnej do programu Python.

---

**User:**

DOstaje błąd
curl: (35) schannel: next InitializeSecurityContext failed: Unknown error (0x80092012) - The revocation function was unable to check revocation for the certificate.

---

**Assistant:**

Błąd `curl: (35) schannel: next InitializeSecurityContext failed: Unknown error (0x80092012)` zwykle oznacza, że istnieje problem z certyfikatem SSL podczas próby nawiązania bezpiecznego połączenia przez protokół HTTPS. Możesz spróbować dodać flagę `-k` lub `--insecure` do polecenia `curl`, aby wyłączyć weryfikację certyfikatu. Pamiętaj jednak, że ta metoda nie jest zalecana w środowiskach produkcyjnych, ponieważ pomija weryfikację certyfikatu SSL, co może otworzyć potencjalne luki w zabezpieczeniach.

Oto jak to zrobić:

```bash
curl -k -sSL https://install.python-poetry.org | python -
```

Jeśli problem nadal występuje, możesz spróbować rozwiązać problem z certyfikatem SSL na swoim systemie, aby umożliwić prawidłowe nawiązywanie bezpiecznych połączeń HTTPS.