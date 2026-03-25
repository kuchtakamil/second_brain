# Zostańmy przy Server-side Batch API. Możesz mi pokazać jak stworzyć taki JSONL i

**Data:** 18 gru 2025, 15:33:38 CET

---

**User:**

Zostańmy przy Server-side Batch API. Możesz mi pokazać jak stworzyć taki JSONL i jak go w kodzie później wysłać?

---

**Gemini:**

Aby skorzystać z **Server-side Batch API**, musisz przygotować plik w formacie JSONL (JSON Lines), gdzie każda linia jest autonomicznym obiektem żądania. W przypadku modelu Gemini 3, kluczowe jest poprawne zdefiniowanie struktury `contents` oraz `system_instruction`.

### 1. Struktura pliku JSONL

Dla Twojego przypadku, gdzie masz stały system prompt i zmienną zawartość pliku, pojedyncza linia w pliku `inputs.jsonl` powinna wyglądać następująco:

```
{
  "request": {
    "model": "models/gemini-3-pro-preview",
    "system_instruction": {
      "parts": [{"text": "Twój długi system prompt (2400 znaków)..."}]
    },
    "contents": [
      {
        "role": "user",
        "parts": [{"text": "Zawartość Twojego pliku (40000 znaków)..."}]
      }
    ],
    "generationConfig": {
      "temperature": 0.7,
      "maxOutputTokens": 2048
    }
  }
}
```

### 2. Generator pliku JSONL (Python)

Poniższy skrypt automatyzuje proces tworzenia pliku, dbając o poprawne kodowanie znaków i strukturę JSON, co jest krytyczne przy dużych blokach tekstu (40k znaków).

```
import json

def generate_batch_file(system_prompt, file_contents_list, output_file="batch_input.jsonl"):
    """
    Generates a JSONL file for Gemini Batch API.
    
    Args:
        system_prompt (str): The common system instruction.
        file_contents_list (list): List of strings, each being the content of a text file.
        output_file (str): Path to the resulting .jsonl file.
    """
    with open(output_file, 'w', encoding='utf-8') as f:
        for content in file_contents_list:
            payload = {
                "request": {
                    "model": "models/gemini-3-pro-preview",
                    "system_instruction": {
                        "parts": [{"text": system_prompt}]
                    },
                    "contents": [
                        {
                            "role": "user",
                            "parts": [{"text": content}]
                        }
                    ]
                }
            }
            f.write(json.dumps(payload) + '\n')

# Example usage
sys_prompt = "You are a specialized technical analyst..."
files = ["Content of file 1...", "Content of file 2...", "Content of file N..."]
generate_batch_file(sys_prompt, files)
```

---

### 3. Wysyłanie zadania Batch API

Do komunikacji z API zaleca się użycie nowej biblioteki `google-genai` (następcy `google-generativeai`), która natywnie obsługuje asynchroniczne zadania wsadowe.

W pierwszej kolejności musisz wrzucić plik JSONL na serwer Google (lub udostępnić go przez GCS), a następnie zainicjować zadanie.

```
from google import genai
import time

client = genai.Client(api_key='YOUR_API_KEY')

# 1. Upload the file to Gemini API File Service
# This step is necessary to get a URI that Batch API can access
uploaded_file = client.files.upload(path="batch_input.jsonl")

# 2. Create the Batch Job
batch_job = client.batches.create(
    model='models/gemini-3-pro-preview',
    src=uploaded_file.uri,
)

print(f"Batch Job Created: {batch_job.name}")

# 3. Monitor the status
while True:
    job = client.batches.get(batch_job.name)
    print(f"Current Status: {job.state}")
    
    if job.state == 'SUCCEEDED':
        print("Batch processing finished!")
        break
    elif job.state == 'FAILED':
        print("Job failed.")
        break
        
    time.sleep(60) # Wait 60 seconds before next check

# 4. Download results
# Results are typically saved in a new file in the cloud
if job.response_file_uri:
    # You can download the result file using the URI
    print(f"Results available at: {job.response_file_uri}")
```

### 4. Zarządzanie wynikami

Po zakończeniu zadania (`SUCCEEDED`), API wygeneruje plik wyjściowy, również w formacie JSONL. Każda linia będzie zawierać odpowiedź modelu powiązaną z indeksem zapytania.

```
{"response": {"candidates": [{"content": {"parts": [{"text": "Model output..."}]}}]}, "status": "OK"}
```

---

### Zaawansowane uwagi techniczne:

- **Limity rozmiaru:** Pojedynczy plik JSONL może mieć zazwyczaj do 100MB lub zawierać określoną liczbę linii (zależnie od tieru API). Przy 40k znaków na linię (~40KB), jeden plik może bezpiecznie pomieścić około 2000-2500 requestów.
- **Retry Policy:** Batch API ma wbudowany mechanizm retry. Jeśli pojedyncze zapytanie wewnątrz wsadu zawiedzie z powodu błędu tymczasowego (np. przeciążenie serwera), Google spróbuje je powtórzyć bez Twojej ingerencji.
- **Wydajność:** Przetworzenie 1000 plików o rozmiarze 40k znaków zajmie w Batch API znacznie mniej czasu (z perspektywy przepustowości) niż wysyłanie ich sekwencyjnie przez LangChain, ze względu na priorytetyzację w kolejkach offline.

Czy chciałbyś, abym przygotował skrypt, który połączy wyniki z pliku wyjściowego z Twoimi oryginalnymi nazwami plików tekstowych?