#!/usr/bin/env python3
"""Fetch raw source material for a Research Radar digest.

Stdlib only (urllib / re / xml.etree) so it runs without pip installs.
Writes work/sources.json — the single grounding file that BOTH the writer
and the reviewer passes read. Every item here must carry an exact URL so the
reviewer can verify claims against it.

Scope default (see STYLE_GUIDE §4/§10): top 2 repos + 1 paper. Tunable below.
This is a best-effort fetcher; GitHub's trending markup changes occasionally,
so treat the scraper as a maintenance point, not a fixed contract.
"""
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import date, timedelta
from pathlib import Path

N_REPOS = 2
N_PAPERS = 1
POOL = 30  # candidates fetched before the LLM-lean ranking below trims to N.
# Soft LLM preference (NOT a hard filter): items matching these float to the top,
# but non-LLM items still appear when there aren't enough LLM ones — the author
# is a researcher *and* a developer, so general dev/ML items are welcome too.
LLM_KW = ["llm", "language model", "large language model", "gpt", "llama",
          "transformer", "rag", "retrieval-augmented", "agent", "fine-tun",
          "instruction", "chatbot", "prompt", "mixture-of-experts", "moe"]
# arXiv categories: cs.CL (LLM / NLP home) first, plus general AI/ML.
ARXIV_CATS = ["cs.CL", "cs.AI", "cs.LG"]
UA = {"User-Agent": "research-radar/0.1 (personal digest; +https://hyeonjongjang.github.io)"}
WORK = Path(__file__).parent / "work"


def _get(url: str, timeout: int = 20) -> str:
    headers = dict(UA)
    if "api.github.com" in url:
        headers["Accept"] = "application/vnd.github+json"
        tok = os.environ.get("GITHUB_TOKEN")  # optional: raises rate limit 60->5000/hr
        if tok:
            headers["Authorization"] = f"Bearer {tok}"
    req = urllib.request.Request(url, headers=headers)
    for attempt in range(2):  # one retry on 429 (arXiv / unauthenticated GitHub)
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return r.read().decode("utf-8", "replace")
        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt == 0:
                time.sleep(5)
                continue
            raise


def _llm_score(text: str) -> int:
    t = text.lower()
    return sum(1 for k in LLM_KW if k in t)


def fetch_trending_repos(n: int) -> list[dict]:
    """GitHub Search API: most-starred repos created in the last ~14 days — a
    robust 'trending' proxy. Stable JSON, unlike scraping the trending page."""
    since = (date.today() - timedelta(days=14)).isoformat()
    q = urllib.parse.quote(f"created:>{since}")
    url = (
        f"https://api.github.com/search/repositories?q={q}"
        f"&sort=stars&order=desc&per_page={POOL}"
    )
    data = json.loads(_get(url))
    repos = []
    for it in data.get("items", []):
        repos.append({
            "type": "repo",
            "name": it["full_name"],
            "url": it["html_url"],
            "description": (it.get("description") or "").strip(),
            "language": it.get("language") or "",
            "stars": str(it.get("stargazers_count", "")),
        })
    # Stable sort keeps star order among equal scores; LLM-matching repos rise.
    repos.sort(key=lambda r: _llm_score(r["name"] + " " + r["description"]), reverse=True)
    return repos[:n]


def fetch_recent_papers(n: int) -> list[dict]:
    """arXiv API, newest in the chosen categories. title/url/authors/abstract."""
    cat = "+OR+".join(f"cat:{c}" for c in ARXIV_CATS)
    url = (
        "http://export.arxiv.org/api/query?"
        f"search_query={cat}&sortBy=submittedDate&sortOrder=descending&max_results={POOL}"
    )
    feed = _get(url)
    ns = {"a": "http://www.w3.org/2005/Atom"}
    papers = []
    for e in ET.fromstring(feed).findall("a:entry", ns):
        link = e.find("a:id", ns).text.strip()
        papers.append({
            "type": "paper",
            "title": " ".join(e.find("a:title", ns).text.split()),
            "url": link,
            "authors": [a.find("a:name", ns).text for a in e.findall("a:author", ns)],
            "abstract": " ".join(e.find("a:summary", ns).text.split()),
            "published": (e.find("a:published", ns).text or "")[:10],
        })
    # LLM-matching papers rise; newest order preserved among equal scores.
    papers.sort(key=lambda p: _llm_score(p["title"] + " " + p["abstract"]), reverse=True)
    return papers[:n]


def main() -> int:
    WORK.mkdir(exist_ok=True)
    out = {"date": date.today().isoformat(), "repos": [], "papers": []}
    try:
        out["repos"] = fetch_trending_repos(N_REPOS)
    except Exception as e:  # noqa: BLE001 - keep going; a thin day is allowed
        print(f"[warn] repo fetch failed: {e}", file=sys.stderr)
    try:
        out["papers"] = fetch_recent_papers(N_PAPERS)
    except Exception as e:  # noqa: BLE001
        print(f"[warn] paper fetch failed: {e}", file=sys.stderr)

    (WORK / "sources.json").write_text(json.dumps(out, indent=2, ensure_ascii=False))
    print(f"wrote {WORK/'sources.json'}: {len(out['repos'])} repos, {len(out['papers'])} papers")
    # Signal a thin/empty day so the orchestrator can skip publishing.
    return 0 if (out["repos"] or out["papers"]) else 3


if __name__ == "__main__":
    raise SystemExit(main())
