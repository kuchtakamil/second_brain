# Skrypt kompatybilny z zsh

**Data:** 2024-11-29

---

**User:**

Mam taki początek skryptu w bash
#!/bin/sh

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
a chcę żeby działał w zsh

---

**Assistant:**

Aby ten skrypt działał w `zsh`, nie trzeba dokonywać żadnych zmian w samej logice kodu. Skrypt jest kompatybilny z `zsh`, ponieważ używa standardowych poleceń zgodnych zarówno z `bash`, jak i `zsh`.

Jednak aby upewnić się, że skrypt będzie działał w `zsh`, możesz zmienić shebang (pierwszą linię skryptu) z:

```sh
#!/bin/sh
```

na:

```sh
#!/bin/zsh
```

Jeśli chcesz, aby skrypt działał zarówno w `bash`, jak i `zsh`, możesz pozostawić pierwotny shebang i uruchamiać go odpowiednią powłoką, np.:

```sh
zsh skrypt.sh
```

lub

```sh
bash skrypt.sh
```

### Uwagi dotyczące kompatybilności
Kod:
```sh
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
```

jest kompatybilny z `zsh` i nie wymaga zmian. Działa poprawnie, ponieważ korzysta ze standardowych poleceń `cd`, `dirname` i `pwd`, które są dostępne w obu powłokach.