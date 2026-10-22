#!/usr/bin/env bash
# Research Radar — local pipeline orchestrator.
#
#   fetch sources -> generate (Claude Code) -> review (Claude Code)
#     -> PASS: translate KO, render title card, write posts, commit+push
#     -> FAIL: quarantine the draft (never published)
#
# Runs LOCALLY under your Claude Max login (Claude Code CLI), so the generate
# and review passes use your Max quota, not per-token API billing. See README.md.
#
# Safety: DRY_RUN=1 by default — it does everything EXCEPT commit/push.
# Set DRY_RUN=0 to actually publish.
set -euo pipefail

cd "$(dirname "$0")"                      # _automation/
REPO="$(cd .. && pwd)"
WORK="./work"; mkdir -p "$WORK"
CLAUDE_BIN="${CLAUDE_BIN:-claude}"        # Claude Code CLI, logged in with Max
CLAUDE_ARGS="${CLAUDE_ARGS:--p}"          # print/headless mode
DRY_RUN="${DRY_RUN:-1}"

run_claude() {                            # prompt-file -> stdout
  "$CLAUDE_BIN" $CLAUDE_ARGS "$(cat "$1")"
}

render_prompt() {                         # template sources [draft] -> stdout
  STYLE="$REPO/_automation/STYLE_GUIDE.md" TPL="$1" SRC="$2" DRAFT="${3:-}" python3 - <<'PY'
import os
t = open(os.environ["TPL"]).read()
t = t.replace("{{STYLE_GUIDE}}", open(os.environ["STYLE"]).read())
t = t.replace("{{SOURCES}}", open(os.environ["SRC"]).read())
if os.environ.get("DRAFT"):
    t = t.replace("{{DRAFT}}", open(os.environ["DRAFT"]).read())
print(t)
PY
}

echo "[1/5] fetch sources"
if ! python3 fetch_sources.py; then
  echo "thin/empty day — nothing to publish. exiting."; exit 0
fi
SRC="$WORK/sources.json"
DATE="$(python3 -c 'import json;print(json.load(open("work/sources.json"))["date"])')"

echo "[2/5] generate (EN)"
render_prompt prompts/generate.md "$SRC" > "$WORK/gen_prompt.txt"
run_claude "$WORK/gen_prompt.txt" > "$WORK/draft-en.md"

echo "[3/5] review"
render_prompt prompts/review.md "$SRC" "$WORK/draft-en.md" > "$WORK/rev_prompt.txt"
run_claude "$WORK/rev_prompt.txt" | tee "$WORK/review.txt"
if ! head -1 "$WORK/review.txt" | grep -q "VERDICT: PASS"; then
  mkdir -p "$WORK/quarantine"
  mv "$WORK/draft-en.md" "$WORK/quarantine/$DATE-FAILED.md"
  echo "REVIEW FAILED — quarantined, not published. See $WORK/review.txt"
  exit 0
fi

echo "[4/5] translate (KO) + render card"
cat prompts/translate.md "$WORK/draft-en.md" > "$WORK/ko_prompt.txt"
run_claude "$WORK/ko_prompt.txt" > "$WORK/draft-ko.md" || true
THEME="$(grep -m1 '^title:' "$WORK/draft-en.md" | sed 's/.*—[[:space:]]*//; s/"//g')"
[ -z "$THEME" ] && THEME="today"
python3 render_card.py "$DATE" "$THEME" || echo "[warn] card render skipped (install Pillow)"

echo "[5/5] write posts + publish"
cp "$WORK/draft-en.md" "$REPO/_posts/$DATE-research-radar.md"
[ -s "$WORK/draft-ko.md" ] && cp "$WORK/draft-ko.md" "$REPO/_posts/$DATE-research-radar-ko.md"

if [ "$DRY_RUN" = "0" ]; then
  cd "$REPO"
  git add "_posts/$DATE-research-radar"*.md "images/radar/$DATE-card.png" 2>/dev/null || true
  git commit -q -m "Research Radar — $DATE" && git push origin master
  echo "published $DATE"
else
  echo "DRY_RUN=1 — wrote files under _posts/ but did not commit. Review, then rerun with DRY_RUN=0."
fi
