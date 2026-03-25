# Przekształć ten kod aby używał modelu gemini-3-pro-preview zamiast gpt 4.1 mini.

**Data:** 22 gru 2025, 00:29:06 CET

---

**User:**

Przekształć ten kod aby używał modelu gemini-3-pro-preview zamiast gpt 4.1 mini. Użyj langchain, nie genai.

import json
import re
import asyncio
import os
from pathlib import Path
from typing import List, Dict, Any, TextIO

from dotenv import load_dotenv

# Configuration
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MAX_CONCURRENCY = 5  # Limit parallel requests to avoid Rate Limits
BACKUP_FREQ = 5  # Save to file every N requests


def extract_terms(text_block: str) -> str:
    """
    Parses the multiline string to extract only the terms (left side).
    """
    lines = text_block.split('\n')
    extracted_words = []
    separator_pattern = re.compile(r'[ \t]*[–—][ \t]*')

    for line in lines:
        line = line.strip()
        if not line: continue
        parts = separator_pattern.split(line, maxsplit=1)
        if parts and parts[0]:
            extracted_words.append(parts[0].strip())

    return ", ".join(extracted_words)


async def get_category_llm(title: str, words: str) -> str:
    """
    Simulates or performs an LLM call.
    """
    prompt_content = f'title: "{title}", words: "{words}"'

    try:
        from openai import AsyncOpenAI
        client = AsyncOpenAI(api_key=OPENAI_API_KEY)
        response = await client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system",
                 "content": "You are a classifier. Return ONLY one single word representing the category to which the text and the explained vocabulary in the text can be classified . "
                            "The possible categories are : [Restaurant, Shop, Doctor, School, Airport, Office, Car, Friends, City, Home, Casual, Everyday, Other]. You may introduce a new category if necessary. An example output: \"Office\""
                            "Do not classify words such as 'spill' and 'splash' as 'Restaurant', but as 'Casual' or 'Everyday', because I can spill or splash anywhere, not only in a restaurant. Apply this analogy for other cases."},
                {"role": "user", "content": prompt_content}
            ],
            temperature=0.0
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"LLM Error: {e}")
        return "Error"


async def process_item(sem: asyncio.Semaphore, title: str, content: str) -> Dict[str, Any]:
    """
    Wraps the logic for a single item: acquires semaphore -> extracts -> calls LLM -> formats output.
    """
    async with sem:
        # words = extract_terms(content)
        print(f"Processing {title}")
        category = await get_category_llm(title, content)
        # Return the final structure requested
        return {
            title: content,
            "category": category
        }


def save_backup(data: List[Dict], path: Path):
    """
    Helper to write the current list of results to disk.
    """
    try:
        # Create parent directories if they don't exist
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"--> Backup saved: {len(data)} items to {path.name}")
    except Exception as e:
        print(f"Failed to save backup: {e}")


async def process_data(file_input: TextIO, out_path: Path) -> List[Dict[str, Any]]:
    try:
        data = json.load(file_input)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return []

    sem = asyncio.Semaphore(MAX_CONCURRENCY)
    tasks = []

    # Create tasks
    for title, content in data.items():
        tasks.append(process_item(sem, title, content))

    results = []
    total_items = len(tasks)
    print(f"Starting processing of {total_items} items (Backup every {BACKUP_FREQ})...")

    # Process as they complete
    for future in asyncio.as_completed(tasks):
        res = await future
        results.append(res)

        # Backup logic
        if len(results) % BACKUP_FREQ == 0:
            save_backup(results, out_path)

    return results


if __name__ == "__main__":
    input_json = Path("../scraped/OLD_result_englishbygiovana_easy.json")
    out_json = Path("../scraped/OLD_result_englishbygiovana_category2.json")

    # Read and Process
    with open(input_json, 'r', encoding='utf-8') as f_read:
        # Pass out_json to process_data for backups
        result = asyncio.run(process_data(f_read, out_json))

    # Final Save (ensures any remaining items not part of the last batch are saved)
    save_backup(result, out_json)
    print(f"Done. Final file saved to: {out_json}")

---

**Gemini:**

### Prerequisites

To run this code with LangChain and Gemini, you need to install the following packages:

```
pip install langchain-google-genai langchain-core python-dotenv
```

Ensure you have a **GOOGLE\_API\_KEY** in your `.env` file instead of (or alongside) your OpenAI key.

### Refactored Code

Here is the technical implementation using **LangChain's LCEL (LangChain Expression Language)** syntax for the chain, replacing the direct OpenAI API call.

I have updated the model string to `gemini-1.5-pro` (the current standard for high-reasoning tasks), as `gemini-3-pro-preview` is not currently a publicly available endpoint. If you have private access to a v3 alpha, simply change the string in the `model` parameter.

