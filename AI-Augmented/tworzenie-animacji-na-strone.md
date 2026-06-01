Wdrożenie "żywego" tła wideo lub animowanego obiektu (np. lewitujący cyber miecz) to świetny sposób, aby przyciągnąć uwagę na waszej sekcji Hero. Zamiast obciążać stronę bibliotekami 3D (np. Three.js), wykorzystujemy najnowsze modele AI do generowania wideo i optymalizujemy je tak, by strona ładowała się błyskawicznie!

Poniżej kompletna procedura krok po kroku:



Krok 1: Generowanie obrazu referencyjnego (Base Image)

Zanim wygenerujemy wideo, potrzebujemy świetnej jakości obrazu wyjściowego (grafiki statycznej). Możesz użyć Midjourney, narzędzi typu "nano banana" lub GPT-image-2 (dla mnie sprawdza się nawet lepiej) lub wygenerować go natywnie bezpośrednio w nowym Antigravity IDE, po prostu rozmawiając z agentem.



Złota zasada: Zadbaj o to, aby główny obiekt znajdował się na jednolitym tle (najlepiej idealnie czarnym #000000 dla ciemnych motywów). Znacznie ułatwi to późniejsze wtopienie wideo w strukturę strony.

Krok 2: Animacja obiektu (Video Generation)

Mając grafikę bazową, przechodzimy do generatorów wideo (np. Veo 3 w Gemini, Runway Gen-3, Luma Dream Machine, Kling, Sora czy Higgsfield).

Żeby uzyskać super efekt, warto budować prompt z konkretnych elementów. Zamiast pisać ogólniki, po prostu opisz poszczególne składowe klatki, na przykład:





Styl i Kadr (Cinematic close-up, Macro shot, Minimalist studio shot)



Główny Obiekt (futuristic cyber katana, glowing glass sneaker, abstract AI core)



Pozycję (floating horizontally, rotating slowly 360 degrees)



Tło (solid black background, clean abstract white space)



Ruch (Subtle, gentle hovering motion, Smooth continuous loop)



Efekty i Detale (Brilliant gold lightning, Glowing neon lines pulsing)



Oświetlenie (Studio lighting, Volumetric cinematic lighting, Dynamic reflections)



Parametry Techniczne (highly detailed, photorealistic, seamless animation, perfect loop, 60fps)

Dzięki takiemu rozbiciu modele bardzo dokładnie odwzorowują to, czego chcemy. Zobaczcie jak to wygląda w praktyce na tych dwóch przykładach:

Przykład 1: Nasza cyber katana z Landing Page



Cinematic close-up of a futuristic cyber katana floating horizontally against a solid black background. Subtle, gentle hovering motion, slowly drifting up and down in a calm animation. Brilliant gold lightning and electrical sparks shimmering and traveling upwards along the blade. Glowing gold circuit board lines on the blade pulse with warm amber light. Light glints and reflections dynamically shift across the metallic hilt and panels. Studio lighting, highly detailed, photorealistic, seamless animation, 60fps.

Przykład 2: Abstrakcja / SaaS (Szklana ikona)



Macro shot of a translucent glass cube with a glowing holographic core, floating horizontally against a solid dark violet background. Gentle, slow-motion bobbing up and down. Warm amber data streams and light particles shifting inside the glass. Crisp studio lighting, sharp refractions and caustic light effects on the surface. Minimalist, photorealistic, seamless animation, perfect loop, 60fps.

Pro Tip: Zwroty seamless animation oraz perfect animation są tu bardzo ważne. Wymuszają na modelu próbę stworzenia wideo, które po zapętleniu nie będzie przeskakiwać, co daje perfekcyjnie płynny, niekończący się efekt.

PS. Podgląd wygląda dziwnie, bo zrobiłem konwersje mp4 do gif na potrzeby tej procedury.



Krok 3: Usuwanie Watermarków

Gdy generujesz wideo przez darmowe aplikacje webowe (np. w przeglądarce), często dostajesz w rogu mały znak wodny.

Jak sobie z tym poradzić? Jeśli wygenerowałeś obiekt na jednolitym tle (co zalecałem w kroku pierwszym), znak wodny to nie problem. Wystarczy poprosić agenta w Antigravity IDE, żeby przy pomocy FFmpeg przyciął wideo (np. odcinając trochę pikseli od dołu), co całkowicie pozbędzie się watermarka. Oczywiście, jeśli korzystasz z płatnego API, od razu dostajesz czysty plik.

Krok 4: Dopasowanie do Tła i Blending (Magia Optyczna)

Zdarza się, że to wygenerowane "czarne" tło z wideo to w rzeczywistości ciemnoszary "brud". Po wstawieniu na idealnie czarną stronę widać wtedy obrzydliwy kwadrat. Żeby to naprawić, robimy dwa kroki:





Korekta kontrastu i jasności (FFmpeg) Nie musisz tego robić ręcznie. Wystarczy, że poprosisz agenta, aby użył FFmpeg i podbił delikatnie kontrast (np. contrast=1.1) oraz obniżył jasność (brightness=-0.05). Szare artefakty momentalnie zlewają się w idealną czerń.



Stylizacja CSS (mix-blend-mode) Aby mieć pewność 100% stopienia z tłem, dodajemy do wideo w HTML jedną krótką regułę CSS:

#hero-katana-video {
    mix-blend-mode: screen;
}

Ten tryb ignoruje czarne piksele i wyświetla tylko te jaśniejsze elementy (jak nasz świecący miecz), przez co wideo wtapia się w stronę niczym warstwa w Photoshopie.

Krok 5: Optymalizacja Formatów dla Webu (LCP & Wydajność)

Standardowe, ciężkie pliki MP4 potrafią zabić wydajność strony i spowolnić jej wczytywanie. Dlatego zawsze przekonwertuj gotowy plik.

Najłatwiej po prostu powiedzieć agentowi - Claude Code, Codex lub innemu, z którego korzystasz, by zamienił to wideo w animowanego WebP (świetnie sprawdza się do krótkich zapętleń i ma mały rozmiar, a dodatkowo obsługuje przezroczystość). Jeśli film jest dłuższy, poproś o konwersję do formatu WebM (VP9). Oba te formaty znacznie odciążą stronę i ułatwią przeglądarce renderowanie.