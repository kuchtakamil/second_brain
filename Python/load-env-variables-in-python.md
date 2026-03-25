# Load .env variables in Python

**Data:** 2024-05-20

---

**User:**

In python project I have .env file. How to load variables from .env?

---

**Assistant:**

To load variables from a `.env` file in a Python project, you can use the `python-dotenv` library. First, install the library using pip:

```bash
pip install python-dotenv
```

Then, create a `.env` file in the root directory of your project and add your environment variables in the format `KEY=VALUE`, for example:

```
DATABASE_URL=mysql://user:password@localhost/db_name
SECRET_KEY=my_secret_key
```

Next, in your Python script, you can load these variables using `dotenv`:

```python
from dotenv import load_dotenv
import os

# Load variables from the .env file
load_dotenv()

# Access the variables
database_url = os.getenv("DATABASE_URL")
secret_key = os.getenv("SECRET_KEY")
```

Now, `database_url` and `secret_key` will contain the values specified in your `.env` file. Make sure to add `.env` to your `.gitignore` file if your project is under version control to avoid committing sensitive information.