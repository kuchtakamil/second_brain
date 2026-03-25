# Zmienna środowiskowa i funkcja.

**Data:** 2023-07-14

---

**User:**

W lua chcę stworzyć funkcję kótra korzysta ze zmiennej środowiskowej o nazwie "MY_ENV_VAR", jeśli jest ustawiona na "true", chciałbym wypisć na ekran "jest ok". 
Funkcja będzie wykorzystywana wiele razy ale chciałbym aby zmienna środowiskowa była pobierana tylko raz. Czy to możliwe?

---

**Assistant:**

Tak, jest możliwe. Możesz zapisać wartość zmiennej środowiskowej w lokalnej zmiennej, aby uniknąć wielokrotnego pobierania jej wartości. Oto przykładowy kod w języku Lua, który wykonuje to zadanie:

```lua
local myEnvVar = os.getenv("MY_ENV_VAR") -- Pobranie wartości zmiennej środowiskowej

function checkEnvVar()
  if myEnvVar == "true" then
    print("jest ok")
  end
end
```

W powyższym kodzie funkcja `os.getenv("MY_ENV_VAR")` pobiera wartość zmiennej środowiskowej "MY_ENV_VAR" i przypisuje ją do lokalnej zmiennej `myEnvVar`. Następnie, w funkcji `checkEnvVar()`, sprawdzane jest, czy wartość `myEnvVar` wynosi "true", a jeśli tak, wypisywane jest na ekranie "jest ok".

Pamiętaj, że musisz mieć ustawioną zmienną środowiskową "MY_ENV_VAR" przed uruchomieniem tego kodu, aby działał poprawnie.