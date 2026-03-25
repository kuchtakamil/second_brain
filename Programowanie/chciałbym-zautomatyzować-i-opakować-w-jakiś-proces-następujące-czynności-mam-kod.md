# Chciałbym zautomatyzować i opakować w jakiś proces następujące czynności.  Mam k

**Data:** 22 lis 2025, 11:15:33 CET

---

**User:**

Chciałbym zautomatyzować i opakować w jakiś proces następujące czynności. 
Mam kod w python który robi scraping określonych shortów z youtube, procesuje ich subtitles za pomocą OpenAI API i zapisuje wynik w pliku json.
Później chcę generować obrazki do tych wyników przy pomocy nano banana, a na końcu sklejać to w jeden PDF.
Zaproponuj stack technologiczny - może jakiś AI Pipeline - do tego celu.

---

**Gemini:**

Biorąc pod uwagę istniejący kod Python oraz potrzebę skalowalności, obsługi błędów i integracji modeli generatywnych, proponuję architekturę opartą na **nowoczesnym orkiestratorze przepływu danych (Data/AI Orchestrator)**. Zamiast prostego skryptu, należy zbudować pipeline, który obsłuży asynchroniczność (generowanie obrazów trwa) oraz potencjalne awarie (błędy API, limity rate-limit).

Oto propozycja profesjonalnego stacku technologicznego "AI Pipeline":

### 1. Architektura Rozwiązania

System podzielimy na 4 logiczne warstwy:

- **Orchestration Layer:** Zarządzanie stanem, retry policy, logowanie.
- **Ingestion & NLP Layer:** Twój obecny kod (Scraping + OpenAI).
- **Generative Media Layer:** Równoległe generowanie grafik (Banana.dev).
- **Presentation Layer:** Składanie raportu PDF.

### 2. Rekomendowany Stack Technologiczny

| Komponent | Technologia | Uzasadnienie techniczne |
| --- | --- | --- |
| **Orchestrator** | **Prefect** (v3) | Python-native workflow engine. Pozwala zamienić funkcje Python w "Tasks" z wbudowaną obsługą asynchroniczności, cache'owania i ponawiania prób (retries). Jest lżejszy niż Airflow i idealny do AI pipelines. |
| **NLP & Logic** | **LangChain** + **Pydantic** | LangChain do zarządzania promptami. Pydantic do wymuszenia ścisłej struktury JSON z OpenAI (Structured Outputs), co jest krytyczne dla dalszych kroków pipeline'u. |
| **Image Gen** | **Banana.dev** (Serverless GPU) | Jeśli masz własny model (np. SDXL/Flux) na Banana, to najlepszy wybór kosztowy. Umożliwia skalowanie do zera, gdy pipeline nie działa. |
| **PDF Engine** | **WeasyPrint** + **Jinja2** | Podejście "HTML-first". Zamiast rysować PDF liniami kodu (jak w ReportLab), generujesz HTML z CSS za pomocą Jinja2, a WeasyPrint renderuje to do PDF. To pozwala na łatwe stylowanie i debugowanie layoutu w przeglądarce. |
| **Environment** | **Docker** | Konteneryzacja całego procesu, aby uniknąć problemów z zależnościami (szczególnie biblioteki systemowe dla WeasyPrint). |

---

### 3. Implementacja Pipeline (Prefect Flow)

Poniżej znajduje się szkielet implementacji w języku Python, wykorzystujący `Prefect` do zarządzania przepływem oraz `asyncio` do równoległego generowania obrazów, co drastycznie przyspieszy proces.

#### `requirements.txt`

```
prefect>=3.0.0
openai
langchain
requests
jinja2
weasyprint
yt-dlp
pydantic
```

#### `pipeline.py`

