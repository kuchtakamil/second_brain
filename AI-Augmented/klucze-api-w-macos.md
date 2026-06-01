Klucze API w macOS Keychain - alternatywa .env

Trzymanie kluczy API (OpenAI, Gemini, Stripe, Anthropic) w pliku .env to zwykły tekst leżący na dysku. 

Wystarczy jedno git add . po zmęczonym dniu, jeden backup do iCloud Drive, jedna paczka z npm/pip która sobie czyta zmienne środowiskowe i klucz wycieka. MacOS i Windows mają natywne, zaszyfrowane sejfy na hasła, które chronią klucze i wymagają zgody przy dostępie. 

Setup zajmuje 5 minut.

To nie zamiennik dla zarządzania sekretami w teamie/produkcji (Vault, Doppler, AWS Secrets Manager), a dobra higiena lokalna.
Wymagania (macOS)

    macOS (dowolna wersja), FileVault włączony, mocne hasło użytkownika

    Komenda security jest wbudowana - nie instalujesz żadnych dodatkowych rzeczy

Jak to działa - po ludzku

Wyobraź sobie sejf w domu. Sejf jest otwarty ciągle, kiedy jesteś zalogowany na macu - to wygodne. Ale każda paczka w sejfie ma własną kłódkę z listą osób, które mogą ją otworzyć. Aplikacja, która włożyła klucz do sejfu, ma swoją kłódkę otwartą bez pytania. Inna aplikacja sięgająca po ten sam klucz dostaje popup "wpuścić?".
Procedura - zapis klucza

Nie wpisuj wartości klucza wprost w komendzie - wyląduje w historii terminala.
Sposób 1 - z aktualnego .env

Wejdź do folderu/projektu, gdzie posiadasz plik .env i wykonaj w terminalu komende:

( set -a; source .env; set +a; \
  security add-generic-password -a "$USER" -s OPENAI_API_KEY -l OPENAI_API_KEY -w "$OPENAI_API_KEY" -U \
)

Co się dzieje:

    ( ... ) - "zrób to w odizolowanym pudełku, po wyjściu sprzątnij" - klucze nie zostają w terminalu

    set -a; source .env; set +a - wczytuje plik .env, robi z każdej linii KEY=value zmienną

    -s OPENAI_API_KEY - nazwa, pod jaką wyciągniesz wartość. Twój identyfikator.

    -w "$OPENAI_API_KEY" - wartość. Terminal podstawia ją w locie, w historii widać tylko $OPENAI_API_KEY

    -U - update jeśli jest. Możesz uruchamiać wielokrotnie.

Sposób 2 - wpisanie ręczne (najbezpieczniejszy)

Komenda zapyta o wartość interaktywnie - nic nie ląduje w pliku ani w historii:

security add-generic-password -a "$USER" -s OPENAI_API_KEY -l OPENAI_API_KEY -w

Sprawdzenie zapisu (bez pokazywania wartości)

security find-generic-password -a "$USER" -s OPENAI_API_KEY 2>&1 | grep -E '"(svce|cdat)"'

Bez flagi -w widać tylko metadane (nazwa, data utworzenia). Wartość zostaje ukryta, popup się nie pojawia.

GUI: open "/System/Applications/Utilities/Keychain Access.app". 

Pułapka: API keys nie pojawią się w nowej apce Passwords - tylko w starej Keychain Access.
Użycie w skryptach (Python - cross-platform)

import os, subprocess, sys

def get_secret(name: str) -> str:
    if val := os.environ.get(name):
        return val
    if sys.platform == "darwin":
        return subprocess.check_output(
            ["security", "find-generic-password", "-a", os.environ["USER"], "-s", name, "-w"],
            text=True
        ).strip()
    if sys.platform == "win32":
        import keyring
        return keyring.get_password("api", name)
    raise RuntimeError(f"Brak sekretu {name}")

OPENAI_API_KEY = get_secret("OPENAI_API_KEY")

Najpierw szuka klucza w zmiennych środowiskowych (przyda się w produkcji / CI), potem w lokalnym sejfie. Jeden kod, dwa środowiska.
Windows - Credential Manager

