# Research Radar — Editorial Style Guide

> The single source of truth for the automated blog pipeline. **Both** the
> *writer* pass and the *reviewer* pass of Claude Code read this file on every
> run. If a rule here conflicts with a model's instinct, this file wins.
> Location: `_automation/` is ignored by Jekyll, so this file is never published.

---

## 1. Purpose, audience, positioning

- **What this is:** *Research Radar* — a short, source-grounded digest of a few
  notable AI/ML GitHub repositories and papers, each with a one-line human take.
- **Who reads it:** researchers, graduate students, and hiring/admissions
  committees. **Not** a general-traffic/SEO audience.
- **Positioning:** a curated adjunct to a research portfolio centered on
  automatic heuristic design with LLMs, multi-agent path finding (MAPF), and
  adaptive search control. The blog must read as *a researcher's curated notes*,
  never as a content farm. When in doubt, bias toward the author's own research
  themes in selection and framing.

## 2. Voice & tone

**Do:** precise, calm, specific, sourced. Explain *what is new* and *why it
matters* in plain language. Prefer concrete nouns and numbers over adjectives.
State limitations honestly. One clearly-labeled personal take per item.

**Don't:** hype ("game-changer", "revolutionary", "you won't believe"),
clickbait, listicle padding, emoji-as-decoration, fake urgency, vague praise
("amazing work"), or any claim the source doesn't support.

Reading level: a second-year grad student skims it in 60 seconds and knows
whether to click through.

## 3. Reference exemplars (borrow principles, never prose)

Derive *principles* from these; never copy wording (plagiarism + duplicate-content risk).

- **The Batch (DeepLearning.AI)** — neutral "what happened / why it matters" framing.
- **Hugging Face Daily Papers** — tight one-paragraph paper summaries; link-first.
- **Sebastian Raschka** — plain-language explanation of method + takeaway.
- **Import AI (Jack Clark)** — "why this matters" sections; sober tone on hype.
- **Lil'Log (Lilian Weng)** — accuracy and definitional care.
- **Papers with Code / arXiv** — canonical linking, exact titles, author credit.

**Tone from the research digests; structure/readability from general best
practice (headings, TL;DR, scannability, meta discipline) — but never their
traffic-optimized clickbait.**

## 4. Post structure (template)

Every post is one day's digest. Order:

1. **Title** — see §5.
2. **One-line TL;DR** (italic) — what today's picks are about, ≤ 25 words.
3. **Repositories** section — up to N repo blocks (§6).
4. **Papers** section — up to M paper blocks (§6).
5. **Sources** — a bullet list repeating every external link used.

Default scope: **2 repositories + 1 paper** (tunable). A thin day is fine — skip
an item rather than pad it. Never invent items to hit a count.

### Jekyll front matter (exact keys)

```yaml
---
title: "Research Radar — <Mon DD, YYYY>"
date: YYYY-MM-DD
excerpt: "<= 155 chars, plain summary of the day's picks, no clickbait>"
tags:
  - research-radar
  - <2-4 topical tags, lowercase-hyphenated>
header:
  teaser: /images/radar/YYYY-MM-DD-card.png   # title card (§9)
lang: en
translated_url: /blog/<slug>-ko/              # link to the KO version (§8)
---
```

## 5. Title rules

- Format: `Research Radar — <Mon DD, YYYY>` for the daily digest. Optional
  subtitle after an em dash naming the theme, e.g. `… — MAPF solvers & LLM agents`.
- No numbers-as-bait ("7 repos that..."), no questions, no ALL CAPS, no emoji.
- Slug: `YYYY-MM-DD-research-radar` (KO version: append `-ko`).

## 6. Per-item block format

**Repository**
```
### <exact repo name> — <one-line what-it-is>
[`owner/repo`](<github url>) · <language> · <star count as of date>

- **What's new:** <1-2 sentences, grounded in the repo's README/release>
- **Why it matters:** <1 sentence>
- **Caveat:** <1 sentence — maturity, scope, or unknowns>
- **Take:** <1 line, clearly the author's opinion>
```

**Paper**
```
### <exact paper title>
[<arXiv/venue id>](<url>) · <authors et al.> · <year>

- **Claim:** <what the paper claims, grounded in the abstract>
- **Why it matters:** <1 sentence>
- **Caveat:** <1 sentence — e.g. "abstract-only read", eval scope, no code>
- **Take:** <1 line, clearly the author's opinion>
```

