#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "markdown",
#   "weasyprint",
# ]
# ///

"""
Konwerter Markdown → PDF
Użycie: uv run md_to_pdf.py plik.md [plik2.md ...] [-o katalog_wyjsciowy]
"""

import argparse
import sys
from pathlib import Path

import markdown
from weasyprint import HTML

CSS = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&family=JetBrains+Mono&display=swap');

body {
    font-family: 'Inter', sans-serif;
    font-size: 14px;
    line-height: 1.5;
    color: #1a1a2e;
    margin: 0;
    padding: 0;
}

h1, h2, h3, h4 {
    color: #16213e;
    margin-top: 0.9em;
    margin-bottom: 0.2em;
}

h1 { font-size: 2em; border-bottom: 3px solid #6c63ff; padding-bottom: 4px; }
h2 { font-size: 1.5em; border-bottom: 1px solid #ddd; padding-bottom: 2px; }
h3 { font-size: 1.2em; }

code {
    font-family: 'JetBrains Mono', monospace;
    background: #f0f0f8;
    padding: 2px 6px;
    border-radius: 4px;
    font-size: 0.88em;
    color: #6c63ff;
}

pre {
    background: #fefefe;
    color: #1a1a2e;
    border: 1px solid #ddd;
    padding: 8px 12px;
    border-radius: 6px;
    overflow-x: auto;
    line-height: 1.4;
    margin: 0.5em 0;
}

pre code {
    background: none;
    color: #1a1a2e;
    padding: 0;
    font-size: 0.85em;
}

blockquote {
    border-left: 4px solid #6c63ff;
    margin: 0.4em 0;
    padding: 4px 12px;
    background: #f5f5ff;
    color: #444;
    border-radius: 0 6px 6px 0;
}

table {
    border-collapse: collapse;
    width: 100%;
    margin: 0.4em 0;
}

th, td {
    border: 1px solid #ddd;
    padding: 8px 12px;
    text-align: left;
}

th {
    background: #6c63ff;
    color: white;
    font-weight: 600;
}

tr:nth-child(even) { background: #f9f9ff; }

a { color: #6c63ff; text-decoration: none; }
a:hover { text-decoration: underline; }

hr { border: none; border-top: 2px solid #eee; margin: 0.8em 0; }

p { margin: 0.3em 0; }

ul, ol { padding-left: 1.4em; margin: 0.2em 0; }
li { margin: 0.1em 0; }

@page {
    margin: 10mm 12mm;
    @bottom-right {
        content: counter(page);
        font-size: 10px;
        color: #999;
    }
}
"""


def convert(md_path: Path, output_dir: Path) -> Path:
    text = md_path.read_text(encoding="utf-8")
    html_body = markdown.markdown(
        text,
        extensions=["tables", "fenced_code", "codehilite", "toc", "nl2br"],
    )
    html = f"""<!DOCTYPE html>
<html lang="pl">
<head>
  <meta charset="UTF-8">
  <style>{CSS}</style>
</head>
<body>
{html_body}
</body>
</html>"""

    output_dir.mkdir(parents=True, exist_ok=True)
    out_path = output_dir / md_path.with_suffix(".pdf").name
    HTML(string=html, base_url=str(md_path.parent)).write_pdf(str(out_path))
    return out_path


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Konwertuje pliki Markdown do PDF (via WeasyPrint).",
    )
    parser.add_argument(
        "files",
        nargs="+",
        metavar="plik.md",
        help="Ścieżki do plików .md do konwersji",
    )
    parser.add_argument(
        "-o", "--output",
        default=".",
        metavar="KATALOG",
        help="Katalog wyjściowy dla plików PDF (domyślnie: bieżący)",
    )
    args = parser.parse_args()

    output_dir = Path(args.output)
    errors = 0

    for raw in args.files:
        path = Path(raw)
        if not path.exists():
            print(f"[BŁĄD] Nie znaleziono pliku: {path}", file=sys.stderr)
            errors += 1
            continue
        if path.suffix.lower() != ".md":
            print(f"[POMINIĘTO] Nie jest plikiem .md: {path}", file=sys.stderr)
            continue
        try:
            out = convert(path, output_dir)
            print(f"[OK] {path} → {out}")
        except Exception as exc:
            print(f"[BŁĄD] {path}: {exc}", file=sys.stderr)
            errors += 1

    sys.exit(errors)


if __name__ == "__main__":
    main()
