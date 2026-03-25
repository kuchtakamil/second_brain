# Serwis nie może uruchomić się poprawnie  systemctl status litellm

**Data:** 23 gru 2025, 18:29:16 CET

---

**User:**

Serwis nie może uruchomić się poprawnie

systemctl status litellm                                                                                                                                     141 ↵ ──(wto,gru23)─┘
● litellm.service - LiteLLM Proxy Service (Token Monitoring)
     Loaded: loaded (/etc/systemd/system/litellm.service; enabled; preset: enabled)
     Active: activating (auto-restart) (Result: exit-code) since Tue 2025-12-23 18:28:25 CET; 2s ago
    Process: 26944 ExecStart=/bin/litellm --config /config.yaml --port (code=exited, status=203/EXEC)
   Main PID: 26944 (code=exited, status=203/EXEC)


journalctl:
gru 23 18:06:23 gr systemd[1]: litellm.service: Scheduled restart job, restart counter is at 6.
gru 23 18:06:23 gr systemd[1]: Started litellm.service - LiteLLM Proxy Service (Token Monitoring).
gru 23 18:06:23 gr systemd[1]: litellm.service: Main process exited, code=exited, status=203/EXEC
gru 23 18:06:23 gr systemd[1]: litellm.service: Failed with result 'exit-code'.

---

**Gemini:**

Błąd **203/EXEC** w systemd oznacza, że manager procesów nie może odnaleźć pliku wykonywalnego wskazanego w `ExecStart` lub nie ma uprawnień do jego uruchomienia. W Twoim logu widać, że komenda próbuje uruchomić `/bin/litellm`, co jest błędną ścieżką, oraz brakuje argumentu dla flagi `--port`.

Oto kroki naprawcze:

### 1. Korekta pliku litellm.service

Twoja bieżąca konfiguracja używa błędnych ścieżek. Musisz wskazać na binarkę wewnątrz środowiska wirtualnego oraz poprawną ścieżkę do pliku konfiguracyjnego.

Edytuj plik:

```
sudo nano /etc/systemd/system/litellm.service
```

Zaktualizuj sekcję `[Service]`, upewniając się, że ścieżki są bezwzględne i poprawne:

```
[Service]
Type=simple
User=litellm
Group=litellm
WorkingDirectory=/opt/litellm-proxy
# Poprawne ścieżki do binarki z venv i konfiguracji
ExecStart=/opt/litellm-proxy/venv/bin/litellm --config /etc/litellm/config.yaml --port 4000
Restart=always
RestartSec=5
# Upewnij się, że zmienne środowiskowe są obecne, jeśli nie ma ich w config.yaml
Environment="DATABASE_URL=postgresql://litellm_user:password@localhost:5432/litellm_db"
Environment="OPENAI_API_KEY=sk-..."
Environment="ANTHROPIC_API_KEY=sk-..."
```

### 2. Weryfikacja uprawnień binarki

Upewnij się, że użytkownik `litellm` ma prawo do wykonywania plików wewnątrz venv:

```
sudo chown -R litellm:litellm /opt/litellm-proxy
sudo chmod +x /opt/litellm-proxy/venv/bin/litellm
```

### 3. Przeładowanie i restart

Po każdej zmianie w pliku `.service` konieczne jest odświeżenie konfiguracji systemd:

```
sudo systemctl daemon-reload
sudo systemctl restart litellm
```

### 4. Diagnostyka (jeśli nadal nie działa)

Jeśli serwis nadal zgłasza błąd, sprawdź czy binarka w ogóle działa wywołana bezpośrednio z kontekstu użytkownika `litellm`:

```
sudo -u litellm /opt/litellm-proxy/venv/bin/litellm --config /etc/litellm/config.yaml --port 4000
```

**Najczęstsze przyczyny błędu 203 w tym przypadku:**

- **Błędna ścieżka:** Systemd szuka `/bin/litellm`, podczas gdy pip instaluje go w `/usr/local/bin` (globalnie) lub `$VENV_PATH/bin/litellm` (lokalnie).
- **Missing Shebang:** Jeśli `litellm` jest skryptem, venv musi być poprawnie zainicjalizowane, aby system wiedział, którego interpretera Python użyć.
- **Brak wartości portu:** W Twoim logu widać `--port` na końcu linii bez przypisanej wartości (np. `4000`), co powoduje błąd parsowania argumentów przez LiteLLM już na starcie.

Czy po poprawieniu ścieżek w `ExecStart` logi `journalctl -u litellm` pokazują teraz błąd związany z połączeniem do PostgreSQL, czy serwis wstał poprawnie?