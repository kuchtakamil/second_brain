# Ukrywanie wrażliwych danych

**Data:** 2023-06-19

---

**User:**

czy w kibana istnieje możliwość ukrycia niektórych wrażliwych danych? np. podczas przeglądania logów, nie chcę widzieć żadnych adresów email

---

**Assistant:**

Tak, w Kibana istnieje możliwość ukrycia niektórych wrażliwych danych podczas przeglądania logów. Możesz to osiągnąć przy użyciu funkcji maskowania danych lub filtrów.

1. Maskowanie danych: Kibana umożliwia zastosowanie maskowania na polach, które zawierają wrażliwe dane. Na przykład, jeśli chcesz ukryć adresy e-mail, możesz zdefiniować maskowanie dla pola zawierającego te adresy. Maskowanie może zastąpić wrażliwe dane innymi znakami, na przykład gwiazdkami lub znakami zastępczymi. Dzięki temu podczas przeglądania logów zamiast pełnych adresów e-mail zobaczysz zasłonięte wersje.

2. Filtry: Możesz również skonfigurować filtry w Kibana, aby wykluczyć wybrane pola zawierające wrażliwe dane. Na przykład, można stworzyć filtr, który automatycznie wyklucza pola zawierające adresy e-mail z wyników przeglądanych logów. Filtry pozwalają na bardziej precyzyjne zarządzanie widocznymi danymi.

Warto pamiętać, że ukrywanie wrażliwych danych w Kibana jest kwestią konfiguracji i zależy od sposobu przechowywania i indeksowania logów oraz zastosowanych w Kibana uprawnień użytkowników. Należy odpowiednio skonfigurować rolę i uprawnienia użytkowników w Kibana, aby zapewnić odpowiednią ochronę danych w zależności od potrzeb i wymagań organizacji.

---

**User:**

napisz coś więcej o maskowaniu

---

**Assistant:**

Maskowanie danych w Kibana polega na zastąpieniu wrażliwych informacji specjalnymi znakami lub pseudonimami, aby uniemożliwić ich odczytanie przez użytkowników, którzy nie mają odpowiednich uprawnień. Jest to użyteczne w przypadkach, gdy chcesz zachować poufność pewnych danych, takich jak hasła, numery kart kredytowych, adresy e-mail czy numery identyfikacyjne.

Kibana oferuje kilka mechanizmów maskowania, które można skonfigurować dla konkretnych pól:

1. Stałe maskowanie: Polega na zastąpieniu wrażliwych danych określonymi stałymi znakami. Na przykład, wszystkie adresy e-mail mogą zostać zastąpione znakiem "*".

2. Maskowanie z wykorzystaniem wyrażeń regularnych: Pozwala na zdefiniowanie bardziej zaawansowanych wzorców do maskowania danych. Możesz użyć wyrażeń regularnych, aby dopasować konkretne wzorce, takie jak adresy e-mail, numery telefonów itp., i zastąpić je odpowiednimi znakami zastępczymi.

3. Maskowanie za pomocą funkcji transformacji: Kibana udostępnia funkcje transformacji, które pozwalają na dynamiczne modyfikowanie danych przed ich wyświetleniem. Możesz zastosować funkcję transformacji do konkretnego pola, aby przeprowadzić niestandardowe operacje maskowania.

Ważne jest, aby pamiętać, że maskowanie danych w Kibana wpływa tylko na sposób wyświetlania danych w interfejsie użytkownika. Samo maskowanie nie wpływa na faktyczne przechowywanie danych. Dlatego też konieczne jest odpowiednie zabezpieczenie danych na poziomie indeksu, aby zapewnić, że wrażliwe informacje nie będą dostępne dla osób nieupoważnionych.

Maskowanie danych jest ważnym narzędziem w zarządzaniu wrażliwymi informacjami i zapewnianiu poufności danych w Kibana. Pamiętaj, że dokładne metody i możliwości maskowania danych w Kibana mogą się różnić w zależności od wersji oprogramowania i zastosowanych rozwiązań.