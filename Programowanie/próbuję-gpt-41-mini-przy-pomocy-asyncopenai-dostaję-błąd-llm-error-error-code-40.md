# Próbuję gpt 4.1 mini przy pomocy AsyncOpenAI. Dostaję błąd LLM Error: Error code

**Data:** 25 gru 2025, 00:09:38 CET

---

**User:**

Próbuję gpt 4.1 mini przy pomocy AsyncOpenAI. Dostaję błąd
LLM Error: Error code: 401 - {'error': {'message': 'Authentication Error, Invalid proxy server token passed. Received API Key = sk-...U-sA, Key Hash (Token) =5014a5c50a547c1efd08c5d0f435de4f4ca3ade2f596cb3fc45fc74908737d80. Unable to find token in cache or `LiteLLM_VerificationTokenTable`', 'type': 'token_not_found_in_db', 'param': 'key', 'code': '401'}}

w litellm.service jest poprawnie wypełniony klucz.

Zauważyłem że nie ma tabeli LiteLLM_ProxyAPIKeys.
W tabeli LiteLLM_VerificationTokenTable jest jeden wiersz.Nie wiem jakiego klucza on dotyczy

---

**Gemini:**

Błąd `401 - token_not_found_in_db` oznacza, że włączyłeś tryb bazy danych, w którym LiteLLM przestaje polegać wyłącznie na zmiennych środowiskowych do autoryzacji zapytań przychodzących. Od tego momentu proxy wymaga, abyś w kliencie `AsyncOpenAI` podał albo **Master Key** (zdefiniowany w `config.yaml`), albo **Virtual Key** (wygenerowany i zapisany w bazie).

Oto techniczna ścieżka naprawcza:

### 1. Rozróżnienie kluczy (Kwestia kluczowa)

W Twoim setupie występują dwa rodzaje kluczy:

1. **Provider Key (OpenAI/Gemini):** Służy do komunikacji LiteLLM -> Google/OpenAI. Masz go w serwisie systemd.
2. **Proxy Key (Virtual/Master Key):** Służy do komunikacji Twoja Aplikacja -> LiteLLM.

Błąd, który otrzymujesz, dotyczy tego drugiego. Twoja aplikacja wysyła klucz `sk-...U-sA`, którego LiteLLM nie widzi w swojej bazie danych.

### 2. Naprawa brakujących tabel (Prisma Sync)

Brak tabeli `LiteLLM_ProxyAPIKeys` przy obecności `LiteLLM_VerificationTokenTable` sugeruje niepełną migrację. Musimy wymusić synchronizację schematu.

Wykonaj poniższą komendę, upewniając się, że ścieżka do `schema.prisma` jest poprawna:

```
sudo -u litellm bash -c "
export PATH='/opt/litellm-proxy/venv/bin:\$PATH' && \
export DATABASE_URL='postgresql://litellm_user:password@localhost:5432/litellm_db' && \
/opt/litellm-proxy/venv/bin/prisma db push --schema /opt/litellm-proxy/venv/lib/python3.12/site-packages/litellm/proxy/schema.prisma
"
```

Następnie sprawdź w `psql`, czy tabela się pojawiła:

```
\c litellm_db
\dt "LiteLLM*"
```

Powinieneś zobaczyć około 15-20 tabel, w tym `LiteLLM_ProxyAPIKeys`.

### 3. Użycie poprawnego Master Key w AsyncOpenAI

Dopóki nie wygenerujesz "Wirtualnych Kluczy" przez UI lub API, Twoja aplikacja musi autoryzować się za pomocą `master_key` zdefiniowanego w `config.yaml`.

**Konfiguracja `config.yaml`:**

```
general_settings:
  master_key: "sk-admin-1234" # To jest klucz, którego musi użyć Twoja aplikacja
  database_url: "postgresql://..."
```

**Poprawny kod klienta:**

```
import asyncio
from openai import AsyncOpenAI

async def main():
    client = AsyncOpenAI(
        api_key="sk-admin-1234", # Musi być identyczny z master_key w config.yaml
        base_url="http://localhost:4000/v1"
    )

    response = await client.chat.completions.create(
        model="gpt-4o-mini", # LiteLLM zmapuje to na dostawcę
        messages=[{"role": "user", "content": "Hello world"}]
    )
    print(response.choices[0].message.content)

asyncio.run(main())
```

### 4. Generowanie Wirtualnych Kluczy (Zalecane)

Jeśli chcesz monitorować zużycie per projekt/użytkownik, powinieneś stworzyć osobne klucze. Możesz to zrobić przez Dashboard pod adresem `http://localhost:4000/ui` lub przez API LiteLLM:

```
curl -X POST 'http://localhost:4000/key/generate' \
-H 'Authorization: Bearer sk-admin-1234' \
-H 'Content-Type: application/json' \
-d '{
    "models": ["gpt-4o-mini", "gemini/*"],
    "duration": "30d",
    "metadata": {"user": "Kamil"}
}'
```

W odpowiedzi otrzymasz nowy klucz (np. `sk-LITELLM-XXXX`), który teraz będzie widoczny w tabeli `LiteLLM_ProxyAPIKeys`. Używając tego klucza w aplikacji, zobaczysz statystyki w Dashboardzie.

### 5. Wyjaśnienie tabeli `LiteLLM_VerificationTokenTable`

Ta tabela służy do przechowywania hashowanych tokenów dostępowych i tymczasowych sesji. To, że widzisz tam jeden wiersz, to prawdopodobnie hash Twojego `master_key`, który LiteLLM zainicjalizował przy starcie. Jednak do autoryzacji zapytań o modele, LiteLLM szuka powiązań w tabelach uprawnień (których brak u Ciebie powoduje błąd).

### Dlaczego to nie działało z "sk-...U-sA"?

Prawdopodobnie w `AsyncOpenAI` podałeś swój prawdziwy klucz OpenAI. W trybie Proxy z bazą danych, LiteLLM **odrzuca** bezpośrednie klucze dostawców dla bezpieczeństwa (chyba że ustawisz `allow_user_managed_keys: true`, ale i tak LiteLLM musi najpierw "znać" ten klucz w swojej bazie, aby zliczać tokeny).

**Kolejny krok:** Czy po wykonaniu `prisma db push` tabela `LiteLLM_ProxyAPIKeys` jest już widoczna w Twojej bazie danych? Jeśli tak, spróbuj wykonać request z użyciem `master_key`.