Windows ma swój odpowiednik: Credential Manager (Menedżer poświadczeń). Najprościej obsłużyć go przez bibliotekę keyring w Pythonie:

pip install keyring

Zapis klucza:

python -c "import keyring; keyring.set_password('api', 'OPENAI_API_KEY', input('Klucz: '))"

Odczyt - identyczna składnia jak w funkcji wyżej. Pakiet keyring automatycznie wykrywa system: na macOS sięga do Keychain, na Windowsie do Credential Manager, na Linuksie do Secret Service / GNOME Keyring. Kod aplikacji jest jeden.

GUI po stronie Windows: Control Panel → User Accounts → Credential Manager → Windows Credentials. Tam zobaczysz wpisy zapisane przez keyring.

Alternatywa po stronie PowerShell:

# zapis (wpiszesz interaktywnie, klucz nie ląduje w historii)
$cred = Get-Credential -UserName OPENAI_API_KEY -Message "Wpisz klucz"
cmdkey /generic:OPENAI_API_KEY /user:$env:USERNAME /pass:$cred.GetNetworkCredential().Password

# odczyt
[System.Net.NetworkCredential]::new("", (Get-StoredCredential -Target OPENAI_API_KEY).Password).Password

Get-StoredCredential wymaga modułu CredentialManager (Install-Module CredentialManager). Dla większości użycia keyring w Pythonie to prostsze rozwiązanie cross-platform.
Kiedy realnie tego używasz

    Lokalny dev - klucze do OpenAI / Anthropic / Gemini / Stripe test

    Wiele projektów ten sam klucz - jeden OPENAI_API_KEY w sejfie, używasz w 5 projektach bez kopiowania .env

    Po wpadce typu "wypchnąłem .env do publicznego repo" - rotujesz klucz, nowy ląduje w sejfie, .env znika

    Cross-project skille / agenty - skille Claude Code, narzędzia z ~/bin mogą czytać z sejfu bez kopiowania configu

Najczęstsze pułapki

    "Always Allow" dla /usr/bin/python3 (macOS) - antywzorzec. Każdy skrypt Pythona dostanie wartość bez popupu. Zostaw "Allow Once" albo "Confirm before allowing".

    Klucz wpisany wprost w komendzie - zostaje w historii terminala na zawsze. Używaj sposobu 1 ($VAR) albo sposobu 2 (interaktywny).

    Klucze nie syncują się - twój drugi mac/komputer nie ma dostępu. Każde urządzenie = osobno.

    Team / CI nie zadziała - kolega z Linuksa nie ma dostępu, GitHub Actions nie ma. Dla teamu: Doppler / 1Password / Vault.

    .env w gicie kiedyś - jeśli było w gicie kiedykolwiek, zrotuj wszystkie klucze. Historia gita pamięta nawet po skasowaniu pliku.

Pro tip - popup dla cennych kluczy

Klucze do Stripe live, AWS root, OpenAI z dużym limitem - wymuś popup za każdym razem.

macOS (Keychain Access → wpis → Access Control):

    "Confirm before allowing access" + "Ask for Keychain password" → każde odczytanie wymaga hasła użytkownika

Windows (Credential Manager): brak natywnego "confirm per use" - dla cennych kluczy używaj 1Password CLI lub osobnego narzędzia z biometrią (Windows Hello + DPAPI).
Inne narzędzia okolicy

    envchain (macOS/Linux) - sejf + uruchamianie aplikacji z profilem

    keyring (Python, cross-platform) - jednolity API do Keychain / Credential Manager / Secret Service

    1Password CLI (op) - sync między urządzeniami i platformami, najlepszy cross-platform

    Doppler - secrets manager dla teamów, lokalnie i w CI

    gh secret - sekrety dla GitHub Actions

Idź dalej (źródła)

    Apple - Keychain services

    Microsoft - Credential Manager

    noboxdev - macOS Keychain Tutorial for Developers

    jonmagic - Stop Putting Secrets in .env Files

    Python keyring - PyPI