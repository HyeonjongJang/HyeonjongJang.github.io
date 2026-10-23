# Research Radar — automation

Local pipeline that publishes an in-depth explainer to `/blog/`, in two post types:

- **paper** — one notable AI/ML paper, from its **full text**: problem, intuition,
  mechanism, the central math (every symbol explained), results, limitations.
- **repo** — one trending open-source project, from its **README**: what it is,
  how it works, how to use it, notable details, why it matters.

With no argument the pipeline **alternates daily** (paper on even day-of-year,
repo on odd). Everything here is under `_automation/`, which Jekyll ignores.

```
_automation/
  common.py              # shared fetch/ranking helpers
  fetch_paper.py         # pick 1 paper + FULL TEXT        -> work/sources.json
  fetch_repo.py          # pick 1 trending repo + README   -> work/sources.json
  STYLE_GUIDE_paper.md   # editorial source of truth (paper)
  STYLE_GUIDE_repo.md    # editorial source of truth (repo)
  prompts/
    generate_paper.md  review_paper.md
    generate_repo.md   review_repo.md
    translate.md         # faithful KO translation (shared)
  render_card.py         # 1200x630 title card -> /images/radar/<date>-card.png
  sanitize.py            # strip model preamble/fences; normalize math to $$…$$
  run.sh                 # orchestrator (type-parameterized)
  work/                  # transient (gitignored): sources.json, drafts, quarantine
```

## How it stays free

The generate / review / translate passes call the **Claude Code CLI** (`claude
-p`) under your **Max subscription** quota — not per-token API billing. So it must
run where you're logged into Claude Code with Max (your own machine via cron),
**not** on GitHub's cloud runners. Paper/repo fetching and the title card are free;
no generative images.

> Max usage: a clean post is ~3 Claude Code runs (generate, review, KO translate)
> over a paper's full text or a repo's README. A review FAIL re-generates with the
> reviewer's notes, up to `MAX_ATTEMPTS` (default 3) before quarantining — a bad
> day can reach ~7 runs. Watch your Max weekly cap.

## Setup

```bash
pip install pillow          # only dependency (title card); fetch is stdlib
claude --version            # Claude Code CLI, logged in with Max
```

## Run

```bash
cd _automation
./run.sh                    # alternates paper/repo by day; DRY_RUN=1 (no push)
./run.sh repo               # force a type
DRY_RUN=0 ./run.sh          # commit + push -> GitHub Pages deploys
```

Overrides:

- `CLAUDE_BIN` (default `claude`).
- `GEN_ARGS` / `REVIEW_ARGS` (both default `-p`) — flags per pass; both use the
  strong (default Max) model, review at slightly lower effort.
- `MAX_ATTEMPTS` (default `3`) — regenerate-with-notes attempts before quarantine.
- `KO` is on by design: EN canonical + faithful Korean translation; `/blog/` lists
  EN only, with an in-post toggle.
- `GITHUB_TOKEN` (optional) — raises the GitHub API rate limit for repo days.

Selection: `fetch_paper.py` uses Hugging Face Daily Papers (then arXiv) with a soft
LLM lean and requires retrievable full text. `fetch_repo.py` uses the GitHub Search
API (recent, most-starred) with a soft LLM lean and requires a substantial README.
Tune the constants at the top of each file.

## Flow / guarantees

1. **fetch** → `work/sources.json`: one paper's full text, or one repo's README
   (the grounding file). Nothing suitable today → exits without publishing.
2. **generate → review (loop)** → the writer drafts grounded only in the source;
   the reviewer verifies every claim against it (STYLE_GUIDE §§ checklists). On
   `VERDICT: FAIL` the writer regenerates with the reviewer's notes, up to
   `MAX_ATTEMPTS`. If every attempt fails, drafts go to `work/quarantine/` and
   **nothing is published** — the gate is automated, no human step.
3. **publish** → EN + KO posts to `_posts/`, title card to `/images/radar/`, one
   commit, push. `/blog/` lists the EN canonical only (KO via in-post toggle).

Slugs: paper → `/blog/<date>-research-radar/`, repo → `/blog/<date>-repo/`
(KO adds `-ko`).

## Cron (example — once daily at 08:30 local, alternating type)

```cron
30 8 * * *  cd /home/jang/PORTFOLIO/HyeonjongJang.github.io/_automation && DRY_RUN=0 ./run.sh >> work/cron.log 2>&1
```

## Tuning points (by design, left open)

- `fetch_paper.py` / `fetch_repo.py`: selection source/ranking, candidate counts,
  `LLM_KW` (in `common.py`), `ARXIV_CATS`, README/full-text size thresholds.
- `GEN_ARGS` / `REVIEW_ARGS` / `MAX_ATTEMPTS`.
- `render_card.py`: fonts/palette/layout (Hangul-capable TTF for a Korean card).
- `STYLE_GUIDE_paper.md` / `STYLE_GUIDE_repo.md`: the editorial bar — tighten after
  reading real output.
