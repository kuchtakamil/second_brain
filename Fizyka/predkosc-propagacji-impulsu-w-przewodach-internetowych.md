# Prędkość propagacji impulsu w przewodach sieci Internet

## Krótkie podsumowanie
Temat ten opisuje, z jaką faktyczną prędkością przemieszczają się sygnały (impulsy elektryczne lub świetlne) w różnych rodzajach kabli używanych w infrastrukturze internetowej. Co ciekawe, impulsy te nie poruszają się z pełną prędkością światła w próżni, a ich prędkość zależy głównie od właściwości fizycznych nośnika. Czas potrzebny na to, aby impuls fizycznie "obiegł" kulę ziemską (ok. 40 000 km) z pominięciem opóźnień na routerach, wynosi **około 0,2 sekundy (200 milisekund)**.

## Zastosowanie i znaczenie
Zrozumienie prędkości propagacji sygnału jest kluczowe w projektowaniu globalnych sieci telekomunikacyjnych, systemów rozproszonych i technologii wymagających bardzo niskich opóźnień (np. giełdy High-Frequency Trading, gry online, obliczenia rozproszone). Fizyczne ograniczenia rozchodzenia się fal w różnych ośrodkach tworzą tzw. "twardy limit" opóźnienia (*latency*), którego w żaden sposób nie da się zlikwidować poprzez optymalizację oprogramowania sieciowego.

## Jak to działa w różnych kablach

Propagacja impulsu to przesyłanie fali elektromagnetycznej, niezależnie od tego, czy mówimy o miedzi czy szkle. Jej prędkość w medium różnym od próżni określa się za pomocą Współczynnika Prędkości (*Velocity Factor* - $VF$), który wyraża stosunek prędkości sygnału w danym ośrodku do niezmiennej prędkości światła w próżni ($c \approx 300\ 000\text{ km/s}$).
$$ v = VF \cdot c $$

### 1. Światłowody (Kable optyczne)
W kablach światłowodowych będących np. fundamentem tzw. szkieletu Internetu, sieć przesyła sygnał za pomocą światła biegnącego najczęściej w rdzeniu szklanym.
- **Współczynnik załamania**: Światło rozchodzi się wolniej niż w próżni z powodu współczynnika załamania światła charakteryzującego szkło (wynoszącego zwykle od 1,45 do 1,5).
- **Prędkość**: $VF \approx 0,67$. Zatem faktyczna prędkość przesyłu sygnału świetlnego w rurce światłowodu wynosi **około 200 000 km/s** (ok. 67% prędkości stałej $c$).
- To takie kable leżą na dnie oceanów, łącząc kontynenty i transportując przytłaczającą większość globalnego ruchu.

### 2. Kable miedziane (Skrętka - Ethernet, kable koncentryczne)
Niewielkie dystanse (np. w sieci domowej czy LAN) często obsługują przewody ze stopami metalu w środku, po których biegają impulsy prądu (a właściwie przemieszcza się fala elektromagnetyczna).
- **Dielektryk**: Wbrew obiegowej opinii, fala elektromagnetyczna rozchodzi się wokół przewodnika – w jego izolacji (dielektryku), która go otacza i oddziela od innych par żył, i to ona dyktuje jej prędkość. 
- **Prędkość**: Typowe okablowanie osiąga współczynniki $VF$ w przedziale od 0,60 do 0,85 w zależności od jakości zastosowanego tworzywa izolacyjnego. Przekłada się to uśredniając na prędkości ról rzędu **180 000 km/s do 250 000 km/s**.
- Chociaż miedź charakteryzuje się tu dość dobrą prędkością propagacji, sam nośnik generuje ogromne tłumienia, dlatego bez regeneracji nie nadaje się do wysyłania impulsów na dziesiątki czy setki kilometrów.

## Czas potrzebny na okrążenie Ziemi

Zakładając hipotetyczną sytuację, w której chcemy wysłać impuls, wymuszając jego podróż wokół obwodu Ziemi idealnym przewodem bez jakichkolwiek wzmacniaczy po drodze ani routerów wnoszących czas na cyfrowe przetwarzanie:

1. **Obwód Ziemi** wzdłuż równika wnosi około $s = 40\ 000\text{ km}$.
2. **Prędkość sygnału** typowa dla standardowych światłowodów i kabli komunikacyjnych w infrastrukturze to około $v = 200\ 000\text{ km/s}$.

Korzystając ze standardowego wzoru na czas ($t = \frac{s}{v}$):
$$ t = \frac{40\ 000\text{ km}}{200\ 000\text{ km/s}} = 0,2\text{ s} $$

**Wniosek:** Czas niezbędny na obiektywne przebycie impulsu z punktu A w powrotem do punktu A (jeden obieg guli ziemskiej) to równe **200 milisekund (ms)** w jedną stronę. Stanowi to minimalny fizyczny interwał do pokonania i nieścisłą "ramę" najpowszechniejszego światowego *latency*. Gdybyśmy liczyli PING (który mierzy czas podróży w tam i z powrotem - ang. *round-trip time*), wynosiłby on na takim dystansie co najmniej **400 ms** z samej tylko racji oporu czasowego medium, pomijając urządzenia aktywne.

## Powiązane pliki
- [Wymiana ciepła z powietrzem](wymiana-ciepła-z-powietrzem.md) - zagadnienia związane z fizycznymi stratami energii.
- [Równania Maxwella wyjaśnione](równania-maxwella-wyjaśnione.md) - wyjaśnienie mechanizmów fal elektromagnetycznych.
- [Średnica przewodu, kabla](średnica-przewodu-kabla.md) - zjawiska na styku elektrotechniki i fizyki przewodników.
