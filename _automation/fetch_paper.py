#!/usr/bin/env python3
"""Pick ONE notable paper and fetch its FULL TEXT for a deep-dive explainer.

Writes work/sources.json — the grounding file BOTH the writer and reviewer read.
A deep dive is checked against full text, so full text (not just the abstract) is
required: a candidate without retrievable full text is skipped.

Selection: Hugging Face Daily Papers (community-upvoted, LLM-heavy) first, with a
soft LLM lean; falls back to recent arXiv. Full text: arXiv HTML, then ar5iv.
"""
import html
import json
import re
import sys
import xml.etree.ElementTree as ET
from datetime import date

from common import WORK, get, llm_score

CANDIDATES = 8          # papers to consider before taking the first with full text
MAX_CHARS = 120_000     # truncate full text to keep the prompt bounded
ARXIV_CATS = ["cs.CL", "cs.AI", "cs.LG"]


def _norm_id(arxiv_id: str) -> str:
    m = re.search(r"(\d{4}\.\d{4,5})", arxiv_id)
    return m.group(1) if m else arxiv_id.strip()


def candidates_from_hf() -> list[dict]:
    data = json.loads(get("https://huggingface.co/api/daily_papers?limit=50"))
    out = []
    for item in data:
        p = item.get("paper", item)
        pid = p.get("id") or p.get("arxiv_id") or ""
        if not pid:
            continue
        out.append({
            "id": _norm_id(pid),
            "title": " ".join((p.get("title") or "").split()),
            "abstract": " ".join((p.get("summary") or p.get("abstract") or "").split()),
            "authors": [a.get("name", "") for a in (p.get("authors") or []) if isinstance(a, dict)],
            "upvotes": p.get("upvotes", item.get("upvotes", 0)) or 0,
        })
    out.sort(key=lambda c: (c["upvotes"], llm_score(c["title"] + " " + c["abstract"])), reverse=True)
    return out


def candidates_from_arxiv() -> list[dict]:
    cat = "+OR+".join(f"cat:{c}" for c in ARXIV_CATS)
    url = ("http://export.arxiv.org/api/query?"
           f"search_query={cat}&sortBy=submittedDate&sortOrder=descending&max_results=30")
    ns = {"a": "http://www.w3.org/2005/Atom"}
    out = []
    for e in ET.fromstring(get(url)).findall("a:entry", ns):
        out.append({
            "id": _norm_id(e.find("a:id", ns).text),
            "title": " ".join(e.find("a:title", ns).text.split()),
            "abstract": " ".join(e.find("a:summary", ns).text.split()),
            "authors": [a.find("a:name", ns).text for a in e.findall("a:author", ns)],
            "upvotes": 0,
        })
    out.sort(key=lambda c: llm_score(c["title"] + " " + c["abstract"]), reverse=True)
    return out


def _strip_html(h: str) -> str:
    h = re.sub(r"(?is)<(script|style|nav|header|footer)[^>]*>.*?</\1>", " ", h)
    h = re.sub(r"(?s)<[^>]+>", " ", h)
    return re.sub(r"\s+\n", "\n", re.sub(r"[ \t]+", " ", html.unescape(h))).strip()


def fetch_fulltext(arxiv_id: str) -> str | None:
    for url in (f"https://arxiv.org/html/{arxiv_id}", f"https://ar5iv.org/abs/{arxiv_id}"):
        try:
            text = _strip_html(get(url))
        except Exception:  # noqa: BLE001
            continue
        if len(text) > 4000:
            return text[:MAX_CHARS]
    return None


def main() -> int:
    WORK.mkdir(exist_ok=True)
    cands = []
    try:
        cands = candidates_from_hf()
    except Exception as e:  # noqa: BLE001
        print(f"[warn] HF daily papers failed: {e}", file=sys.stderr)
    if not cands:
        try:
            cands = candidates_from_arxiv()
        except Exception as e:  # noqa: BLE001
            print(f"[warn] arXiv fallback failed: {e}", file=sys.stderr)

    chosen = None
    for c in cands[:CANDIDATES]:
        ft = fetch_fulltext(c["id"])
        if ft:
            c["full_text"] = ft
            c["url"] = f"https://arxiv.org/abs/{c['id']}"
            chosen = c
            break
        print(f"[skip] no full text for {c['id']}", file=sys.stderr)

    if not chosen:
        print("no paper with retrievable full text today — skipping.")
        return 3

    (WORK / "sources.json").write_text(json.dumps({"type": "paper", "date": date.today().isoformat(),
                                                   "paper": chosen}, indent=2, ensure_ascii=False))
    print(f"wrote sources.json: {chosen['id']} — {chosen['title'][:70]} "
          f"({len(chosen['full_text'])} chars full text)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
