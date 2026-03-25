# Here is an example json which should be processed  { "In a public space": "in li

**Data:** 2 gru 2025, 00:33:07 CET

---

**User:**

Here is an example json which should be processed

{
"In a public space": "in line / waiting in line – standing in a line with other people, waiting your turn for service.\ncut the line / cut in line – move ahead of others in a line and take a place you haven't waited for.\ncashier – the store employee who scans items and handles customers' payments.\nimpolite – behaving rudely or without good manners.",
"Taking a taxi/Uber 🚕": "- hop on in – an informal way to tell someone to quickly get into a car.  \n- get in the car – a neutral message to enter the car.  \n- ride pool / ridepool – a shared ride where other people may be picked up and the cost is shared.  \n- lean back and relax – sit back and do not worry about anything.",
"Ordering pizza in your second language 🍕": "can i have — a polite way to ask for or order something.  \ncrust — the pizza’s base and outer edge that holds the toppings.  \nstuffed crust — a crust whose edge is filled (usually with cheese) so it has a filling inside.  \ncheese crust — a crust that has extra cheese on the edge.  \nsoft crust — a crust that is soft and not very crisp.  \nsimple crust / classic crust — a plain, basic crust without added fillings or extra toppings.  \nin a few minutes — very soon; in a short time.  \nI'll bring your order — I will bring or serve your food to you.",
"Milking the cow? 🐮 🥛": "milk (animal) – the pale, nutrient-rich fluid mammals produce to feed their young.  \nmilk (plant) – a pale liquid made from plants (e.g., almonds, soy) used as a dairy alternative.  \nto milk (extract) – to draw milk from an animal, such as milking a cow by hand or machine.  \nto milk (exploit) – to squeeze as much benefit, information, or value as possible out of something.",
"Complimenting someone on the street 👚": "T-shirt — a casual, short-sleeved knit shirt with a simple crew or V neckline.\n\nasymmetrical top — a blouse whose cut or edge is on purpose uneven or lopsided for a stylish effect.\n\noff-the-shoulder top — a top designed to sit below the shoulders so the shoulders and upper chest are exposed.\n\nfuzzy socks — soft socks made from thick, fluffy material for extra warmth and comfort.",
"Trying to buy a bag 👛👜Shopping Vocabulary": "purse – a small handbag for carrying personal items like a wallet, phone, and keys.  \ncrossbody bag – a bag with a long strap worn across the body from one shoulder to the opposite hip.  \ntote – a large, open-top bag with two handles made to carry many things or shopping.  \nclutch (box clutch) – a small bag without a strap for use in the evening; a box clutch is a hard, box-shaped version."
}


I want to add a category property for each line. So the struct of json has to be changed. I will provide a struct at the end of the prompt.
Category should be established by LLM. LLM will receive a key and only the parts of the values. 
From values only the defined words should be send. The definitions should be skiped

So for the line
"In a public space": "in line / waiting in line – standing in a line with other people, waiting your turn for service.\ncut the line / cut in line – move ahead of others in a line and take a place you haven't waited for.\ncashier – the store employee who scans items and handles customers' payments.\nimpolite – behaving rudely or without good manners.",

this should be sent to LLM
title: "In a public space", words: "in line / waiting in line, cut the line / cut in line, cashier, impolite"

For this line 
"Taking a taxi/Uber 🚕": "- hop on in – an informal way to tell someone to quickly get into a car.  \n- get in the car – a neutral message to enter the car.  \n- ride pool / ridepool – a shared ride where other people may be picked up and the cost is shared.  \n- lean back and relax – sit back and do not worry about anything.",

this should be sent to LLM:
title:"Taking a taxi/Uber 🚕", words:"- hop on in, - get in the car, - ride pool / ridepool, - lean back and relax",

Look out because the words can start with short dash. 
But the definitions which we want to skip start always after a long dash. 

LLM should return only a one word for each line - a value of a category. 
The the program shhould create a new json file with a new structure. Of course the definitions have to be there in the right place.

