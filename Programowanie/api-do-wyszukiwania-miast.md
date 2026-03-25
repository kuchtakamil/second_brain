# API do wyszukiwania miast

**Data:** 2024-04-23

---

**User:**

Chcę znaleźć API dzięki któremu znajdę wszystkie miasta lub gminy w promieniu danej liczby kilometrów

---

**Assistant:**

Jeśli chcesz znaleźć API, które umożliwia wyszukiwanie miast lub gmin w określonym promieniu, możesz spróbować skorzystać z serwisu takiego jak OpenStreetMap. OpenStreetMap (OSM) jest projektem mapowania, który udostępnia dane geograficzne dla całego świata, a dostępne są różne narzędzia i API do pobierania tych danych.

Jednym z popularnych sposobów dostępu do danych OSM jest korzystanie z Overpass API. Overpass API umożliwia wyszukiwanie i pobieranie danych geograficznych z OpenStreetMap. Możesz skorzystać z Overpass API, aby znaleźć wszystkie miasta lub gminy w danym promieniu od określonego punktu.

Oto jak możesz to zrobić:

1. Określ współrzędne punktu odniesienia (np. długość i szerokość geograficzną).
2. Użyj Overpass API, aby zapytać o wszystkie miasta lub gminy w określonym promieniu od tego punktu.

Przykładowe zapytanie Overpass API mogłoby wyglądać tak:

```
[out:json];
(
  node["place"="city"](around:10000,51.5074,-0.1278); // Wyszukuje miasta w promieniu 10 km od Londynu
  node["place"="town"](around:10000,51.5074,-0.1278); // Wyszukuje miasteczka w promieniu 10 km od Londynu
  node["place"="village"](around:10000,51.5074,-0.1278); // Wyszukuje wioski w promieniu 10 km od Londynu
);
out body;
>;
out skel qt;
```

W powyższym przykładzie `around:10000` oznacza promień w metrach (10 km), a `(51.5074,-0.1278)` to współrzędne geograficzne Londynu.

Możesz dostosować to zapytanie do swoich potrzeb, zmieniając rodzaj miejscowości (`"place"`) i promień (`around:xxxxx`). Upewnij się, że zapoznałeś się z dokumentacją Overpass API, aby dowiedzieć się więcej o dostępnych opcjach wyszukiwania i formatach odpowiedzi.