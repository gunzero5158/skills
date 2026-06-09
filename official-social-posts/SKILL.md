---
name: official-social-posts
description: "Use when drafting daily official-account social posts or replies for a brand, especially multilingual Twitter/X posts. Follow a context-first workflow: infer or confirm brand/business/social-account requirements, decide languages and length constraints, gather official-account materials when needed, confirm or propose topics, then produce complete post copy, hashtags, and matching visual guidance or assets for every requested language."
---

# Official Social Posts

## Purpose

Create official-account social posts and replies that are useful, natural, and not annoyingly promotional. The default output package is:

- post copy for each requested language
- matching hashtags for each language
- image/visual concept or generated/local asset when requested or useful

Use this for Twitter/X by default unless the user names another platform.

## Context Check

At the start of a new brand/workflow, first review available context before asking questions:

1. Read the current conversation for prior official-account style, business value props, target audience, language preferences, membership/length constraints, and image preferences.
2. If memory is likely relevant, do the normal lightweight memory pass and cite it in the final answer if used.
3. Search the project folder for brand/business materials when the task is project-bound. Prefer `rg` and existing assets such as `logo/`, `poster/`, `assets/`, `README`, press releases, pricing pages, and presentation docs.
4. If current trends or official-account content are needed, browse. Use official/primary sources for factual claims and use browser tools when the user asks to inspect the account itself or dynamic social pages.

After this check:

- If the conversation shows this is an established repeating workflow, do not ask the setup questions again. Reuse the most recent confirmed defaults: brand, languages, post length, platform, tone, output package, hashtag style, image expectations, asset folder, and any known business claims. Apply the user's new topic/material to those defaults and draft directly.
- If relevant context exists but this appears to be the first execution for that brand/workflow, summarize your understanding briefly and ask the user to confirm only if the inferred scope could be wrong.
- If no relevant context exists, ask concise questions before drafting:
  - Is this for a multilingual official account, and which languages?
  - How many languages/post variants are needed?
  - Is the account limited to short posts such as 140 characters, or can it publish longer posts?
  - Should the topic be user-specified, or should you propose topics to choose from?

Do not over-question once the workflow is established; use the known defaults and produce drafts.

Only ask again in an established workflow when the new request conflicts with the prior defaults, when a required output parameter is genuinely missing, or when live/current information must be verified before making a factual claim.

## Topic Workflow

When the user gives a topic, draft from that topic directly.

When the user asks for topics:

1. Gather current, relevant trends if the topic should be timely.
2. Propose 3-6 options with a one-line rationale for each.
3. Identify the most recommended option.
4. After the user picks one, produce the full package.

When the user provides a post, screenshot, or quote to reply to:

1. Identify the other post's main point.
2. Start by acknowledging or extending the point.
3. Mention the brand value subtly, usually near the end.
4. Keep replies shorter and less promotional than standalone posts.

## Drafting Rules

- Match official-account tone: calm, credible, useful, and restrained.
- Avoid hard selling, exaggerated claims, competitor dunking, spammy hashtag piles, and repetitive brand mentions.
- Lead with the market/user problem or practical insight; introduce the brand as one possible solution.
- For multilingual output, do not translate mechanically. Localize each language naturally while preserving the same intent.
- For X/Twitter, prefer short paragraphs and readable line breaks.
- If the user has a paid/long-post account, longer posts are allowed but should still be concise.
- If a strict character limit applies, state that the draft is designed for that limit.
- Avoid making factual claims about news, pricing, policies, or model availability unless verified or clearly based on provided/project context.
- If using current events, cite sources in the final answer when appropriate.

## Output Package

For each requested language, provide:

1. **Post Copy**: ready-to-post text.
2. **Hashtags**: 3-5 natural hashtags. Avoid more unless the user asks.
3. **Image**: one of:
   - a concrete visual concept/prompt
   - a generated/local image asset
   - a note that no image is recommended for this specific reply

For multilingual posts, include the full package for every language. Do not provide only one shared hashtag list unless it genuinely fits all languages.

## Visual Workflow

Use existing brand assets first when available. For project-bound work:

1. Look for logo, poster, palette, and prior visual assets in the project.
2. Prefer deterministic layouts for graphics with text: HTML/CSS rendered to PNG, slides, or other controllable tools. This avoids bad typography and multilingual text errors.
3. Use image generation for raster imagery when a photographic/illustrative asset is desired and exact text is not the main content.
4. Keep social images simple: one headline, one short supporting line, and 2-4 value points at most.
5. Generate one visual per language when the image contains language-specific text.
6. Save project-bound assets inside the project, usually in an existing `poster/` or assets folder, and report the absolute path.

For Twitter/X cards, 1600x900 is a good default unless the user requests another size.

## Useful Reference

For compact templates and package examples, read `references/output-patterns.md` when helpful.