Here is an output for the example json from the beginning:
[
{
"In a public space": "in line / waiting in line – standing in a line with other people, waiting your turn for service.\ncut the line / cut in line – move ahead of others in a line and take a place you haven't waited for.\ncashier – the store employee who scans items and handles customers' payments.\nimpolite – behaving rudely or without good manners.", category: "Shop",
},
{
"Taking a taxi/Uber 🚕": "- hop on in – an informal way to tell someone to quickly get into a car.  \n- get in the car – a neutral message to enter the car.  \n- ride pool / ridepool – a shared ride where other people may be picked up and the cost is shared.  \n- lean back and relax – sit back and do not worry about anything.", category: "Taxi",
},
{
"Ordering pizza in your second language 🍕": "can i have — a polite way to ask for or order something.  \ncrust — the pizza’s base and outer edge that holds the toppings.  \nstuffed crust — a crust whose edge is filled (usually with cheese) so it has a filling inside.  \ncheese crust — a crust that has extra cheese on the edge.  \nsoft crust — a crust that is soft and not very crisp.  \nsimple crust / classic crust — a plain, basic crust without added fillings or extra toppings.  \nin a few minutes — very soon; in a short time.  \nI'll bring your order — I will bring or serve your food to you.", category: "Restaurant",
},
{
"Milking the cow? 🐮 🥛": "milk (animal) – the pale, nutrient-rich fluid mammals produce to feed their young.  \nmilk (plant) – a pale liquid made from plants (e.g., almonds, soy) used as a dairy alternative.  \nto milk (extract) – to draw milk from an animal, such as milking a cow by hand or machine.  \nto milk (exploit) – to squeeze as much benefit, information, or value as possible out of something.", category: "Casual"
},
{
"Complimenting someone on the street 👚": "T-shirt — a casual, short-sleeved knit shirt with a simple crew or V neckline.\n\nasymmetrical top — a blouse whose cut or edge is on purpose uneven or lopsided for a stylish effect.\n\noff-the-shoulder top — a top designed to sit below the shoulders so the shoulders and upper chest are exposed.\n\nfuzzy socks — soft socks made from thick, fluffy material for extra warmth and comfort.", category: "Clothes"
},
{
"Trying to buy a bag 👛👜Shopping Vocabulary": "purse – a small handbag for carrying personal items like a wallet, phone, and keys.  \ncrossbody bag – a bag with a long strap worn across the body from one shoulder to the opposite hip.  \ntote – a large, open-top bag with two handles made to carry many things or shopping.  \nclutch (box clutch) – a small bag without a strap for use in the evening; a box clutch is a hard, box-shaped version.", category: "Clothes"
}
]
Writhe a python script

---

**Gemini:**

Here is a complete Python script that processes the JSON, parses the text using regular expressions to distinguish between hyphens and long dashes, and structures the data as requested.

To make this script immediately executable, I have included a **mock LLM function**. I also provided the implementation for a real **OpenAI API** call, which you can enable by setting the `USE_REAL_LLM` flag to `True` and providing an API key.

