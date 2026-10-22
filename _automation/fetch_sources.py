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
import re
import sys
import urllib.request
import xml.etree.ElementTree as ET
from datetime import date
from pathlib import Path

N_REPOS = 2
N_PAPERS = 1
# arXiv categories aligned with the author's themes (LLM / MAPF / adaptive search).
ARXIV_CATS = ["cs.AI", "cs.LG", "cs.RO"]
UA = {"User-Agent": "research-radar/0.1 (personal digest; +https://hyeonjongjang.github.io)"}
WORK = Path(__file__).parent / "work"


def _get(url: str, timeout: int = 20) -> str:
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode("utf-8", "replace")


def fetch_trending_repos(n: int) -> list[dict]:
    """Scrape github.com/trending. Returns name/url/description/language/stars."""
    html = _get("https://github.com/trending?since=daily")
    repos: list[dict] = []
    # Each repo heading: <h2 ...><a href="/owner/repo" ...>
    for m in re.finditer(r'<h2[^>]*>\s*<a href="/([^"/]+/[^"?]+)"', html):
        slug = m.group(1).strip()
        if slug.count("/") != 1:
            continue
        block = html[m.end(): m.end() + 2000]
        desc = re.search(r'<p[^>]*col-9[^>]*>\s*(.*?)\s*</p>', block, re.S)
        lang = re.search(r'itemprop="programmingLanguage">([^<]+)<', block)
        stars = re.search(r'/stargazers">\s*([\d,]+)', block)
        repos.append({
            "type": "repo",
            "name": slug,
            "url": f"https://github.com/{slug}",
            "description": re.sub(r"<[^>]+>", "", desc.group(1)).strip() if desc else "",
            "language": lang.group(1).strip() if lang else "",
            "stars": stars.group(1).strip() if stars else "",
        })
        if len(repos) >= n:
            break
    return repos


def fetch_recent_papers(n: int) -> list[dict]:
    """arXiv API, newest in the chosen categories. title/url/authors/abstract."""
    cat = "+OR+".join(f"cat:{c}" for c in ARXIV_CATS)
    url = (
        "http://export.arxiv.org/api/query?"
        f"search_query={cat}&sortBy=submittedDate&sortOrder=descending&max_results={n}"
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
    return papers


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
