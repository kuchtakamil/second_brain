# add functionality to backup the result every 5 requests

**Data:** 6 gru 2025, 21:47:04 CET

---

**User:**

add functionality to backup the result every 5 requests

---

**Gemini:**

Here is the updated Python script.

To implement the backup functionality effectively, I made the following changes:

1. **Added a `process_item` wrapper**: This function handles the logic for a single item (extraction + LLM call) and returns the fully formed dictionary entry.
2. **Added `asyncio.Semaphore`**: Included a limit (set to 5) to control concurrency, which prevents API rate limits and works well with the batch saving.
3. **Used `asyncio.as_completed`**: Instead of waiting for all tasks to finish at once, this processes them as they finish.
4. **Added Backup Logic**: Inside the completion loop, it checks if the number of processed items is a multiple of `BACKUP_FREQ` (5) and writes the current results to the file.

```
import json
import re
import asyncio
import os
from pathlib import Path
from typing import List, Dict, Any, TextIO

# Configuration
USE_REAL_LLM = False
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MAX_CONCURRENCY = 5  # Limit parallel requests to avoid Rate Limits
BACKUP_FREQ = 5      # Save to file every N requests

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
    
    if USE_REAL_LLM:
        try:
            from openai import AsyncOpenAI
            client = AsyncOpenAI(api_key=OPENAI_API_KEY)
            response = await client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a classifier. Return ONLY one single word representing the category. Do not use punctuation."},
                    {"role": "user", "content": prompt_content}
                ],
                temperature=0.0
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"LLM Error: {e}")
            return "Error"
    else:
        # Mock logic
        await asyncio.sleep(0.5) # Simulate network delay
        title_lower = title.lower()
        if "taxi" in title_lower: return "Taxi"
        if "pizza" in title_lower: return "Restaurant"
        if "cow" in title_lower: return "Casual"
        if "bag" in title_lower or "complimenting" in title_lower: return "Clothes"
        if "public space" in title_lower: return "Shop"
        return "General"

async def process_item(sem: asyncio.Semaphore, title: str, content: str) -> Dict[str, Any]:
    """
    Wraps the logic for a single item: acquires semaphore -> extracts -> calls LLM -> formats output.
    """
    async with sem:
        words = extract_terms(content)
        category = await get_category_llm(title, words)
        
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
    out_json = Path("../scraped/OLD_result_englishbygiovana_category.json")
    
    # Create dummy file if not exists (for testing)
    if not input_json.exists():
        input_json.parent.mkdir(parents=True, exist_ok=True)
        # Create enough data to trigger a backup
        dummy_data = {f"Item {i}": f"word – def" for i in range(1, 12)}
        with open(input_json, 'w', encoding='utf-8') as f:
            json.dump(dummy_data, f, ensure_ascii=False, indent=4)

    # Read and Process
    with open(input_json, 'r', encoding='utf-8') as f_read:
        # Pass out_json to process_data for backups
        result = asyncio.run(process_data(f_read, out_json))

    # Final Save (ensures any remaining items not part of the last batch are saved)
    save_backup(result, out_json)
    print(f"Done. Final file saved to: {out_json}")
```