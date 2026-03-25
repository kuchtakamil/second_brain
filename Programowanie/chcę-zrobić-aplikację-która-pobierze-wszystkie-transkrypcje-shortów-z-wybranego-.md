# Chcę zrobić aplikację która pobierze wszystkie transkrypcje shortów z wybranego

**Data:** 7 lis 2025, 14:20:16 CET

---

**User:**

Chcę zrobić aplikację która pobierze wszystkie transkrypcje shortów z wybranego kanału na youtube. Jednak wiem że używając youtube api odróżnienie shortów od zwykłych filmów nie jest łatwe.
Ta sama treść która mnie interesuje jest też dostępna na tiktok. Czy ściąganie transkrypcji z wybranego kanału byłoby łatwiejsze gdyby źródłem był tiktok a nie youtube?

---

**Gemini:**

Nie, jest to znacznie trudniejsze, a pod wieloma względami wręcz niemożliwe do wykonania w stabilny i niezawodny sposób.

Problem z TikTokiem jest fundamentalny: **brak publicznego, oficjalnego API** do pobierania treści i metadanych z kont innych użytkowników.

---

### 🏛️ Stan API: TikTok

Platforma TikTok udostępnia API dla deweloperów, ale służy ono zupełnie innym celom i jest bezużyteczne dla Twojego przypadku:

1. **TikTok for Business / Ads API:** Służy do zarządzania kampaniami reklamowymi.
2. **Content Posting API:** Służy do... publikowania treści. Wymaga, aby właściciel kanału aktywnie udzielił Twojej aplikacji zgody (OAuth 2.0) na publikowanie w jego imieniu.
3. **Login Kit / Basic Data API:** Służy do logowania użytkowników ("Zaloguj przez TikTok") i pobierania *ich własnych* (autoryzowanych) danych i listy filmów.

Żadne z tych API nie zapewnia publicznego, anonimowego (lub nawet uwierzytelnionego kluczem API) dostępu do odczytu wszystkich filmów z dowolnego, publicznego kanału, tak jak robi to YouTube Data API (`search/list` lub `playlistItems/list`).

#### Ścieżka nieoficjalna (Web Scraping)

Jedyną metodą pozyskania tych danych z TikToka jest web scraping. Jest to jednak ekstremalnie trudne i niestabilne z powodów technicznych:

- **Podpisywanie żądań (Request Signing):** Wewnętrzne API, z którego korzysta aplikacja webowa TikToka (widoczne w zakładce Network w przeglądarce), wymaga dynamicznie generowanych i obfuskowanych sygnatur (np. `X-Bogus`, `_signature`). Inżynieria wsteczna tego mechanizmu jest bardzo zaawansowanym zadaniem i łamie się przy każdej aktualizacji frontendu TikToka.
- **Raportowanie i blokowanie:** Adresy IP serwerów próbujące scrapować są szybko identyfikowane i blokowane (wymagane są duże pule proxy).
- **Brak API dla transkrypcji:** Nawet jeśli udałoby Ci się pobrać listę ID filmów, TikTok nie udostępnia formalnego punktu końcowego do pobierania transkrypcji/napisów (tak jak `captions/download` w YouTube). Musiałbyś polegać na dalszym scrapingu strony konkretnego filmu i parsowaniu wygenerowanych przez AI napisów, co jest jeszcze bardziej kruchym procesem.

Krótko mówiąc, każda aplikacja oparta na scrapingu TikToka przestaje działać co kilka tygodni lub miesięcy i wymaga ciągłej, kosztownej konserwacji.

---

### ⚙️ Rozwiązanie problemu na YouTube

Twój początkowy problem (identyfikacja Shortów na YouTube) jest jak najbardziej realny, ale w przeciwieństwie do problemu z TikTokiem, jest **w pełni rozwiązywalny** przy użyciu oficjalnego i stabilnego API.

Problem polega na tym, że API YouTube traktuje Shorty po prostu jako filmy (`videos`), które znajdują się na regularnej playliście `uploads` kanału. Nie ma prostego filtra `videoType=short`.

**Techniczny proces obejścia tego problemu jest następujący:**

