[**中文**](README.md) | [**English**](README_en.md) | [**日本語**](README_ja.md)

# My Antigravity Skills Collection 🚀
Here is a collection of custom local skills created and maintained by me for [Antigravity](https://github.com/GoogleDeepMind/antigravity) (or Agent terminals like Claude Code).
By writing these custom skills, I can empower the AI assistant with exclusive capabilities in specific domains, breaking through the limits of standard interactions and achieving deeper automated workflows.

## 🛠️ List of Included Skills
### 1. WeChat Public Account Article Grabber (wechat-article-summarizer)
**Introduction**:
A tool specifically developed to bypass the strong anti-scraping and CAPTCHA mechanisms of WeChat public accounts. When asking the AI to summarize WeChat articles, default browser nodes or normal HTTP requests often trigger CAPTCHA, leading to failure.
**Core Features**:
- **Seamless CAPTCHA Bypass**: Uses a Python script to spoof standard browser request headers and fetch the HTML source code headlessly, perfectly bypassing CAPTCHA pop-ups.
- **Accurate Extraction**: Highly accurate extraction based on regex to strip away excess CSS, JS, and HTML tags, keeping only the core article title, author, and text.
- **Fully Automated AI Integration**: When the Agent detects a user sending an `mp.weixin.qq.com` link, it seamlessly calls this script to get the plain text, ultimately outputting a high-quality structured summary.
**Usage Scenario**:
"Help me summarize this article: https://mp.weixin.qq.com/s/..."

### 2. Webpage to Clean PDF Assistant (webpage-to-pdf)
**Introduction**:
A local skill dedicated to converting complex web pages (containing ads, sidebars, and pop-ups) into clean, e-book-like PDF files.
**Core Features**:
- **Bypass Lazy Loading**: Uses Playwright to drive the Chromium browser, simulating the natural scrolling behavior of real human users to ensure all "lazy-loaded" images are fully loaded before capturing.
- **Smart DOM Purification**: Automatically injects specific CSS rules to forcefully block common distractions like navigation bars, sidebars, floating ads, and footer copyright information.
- **Layout Reset**: Automatically removes the width limit of the webpage's main content (100% full width), making the final exported A4 PDF compact, high-definition, and aesthetically pleasing.
**Usage Scenario**:
"Help me save this webpage cleanly as a PDF: https://www..."

### 3. Multilingual Official Social Post Assistant (official-social-posts)
**Introduction**:
A multilingual social-writing skill for daily official-account content. It defaults to Twitter/X but can also support other official social channels. It first reviews the conversation, project materials, and existing account style; if the workflow has already been established, it reuses the last confirmed languages, length constraints, tone, output format, and image preferences.
**Core Features**:
- **Context-first workflow**: Reviews prior context, project files, and brand assets before asking setup questions; reuses prior defaults for repeated workflows.
- **Complete multilingual packages**: Produces post copy, hashtags, and image guidance or assets for each requested language.
- **Topic and trend support**: Drafts from user-specified topics or proposes several timely topic options for the user to choose from.
- **Official-account tone control**: Keeps posts natural, restrained, useful, and not overly promotional.
- **Visual workflow**: Uses existing logos, posters, and brand assets first; for text-heavy social cards, prefers controllable HTML/CSS rendering to avoid multilingual text errors.
**Usage Scenario**:
"Based on current AI trends, write a Japanese and English official X post with hashtags and a promotional image."

---
*To be continued... Welcome to Star ⭐️ and Fork!*