```
import json
import re
import asyncio
import os
from typing import List, Dict, Any

# Configuration
USE_REAL_LLM = False  # Set to True to use OpenAI API
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Input Data
input_json = """
{
"In a public space": "in line / waiting in line – standing in a line with other people, waiting your turn for service.\\ncut the line / cut in line – move ahead of others in a line and take a place you haven't waited for.\\ncashier – the store employee who scans items and handles customers' payments.\\nimpolite – behaving rudely or without good manners.",
"Taking a taxi/Uber 🚕": "- hop on in – an informal way to tell someone to quickly get into a car. \\n- get in the car – a neutral message to enter the car. \\n- ride pool / ridepool – a shared ride where other people may be picked up and the cost is shared. \\n- lean back and relax – sit back and do not worry about anything.",
"Ordering pizza in your second language 🍕": "can i have — a polite way to ask for or order something. \\ncrust — the pizza’s base and outer edge that holds the toppings. \\nstuffed crust — a crust whose edge is filled (usually with cheese) so it has a filling inside. \\ncheese crust — a crust that has extra cheese on the edge. \\nsoft crust — a crust that is soft and not very crisp. \\nsimple crust / classic crust — a plain, basic crust without added fillings or extra toppings. \\nin a few minutes — very soon; in a short time. \\nI'll bring your order — I will bring or serve your food to you.",
"Milking the cow? 🐮 🥛": "milk (animal) – the pale, nutrient-rich fluid mammals produce to feed their young. \\nmilk (plant) – a pale liquid made from plants (e.g., almonds, soy) used as a dairy alternative. \\nto milk (extract) – to draw milk from an animal, such as milking a cow by hand or machine. \\nto milk (exploit) – to squeeze as much benefit, information, or value as possible out of something.",
"Complimenting someone on the street 👚": "T-shirt — a casual, short-sleeved knit shirt with a simple crew or V neckline.\\n\\nasymmetrical top — a blouse whose cut or edge is on purpose uneven or lopsided for a stylish effect.\\n\\noff-the-shoulder top — a top designed to sit below the shoulders so the shoulders and upper chest are exposed.\\n\\nfuzzy socks — soft socks made from thick, fluffy material for extra warmth and comfort.",
"Trying to buy a bag 👛👜Shopping Vocabulary": "purse – a small handbag for carrying personal items like a wallet, phone, and keys. \\ncrossbody bag – a bag with a long strap worn across the body from one shoulder to the opposite hip. \\ntote – a large, open-top bag with two handles made to carry many things or shopping. \\nclutch (box clutch) – a small bag without a strap for use in the evening; a box clutch is a hard, box-shaped version."
}
"""

def extract_terms(text_block: str) -> str:
    """
    Parses the multiline string to extract only the terms (left side).
    It looks for En-dash (\u2013) or Em-dash (\u2014) as separators.
    It preserves the Hyphen-minus (\u002D) if it appears at the start of the word.
    """
    lines = text_block.split('\n')
    extracted_words = []

    # Regex pattern: looks for spaces surrounding an en-dash or em-dash.
    # [ \t]* matches optional whitespace
    # [–—] matches the specific unicode dashes
    separator_pattern = re.compile(r'[ \t]*[–—][ \t]*')

    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Split only on the first occurrence of the separator
        parts = separator_pattern.split(line, maxsplit=1)
        
        if parts and parts[0]:
            extracted_words.append(parts[0].strip())

    return ", ".join(extracted_words)

async def get_category_llm(title: str, words: str) -> str:
    """
    Simulates or performs an LLM call to categorize the input.
    """
    prompt_content = f'title: "{title}", words: "{words}"'
    
    if USE_REAL_LLM:
        try:
            from openai import AsyncOpenAI
            client = AsyncOpenAI(api_key=OPENAI_API_KEY)
            
            response = await client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a classifier. Return ONLY one single word representing the category (e.g., Shop, Taxi, Restaurant). Do not use punctuation."},
                    {"role": "user", "content": prompt_content}
                ],
                temperature=0.0
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"LLM Error: {e}")
            return "Error"
    else:
        # Mock logic for demonstration purposes (Deterministic heuristics)
        title_lower = title.lower()
        if "taxi" in title_lower: return "Taxi"
        if "pizza" in title_lower: return "Restaurant"
        if "cow" in title_lower: return "Casual"
        if "bag" in title_lower or "complimenting" in title_lower: return "Clothes"
        if "public space" in title_lower: return "Shop"
        return "General"

async def process_data(json_str: str) -> List[Dict[str, Any]]:
    data = json.loads(json_str)
    tasks = []
    keys = []
    
    # 1. Prepare tasks for async processing
    for title, content in data.items():
        words = extract_terms(content)
        keys.append(title)
        tasks.append(get_category_llm(title, words))
    
    # 2. Run LLM calls concurrently
    categories = await asyncio.gather(*tasks)
    
    # 3. Construct the new JSON structure
    output_structure = []
    for title, category in zip(keys, categories):
        original_content = data[title]
        
        # Create dictionary with dynamic key + category
        entry = {
            title: original_content,
            "category": category
        }
        output_structure.append(entry)
        
    return output_structure

# Execution
if __name__ == "__main__":
    result = asyncio.run(process_data(input_json))
    
    # Print formatted JSON output
    print(json.dumps(result, indent=4, ensure_ascii=False))
```

