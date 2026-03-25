# podaj co ma się znaleźć w requirements.txt

**Data:** 17 gru 2025, 22:10:54 CET

---

**User:**

podaj co ma się znaleźć w requirements.txt

---

**Gemini:**

Based on the Python code provided in the previous step, your `requirements.txt` file must contain the following external packages.

### `requirements.txt`

```
EbookLib
beautifulsoup4
```

### Technical Explanation of Dependencies

1. **`EbookLib`**:

   - **Import in code:** `import ebooklib`, `from ebooklib import epub`
   - **Purpose:** Handles the reading and parsing of the `.epub` container format (ZIP archive structure, OPF manifest, NCX table of contents).
   - **Note:** This library handles the low-level extraction of the raw HTML content items from the book structure.
2. **`beautifulsoup4`**:

   - **Import in code:** `from bs4 import BeautifulSoup`
   - **Purpose:** Parses the extracted HTML/XHTML content. It traverses the DOM tree to locate tags (like `<h1>`, `<p>`), manipulate them (clean headers), and extract plain text.
   - **Note:** The package name on PyPI is `beautifulsoup4`, even though the import name is `bs4`.

### Recommended Additions (Production Grade)

While the code explicitly uses `html.parser` (which is built into Python's standard library), for high-performance parsing or handling malformed XML often found in ebooks, it is industry standard to use `lxml` as the parser backend.

If you plan to process many files or require strict XML adherence, add `lxml` and update the `BeautifulSoup` constructor in the code to `BeautifulSoup(html_content, 'lxml')`.

**Updated `requirements.txt` for production:**

```
EbookLib>=0.17.1
beautifulsoup4>=4.12.0
lxml>=4.9.0
```

### How to install

To install these dependencies in your current environment, run:

```
pip install -r requirements.txt
```

To generate this file automatically based on your currently installed packages (frozen versions), use:

```
pip freeze > requirements.txt
```

Would you like me to update the Python script to use `lxml` instead of `html.parser` for better performance?