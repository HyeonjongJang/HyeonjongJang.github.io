# Research Radar — Deep-Dive Editorial Style Guide

> The single source of truth for the automated deep-dive pipeline. **Both** the
> *writer* pass and the *reviewer* pass of Claude Code read this file on every
> run. If a rule here conflicts with a model's instinct, this file wins.
> `_automation/` is ignored by Jekyll, so this file is never published.

Each post is **one paper, explained in depth** — background, the core idea in
plain intuition, how the mechanism works step by step, the central math (every
symbol explained), results, and honest limitations. Not a "what's new" blurb:
a teaching walkthrough a grad student can learn the paper from without opening
the PDF first.

---

## 1. Purpose, audience, positioning

- **What this is:** a careful, intuition-first explainer of a single notable
  AI/ML paper, grounded in its **full text**.
- **Who reads it:** researchers and graduate students; also the author's future
  self. Not a general-traffic/SEO audience.
- **Positioning:** a curated adjunct to a research portfolio centered on LLMs,
  automatic heuristic design, multi-agent path finding (MAPF), and adaptive
  search control. Bias selection and framing toward LLM/ML systems.

## 2. Voice & tone

**Do:** explain like a good teacher. Lead with intuition, then precision. Build
an analogy for every hard idea, then connect it back to the real mechanism.
Define terms on first use. Walk the reader through the math one symbol at a time.
Be honest about what the paper does and doesn't show.

**Don't:** hype ("revolutionary", "game-changer"), clickbait, emoji-as-decoration,
vague praise, or hand-waving over the hard part. Never pretend to a depth of
reading you don't have; the full text is provided, so read it.

**No em dashes.** Do not use the `—` (em dash) character anywhere. Use a period,
comma, colon, or parentheses instead. (Hyphens in names/ranges are fine.)

Length: **1,500–3,000 words.** Depth over breadth; it is fine to focus on the
core contribution and say which sections you are skipping and why.

## 3. Reference exemplars (borrow principles, never prose)

Derive *principles* from these; never copy wording.

- **distill.pub / Lil'Log (Lilian Weng)** — build intuition before formalism;
  definitional care.
- **Jay Alammar ("The Illustrated …")** — one clear mental model carried through.
- **Sebastian Raschka** — plain-language method + takeaway, honest scope.
- **The Gradient / Papers with Code** — sober framing, exact linking/attribution.

## 4. Post structure (template)

1. **Title** — see §5.
2. **One-line TL;DR** (italic) — the paper's core contribution in ≤ 30 words.
3. **`## The problem`** — what's broken / why it matters, with a concrete setup.
4. **`## The core idea`** — the key insight in one or two intuitive analogies
   (§6) before any formalism.
5. **`## How it works`** — the mechanism, step by step, grounded in the paper.
   Use sub-sections for distinct components.
6. **`## The math`** *(include only if an equation is central)* — present the key
   equation in `$$ … $$` and explain **every symbol in plain words** (§7).
7. **`## Results`** — the headline numbers, with the baselines and the setup they
   were measured against. Exact figures from the paper.
8. **`## Limitations & what's not covered`** — honest scope; name sections of the
   paper you did not dive into.
9. **`## Why it matters`** — the takeaway, and where it connects to the broader
   field (one or two sentences of the author's own view, clearly as opinion).
10. **`## Source`** — the paper, linked (arXiv), with authors.

Not every paper needs every section — drop `## The math` when there's no central
equation. Never invent results or sections that aren't in the paper.

### Jekyll front matter (exact keys — the TASK gives you the exact slug/date)

```yaml
---
title: "<Paper short name>: <one-line what it does>"
date: <DATE>
excerpt: "<= 155 chars, plain summary of the paper's contribution, no clickbait>"
tags:
  - paper-dive
  - <2-4 topical tags, lowercase-hyphenated>
header:
  teaser: radar/<DATE>-card.png
  image: radar/<DATE>-card.png
lang: en
translated_url: /blog/<SLUG>-ko/
---
```

## 5. Title rules

- Format: `<Paper short name>: <plain one-line of what it does>`,
  e.g. `PagedAttention: paging the KV cache to serve LLMs faster`.
- No numbers-as-bait, no questions, no ALL CAPS, no emoji.

## 6. Intuition & analogies (the differentiator)

- For every hard mechanism, give a **concrete analogy** first, then map it back:
  "the KV cache is like a concert hall booked for 2048 seats when only 500 show
  up — the rest is reserved and wasted" → then the real term (internal
  fragmentation).
- Analogies are **your teaching device, not the paper's** — never attribute them
  to the authors. They must be *accurate*: if the analogy implies something the
  mechanism doesn't do, fix the analogy, don't bend the facts.
- One or two strong analogies per hard idea beats a pile of weak ones.