### Key Technical Details

1. **Regex Parsing (`extract_terms`)**:

   - The script distinguishes between the "short dash" (Hyphen-minus `-` used in lists like `- hop on in`) and the "long dashes" used for definitions.
   - It strictly targets the **En-dash** (`–` / `\u2013`) and **Em-dash** (`—` / `\u2014`) as delimiters.
   - `re.split(..., maxsplit=1)` ensures that if a definition contains another dash later on, the line isn't split incorrectly; we only care about the separation between the word and the definition.
2. **Asynchronous Processing (`asyncio`)**:

   - Categorizing items via an LLM is an I/O-bound operation. Processing them sequentially would be inefficient.
   - The script uses `asyncio.gather` to send all prompts to the LLM (or mock function) concurrently, significantly reducing execution time when scaling to larger JSON files.
3. **Data Structure Transformation**:

   - The input is a `Dict`, but the requested output is a `List` of dictionaries.
   - The script constructs the specific non-standard dictionary format requested: `{ "KeyName": "Value", "category": "Value" }`.

### Expected Output

Running the script provided above will generate the following JSON:

```
[
    {
        "In a public space": "in line / waiting in line – standing in a line with other people, waiting your turn for service.\ncut the line / cut in line – move ahead of others in a line and take a place you haven't waited for.\ncashier – the store employee who scans items and handles customers' payments.\nimpolite – behaving rudely or without good manners.",
        "category": "Shop"
    },
    {
        "Taking a taxi/Uber 🚕": "- hop on in – an informal way to tell someone to quickly get into a car. \n- get in the car – a neutral message to enter the car. \n- ride pool / ridepool – a shared ride where other people may be picked up and the cost is shared. \n- lean back and relax – sit back and do not worry about anything.",
        "category": "Taxi"
    },
    {
        "Ordering pizza in your second language 🍕": "can i have — a polite way to ask for or order something. \ncrust — the pizza’s base and outer edge that holds the toppings. \nstuffed crust — a crust whose edge is filled (usually with cheese) so it has a filling inside. \ncheese crust — a crust that has extra cheese on the edge. \nsoft crust — a crust that is soft and not very crisp. \nsimple crust / classic crust — a plain, basic crust without added fillings or extra toppings. \nin a few minutes — very soon; in a short time. \nI'll bring your order — I will bring or serve your food to you.",
        "category": "Restaurant"
    },
    {
        "Milking the cow? 🐮 🥛": "milk (animal) – the pale, nutrient-rich fluid mammals produce to feed their young. \nmilk (plant) – a pale liquid made from plants (e.g., almonds, soy) used as a dairy alternative. \nto milk (extract) – to draw milk from an animal, such as milking a cow by hand or machine. \nto milk (exploit) – to squeeze as much benefit, information, or value as possible out of something.",
        "category": "Casual"
    },
    {
        "Complimenting someone on the street 👚": "T-shirt — a casual, short-sleeved knit shirt with a simple crew or V neckline.\n\nasymmetrical top — a blouse whose cut or edge is on purpose uneven or lopsided for a stylish effect.\n\noff-the-shoulder top — a top designed to sit below the shoulders so the shoulders and upper chest are exposed.\n\nfuzzy socks — soft socks made from thick, fluffy material for extra warmth and comfort.",
        "category": "Clothes"
    },
    {
        "Trying to buy a bag 👛👜Shopping Vocabulary": "purse – a small handbag for carrying personal items like a wallet, phone, and keys. \ncrossbody bag – a bag with a long strap worn across the body from one shoulder to the opposite hip. \ntote – a large, open-top bag with two handles made to carry many things or shopping. \nclutch (box clutch) – a small bag without a strap for use in the evening; a box clutch is a hard, box-shaped version.",
        "category": "Clothes"
    }
]
```