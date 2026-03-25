# Use lib functions solution.

**Data:** 2024-05-20

---

**User:**

I have the following directory structure
├── lib
│   ├── get_model.py
│   ├── handle_task.py
│   ├── openai_utilities.py
│   ├── __pycache__
│   │   └── handle_task.cpython-310.pyc
│   └── utilities.py
├── openai_models
│   └── model_list.json
├── README.md
├── requirements.txt
├── solutions
│   ├── C01L01_helloapi.py
│   ├── C01L04_blogger.py
│   ├── C01L04_moderation.py
│   ├── C01L05_liar.py
│   ├── C02L02_inprompt.py
│   ├── C02L03_embedding.py
│   ├── C02L04_whisper.py
│   ├── C02L05_functions.py
│   ├── C03L01_rodo.py
│   ├── C03L02_scraper.py
│   ├── C03L03_whoami.py
│   ├── C03L04_search.py
│   ├── C03L05_people.py
│   ├── C04L01_knowledge.py
│   ├── C04L02_tools.py
│   ├── C04L03_gnome.py
│   ├── C04L04_ownapi.py
│   ├── C04L05_ownapipro
│   │   └── ownapi.py
│   ├── C04L05_ownapipro.py
│   ├── C05L01_meme.py
│   ├── C05L02_optimaldb.py
│   ├── C05L03_google
│   │   └── ownapi.py
│   ├── C05L03_google.py
│   ├── C05L04_md2html
│   │   ├── data_set.jsonl
│   │   └── fine_tuning.py
│   └── C05L04_md2html.py
I want to open a terminal for example in "solutions" directory and run some Python code and use functions from handle_task.py. Can I do it, if so... how.

---

**Assistant:**

Yes, you can run Python code from the `solutions` directory and use functions from `handle_task.py` located in the `lib` directory. To do this, you need to make sure Python can find the `lib` directory so it can import the necessary modules. Here are the steps:

1. **Navigate to the `solutions` directory:**
   Open a terminal and navigate to the `solutions` directory:
   ```sh
   cd path/to/your/project/solutions
   ```

2. **Set the `PYTHONPATH` environment variable:**
   You need to add the `lib` directory to the `PYTHONPATH` so that Python knows where to find `handle_task.py`. You can do this in two ways:

   **Temporary method:**
   ```sh
   export PYTHONPATH=$PYTHONPATH:../lib
   ```

   **Permanent method (only for the current script):**
   Add the following lines at the beginning of your Python script:
   ```python
   import sys
   import os
   sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../lib')))
   ```

3. **Import the necessary module in your script:**
   Now you can import `handle_task` in your script:
   ```python
   import handle_task

   # Now you can use functions from handle_task
   result = handle_task.some_function()
   print(result)
   ```

Here's an example of how you can create and run a script from the `solutions` directory that uses functions from `handle_task.py`.

### Example Script: `use_handle_task.py`
Save this script in the `solutions` directory:
```python
import sys
import os

# Append the lib directory to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../lib')))

# Now import the handle_task module
import handle_task

# Use a function from handle_task
result = handle_task.some_function()
print(result)
```

### Run the Script
In your terminal, navigate to the `solutions` directory and run the script:
```sh
python use_handle_task.py
```

This setup ensures that Python can locate the `lib` directory and import `handle_task.py` correctly.