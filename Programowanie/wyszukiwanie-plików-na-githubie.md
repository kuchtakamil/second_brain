# Wyszukiwanie plików na GitHubie

**Data:** 2023-08-16

---

**User:**

czy możliwe jest wyszukanie w github repozytoriów które zawierają konkretne nazwy plików?

---

**Assistant:**

Tak, możliwe jest wyszukanie repozytoriów na GitHubie, które zawierają konkretne nazwy plików. GitHub zapewnia zaawansowane funkcje wyszukiwania, które umożliwiają dokładne i sprecyzowane wyszukiwanie plików w repozytoriach. Możesz to zrobić za pomocą tzw. języka zapytań (Query Language), który umożliwia tworzenie bardziej zaawansowanych zapytań wyszukiwania.

Aby wyszukać repozytoria zawierające konkretne nazwy plików, możesz skorzystać z GitHub Search API lub GitHub Search Bar na stronie głównej serwisu.

Przykład użycia GitHub Search API w celu znalezienia repozytoriów zawierających plik o nazwie "example.txt":

```
https://api.github.com/search/code?q=filename:example.txt
```

Alternatywnie, jeśli chcesz użyć GitHub Search Bar, możesz wpisać zapytanie bezpośrednio na stronie GitHub:

```
filename:example.txt
```

Powyższe zapytanie spowoduje wyświetlenie listy repozytoriów zawierających plik o nazwie "example.txt".

Warto pamiętać, że GitHub Search API i GitHub Search Bar oferują różne opcje i możliwości filtrowania wyników. Możesz także używać bardziej skomplikowanych zapytań, aby dokładnie dopasować wyszukiwanie do swoich potrzeb.