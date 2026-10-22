# Research Radar — automation

Local pipeline that publishes an in-depth explainer of **one AI/ML paper** to
`/blog/` — background, intuition/analogies, the mechanism step by step, the
central math (every symbol explained), results, and honest limitations.
Everything here lives under `_automation/`, which Jekyll ignores (never published).

```
_automation/
  STYLE_GUIDE.md     # editorial source of truth (writer + reviewer both read it)
  fetch_sources.py   # pick 1 notable paper + fetch its FULL TEXT -> work/sources.json
  render_card.py     # 1200x630 title card -> /images/radar/<date>-card.png  (Pillow)
  sanitize.py        # strip model preamble / code fences before front matter
  prompts/
    generate.md      # writer prompt ({{STYLE_GUIDE}}/{{SOURCES}})
    review.md        # reviewer prompt ({{...}}/{{DRAFT}})
    translate.md     # faithful KO translation prompt
  run.sh             # orchestrator: fetch -> (generate+review loop) -> KO -> card -> publish
  work/              # transient (gitignored): sources.json, drafts, quarantine
```

## How it stays free

The generate / review / translate passes call the **Claude Code CLI** (`claude
-p`), which runs under your **Max subscription** quota — not per-token API
billing. So it must run where you're logged into Claude Code with Max (your own
machine via cron), **not** on GitHub's cloud runners. Hosting, paper fetching,
and the title card are all free; no generative images.

> Max usage: a clean post is ~3 Claude Code runs (generate, review, KO translate),
> but each works over a paper's **full text**, so these are large-context calls.
> A review FAIL re-generates with the reviewer's notes and re-reviews, up to
> `MAX_ATTEMPTS` (default 3) before quarantining — a bad day can reach ~7 runs.
> Watch your Max weekly cap.

## Setup

```bash
pip install pillow          # only dependency (title card); fetch is stdlib
claude --version            # Claude Code CLI, logged in with Max
```

## Run

```bash
cd _automation
./run.sh                    # DRY_RUN=1 by default: writes posts but does NOT push
DRY_RUN=0 ./run.sh          # commit + push -> GitHub Pages deploys
```

Overrides:

- `CLAUDE_BIN` (default `claude`).
- `GEN_ARGS` / `REVIEW_ARGS` (both default `-p`) — flags for the generate+translate
  pass and the review pass. Both use the strong (default Max) model; pin with
  `--model` if you like. The review is a focused verification, so it runs at
  slightly lower effort; add your CLI's effort flag to `REVIEW_ARGS` if it has one.
- `MAX_ATTEMPTS` (default `3`) — on a review FAIL, regenerate with the reviewer's
  notes and re-review, up to this many attempts before quarantining the day.
- `KO` is on by design: EN canonical + faithful Korean translation; `/blog/`
  lists EN only, with an in-post language toggle.
- `GITHUB_TOKEN` (optional) — only used if you later re-add GitHub sources.

Selection (`fetch_sources.py`): picks one notable paper — **Hugging Face Daily
Papers** (community-upvoted, LLM-heavy) first, with a soft LLM lean, falling back
to recent arXiv. Then fetches **full text** (arXiv HTML → ar5iv); a paper without
retrievable full text is skipped. Tune `CANDIDATES`, `MAX_CHARS`, `LLM_KW`,
`ARXIV_CATS` at the top of the file.

## Flow / guarantees

1. **fetch** → `work/sources.json`: one paper's metadata **and full text** (the
   grounding file). No paper with retrievable full text → exits without publishing.
2. **generate → review (loop)** → the writer produces a deep-dive grounded only in
   the full text; the reviewer verifies every claim, number, equation, and analogy
   against it (STYLE_GUIDE §12). On `VERDICT: FAIL` the writer regenerates with the
   reviewer's notes, up to `MAX_ATTEMPTS`. If every attempt fails, the drafts go to
   `work/quarantine/` and **nothing is published** — no human gate, the gate is
   automated.
3. **publish** → EN + KO posts to `_posts/`, title card to `/images/radar/`, one
   commit, push. `/blog/` lists the EN canonical only (KO via in-post toggle).

## Cron (example — once daily at 08:30 local)

```cron
30 8 * * *  cd /home/jang/PORTFOLIO/HyeonjongJang.github.io/_automation && DRY_RUN=0 ./run.sh >> work/cron.log 2>&1
```

## Tuning points (by design, left open)

- `fetch_sources.py`: selection source/ranking, `CANDIDATES`, `MAX_CHARS`,
  `LLM_KW`, `ARXIV_CATS`.
- `GEN_ARGS` / `REVIEW_ARGS` / `MAX_ATTEMPTS`.
- `render_card.py`: fonts/palette/layout. For a Korean title card, swap the font
  to a Hangul-capable TTF (Noto Sans KR / Pretendard).
- `STYLE_GUIDE.md`: the editorial bar — tighten after reading real output.
