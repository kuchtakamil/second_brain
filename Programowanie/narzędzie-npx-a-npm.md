# Narzędzie `npx` a `npm`

**Data:** 2024-03-26

---

**User:**

co to jest npx i czym się różni od npm

---

**Assistant:**

`npx` jest narzędziem wchodzącym w skład narzędzi do zarządzania pakietami Node.js (Node Package Manager - npm). Różni się od samego `npm` w kilku istotnych aspektach:

1. **Wykonywanie paczek bez instalacji**: Główną różnicą między `npx` a `npm` jest to, że `npx` pozwala na uruchamianie pakietów Node.js bez konieczności ich wcześniejszej instalacji. Dzięki temu można korzystać z paczek zdefiniowanych w npm bezpośrednio z wiersza poleceń, nawet jeśli nie są one zainstalowane globalnie ani lokalnie.

2. **Wersje pakietów**: `npx` pozwala na uruchamianie paczek z określoną wersją, nawet jeśli ta wersja nie jest obecnie zainstalowana na Twoim systemie. W przypadku `npm`, musisz najpierw zainstalować daną wersję pakietu, aby móc z niej skorzystać.

3. **Lokalne wykonanie**: `npx` może wykonywać paczki z lokalnych źródeł, czyli z katalogu projektu, w którym znajdujesz się w danym momencie. Możesz więc użyć `npx` do uruchomienia paczki znajdującej się w danym projekcie bez konieczności instalowania jej globalnie ani lokalnie.

Podsumowując, `npx` jest narzędziem, które ułatwia korzystanie z pakietów Node.js poprzez wykonywanie ich bezpośrednio z wiersza poleceń, zarządzanie wersjami oraz umożliwia lokalne wykonanie paczek bez konieczności ich instalacji.