"""
DX Certification Portal Scraper - Data Extraction Only
========================================================
Downloads and extracts text from DX certification application documents.
Outputs a JSON file with company metadata + document full text for
downstream semantic analysis by an LLM agent.

This script is intentionally "dumb" — it does NOT attempt to judge
whether a company is truly pursuing AI transformation. That judgment
is left to the LLM agent that reads the extracted text.
"""

import argparse
import csv
import io
import json
import os
import re
import struct
import sys
import time
import urllib.request
import zipfile
import xml.etree.ElementTree as ET
from html.parser import HTMLParser

# Ensure UTF-8 output on Windows
sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

BASE_URL = "https://disclosure.dx-portal.ipa.go.jp"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/131.0.0.0 Safari/537.36"
}


def fetch_url(url: str, max_retries: int = 3) -> bytes:
    """Fetch URL content with retry logic and proper headers."""
    for attempt in range(max_retries):
        try:
            req = urllib.request.Request(url, headers=HEADERS)
            with urllib.request.urlopen(req, timeout=30) as resp:
                return resp.read()
        except Exception as e:
            if attempt < max_retries - 1:
                wait = 2 ** attempt
                print(f"  Retry {attempt + 1}/{max_retries} after {wait}s: {e}")
                time.sleep(wait)
            else:
                raise
    return b""


def download_all_csv() -> list[dict]:
    """Download and parse the full CSV of all certified businesses."""
    print("Downloading full CSV from portal...")
    data = fetch_url(f"{BASE_URL}/download/AllData.csv")

    try:
        text = data.decode("utf-8-sig")
    except UnicodeDecodeError:
        text = data.decode("cp932")

    reader = csv.DictReader(io.StringIO(text))
    companies = []
    for row in reader:
        companies.append({
            "procedure_id": row.get("手続き番号", "").strip(),
            "corp_number": row.get("法人番号等", "").strip(),
            "company_name": row.get("一般事業主の氏名又は名称", "").strip(),
            "prefecture": row.get("都道府県名", "").strip(),
            "address": row.get("住所", "").strip(),
            "representative": row.get("代表者の氏名", "").strip(),
            "cert_start": row.get("認定の適用開始日", "").strip(),
            "cert_end": row.get("認定の適用終了日", "").strip(),
            "cancelled": row.get("認定の取消日", "").strip(),
            "employees": row.get("従業員数（単体）", "").strip(),
            "scale": row.get("規模", "").strip(),
            "industry": row.get("大分類①", "").strip(),
            "sub_industry": row.get("中分類①", "").strip(),
        })

    print(f"  Loaded {len(companies)} entries from CSV")
    return companies


class DXPageParser(HTMLParser):
    """Parse the DX portal HTML page to extract company data."""

    def __init__(self):
        super().__init__()
        self.companies = []
        self._current = {}
        self._in_td = False
        self._td_label = ""
        self._td_text = ""
        self._in_row_type = None
        self._download_href = ""

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        if tag == "tr":
            cls = attrs_dict.get("class", "")
            if "row-corporate" in cls:
                self._in_row_type = "corporate"
                self._current = {}
            elif "row-certification" in cls:
                self._in_row_type = "certification"
        elif tag == "td":
            self._in_td = True
            self._td_label = attrs_dict.get("data-label", "")
            self._td_text = ""
        elif tag == "a" and self._td_label == "申請書":
            href = attrs_dict.get("href", "")
            if href:
                self._download_href = href

    def handle_data(self, data):
        if self._in_td:
            self._td_text += data.strip()

    def handle_endtag(self, tag):
        if tag == "td" and self._in_td:
            self._in_td = False
            label = self._td_label
            text = self._td_text.strip()

            if self._in_row_type == "corporate":
                if label == "手続き番号":
                    m = re.search(r"((?:DX|DPF)-\d{4}-\d{2}-\d{4}-\d{2})", text)
                    self._current["procedure_id"] = m.group(1) if m else text
                elif label == "一般事業主の氏名又は名称":
                    self._current["company_name"] = text
                elif label == "代表者の氏名":
                    self._current["representative"] = text
                elif label == "従業員数":
                    self._current["employees"] = text
                elif label == "業種（大分類）":
                    self._current["industry"] = text
            elif self._in_row_type == "certification":
                if label == "法人番号等":
                    self._current["corp_number"] = text
                elif label == "住所":
                    self._current["address"] = text
                elif label == "認定の適用日":
                    self._current["cert_start"] = text
                elif label == "規模":
                    self._current["scale"] = text
                elif label == "申請書" and self._download_href:
                    self._current["download_url"] = self._download_href
                    self._download_href = ""

        if tag == "tr" and self._in_row_type == "certification":
            if self._current.get("procedure_id"):
                self.companies.append(self._current)
            self._current = {}
            self._in_row_type = None


