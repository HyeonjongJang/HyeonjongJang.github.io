# Research Radar — Repo Explainer Style Guide

> The single source of truth for the **repo** post type. **Both** the writer and
> the reviewer read this file. If a rule here conflicts with a model's instinct,
> this file wins. `_automation/` is ignored by Jekyll, so it is never published.

Each post explains **one trending open-source project** clearly and usefully,
grounded in its **README**: what it is, the problem it solves, how it works, how
to actually use it, and why it matters. Practical and honest — not marketing copy.

---

## 1. Purpose, audience, positioning

- **What this is:** a clear, hands-on explainer of one notable GitHub project,
  grounded in its README and repo metadata.
- **Who reads it:** developers and researchers deciding whether a tool is worth
  their time. Not a general-traffic/SEO audience.
- **Positioning:** a curated adjunct to a research/engineering portfolio. Bias
  selection toward LLM/ML and developer tooling.

## 2. Voice & tone

**Do:** explain like an experienced engineer showing a colleague a useful tool.
Say plainly what it does, who it's for, and when you'd reach for it. Build an
analogy for any non-obvious design idea. Be honest about maturity and scope.

**Don't:** hype ("revolutionary", "must-have"), marketing superlatives, clickbait,
emoji-as-decoration, or implying you've run/audited the code when you've only read
the README. Opinion goes in one clearly-labeled takeaway sentence.

Length: **1,000–2,000 words.** Enough to actually understand and try the tool.

## 3. Reference exemplars (borrow principles, never prose)

- **A great project README / "Awesome" writeups** — lead with what it does and a
  minimal example.
- **The Changelog / console.dev** — sober, practical tool framing.
- **Julia Evans ("wizardzines")** — plain-language, hands-on explanation.

## 4. Post structure (template)

1. **Title** — see §5.
2. **One-line TL;DR** (italic) — what the project does and who it's for, ≤ 30 words.
3. **`## What it is`** — the project in a paragraph: problem it solves, who it's
   for, its one-sentence pitch (grounded in the README).
4. **`## How it works`** — the design/architecture and the key ideas, from the
   README. Use an analogy (§6) for any non-obvious mechanism.
5. **`## Using it`** — the minimal path to try it: install and a small usage
   example, taken from the README (don't invent commands). Note requirements.
6. **`## Notable details`** — standout features, limitations, maturity signals
   (stars, language, license if stated), and what the README leaves unclear.
7. **`## Why it matters`** — where this fits in the landscape; one or two
   sentences of the author's own view, clearly labeled as opinion.
8. **`## Source`** — the repo, linked, with owner and star count.

Drop a section if the README doesn't support it. Never invent features, commands,
or results that aren't in the README/metadata.

### Jekyll front matter (exact keys — the TASK gives you the exact slug/date)

```yaml
---
title: "<repo name>: <one-line of what it does>"
date: <DATE>
excerpt: "<= 155 chars, plain summary of what the tool does, no hype>"
tags:
  - repo-dive
  - <2-4 topical tags, lowercase-hyphenated>
header:
  teaser: /images/radar/<DATE>-card.png
lang: en
translated_url: /blog/<SLUG>-ko/
---
```

## 5. Title rules

- Format: `<repo name>: <plain one-line of what it does>`,
  e.g. `llama.cpp: running LLMs on your laptop in plain C/C++`.
- No numbers-as-bait, no questions, no ALL CAPS, no emoji.

## 6. Intuition & analogies

- For any non-obvious design idea, give a concrete analogy first, then map it
  back to the real mechanism. Label analogies as **yours, not the project's**,
  and keep them accurate — if an analogy implies something the tool doesn't do,
  fix the analogy.

## 7. Figures & code

- Show commands/snippets **only if they appear in the README** (install, minimal
  usage). Keep them short. Don't invent flags or APIs.
- Don't embed the repo's images; describe and link instead.

## 8. Hard rules (non-negotiable — the reviewer enforces these)

1. **Grounding:** every factual claim, feature, command, and number traces to the
   README or repo metadata in the source. If it isn't there, cut it — except
   clearly-labeled analogies (§6) and the one-sentence opinion.
2. **No fabrication:** repo name, owner, URL, star count, language, commands, and
   features are copied from the source, not reconstructed from memory.
3. **README-only honesty:** you have read the README, not run the code — say so
   where it matters (reliability, benchmarks, "it works" claims).
4. **Analogies accurate and labeled as the author's own** (§6).
5. **No hype/clickbait/emoji decoration** (§2). Opinion only in the one labeled
   takeaway sentence.
6. **Length 1,000–2,000 words.**
7. **No sensitive/pen-name/real-name-unsafe content.**

## 9. Bilingual rules (EN primary + KO)

- The **English post is canonical.** Generate a **Korean version** in the same
  run with `lang: ko` and `translated_url` to the EN post.
- **URL convention:** the TASK gives you the exact slug. EN is `/blog/<SLUG>/`,
  KO is `/blog/<SLUG>-ko/`. Use these for the toggle and `translated_url`.
- Top of each post: `[EN](/blog/<SLUG>/) · [한국어](/blog/<SLUG>-ko/)`.
- Translation is faithful: same claims, commands, numbers, links. Keep tool names
  and code in English; gloss technical terms, e.g. "추론(inference)".

## 10. Title-card spec

- HTML/CSS → PNG (Pillow). No generative images. 1200 × 630, < 80 KB.
- Path `/images/radar/<DATE>-card.png`. Content: "RESEARCH RADAR", the repo name,
  the date. Fixed brand palette, one typeface.

## 11. Automated review checklist (the reviewer pass)

The reviewer receives **the draft + the README/metadata** and verifies, one by
one. **Any FAIL quarantines the post (not published):**

- [ ] Every feature, command, and number is supported by the README/metadata.
- [ ] Repo name, owner, URL, stars, and language match the source.
- [ ] Commands/snippets appear in the README (none invented).
- [ ] "README-only" honesty is respected (no unverified "it works" claims).
- [ ] Analogies are accurate and labeled as the author's own.
- [ ] No hype/clickbait/emoji; opinion only in the labeled takeaway.
- [ ] Length 1,000–2,000 words.
- [ ] EN and KO carry the same claims, commands, and links.
- [ ] Front matter valid; title, excerpt, tags, teaser, `translated_url` present.
- [ ] No sensitive/pen-name/real-name-unsafe content.

The reviewer outputs a short PASS/FAIL report with the specific failing line for
any FAIL. Grounding is checked against the README, **not** vibes.

## 12. Worked micro-examples

**Good title:** `llama.cpp: running LLMs on your laptop in plain C/C++`
**Bad title:** `🚀 This repo will BLOW YOUR MIND (10k stars!!)`

**Good honesty:** "I've read the README, not benchmarked it — the throughput
numbers below are the authors'."
**Bad:** "It's blazing fast and just works." (unverified, hype)