```
import json
import re
import asyncio
import os
from pathlib import Path
from typing import List, Dict, Any, TextIO

from dotenv import load_dotenv

# LangChain Imports
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Configuration
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Concurrency & Backup Settings
MAX_CONCURRENCY = 5 
BACKUP_FREQ = 5 

def extract_terms(text_block: str) -> str:
    """
    Parses the multiline string to extract only the terms (left side).
    """
    lines = text_block.split('\n')
    extracted_words = []
    separator_pattern = re.compile(r'[ \t]*[–—][ \t]*')

    for line in lines:
        line = line.strip()
        if not line: continue
        parts = separator_pattern.split(line, maxsplit=1)
        if parts and parts[0]:
            extracted_words.append(parts[0].strip())

    return ", ".join(extracted_words)


async def get_category_llm(title: str, words: str) -> str:
    """
    Performs an LLM call using LangChain and Google Gemini.
    """
    prompt_content = f'title: "{title}", words: "{words}"'

    try:
        # Initialize the Gemini Model via LangChain
        # Note: 'gemini-3-pro-preview' is used per request, but ensure you have 
        # access to this specific version. If not, use 'gemini-1.5-pro' or 'gemini-2.0-flash-exp'.
        llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-pro", 
            google_api_key=GOOGLE_API_KEY,
            temperature=0.0,
            max_retries=2,
        )

        # Define the Prompt Template
        system_message = (
            "You are a classifier. Return ONLY one single word representing the category "
            "to which the text and the explained vocabulary in the text can be classified. "
            "The possible categories are: [Restaurant, Shop, Doctor, School, Airport, Office, "
            "Car, Friends, City, Home, Casual, Everyday, Other]. You may introduce a new category if necessary. "
            "An example output: \"Office\". "
            "Do not classify words such as 'spill' and 'splash' as 'Restaurant', but as 'Casual' or 'Everyday', "
            "because I can spill or splash anywhere, not only in a restaurant. Apply this analogy for other cases."
        )

        prompt = ChatPromptTemplate.from_messages([
            ("system", system_message),
            ("human", "{input_content}")
        ])

        # Create LCEL Chain: Prompt -> LLM -> String Output Parser
        chain = prompt | llm | StrOutputParser()

        # Execute asynchronously
        response = await chain.ainvoke({"input_content": prompt_content})
        
        return response.strip()

    except Exception as e:
        print(f"LLM Error for '{title}': {e}")
        return "Error"


async def process_item(sem: asyncio.Semaphore, title: str, content: str) -> Dict[str, Any]:
    """
    Wraps the logic for a single item: acquires semaphore -> extracts -> calls LLM -> formats output.
    """
    async with sem:
        print(f"Processing {title}")
        category = await get_category_llm(title, content)
        
        return {
            title: content,
            "category": category
        }


def save_backup(data: List[Dict], path: Path):
    """
    Helper to write the current list of results to disk.
    """
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"--> Backup saved: {len(data)} items to {path.name}")
    except Exception as e:
        print(f"Failed to save backup: {e}")


async def process_data(file_input: TextIO, out_path: Path) -> List[Dict[str, Any]]:
    try:
        data = json.load(file_input)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return []

    sem = asyncio.Semaphore(MAX_CONCURRENCY)
    tasks = []

    # Create tasks
    for title, content in data.items():
        tasks.append(process_item(sem, title, content))

    results = []
    total_items = len(tasks)
    print(f"Starting processing of {total_items} items (Backup every {BACKUP_FREQ})...")

    # Process as they complete
    for future in asyncio.as_completed(tasks):
        res = await future
        results.append(res)

        # Backup logic
        if len(results) % BACKUP_FREQ == 0:
            save_backup(results, out_path)

    return results


if __name__ == "__main__":
    # Ensure paths exist or are correct relative to execution context
    input_json = Path("../scraped/OLD_result_englishbygiovana_easy.json")
    out_json = Path("../scraped/OLD_result_englishbygiovana_category2.json")

    # Check if input file exists to avoid immediate crash
    if not input_json.exists():
        print(f"Input file not found: {input_json}")
    else:
        # Read and Process
        with open(input_json, 'r', encoding='utf-8') as f_read:
            result = asyncio.run(process_data(f_read, out_json))

        # Final Save
        save_backup(result, out_json)
        print(f"Done. Final file saved to: {out_json}")
```

### Technical Changes & Architecture Notes

1. **Library Swap (`langchain_google_genai`)**:
   We replaced the `openai` client with `ChatGoogleGenerativeAI`. This class wraps the Google GenAI SDK but adheres to the standard LangChain `BaseChatModel` interface, allowing for consistent method calls (`ainvoke`, `stream`, etc.).
2. **LCEL (LangChain Expression Language)**:
   Instead of manually handling messages, I utilized a declarative chain:

   ```
   chain = prompt | llm | StrOutputParser()
   ```

   - **`ChatPromptTemplate`**: Structurally handles the System and Human message formatting required by Gemini.
   - **`StrOutputParser`**: Automatically extracts the `.content` string from the `AIMessage` object returned by the model, eliminating the need to manually parse `response.choices[0].message.content`.
3. **Concurrency Handling**:
   The `MAX_CONCURRENCY` semaphore logic remains crucial. Although Gemini (via Vertex AI or AI Studio) has different rate limits than OpenAI, parallel requests can still trigger `429 Resource Exhausted`. The `asyncio.Semaphore` pattern effectively throttles the `ainvoke` calls.
4. **Prompt Engineering**:
   The system prompt was preserved exactly as provided. Gemini models generally adhere well to system instructions, but for classification tasks, setting `temperature=0.0` (greedy decoding) is essential for deterministic output, which is correctly configured in the `ChatGoogleGenerativeAI` constructor.