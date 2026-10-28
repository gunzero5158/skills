[**中文**](README.md) | [**English**](README_en.md) | [**日本語**](README_ja.md)

# My AI Agent Skills Collection 🚀
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
A multilingual social-writing skill for daily official-account content, defaulting to Twitter/X. All brand conventions (languages, tone, length limits, hashtag style, forbidden terms, tone-anchoring examples) live in "brand profile" files that every output must read from — no reliance on conversation memory, so a fresh session seamlessly continues the established style and confirmed preferences are never lost.
**Core Features**:
- **Profile-driven**: With a profile present it drafts directly with zero repeated setup questions; without one it enters an onboarding mode (extracting existing materials or interviewing in rounds); corrections made during use can be written back into the profile.
- **Complete multilingual packages**: A mandatory three-part template per language (ready-to-post copy + 3-5 language-specific hashtags + visual plan), each language localized independently rather than machine-translated.
- **Example-anchored tone**: Built-in good/bad post contrasts (problem-first vs. brand-name-first) and a dedicated reply mode enforcing "add value, don't sell, no links" to avoid embarrassing promotional replies.
- **Pre-delivery checklist**: Character counts measured by command (never eyeballed), hashtag counts verified, zero forbidden-term hits, and every factual claim sourced — all checks pass before delivery.
**Usage Scenario**:
"Based on current AI trends, write a Japanese and English official X post with hashtags."

### 4. DX Certified Business Application Scraper & Semantic Analyzer (dx-certification-scraper)
**Introduction**:
A specialized tool for scraping and analyzing DX application documents (ZIP files) on the Japanese IPA DX Portal. It combines automated data extraction with LLM semantic reasoning to filter and screen target companies matching specific sales profiles (e.g., AI API demand, SaaS software development, or construction modernization).
**Core Features**:
- **Two-phase Smart Pipeline**: Phase 1 utilizes Python scripts to download CSV catalogs and ZIP documents, decode Shift-JIS Japanese filenames, and dump the docx text to JSON. Phase 2 leverages LLM reasoning to perform semantic filtering and tier-classification in context.
- **Dynamic Targeting Criteria**: Moves beyond rigid keyword searches. The agent dynamically assesses the actual progress of AI systems, SaaS projects, or industry-specific alignment based on current goals and assigns A/B/C tiers.
- **Polished Excel Reports**: Automatically builds multi-sheet styled Excel files detailing classifications, logic, context snippets, and sales action items.
**Usage Scenario**:
"Analyze this DX portal page to find companies with genuine AI API integration needs: https://disclosure.dx-portal.ipa.go.jp/p/dxcp/top?page=1"

### 5. X (Twitter) Account Analyzer & Outreach Copywriter (x-outreach)
**Introduction**:
A writing skill for B2B cold outreach (partner recruiting, customer conversion): it first investigates the real identity behind an X (Twitter) account, then generates a personalized Japanese DM or public reply based on a "campaign profile" mechanism. It solves the "context lost between sessions" problem — all approved wording, offer numbers, and forbidden terms live in profile files, so any fresh session can cold-start.
**Core Features**:
- **Deep Identity Verification**: Cross-checks social vertical search with web sources to confirm the person's real name (including the correct kanji spelling), current title, and company — avoiding outdated titles, renamed accounts, and homophone surname mistakes.
- **Compliance Gating**: A built-in constraint table — never offer revenue share to civil servants (side-job restrictions), give concrete numbers only to private-sector owners — plus a risk scan (controversies, scam allegations) reported honestly for the user to decide.
- **Profile-driven Generation**: Selling-point order, pricing wording, forbidden-term list, and signature formats are all read from profile files; with no profile present it enters an onboarding mode (extracting existing materials or interviewing in rounds); corrections made during use can be written back into the profile.
- **Two Output Modes**: DM mode produces a fully structured private message (with a concrete hook mined from recent posts and a low-friction question-form CTA); reply mode produces short, non-promotional public comments to build presence first.
**Usage Scenario**:
"Check out this person's account https://x.com/xxx — I'd like to DM them about a partnership."

### 6. Game Port Archive (game-port-archive)
**Introduction**:
Collect and update game decompilation, recompilation, PC port, and fan-remake projects from GitHub. Compare local archives with upstream commits and releases, then preserve suitable runtime packages, pinned source, specialized dependencies, Chinese instructions, and update links.
**Core Features**:
- **Incremental comparison**: Track source and runtime updates separately; prefer Windows x64, retain complete x86 packages when necessary, and keep alternatives with distinct functionality.
- **Compressed preservation**: Include pinned project-specific submodules, tools, patches, and licenses; document general development prerequisites instead of downloading them.
- **Traceable verification**: Includes ZIP integrity, PE architecture, and per-file SHA256 round-trip packing tools, alongside HTML, CSV, and provenance records.
- **Clear limits**: Distinguish portable games, build/import wizards, other platforms, and research-only source. Does not obtain commercial ROMs or present file checks as gameplay tests.
**Usage Scenario**:
"Compare these GitHub game ports with my local collection and archive new or updated projects with suitable runtime packages, complete source, Chinese instructions, and update links."

---
*To be continued... Welcome to Star ⭐️ and Fork!*
