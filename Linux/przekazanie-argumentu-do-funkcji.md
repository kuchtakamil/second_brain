# Przekazanie argumentu do funkcji.

**Data:** 2024-01-19

---

**User:**

Bash, jak mogę przekazać argument do takiej funkcji
do_sth() {
echo "ok"
}

---

**Assistant:**

W języku skryptowym Bash, aby przekazać argument do funkcji, możesz po prostu wywołać funkcję z argumentem, a następnie odnieść się do tego argumentu wewnątrz funkcji za pomocą specjalnych zmiennych `$1`, `$2`, `$3`, itd., które odnoszą się do pierwszego, drugiego, trzeciego argumentu i tak dalej.

Oto przykład, jak możesz to zrobić:

```bash
do_sth() {
  echo "ok, argument: $1"
}

do_sth "mój argument"
```

W tym przykładzie, gdy wywołujesz `do_sth "mój argument"`, argument `"mój argument"` jest przekazywany do funkcji `do_sth`. Wewnątrz funkcji, `$1` odnosi się do pierwszego argumentu przekazanego do funkcji, czyli `"mój argument"`. Funkcja wypisze na ekranie `"ok, argument: mój argument"`.