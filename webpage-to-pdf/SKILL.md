---
name: webpage-to-pdf
description: Convert a webpage URL into a clean, ad-free PDF using Playwright. Use this skill whenever the user wants to save a webpage, article, or URL as a PDF, especially when they mention wanting to remove ads, sidebars, or keep only the main content.
---

# Webpage to PDF Converter

This skill allows you to convert a webpage to a clean PDF by running a bundled Python script that uses Playwright.

## Prerequisites

Playwright and its Chromium browser must be installed in the python environment. 
If not installed, run: `pip install playwright && playwright install chromium`

## Usage

When the user asks to save a webpage as a PDF, run the bundled `generate_pdf.py` script.

Command:
```powershell
python scripts/generate_pdf.py "<URL>" "<OUTPUT_PDF_PATH>"
```

- `<URL>`: The URL of the webpage to convert.
- `<OUTPUT_PDF_PATH>`: The absolute path where the PDF should be saved (e.g., the user's desktop).

The script automatically:
1. Scrolls the page to trigger lazy-loaded images.
2. Hides common ad/sidebar/header classes using CSS.
3. Renders the clean page to a PDF.