If the summary is based only on an abstract (not the full paper), the **Caveat**
must say so. Never imply a depth of reading that did not happen.

## 7. Hard rules (non-negotiable — the reviewer enforces these)

1. **Grounding:** every factual sentence must trace to a fetched source
   (README, release notes, abstract, repo metadata). If it isn't in the source,
   cut it.
2. **No fabrication:** repo names, paper titles, author names, numbers, and URLs
   must be real and copied, not reconstructed from memory. Verify each link.
3. **Attribution:** always credit authors/owners; always link the original.
4. **Opinion is labeled:** personal judgment appears only under **Take**, never
   smuggled into **What's new / Claim**.
5. **Length:** a repo/paper block ≤ ~120 words; whole post ≤ ~700 words
   (per language).
6. **No hype, no clickbait, no emoji decoration** (§2).
7. **No sensitive/pen-name content**, nothing that isn't safe under the author's
   real name. Never link pen-name work. (See portfolio-wide rule.)
8. **Copyright:** quote ≤ 1 short sentence from any source; summarize in your own
   words; do not reproduce figures or long excerpts. Link, don't rehost.

## 8. Bilingual rules (EN primary + KO)

- The **English post is canonical.** Generate a **Korean version** in the same
  run as a separate file: `_posts/YYYY-MM-DD-research-radar-ko.md` with
  `lang: ko` and `translated_url` pointing back to the EN post.
- Top of each post: a one-line language toggle (`EN · 한국어`) linking the pair.
- Translation is **faithful, not re-interpreted** — same claims, same caveats,
  same links. Technical terms keep their English form on first use with a Korean
  gloss where natural (e.g. "다중로봇 경로계획(MAPF)").
- If the KO pass would change meaning to sound smoother, keep meaning and accept
  a plainer sentence. The reviewer checks EN↔KO claim parity.

## 9. Title-card spec (free, no generative images)

- **Render:** an HTML/CSS template → PNG (headless Chromium/Playwright) or Pillow.
  No AI-generated decorative images.
- **Size:** 1200 × 630 (OG ratio). **Weight:** keep < 80 KB (PNG, optimized).
- **Path:** `/images/radar/YYYY-MM-DD-card.png`.
- **Content:** site/author mark, "Research Radar", the date, and the day's theme
  line. Fixed brand palette; one typeface. No stock photos, no clip art.
- **Charts (optional):** if a real number is worth showing (e.g. star growth),
  render a small matplotlib/mermaid chart from actual data — never a decorative
  graphic.

## 10. Selection & sourcing

- **Repos:** GitHub trending (scrape `github.com/trending`) or Search API
  (`sort:stars`, recent window). Prefer items adjacent to the author's themes.
- **Papers:** arXiv (cs.AI/cs.LG/cs.RO), Hugging Face Daily Papers, Papers with
  Code trending, Semantic Scholar. "Hot journal" = trending preprints, not a
  fixed journal feed.
- Record the exact source URL for every item for the Sources section and for the
  reviewer's grounding check.
- Skip anything you cannot fetch and verify. A smaller honest digest beats a
  padded one.

## 11. Automated review checklist (the reviewer pass)

The reviewer receives **the draft + the fetched source material** and verifies,
one by one. **Any FAIL quarantines the post to a `draft` branch (not published):**

- [ ] Every claim is supported by the provided sources (no ungrounded sentences).
- [ ] All repo names, paper titles, authors, numbers, and URLs match the sources.
- [ ] Every link resolves (and points where the text says).
- [ ] Abstract-only summaries are labeled as such in **Caveat**.
- [ ] Opinion appears only under **Take**.
- [ ] No hype/clickbait/emoji-decoration; tone matches §2.
- [ ] Length limits respected (§7.5).
- [ ] EN and KO versions carry the same claims, caveats, and links (§8).
- [ ] Front matter valid; slug, tags, excerpt, teaser present and well-formed.
- [ ] No sensitive/pen-name/real-name-unsafe content.

The reviewer outputs a short PASS/FAIL report with the specific failing line for
any FAIL. Grounding is checked against sources, **not** vibes: if a sentence has
no source, it fails — the writer must cut or fix it.

## 12. Worked micro-examples

**Good title:** `Research Radar — Oct 24, 2026 — anytime MAPF & LLM agents`
**Bad title:** `🚀 5 INSANE AI repos you NEED to see today!!`

**Good item take:** `Take: the held-out eval is the honest part here — most LNS
papers skip it.`
**Bad item take:** `This is a total game-changer for the whole field.`
