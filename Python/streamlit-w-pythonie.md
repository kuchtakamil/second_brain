# Streamlit w Pythonie

**Data:** 2025-07-09

---

**User:**

Co to jest streamlit w kontekście aplikacji python?

---

**Assistant:**

**Streamlit** to open-source’owy framework w Pythonie, który umożliwia szybkie tworzenie interaktywnych aplikacji webowych – głównie do eksploracji danych, prototypowania modeli machine learning i prezentacji wyników analiz. Został zaprojektowany tak, aby programiści (szczególnie ci, którzy nie znają się na frontendzie) mogli łatwo tworzyć GUI bez potrzeby używania HTML, CSS czy JavaScriptu.

### Główne cechy Streamlit:
- **Prosty interfejs API** – interfejs jest oparty na standardowym Pythonie, bez konieczności pisania kodu frontendowego.
- **Interaktywność** – dzięki widgetom takim jak `st.slider`, `st.button`, `st.selectbox`, można szybko dodać kontrolki umożliwiające użytkownikowi interakcję z aplikacją.
- **Reaktywność** – Streamlit działa jak notebook, tzn. aplikacja jest przeliczana od początku przy każdej interakcji użytkownika.
- **Integracja z Pandas, Matplotlib, Plotly, Altair, itp.** – łatwo można wyświetlać wykresy, tabele i inne dane wizualne.

### Przykład użycia:
```python
import streamlit as st
import pandas as pd

st.title("Prosta aplikacja Streamlit")

name = st.text_input("Jak masz na imię?")
age = st.slider("Ile masz lat?", 0, 100, 25)

st.write(f"Cześć {name}, masz {age} lat.")

df = pd.DataFrame({
    'x': [1, 2, 3],
    'y': [4, 5, 6]
})
st.line_chart(df)
```

### Jak uruchomić aplikację Streamlit:
1. Zainstaluj: `pip install streamlit`
2. Zapisz skrypt jako np. `app.py`
3. Uruchom: `streamlit run app.py`

### Typowe zastosowania:
- Prezentacja wyników analiz danych
- Interfejsy do eksploracji modeli ML
- Dashboardy
- Prototypy aplikacji webowych z backendem w Pythonie

Jeśli chcesz, mogę pomóc stworzyć przykład aplikacji pod konkretny use case (np. wizualizacja danych, input/output danych itp.).