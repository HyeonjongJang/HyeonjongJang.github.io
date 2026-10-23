#!/usr/bin/env python3
"""Pick ONE trending GitHub repo and fetch its README for a tool explainer.

Writes work/sources.json — the grounding file BOTH the writer and reviewer read.
The explainer is checked against the README, so a substantial README is required:
a candidate with a thin/missing README is skipped.

Selection: GitHub Search API, most-starred repos created recently (a robust
"trending" proxy), with a soft LLM lean.
"""
import base64
import json
import sys
import urllib.parse
from datetime import date, timedelta

from common import WORK, get, llm_score

CANDIDATES = 15         # repos to consider before taking the first with a good README
POOL = 40               # search results to rank
MIN_README = 800        # chars; below this a README is too thin to explain


def candidates() -> list[dict]:
    since = (date.today() - timedelta(days=21)).isoformat()
    q = urllib.parse.quote(f"created:>{since}")
    url = (f"https://api.github.com/search/repositories?q={q}"
           f"&sort=stars&order=desc&per_page={POOL}")
    out = []
    for it in json.loads(get(url)).get("items", []):
        out.append({
            "name": it["full_name"],
            "url": it["html_url"],
            "description": (it.get("description") or "").strip(),
            "stars": it.get("stargazers_count", 0),
            "language": it.get("language") or "",
            "topics": it.get("topics", []) or [],
            "homepage": (it.get("homepage") or "").strip(),
        })
    out.sort(key=lambda r: llm_score(r["name"] + " " + r["description"] + " " + " ".join(r["topics"])),
             reverse=True)
    return out


def fetch_readme(full_name: str) -> str | None:
    try:
        data = json.loads(get(f"https://api.github.com/repos/{full_name}/readme"))
        text = base64.b64decode(data.get("content", "")).decode("utf-8", "replace").strip()
    except Exception:  # noqa: BLE001
        return None
    return text if len(text) >= MIN_README else None


def main() -> int:
    WORK.mkdir(exist_ok=True)
    try:
        cands = candidates()
    except Exception as e:  # noqa: BLE001
        print(f"[warn] GitHub search failed: {e}", file=sys.stderr)
        cands = []

    chosen = None
    for c in cands[:CANDIDATES]:
        readme = fetch_readme(c["name"])
        if readme:
            c["readme"] = readme
            chosen = c
            break
        print(f"[skip] thin/no README for {c['name']}", file=sys.stderr)

    if not chosen:
        print("no repo with a substantial README today — skipping.")
        return 3

    (WORK / "sources.json").write_text(json.dumps({"type": "repo", "date": date.today().isoformat(),
                                                   "repo": chosen}, indent=2, ensure_ascii=False))
    print(f"wrote sources.json: {chosen['name']} ({chosen['stars']}★, "
          f"{len(chosen['readme'])} chars README)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
