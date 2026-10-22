# Research Radar — automation

Local pipeline that writes a daily research digest to `/blog/`.
Everything here lives under `_automation/`, which Jekyll ignores (never published).

```
_automation/
  STYLE_GUIDE.md     # editorial source of truth (writer + reviewer both read it)
  fetch_sources.py   # GitHub trending + arXiv -> work/sources.json  (stdlib only)
  render_card.py     # 1200x630 title card -> /images/radar/<date>-card.png  (Pillow)
  prompts/
    generate.md      # writer prompt template ({{STYLE_GUIDE}}/{{SOURCES}})
    review.md        # reviewer prompt template ({{...}}/{{DRAFT}})
  run.sh             # orchestrator: fetch -> generate -> review -> publish
  work/              # transient (gitignored): sources.json, drafts, quarantine
```

## How it stays free

The generate and review passes call the **Claude Code CLI** (`claude -p`), which
runs under your **Max subscription** quota — not per-token API billing. So it
must run on a machine where you're logged into Claude Code with Max (i.e. your
own computer via cron), **not** on GitHub's cloud runners (they can't use your
Max login). Hosting, fetching, and the title card are all free. No generative
images. See the project chat notes for the cost rationale.

> Heads up on Max usage: a clean post is ~3 Claude Code runs (generate, review,
> KO translate). A review FAIL re-generates with the reviewer's notes and
> re-reviews, up to `MAX_ATTEMPTS` (default 3) before quarantining — so a bad day
> can reach ~7 runs. Keep an eye on your Max weekly cap if you raise the post
> count or `MAX_ATTEMPTS`.

## Setup

```bash
pip install pillow          # only dependency (title card); fetch is stdlib
claude --version            # Claude Code CLI, logged in with Max
```

## Run

```bash
cd _automation
./run.sh                    # DRY_RUN=1 by default: writes posts but does NOT push
DRY_RUN=0 ./run.sh          # actually commit + push -> GitHub Pages deploys
```

Overrides:

- `CLAUDE_BIN` (default `claude`).
- `GEN_ARGS` / `REVIEW_ARGS` (both default `-p`) — the flags for the generate+
  translate pass and the review pass. Both use the strong (default Max) model;
  pin one explicitly with `--model` if you want (e.g. `GEN_ARGS="-p --model opus"`).
  The review is meant to run at a slightly **lower effort** than generation — it
  is already a focused checklist (see `prompts/review.md`), and if your CLI
  exposes an effort/thinking flag you can add it to `REVIEW_ARGS`.
- `MAX_ATTEMPTS` (default `3`) — on a review FAIL, the writer regenerates with
  the reviewer's notes and is re-reviewed, up to this many attempts before the
  day is quarantined.
- `KO` is **on** by design: each run writes an English post and a faithful Korean
  translation, and `/blog/` shows the English canonical with an in-post language
  toggle to the Korean version.

Selection: `fetch_sources.py` has a **soft LLM preference** — LLM-related repos/
papers float to the top, but general dev/ML items still appear. Tune `N_REPOS`,
`N_PAPERS`, `POOL`, `LLM_KW`, and `ARXIV_CATS` (default `cs.CL, cs.AI, cs.LG`) at
the top of that file.

## Flow / guarantees

1. **fetch** → `work/sources.json` (exact URLs; the grounding file). A thin or
   empty day exits cleanly without publishing.
2. **generate → review (loop)** → the writer drafts only from the sources; the
   reviewer verifies every claim against them (STYLE_GUIDE §11). On `VERDICT:
   FAIL` the writer regenerates with the reviewer's notes and is re-reviewed,
   up to `MAX_ATTEMPTS` times. If every attempt fails, the drafts go to
   `work/quarantine/` and **nothing is published** — no human gate, the gate is
   automated.
4. **publish** → EN + KO posts to `_posts/`, title card to `/images/radar/`,
   one commit, push. `/blog/` lists the EN canonical only (KO via in-post toggle).

## Cron (example — once daily at 08:30 local)

```cron
30 8 * * *  cd /home/jang/PORTFOLIO/HyeonjongJang.github.io/_automation && DRY_RUN=0 ./run.sh >> work/cron.log 2>&1
```

## Tuning points (by design, left open)

- `fetch_sources.py`: `N_REPOS`/`N_PAPERS`/`POOL`, `LLM_KW` soft preference,
  `ARXIV_CATS`, or swap trending for topic search.
- `GEN_ARGS` / `REVIEW_ARGS`: model pin and effort per pass (see Overrides).
- `render_card.py`: fonts/palette/layout, optional data chart. For a Korean
  title card, swap the font to a Hangul-capable TTF (Noto Sans KR / Pretendard).