## 7. Math rules

- Include an equation **only if it is central** to the contribution.
- Use `$$ … $$` for **all** math — display (on its own line) and inline (within a
  sentence). kramdown renders `$$…$$` in both positions. Do **not** use `\( … \)`,
  `\[ … \]`, or bare single-`$`: kramdown leaves them as literal text. Prefer
  naming a lone symbol in prose over heavy inline math.
- After any equation, **explain every symbol in plain words** and say what the
  whole expression computes — as the exemplar does ("$q_i$ is the query of the
  token being generated; it scans every past key …").
- Never show math you don't explain. If the derivation isn't needed to understand
  the idea, describe it in words instead.

## 8. Figures & copyright

- **Do not reproduce the paper's figures** (copyright). Describe the relevant one
  in words and point to it: "see Figure 3 in the paper". Link the paper.
- Quote at most one short sentence from the paper; summarize everything else in
  your own words.
- The title card is the only image (§11); optionally one original diagram/chart
  you build from real numbers.

## 9. Hard rules (non-negotiable — the reviewer enforces these)

1. **Grounding:** every technical claim, number, method detail, and result must
   trace to the provided `full_text`. If it isn't in the paper, cut it — except
   clearly-labeled analogies (§6) and the one-sentence opinion in §9-structure.
2. **No fabrication:** paper title, authors, method names, numbers, baselines,
   and URLs are copied from the source, not reconstructed from memory.
3. **Math is correct and explained** (§7). A wrong or unexplained equation fails.
4. **Analogies are accurate and labeled as the author's own** (§6).
5. **Figures not reproduced** (§8).
6. **No hype/clickbait/emoji decoration** (§2). Opinion only in the one labeled
   takeaway sentence.
7. **Length 1,500–3,000 words.**
8. **No em dashes** (the `—` character) anywhere; use a period, comma, colon, or
   parentheses instead.
9. **No sensitive/pen-name/real-name-unsafe content.**

## 10. Bilingual rules (EN primary + KO)

- The **English post is canonical.** Generate a **Korean version** in the same
  run: `_posts/YYYY-MM-DD-research-radar-ko.md` with `lang: ko` and
  `translated_url` to the EN post.
- **URL convention:** the TASK gives you the exact slug. EN is `/blog/<SLUG>/`,
  KO is `/blog/<SLUG>-ko/`. Use these exact paths for the toggle and
  `translated_url`.
- Top of each post: `[EN](/blog/<slug>/) · [한국어](/blog/<slug>-ko/)`.
- Translation is faithful: same claims, math, analogies, numbers, links. Keep
  technical terms in English on first use with a Korean gloss, e.g.
  "KV 캐시(KV cache)". The reviewer checks EN↔KO parity.

## 11. Title-card spec (free, no generative images)

- HTML/CSS → PNG (Pillow in the pipeline). No AI-generated imagery.
- 1200 × 630, < 80 KB PNG, path `/images/radar/YYYY-MM-DD-card.png`.
- Content: "RESEARCH RADAR", the paper's short name, and the date. Fixed brand
  palette, one typeface.

## 12. Automated review checklist (the reviewer pass)

The reviewer receives **the draft + the paper's full text** and verifies, one by
one. **Any FAIL quarantines the post (not published):**

- [ ] Every technical claim/number/method detail is supported by `full_text`.
- [ ] Paper title, authors, method names, baselines, and URL match the source.
- [ ] Each equation is correct and every symbol is explained (§7).
- [ ] Analogies are technically accurate and not attributed to the authors (§6).
- [ ] No paper figures are reproduced; the paper is linked (§8).
- [ ] Opinion appears only in the single labeled takeaway sentence.
- [ ] Length is 1,500–3,000 words; tone matches §2 (no hype/clickbait).
- [ ] No em dash (`—`) anywhere in the post.
- [ ] EN and KO carry the same claims, math, analogies, and links (§10).
- [ ] Front matter valid; title, excerpt, tags, teaser, `translated_url` present.
- [ ] No sensitive/pen-name/real-name-unsafe content.

The reviewer outputs a short PASS/FAIL report with the specific failing line for
any FAIL. Grounding is checked against the full text, **not** vibes: a claim with
no support in the paper fails.

## 13. Worked micro-examples

**Good title:** `PagedAttention: paging the KV cache to serve LLMs 2–4× faster`
**Bad title:** `🚀 The INSANE trick that makes LLMs 4x faster!!`

**Good analogy framing:** "Think of the KV cache as a concert hall booked for its
maximum 2,048 seats even though only 500 fans show up — the empty 1,548 are
reserved and unusable by anyone else. That waste is *internal fragmentation*, and
it's what PagedAttention attacks."
**Bad:** "The KV cache is basically just memory and it gets full." (no mechanism)
