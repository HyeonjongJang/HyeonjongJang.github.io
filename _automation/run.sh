#!/usr/bin/env bash
# Research Radar — local pipeline orchestrator (paper / repo deep-dives).
#
#   run.sh [paper|repo]   # no arg -> alternate daily (paper on even day-of-year,
#                         #           repo on odd), so cron produces one type a day
#
# For each type:  fetch -> (generate+review loop) -> KO translate -> card -> publish
#   PASS -> EN+KO posts, title card, one commit, push
#   FAIL (after MAX_ATTEMPTS) -> quarantine, publish nothing
#
# Runs LOCALLY under your Claude Max login (Claude Code CLI). DRY_RUN=1 by default
# (does everything except commit/push). Set DRY_RUN=0 to publish. See README.md.
set -euo pipefail

cd "$(dirname "$0")"                      # _automation/
REPO="$(cd .. && pwd)"
WORK="./work"; mkdir -p "$WORK"
CLAUDE_BIN="${CLAUDE_BIN:-claude}"
GEN_ARGS="${GEN_ARGS:--p}"                # generate + translate: full effort
REVIEW_ARGS="${REVIEW_ARGS:--p}"         # review: slightly lower effort
DRY_RUN="${DRY_RUN:-1}"

# Post type: explicit arg, else alternate by day-of-year parity.
TYPE="${1:-}"
if [ -z "$TYPE" ]; then
  if [ $(( 10#$(date +%j) % 2 )) -eq 0 ]; then TYPE=paper; else TYPE=repo; fi
fi
case "$TYPE" in
  paper) FETCH=fetch_paper.py; GUIDE=STYLE_GUIDE_paper.md; GEN=prompts/generate_paper.md; REV=prompts/review_paper.md; SLUG_BASE=research-radar; NOUN=paper;;
  repo)  FETCH=fetch_repo.py;  GUIDE=STYLE_GUIDE_repo.md;  GEN=prompts/generate_repo.md;  REV=prompts/review_repo.md;  SLUG_BASE=repo;           NOUN=repo;;
  *) echo "usage: run.sh [paper|repo]"; exit 2;;
esac

run_claude() { "$CLAUDE_BIN" $1 "$(cat "$2")"; }   # args prompt-file -> stdout

# render_prompt <template> [draft] : fill {{STYLE_GUIDE}}/{{SOURCES}}/{{SLUG}}/{{DATE}}/{{DRAFT}}
render_prompt() {
  RR_GUIDE="$REPO/_automation/$GUIDE" RR_TPL="$1" RR_DRAFT="${2:-}" \
  RR_SLUG="$SLUG" RR_DATE="$DATE" python3 - <<'PY'
import os
t = open(os.environ["RR_TPL"]).read()
t = t.replace("{{STYLE_GUIDE}}", open(os.environ["RR_GUIDE"]).read())
t = t.replace("{{SOURCES}}", open("work/sources.json").read())
t = t.replace("{{SLUG}}", os.environ["RR_SLUG"]).replace("{{DATE}}", os.environ["RR_DATE"])
if os.environ.get("RR_DRAFT"):
    t = t.replace("{{DRAFT}}", open(os.environ["RR_DRAFT"]).read())
print(t)
PY
}

echo "[1/5] fetch sources ($TYPE)"
python3 "$FETCH" || { echo "nothing to publish today — exiting."; exit 0; }
DATE="$(python3 -c 'import json;print(json.load(open("work/sources.json"))["date"])')"
SLUG="$DATE-$SLUG_BASE"

echo "[2-3/5] generate + review (up to ${MAX_ATTEMPTS:=3} attempts)"
passed=0
for a in $(seq 1 "$MAX_ATTEMPTS"); do
  echo "  attempt $a/$MAX_ATTEMPTS: generate"
  render_prompt "$GEN" > "$WORK/gen_prompt.txt"
  if [ "$a" -gt 1 ] && [ -s "$WORK/review.txt" ]; then
    { echo; echo "=== YOUR PREVIOUS DRAFT FAILED REVIEW — fix EACH point, then rewrite the whole post ==="
      cat "$WORK/review.txt"; } >> "$WORK/gen_prompt.txt"
  fi
  run_claude "$GEN_ARGS" "$WORK/gen_prompt.txt" > "$WORK/draft-en.md"

  echo "  attempt $a/$MAX_ATTEMPTS: review"
  render_prompt "$REV" "$WORK/draft-en.md" > "$WORK/rev_prompt.txt"
  run_claude "$REVIEW_ARGS" "$WORK/rev_prompt.txt" | tee "$WORK/review.txt"
  if head -1 "$WORK/review.txt" | grep -q "VERDICT: PASS"; then passed=1; break; fi
  echo "  attempt $a FAILED review."
  mkdir -p "$WORK/quarantine"; cp "$WORK/draft-en.md" "$WORK/quarantine/$SLUG-FAILED-attempt$a.md"
done
if [ "$passed" != "1" ]; then
  echo "REVIEW FAILED after $MAX_ATTEMPTS attempts — quarantined, not published. See $WORK/quarantine/"
  exit 0
fi

echo "[4/5] translate (KO) + render card"
cat prompts/translate.md "$WORK/draft-en.md" > "$WORK/ko_prompt.txt"
run_claude "$GEN_ARGS" "$WORK/ko_prompt.txt" > "$WORK/draft-ko.md" || true
# Card theme = short name (title text before the first colon).
THEME="$(python3 - "$WORK/draft-en.md" <<'PY'
import re, sys
t = open(sys.argv[1], encoding="utf-8").read()
m = re.search(r'^title:\s*"?(.*?)"?\s*$', t, re.M)
print((m.group(1) if m else "").split(":")[0].strip()[:90])
PY
)"
[ -z "$THEME" ] && THEME="today"
python3 render_card.py "$DATE" "$THEME" "$NOUN" || echo "[warn] card render skipped (install Pillow)"

echo "[5/5] write posts + publish"
python3 sanitize.py "$WORK/draft-en.md"
cp "$WORK/draft-en.md" "$REPO/_posts/$SLUG.md"
if [ -s "$WORK/draft-ko.md" ]; then
  python3 sanitize.py "$WORK/draft-ko.md"
  cp "$WORK/draft-ko.md" "$REPO/_posts/$SLUG-ko.md"
fi

if [ "$DRY_RUN" = "0" ]; then
  cd "$REPO"
  git add "_posts/$SLUG"*.md "images/radar/$DATE-card.png" 2>/dev/null || true
  git commit -q -m "Research Radar ($TYPE) — $DATE" && git push origin master
  echo "published $SLUG"
else
  echo "DRY_RUN=1 — wrote _posts/$SLUG.md but did not commit. Review, then rerun with DRY_RUN=0."
fi
