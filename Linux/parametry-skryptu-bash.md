# Parametry skryptu Bash

**Data:** 2024-01-22

---

**User:**

mam skrypt bash który mogę wywołać z parametrami
obowiązkowy ---passpharse=sth
opcjonalne
 --key-lock=sth
 --key-name=sth

Jak zapisać w skrócie informacyjnie to polecenie przy pomocy <> i []


---

**Assistant:**

Aby zapisać polecenie z parametrami w skrócie i informacyjnie, można użyć nawiasów kątowych `<>` do oznaczenia parametrów obowiązkowych i nawiasów kwadratowych `[]` do oznaczenia parametrów opcjonalnych. W twoim przypadku, polecenie będzie wyglądać następująco:

```
skrypt.sh --passphrase=<passphrase> [--key-lock=<key-lock>] [--key-name=<key-name>]
```

W tym zapisie:
- `--passphrase=<passphrase>` oznacza parametr obowiązkowy, gdzie `<passphrase>` należy zastąpić odpowiednią wartością.
- `[--key-lock=<key-lock>]` i `[--key-name=<key-name>]` są parametrami opcjonalnymi, gdzie `<key-lock>` i `<key-name>` to wartości, które można podać, jeśli są potrzebne. Nawiasy kwadratowe wskazują, że te parametry nie są wymagane do działania skryptu.