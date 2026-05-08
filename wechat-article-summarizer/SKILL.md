---
name: wechat-article-summarizer
description: Use this skill whenever the user provides a WeChat official account article link (domain "mp.weixin.qq.com") and asks you to summarize, read, extract, or get the content of the article. It runs a Python script to fetch the text content, bypassing basic anti-bot verifications.
---

# WeChat Article Summarizer

## Overview

This skill allows you to automatically extract the text content from a WeChat official account article (`mp.weixin.qq.com`) to bypass its anti-bot validation. You should trigger this skill whenever the user asks you to summarize, read, or parse a WeChat article link.

## Usage

When triggered, use the `run_command` tool to execute the `fetch.py` script provided in this skill's directory, passing the user's WeChat article URL as the argument.

### Command Format
```bash
python fetch.py "<WeChat_URL>"
```

### Execution Steps
1. Verify the domain of the provided URL is `mp.weixin.qq.com`.
2. Run the `fetch.py` script with the URL using the `run_command` tool. 
   - **Crucial**: Ensure `Cwd` is set to `C:\Users\gunze\.gemini\antigravity\skills\wechat-article-summarizer`.
3. Read the standard output from the command, which will print the Title, Author, and the extracted plain text.
4. Based on the extracted text, generate a comprehensive, well-structured summary for the user (unless the user explicitly asked for the full text).

## Limitations
- **Text Only**: This script only extracts text. Images are not fetched because WeChat uses lazy loading and anti-hotlinking.
- **Complex Articles**: For highly interactive articles, paid reading, or pure video articles, the extraction might fail or return incomplete text.
