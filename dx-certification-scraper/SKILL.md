---
name: dx-certification-scraper
description: >
  Scrape IPA DX Portal (disclosure.dx-portal.ipa.go.jp) certified business listings,
  download application documents (申請書 ZIP), extract and read their content,
  and filter/analyze them semantically using LLM based on user-defined criteria
  (e.g., AI-related, construction industry, SaaS development, etc.).
  Use this skill when the user mentions DX認定, DX推進ポータル, IPA DX Portal,
  DX certified businesses, or wants to extract and screen companies from these portals
  for target profiles.
---

# DX Certification Scraper (Flexible Semantic Filtering)

Scrapes the IPA DX推進ポータル to download DX certification application documents,
then uses LLM semantic analysis to identify and filter companies according to custom criteria
specified by the user (defaulting to AI-related, but customizable to industries like construction,
business models like SaaS, or technology stacks).

## Architecture: Two-Phase Pipeline

This skill uses a **"script extracts, LLM judges"** architecture:

### Phase 1: Data Collection (Script)
The Python script `scripts/scrape_dx_portal.py` handles the mechanical work:
- Downloads company data from the portal (via page HTML or full CSV)
- Downloads each company's 申請書 ZIP archive
- Decompresses ZIPs (handling CP932-encoded Japanese filenames)
- Extracts full text from .docx files
- Outputs a JSON file containing company metadata + full document text

This script is intentionally "dumb" and extracts all documents without filtering.

### Phase 2: Semantic Analysis & Dynamic Filtering (LLM Agent)
After the script produces the JSON, the agent reads the JSON data and applies semantic understanding to screen companies based on the **User's specific targeting criteria** (e.g., finding AI API demand, finding SaaS projects, filtering for construction companies, etc.).

For each run, the agent must:
1. **Identify the Target Profile**: Determine what the user is looking for (e.g., "AI API usage", "SaaS development", "Construction companies").
2. **Define Tier Classification Rules**: Establish custom classification criteria for the target profile. For example:
   - **AI API Demand Targeting (Default)**:
     - **A-tier (High Demand)**: Concrete plans to build/integrate AI APIs, custom models, or AI platforms.
     - **B-tier (Medium Demand)**: Simple internal tool usage (e.g., using ChatGPT/Copilot off-the-shelf) or generic AI training.
     - **C-tier/Not Relevant**: Mentions AI only as a buzzword or has no AI plans.
   - **SaaS Development Targeting**:
     - **A-tier (High Relevance)**: Building a new cloud-based software-as-a-service product for their customers.
     - **B-tier (Medium Relevance)**: Transitioning internal software to cloud-based systems (internal SaaS) or using SaaS products.
     - **C-tier/Not Relevant**: Standard IT migration or unrelated.
   - **Construction Industry Targeting**:
     - **A-tier (High Relevance)**: Core construction companies actively modernizing sites (BIM/CIM, drone surveys).
     - **B-tier (Medium Relevance)**: Auxiliary construction services (real estate development, architectural design, materials trading).
     - **C-tier/Not Relevant**: Other industries.
3. **Analyze the Documents**: Read the `doc_text` for each company and categorize them into these Tiers.
4. **Extract Context & Evidence**: Pull the specific sections of Japanese text from the document supporting the classification.

## Usage

### Step 1: Run the extraction script

Run the script to download and extract documents into a temporary JSON file:
```powershell
# Extract from a specific page
python scripts/scrape_dx_portal.py --url "<PAGE_URL>" -o "extracted_data.json"

# Extract from full CSV (all companies)
python scripts/scrape_dx_portal.py --all -o "extracted_data.json"

# Limit for testing
python scripts/scrape_dx_portal.py --url "<PAGE_URL>" --limit 10 -o "extracted_data.json"
```

### Step 2: Semantic Analysis by the Agent

Read the generated `extracted_data.json` file.
Apply the LLM's reasoning to classify and extract relevant information according to the user's criteria.

### Step 3: Generate the dynamic Excel report

Create an XLSX report (using the xlsx skill or a Python script) containing:
- **Sheet 1**: High priority target list (A-tier) with company metadata, reasons, and supporting excerpts.
- **Sheet 2**: Secondary target list (B-tier).
- **Sheet 3**: The complete list of processed companies with their classifications (A/B/C/Not Relevant).

The columns in Sheet 1 and 2 should adapt to the criteria (e.g., "AI Keywords Found" for AI tasks, or "SaaS Product Concept" for SaaS tasks, "Construction Sub-sector" for construction tasks).

## Dependencies

- Python 3.10+
- openpyxl (for XLSX output)
