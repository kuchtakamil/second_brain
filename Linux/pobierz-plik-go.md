# Pobierz plik go.

**Data:** 2023-05-22

---

**User:**

Jak za pomocą curl lub wget w systemie linux pobrać na dysk plik z pod linku
https://go.dev/dl/go1.20.4.linux-amd64.tar.gz

---

**Assistant:**

Możesz użyć polecenia `curl` lub `wget` w systemie Linux, aby pobrać plik z podanego linku. Oto przykładowe instrukcje dla obu narzędzi:

1. Używając curl:
```
curl -O https://go.dev/dl/go1.20.4.linux-amd64.tar.gz
```
Polecenie `curl -O` pobierze plik z podanego adresu URL i zapisze go w bieżącym katalogu pod tą samą nazwą.

2. Używając wget:
```
wget https://go.dev/dl/go1.20.4.linux-amd64.tar.gz
```
Polecenie `wget` również pobierze plik z podanego adresu URL i zapisze go w bieżącym katalogu pod tą samą nazwą.

W obu przypadkach plik `go1.20.4.linux-amd64.tar.gz` zostanie pobrany i zapisany w bieżącym katalogu, w którym uruchomiłeś polecenie.