def parse_page(url: str) -> list[dict]:
    """Parse a single page of the DX portal and extract company data."""
    print(f"Fetching page: {url}")
    html = fetch_url(url).decode("utf-8", errors="replace")
    parser = DXPageParser()
    parser.feed(html)
    print(f"  Found {len(parser.companies)} companies on page")
    return parser.companies


def extract_zip_docx_text(zip_data: bytes) -> tuple[str, str]:
    """
    Extract text content from a docx inside a ZIP archive.
    Handles CP932-encoded Japanese filenames in ZIP entries.
    Returns (filename, text_content).
    """
    real_filename = ""
    idx = zip_data.find(b"PK\x03\x04")
    if idx >= 0:
        name_len = struct.unpack_from("<H", zip_data, idx + 26)[0]
        name_raw = zip_data[idx + 30 : idx + 30 + name_len]
        try:
            real_filename = name_raw.decode("cp932")
        except UnicodeDecodeError:
            real_filename = name_raw.decode("utf-8", errors="replace")

    with zipfile.ZipFile(io.BytesIO(zip_data)) as z:
        entries = z.infolist()
        if not entries:
            return real_filename, ""
        docx_data = z.read(entries[0])

    try:
        with zipfile.ZipFile(io.BytesIO(docx_data)) as dz:
            doc_xml = dz.read("word/document.xml")
    except (zipfile.BadZipFile, KeyError):
        return real_filename, ""

    ns = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
    root = ET.fromstring(doc_xml)
    paragraphs = []
    for p in root.iter(f"{{{ns}}}p"):
        line_parts = []
        for t in p.iter(f"{{{ns}}}t"):
            if t.text:
                line_parts.append(t.text)
        if line_parts:
            paragraphs.append("".join(line_parts))

    return real_filename, "\n".join(paragraphs)


def process_company(company: dict) -> dict:
    """Download and extract text from a single company's application document."""
    proc_id = company.get("procedure_id", "")
    if not proc_id:
        return company

    download_url = company.get("download_url", "")
    if not download_url:
        download_url = f"/download/{proc_id}/{proc_id}.zip"

    full_url = f"{BASE_URL}{download_url}" if download_url.startswith("/") else download_url

    try:
        zip_data = fetch_url(full_url)
        filename, doc_text = extract_zip_docx_text(zip_data)
        company["doc_filename"] = filename
        company["doc_text"] = doc_text
        company["doc_text_length"] = len(doc_text)
    except Exception as e:
        company["error"] = str(e)
        company["doc_text"] = ""
        company["doc_text_length"] = 0

    return company


def main():
    parser = argparse.ArgumentParser(
        description="Download and extract DX certification application documents"
    )
    parser.add_argument("--url", help="URL of a specific DX portal page to scrape")
    parser.add_argument("--all", action="store_true",
                        help="Download all companies from full CSV")
    parser.add_argument("--output", "-o", required=True,
                        help="Output JSON file path (company data + extracted text)")
    parser.add_argument("--limit", type=int, default=0,
                        help="Limit number of companies to process (0 = no limit)")

    args = parser.parse_args()

    # Collect companies
    if args.all:
        companies = download_all_csv()
        companies = [c for c in companies if not c.get("cancelled")]
    elif args.url:
        companies = parse_page(args.url)
    else:
        parser.error("Must specify either --url or --all")
        return

    if args.limit > 0:
        companies = companies[: args.limit]

    print(f"\nDownloading {len(companies)} application documents...\n")

    total = len(companies)
    errors = 0

    for i, company in enumerate(companies):
        proc_id = company.get("procedure_id", "?")
        name = company.get("company_name", "?")
        print(f"  [{i+1}/{total}] {proc_id} - {name}...", end=" ", flush=True)

        process_company(company)

        if company.get("error"):
            print(f"ERROR: {company['error']}")
            errors += 1
        else:
            print(f"OK ({company['doc_text_length']} chars)")

        if i < total - 1:
            time.sleep(0.3)

    print(f"\n{'='*60}")
    print(f"Download complete:")
    print(f"  Total: {total}")
    print(f"  Success: {total - errors}")
    print(f"  Errors: {errors}")
    print(f"{'='*60}")

    # Save to JSON
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(companies, f, ensure_ascii=False, indent=2)

    print(f"\nData saved to: {args.output}")


if __name__ == "__main__":
    main()