1. **Pobierz ID playlisty `uploads` kanału:** Użyj punktu końcowego `channels/list` z `part=contentDetails` i `id=CHANNEL_ID`. W odpowiedzi znajdziesz `items[0].contentDetails.relatedPlaylists.uploads`, które da Ci `PLAYLIST_ID`.
2. **Pobierz wszystkie `videoId` z playlisty:** Paginuj przez punkt końcowy `playlistItems/list` z `part=contentDetails` i `playlistId=PLAYLIST_ID`. W odpowiedzi otrzymasz listę wszystkich `videoId` na kanale. (`items[N].contentDetails.videoId`).
3. **Pobierz metadane filmów (w partach):** Ponieważ `playlistItems/list` nie zwraca czasu trwania filmu, musisz wykonać dodatkowe zapytanie. Zbierz pobrane `videoId` w paczki po 50 i wywołaj `videos/list` z `part=contentDetails` oraz `id=VIDEO_ID_1,VIDEO_ID_2,...`.
4. **Filtruj filmy:** W odpowiedzi z `videos/list` iteruj po `items`. Kluczowy jest obiekt `items[N].contentDetails.duration`. Jest to string w formacie **ISO 8601** (np. `PT1M30S` dla 1 minuty 30 sekund lub `PT45S` dla 45 sekund).

**Short to każdy film, którego czas trwania (po sparsowaniu) jest krótszy lub równy 60 sekundom.**

To jest główna, niezawodna heurystyka pozwalająca odróżnić Shorty.

1. **Pobierz transkrypcje:** Dla każdego `videoId`, który został zakwalifikowany jako Short, wywołaj `captions/list` z `videoId=VIDEO_ID`, aby zobaczyć dostępne ścieżki napisów. Następnie użyj `captions/download` z `id=CAPTION_ID`, aby pobrać sam plik (zazwyczaj w formacie `.srt` lub `.ttml`).

#### Przykładowa logika w Pythonie (koncept)

Poniższy kod ilustruje logikę filtrowania w kroku 4. Wymaga on funkcji do parsowania czasu trwania ISO 8601 (w produkcji najlepiej użyć biblioteki jak `isodate`).

```
import re

def parse_iso8601_duration(duration_str):
    """
    A basic parser for ISO 8601 durations (e.g., PT1M30S, PT45S).
    This is a simplified example; a robust library like 'isodate' is recommended.
    """
    if not duration_str.startswith('PT'):
        return 0
    
    # Remove 'PT'
    duration_str = duration_str[2:]
    
    total_seconds = 0
    
    # Regex to find hours, minutes, and seconds
    hours = 0
    minutes = 0
    seconds = 0
    
    hour_match = re.search(r'(\d+)H', duration_str)
    if hour_match:
        hours = int(hour_match.group(1))
        
    minute_match = re.search(r'(\d+)M', duration_str)
    if minute_match:
        minutes = int(minute_match.group(1))
        
    second_match = re.search(r'(\d+)S', duration_str)
    if second_match:
        seconds = int(second_match.group(1))

    total_seconds = (hours * 3600) + (minutes * 60) + seconds
    
    # Handle cases like "PT1M" which has no seconds
    if not second_match and not minute_match and not hour_match and 'S' not in duration_str:
         if 'M' in duration_str:
             minutes = int(duration_str.replace('M', ''))
             total_seconds = minutes * 60
    
    return total_seconds

# --- Main Logic ---

# Assume 'videos_response' is the JSON response from youtube.videos().list()
# videos_response = youtube.videos().list(part="contentDetails", id=...").execute()

short_video_ids = []

for item in videos_response.get("items", []):
    video_id = item.get("id")
    duration_iso = item.get("contentDetails", {}).get("duration")
    
    if not duration_iso:
        continue
        
    total_seconds = parse_iso8601_duration(duration_iso)
    
    # A video is a "Short" if it is <= 60 seconds
    if 0 < total_seconds <= 60:
        short_video_ids.append(video_id)

# Now 'short_video_ids' contains only the IDs of the Shorts
# print(f"Found {len(short_video_ids)} Shorts.")

# Next step: Call captions/list and captions/download for each ID
```

### Porównanie

| Cecha | YouTube (przez API v3) | TikTok (przez Scraping) |
| --- | --- | --- |
| **Oficjalne API** | **Tak** | **Nie** (dla tego przypadku użycia) |
| **Stabilność** | **Wysoka.** Gwarantowana przez Google. | **Ekstremalnie niska.** Wymaga ciągłych poprawek. |
| **Wymagany wysiłek** | Średni. Wymaga logiki filtrowania po stronie klienta. | **Ekstremalnie wysoki.** Wymaga inżynierii wstecznej. |
| **Identyfikacja wideo** | **Niezawodna:** `uploads` + filtr `duration`. | **Niestabilna:** Parsowanie HTML / JSON. |
| **Pobieranie transkrypcji** | **Łatwe:** `captions/download` | **Bardzo trudne:** Brak API, konieczność scrapingu strony. |

Trzymaj się YouTube. Problem, który zidentyfikowałeś, jest irytujący (wymaga dodatkowych wywołań API i parsowania), ale jest to problem **inżynieryjny do rozwiązania**, podczas gdy problem z TikTokiem jest **fundamentalną blokadą platformy**.