```
import asyncio
import json
from typing import List
from datetime import timedelta

from prefect import flow, task
from pydantic import BaseModel, Field
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
import requests

# --- Data Structures ---
class SceneData(BaseModel):
    timestamp: str
    description: str
    image_prompt: str
    image_url: str = None

class VideoAnalysis(BaseModel):
    video_id: str
    title: str
    scenes: List[SceneData]

# --- Tasks ---

@task(retries=3, retry_delay_seconds=10, log_prints=True)
def scrape_and_analyze_video(video_url: str) -> VideoAnalysis:
    """
    Wraps your existing logic. 
    1. Uses yt-dlp to get subtitles/audio.
    2. Sends to OpenAI to analyze and extract scene descriptions + prompts.
    Returns a structured Pydantic object.
    """
    print(f"Processing video: {video_url}")
    
    # ... existing logic for scraping ...
    # ... OpenAI API call with structured output ...
    
    # MOCK RETURN for demonstration
    return VideoAnalysis(
        video_id="dQw4w9WgXcQ",
        title="Sample Short Analysis",
        scenes=[
            SceneData(timestamp="00:05", description="Intro scene", image_prompt="Cyberpunk city at night, neon lights"),
            SceneData(timestamp="00:15", description="Action shot", image_prompt="Robot running fast, motion blur")
        ]
    )

@task(retries=2)
async def generate_image_banana(prompt: str, model_key: str, api_key: str) -> str:
    """
    Calls Banana.dev API asynchronously.
    """
    url = "https://api.banana.dev/start/v4/"
    payload = {
        "apiKey": api_key,
        "modelKey": model_key,
        "modelInputs": {"prompt": prompt, "num_inference_steps": 30}
    }
    
    # Use aiohttp here for true async in production
    # Simulating response for structure
    print(f"Requesting image for: {prompt[:20]}...")
    
    # Implement polling logic or await result depending on Banana model configuration
    # ...
    
    mock_image_url = f"https://via.placeholder.com/512?text={prompt.replace(' ', '+')}"
    return mock_image_url

@task
def compile_pdf(analysis: VideoAnalysis, output_filename: str):
    """
    Renders HTML via Jinja2 and converts to PDF using WeasyPrint.
    """
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template('report_template.html')
    
    html_content = template.render(
        title=analysis.title,
        video_id=analysis.video_id,
        scenes=analysis.scenes
    )
    
    HTML(string=html_content).write_pdf(output_filename)
    print(f"PDF generated: {output_filename}")

# --- Main Flow ---

@flow(name="YouTube Shorts to PDF Pipeline")
async def main_pipeline(video_urls: List[str]):
    banana_api_key = "YOUR_KEY"
    banana_model_key = "YOUR_MODEL"

    for url in video_urls:
        # 1. Scrape and Analyze
        analysis_data = scrape_and_analyze_video(url)
        
        # 2. Generate Images in Parallel (Map/Gather pattern)
        # We extract prompts and create a list of async tasks
        prompts = [scene.image_prompt for scene in analysis_data.scenes]
        
        # Use asyncio.gather to hit Banana API concurrently
        image_urls = await asyncio.gather(
            *[generate_image_banana(p, banana_model_key, banana_api_key) for p in prompts]
        )
        
        # 3. Update Data Structure
        for scene, img_url in zip(analysis_data.scenes, image_urls):
            scene.image_url = img_url
            
        # 4. Compile PDF
        output_file = f"report_{analysis_data.video_id}.pdf"
        compile_pdf(analysis_data, output_file)

if __name__ == "__main__":
    asyncio.run(main_pipeline(["https://youtu.be/sample_short"]))
```

### 4. Szablon HTML (Jinja2)

Aby `WeasyPrint` zadziałał poprawnie, potrzebujesz pliku `report_template.html` w tym samym katalogu. To podejście pozwala na pełną kontrolę nad typografią i układem (Grid/Flexbox działają w PDF).

```
<!DOCTYPE html>
<html>
<head>
    <style>
        @page { size: A4; margin: 2cm; }
        body { font-family: 'Helvetica', sans-serif; color: #333; }
        h1 { color: #2c3e50; border-bottom: 2px solid #eee; }
        .scene-card {
            display: flex;
            margin-bottom: 20px;
            page-break-inside: avoid; /* Prevents splitting card across pages */
            border: 1px solid #ddd;
            padding: 10px;
        }
        .scene-img { width: 150px; height: 150px; object-fit: cover; margin-right: 15px; }
        .scene-info { flex: 1; }
        .timestamp { font-weight: bold; color: #e74c3c; }
    </style>
</head>
<body>
    <h1>Video Report: {{ title }}</h1>
    <p>ID: {{ video_id }}</p>
    
    {% for scene in scenes %}
    <div class="scene-card">
        <img src="{{ scene.image_url }}" class="scene-img"/>
        <div class="scene-info">
            <div class="timestamp">{{ scene.timestamp }}</div>
            <p>{{ scene.description }}</p>
            <small><i>Prompt: {{ scene.image_prompt }}</i></small>
        </div>
    </div>
    {% endfor %}
</body>
</html>
```

### 5. Kluczowe wyzwania techniczne i rozwiązania

1. **Structured Outputs (JSON Stability):**
   Modele LLM bywają kapryśne przy zwracaniu JSON. Użyj metody `client.beta.chat.completions.parse()` z biblioteki OpenAI w połączeniu z klasami `Pydantic`. To gwarantuje, że struktura danych przekazywana do generatora obrazków będzie zawsze poprawna (schema validation).
2. **Cold Starts na Banana.dev:**
   Jeśli używasz serverless GPU, pierwszy request może trwać 30-60 sekund (ładowanie modelu do VRAM).

   - *Rozwiązanie:* W kodzie produkcyjnym warto zaimplementować "ping" rozgrzewający lub użyć parametru `keep_alive` jeśli pipeline przetwarza serię filmów jeden po drugim.
3. **Rate Limiting & Concurrency:**
   Uruchomienie 50 requestów na raz do Banana.dev może wyczerpać dostępne repliki.

   - *Rozwiązanie:* W Prefect możesz użyć `TaskConcurrencyLimit`. W czystym Pythonie użyj `asyncio.Semaphore(5)`, aby ograniczyć liczbę jednoczesnych żądań generowania obrazu do np. 5.
4. **Zależności systemowe WeasyPrint:**
   WeasyPrint wymaga bibliotek systemowych takich jak `libpango` czy `libcairo`.

   - *Rozwiązanie:* Dockerfile musi zawierać odpowiednie instrukcje instalacji (dla Debiana/Ubuntu):

   ```
   RUN apt-get update && apt-get install -y build-essential python3-dev python3-pip python3-setuptools python3-wheel python3-cffi libcairo2 libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf2.0-0 libffi-dev shared-mime-info
   ```

### Next Step

Jeśli chcesz, mogę przygotować szczegółową implementację klasy `Pydantic` dla strukturyzowanego wyjścia OpenAI (Function Calling/JSON Mode), która będzie odporna na błędy parsowania napisów z YouTube.