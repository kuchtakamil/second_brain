# how many concurrent requests are run in the code?

**Data:** 6 gru 2025, 21:44:29 CET

---

**User:**

how many concurrent requests are run in the code?

---

**Gemini:**

In the current code, the number of concurrent requests is **unlimited** and exactly equals the **total number of items (keys) in your input JSON file**.

### Why?

The code performs the following steps:

1. Iterates through **every** item in `data.items()`.
2. Creates a coroutine object for each item and adds it to the `tasks` list.
3. Calls `await asyncio.gather(*tasks)`, which schedules **all** tasks in that list to run on the event loop simultaneously.

### The Risk (Rate Limiting)

If your input JSON contains 5 items, it will run 5 concurrent requests. However, if it contains **1,000 items**, it will attempt to open **1,000 connections simultaneously**.

This usually leads to `429 Too Many Requests` errors from APIs like OpenAI.

### Recommendation: Add a Semaphore

To prevent hitting API rate limits, you should limit the concurrency (e.g., to 5 or 10 parallel requests) using `asyncio.Semaphore`.

Here is how to modify the `get_category_llm` function to respect a limit:

```
# Initialize a semaphore with a limit (e.g., 5 concurrent requests)
sem = asyncio.Semaphore(5)

async def get_category_llm(title: str, words: str) -> str:
    # Acquire a "permit" before running the logic
    async with sem:
        prompt_content = f'title: "{title}", words: "{words}"'
        
        if USE_REAL_LLM:
            # ... existing OpenAI logic ...
            pass
        else:
            # ... existing mock logic ...
            pass
```

Alternatively, you can pass the semaphore into the function if you don't want it as a global variable.