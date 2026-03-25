# na ubuntu chcę utworzyć swoje CV w latex. Od czego powinienem zacząć?

**Data:** 2 lut 2026, 20:38:44 CET

---

**User:**

na ubuntu chcę utworzyć swoje CV w latex. Od czego powinienem zacząć?

---

**Gemini:**

### Instalacja środowiska TeX Live

Na systemie Ubuntu najstabilniejszym rozwiązaniem jest instalacja dystrybucji **TeX Live**. Masz dwie główne drogi: wersję okrojoną (podstawową) lub pełną.

```
# Opcja 1: Pełna instalacja (zalecana, ok. 5GB, zawiera wszystkie paczki i fonty)
sudo apt update
sudo apt install texlive-full

# Opcja 2: Instalacja minimalistyczna (wymaga ręcznego doinstalowywania brakujących paczek)
sudo apt install texlive-latex-extra texlive-fonts-recommended
```

Do edycji kodu LaTeX na Ubuntu najlepiej wykorzystać **Visual Studio Code** z rozszerzeniem **LaTeX Workshop** (obsługuje podgląd PDF w czasie rzeczywistym i autouzupełnianie) lub dedykowane IDE typu **Texmaker**.

---

### Wybór silnika i klasy dokumentu

Standardowy `pdflatex` jest szybki, ale jeśli planujesz używać nowoczesnych fontów systemowych (OpenType/TrueType), lepiej skonfigurować projekt pod **XeLaTeX** lub **LuaLaTeX**.

Podstawą CV może być standardowa klasa `article` z silną modyfikacją marginesów lub gotowe klasy typu `moderncv` czy `friggeri`. Jednak dla pełnej kontroli nad layoutem, profesjonaliści często budują własną strukturę w oparciu o paczkę `geometry` i `titlesec`.

---

### Struktura zaawansowanego szablonu (Main File)

Poniżej znajduje się przykład szkieletu CV wykorzystujący makra do zachowania spójności danych (tzw. *separation of concerns*).

```
\documentclass[a4paper,11pt]{article}

% Language and Encoding
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage[english]{babel}

% Layout and Geometry
\usepackage[hmargin=1.5cm, vmargin=1.5cm]{geometry}
\usepackage{titlesec}
\usepackage{enumitem}
\usepackage{hyperref}

% Custom Colors and Styling
\usepackage{xcolor}
\definecolor{primary}{HTML}{2e3440}
\definecolor{secondary}{HTML}{4c566a}

% Custom section formatting
\titleformat{\section}{
  \vspace{-4pt}\scshape\raggedright\large\bfseries
}{}{0em}{}[\color{black}\titlerule \vspace{-5pt}]

% Custom commands for CV entries
\newcommand{\cvitem}[4]{
  \noindent \textbf{#1} \hfill #2 \\
  \noindent \textit{#3} \hfill \textit{#4} \par
  \vspace{4pt}
}

\begin{document}

% Header
\begin{center}
    {\Huge \textbf{John Doe}} \\ \vspace{5pt}
    \href{mailto:john.doe@example.com}{john.doe@example.com} | 
    \href{https://linkedin.com/in/johndoe}{linkedin.com/in/johndoe} |
    +48 123 456 789
\end{center}

\section{Experience}

\cvitem{Senior Software Engineer}{Jan 2022 -- Present}{Tech Solutions Corp}{Kraków, PL}
\begin{itemize}[noitemsep,topsep=0pt]
    \item Architecting microservices using Go and Kubernetes.
    \item Improved CI/CD pipeline efficiency by 40\% using custom GitHub Actions.
    \item Mentoring junior developers and conducting code reviews.
\end{itemize}

\section{Education}

\cvitem{M.Sc. in Computer Science}{2016 -- 2021}{AGH University of Science and Technology}{Kraków, PL}

\section{Skills}
\textbf{Languages:} C++, Python, Rust, Go, SQL. \\
\textbf{Tools:} Docker, Kubernetes, Terraform, Git, \LaTeX.

\end{document}
```

---

### Zarządzanie bibliografią i publikacjami

Jeśli Twoje CV musi zawierać dorobek naukowy, użyj **BibLaTeX**. Pozwala to na separację bazy publikacji (`.bib`) od warstwy prezentacji.

```
\usepackage[backend=biber, style=numeric, sorting=ydnt]{biblatex}
\addbibresource{publications.bib}

% W miejscu gdzie mają się pojawić publikacje:
\nocite{*} % Wyświetla wszystkie pozycje z pliku .bib
\printbibliography[title={Scientific Publications}]
```

Aby skompilować taki dokument na Ubuntu, użyj sekwencji:

```
pdflatex cv.tex
biber cv
pdflatex cv.tex
```

---

### Automatyzacja budowania (Makefile)

Dla zaawansowanych projektów warto utworzyć plik `Makefile`, który zautomatyzuje czyszczenie plików tymczasowych (`.aux`, `.log`, `.out`) i kompilację.

```
FILENAME = cv

pdf:
	latexmk -pdf -shell-escape $(FILENAME).tex

clean:
	latexmk -c
	rm -f *.bbl *.run.xml
```

Wówczas na Ubuntu wystarczy wpisać `make` w terminalu, aby otrzymać gotowy plik PDF.

---

### Wykorzystanie fontów systemowych (XeLaTeX)

Jeśli chcesz użyć fontów takich jak *Roboto* czy *Source Sans Pro* zainstalowanych w Ubuntu:

1. Zmień silnik na `xelatex`.
2. Dodaj paczkę `fontspec`.

```
\usepackage{fontspec}
\setmainfont{Roboto-Regular}[
    BoldFont = Roboto-Bold,
    ItalicFont = Roboto-Italic
]
```

Kompilacja: `xelatex cv.tex`.

Czy chcesz, abym przygotował dla Ciebie bardziej rozbudowane makra dla konkretnej sekcji, np. automatyczne generowanie pasków postępu umiejętności lub integrację z FontAwesome?