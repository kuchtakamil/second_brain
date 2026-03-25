# Rozwiązywanie błędu importu

**Data:** 2025-11-20

---

**User:**

używam cursor.sh i otwieram tam pliki ipynb.
Nie mogę wykonać 
from langchain_huggingface import HuggingFaceEmbeddings
ModuleNotFoundError: No module named 'langchain_huggingface'

---

**Assistant:**

`langchain_huggingface` jest osobnym pakietem i **nie jest instalowany automatycznie razem z LangChain**.  
Dlatego pojawia się:

```
ModuleNotFoundError: No module named 'langchain_huggingface'
```

### Co zrobić?

1. **Zainstaluj brakujący pakiet:**

```
pip install langchain-huggingface
```

W środowiskach Jupyter/`.ipynb` (w tym w Cursorze) najlepiej zrobić:

```python
!pip install langchain-huggingface
```

2. **Upewnij się, że kernel Jupytera jest ten sam, w którym instalujesz pakiet.**

Częsty problem: Cursor odpala kernel z innej wersji Pythona niż ta, w której instalujesz pakiety.  
Możesz sprawdzić:

```python
import sys
print(sys.executable)
```

Otwórz terminal i zrób:

```
which python
pip show langchain-huggingface
```

Jeśli wskazują różne ścieżki — instalacja poszła do innego środowiska.

3. **Poprawny import po instalacji:**

```python
from langchain_huggingface import HuggingFaceEmbeddings
```

---

Jeśli nadal nie działa, powiedz mi:
- wynik `sys.executable`,
- jakiego Pythona używa Cursor (np. venv, pyenv, systemowy),
- czy instalujesz pakiety z poziomu terminala w Cursorze czy globalnie.

Sprawdzimy, gdzie leży konflikt środowisk.

---

**User:**

Mam taki requirements.txt To nie wystarczy?
python-dotenv
ipykernel
ipywidgets
requests
numpy
pandas
scipy
scikit-learn
matplotlib
torch
transformers
tqdm
openai
gradio
langchain
langchain-core
langchain-text-splitters
langchain-openai
langchain-chroma
langchain-community
datasets==3.6.0
matplotlib
google-generativeai
anthropic
chromadb
plotly
jupyter-dash
beautifulsoup4
pydub
modal
ollama
psutil
setuptools
speedtest-cli
sentence_transformers
feedparser
protobuf==3.20.2
wandb

---

**Assistant:**

Niestety **to nie wystarczy**, bo `langchain-huggingface` **nie jest częścią** żadnego z pakietów, które masz w `requirements.txt`.  
Nie znajduje się ani w `langchain`, ani w `langchain-community`, ani w `transformers`, ani w `sentence_transformers`.

To **osobny projekt** i musi być dodany ręcznie.

### Jeśli chcesz, wystarczy dopisać w requirements.txt:

```
langchain-huggingface
```

lub konkretną wersję (najczęściej latest działa dobrze):

```
langchain-huggingface>=0.1.0
```

Potem:

```
pip install -r requirements.txt
```

### Dlaczego ten pakiet nie jest domyślnie instalowany?

LangChain od jakiegoś czasu dzieli integracje na osobne moduły, aby uniknąć instalowania wszystkiego wszystkim.  
HuggingFace dostał własny pakiet:  
`langchain-huggingface` → https://pypi.org/project/langchain-huggingface/

### Po instalacji import będzie działał:

```python
from langchain_huggingface import HuggingFaceEmbeddings
```

---

Jeśli chcesz, mogę przejrzeć cały Twój requirements.txt i podpowiedzieć, czy coś da się uprościć lub zmodernizować.