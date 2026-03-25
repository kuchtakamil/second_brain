# przygotuj kilka nazw czcionek które pasowałyby do w miarę nowoczesnego ale racze

**Data:** 2 lut 2026, 21:01:58 CET

---

**User:**

przygotuj kilka nazw czcionek które pasowałyby do w miarę nowoczesnego ale raczej czystego CV

---

**Gemini:**

Wybór fontu w systemie LaTeX przy użyciu silnika **XeLaTeX** lub **LuaLaTeX** daje dostęp do pełnej biblioteki fontów systemowych Ubuntu oraz profesjonalnych krojów OpenType. Poniżej zestawienie najlepszych propozycji dla nowoczesnego i przejrzystego CV, podzielone na kategorie stylistyczne.

---

### 1. Sans-Serif (Standard nowoczesności)

Te kroje są najbardziej czytelne na ekranach i nadają dokumentowi lekkości.

- **Inter**: Obecnie uważany za "złoty standard" w interfejsach i nowoczesnej typografii. Jest niezwykle precyzyjny, z optymalnym kerningiem (odstępami między literami), co sprawia, że tekst wygląda bardzo czysto nawet przy małym stopniu pisma.
- **Source Sans 3 (dawniej Pro)**: Zaprojektowany przez Adobe specjalnie pod kątem czytelności w interfejsach użytkownika. Jest neutralny, ale posiada bardzo profesjonalny charakter.
- **Lato**: Stworzony przez polskiego projektanta Łukasza Dziedzica. Łączy w sobie elegancję z przyjaznymi, lekko zaokrąglonymi kształtami. Świetnie sprawdza się w sekcjach "O mnie".
- **Montserrat**: Geometryczny font, który doskonale nadaje się do nagłówków i imienia w nagłówku CV. W tekście ciągłym może być nieco zbyt szeroki, dlatego często paruje się go z Interem lub Roboto.

### 2. Wyraziste i techniczne

- **Fira Sans**: Jeśli Twoje CV dotyczy branży IT/Engineering, Fira Sans (stworzona dla systemu Firefox OS) oddaje techniczny, ale nowoczesny charakter. Jest bardzo czytelna przy listowaniu stosu technologicznego.
- **Roboto**: Systemowy font Androida. Jest bezpiecznym, solidnym wyborem – niemożliwym do "zepsucia", choć przez swoją popularność może wydawać się nieco generyczny.

### 3. Nowoczesne szeryfy (Hybrid Look)

Jeśli chcesz zachować klasyczny sznyt, ale uniknąć archaicznego wyglądu *Times New Roman*:

- **Charter (Bitstream Charter)**: Wygląda bardzo nowocześnie i profesjonalnie. Jest "cięższy" niż standardowe szeryfy, co nadaje dokumentowi powagi i autorytetu.
- **Linux Biolinum**: Sans-serifowa alternatywa dla Linux Libertine. Bardzo elegancka, świetnie nadaje się do CV akademickich lub prawniczych, które chcą wyglądać nowocześnie.

---

### Implementacja w LaTeX (XeLaTeX/LuaLaTeX)

Aby użyć tych fontów, musisz wykorzystać paczkę `fontspec`. Poniższy kod pokazuje, jak zdefiniować różne fonty dla nagłówków i treści głównej:

```
\usepackage{fontspec}

% Ustawienie głównego fontu tekstu
\setmainfont{Inter}[
    Path = ./fonts/, % opcjonalne, jeśli pliki .otf są w folderze projektu
    Extension = .otf,
    UprightFont = *-Regular,
    BoldFont = *-Bold,
    ItalicFont = *-Italic
]

% Ustawienie fontu dla nagłówków
\newfontfamily\headerfont{Montserrat}[
    Path = ./fonts/,
    Extension = .otf,
    UprightFont = *-ExtraBold
]

% Przykład użycia w tytule sekcji
\titleformat{\section}{
  \headerfont\Large\bfseries\scshape\raggedright
}{}{0em}{}[\color{black}\titlerule]
```

---

### Instalacja fontów na Ubuntu

Większość z powyższych fontów możesz zainstalować bezpośrednio z repozytoriów Ubuntu, co ułatwi ich wykrywanie przez LaTeX-a:

```
# Instalacja najpopularniejszych fontów
sudo apt update
sudo apt install fonts-inter fonts-lato fonts-roboto fonts-font-awesome fonts-firacode
```

Jeśli pobierasz fonty ręcznie (np. z Google Fonts), umieść pliki `.ttf` lub `.otf` w katalogu `~/.local/share/fonts`, a następnie odśwież cache:

```
fc-cache -f -v
```

---

### Tabela porównawcza

| Nazwa fontu | Typ | Najlepsze zastosowanie | Charakter |
| --- | --- | --- | --- |
| **Inter** | Sans | Tekst główny | Precyzyjny, techniczny |
| **Montserrat** | Sans | Nagłówki / Imię | Bold, geometryczny |
| **Lato** | Sans | Całość CV | Elegancki, ludzki |
| **Charter** | Serif | CV klasyczne/akademickie | Profesjonalny, stabilny |
| **Fira Sans** | Sans | IT / Data Science | Nowoczesny, techniczny |

Czy chciałbyś, abym przygotował konkretną konfigurację `fontspec` dla wybranej pary fontów (np. Montserrat dla nagłówków i Inter dla treści)?