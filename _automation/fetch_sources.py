#!/usr/bin/env python3
"""Pick ONE notable paper and fetch its FULL TEXT for a deep-dive explainer.

Stdlib only. Writes work/sources.json — the single grounding file that BOTH the
writer and the reviewer read. For a deep dive the reviewer checks the whole
explainer against `full_text`, so full text (not just the abstract) is required:
a candidate without retrievable full text is skipped.

Selection: Hugging Face Daily Papers (community-upvoted, LLM-heavy) first, with
a soft LLM lean; falls back to recent arXiv. Full text: arXiv HTML, then ar5iv.
"""
import html
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import date
from pathlib import Path

CANDIDATES = 8          # papers to consider before taking the first with full text
MAX_CHARS = 120_000     # truncate full text to keep the prompt bounded
ARXIV_CATS = ["cs.CL", "cs.AI", "cs.LG"]
LLM_KW = ["llm", "language model", "large language model", "gpt", "llama",
          "transformer", "rag", "retrieval-augmented", "agent", "fine-tun",
          "instruction", "chatbot", "prompt", "mixture-of-experts", "moe",
          "attention", "inference", "serving", "reasoning"]
UA = {"User-Agent": "research-radar/0.2 (personal digest; +https://hyeonjongjang.github.io)"}
WORK = Path(__file__).parent / "work"


def _get(url: str, timeout: int = 30) -> str:
    headers = dict(UA)
    if "api.github.com" in url:
        headers["Accept"] = "application/vnd.github+json"
        if os.environ.get("GITHUB_TOKEN"):
            headers["Authorization"] = f"Bearer {os.environ['GITHUB_TOKEN']}"
    req = urllib.request.Request(url, headers=headers)
    for attempt in range(2):  # one retry on 429
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


def _norm_id(arxiv_id: str) -> str:
    """'2309.06180v2' / 'arXiv:2309.06180' / a URL -> '2309.06180'."""
    m = re.search(r"(\d{4}\.\d{4,5})", arxiv_id)
    return m.group(1) if m else arxiv_id.strip()


def candidates_from_hf() -> list[dict]:
    data = json.loads(_get("https://huggingface.co/api/daily_papers?limit=50"))
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
    # Prefer upvotes, then LLM lean.
    out.sort(key=lambda c: (c["upvotes"], _llm_score(c["title"] + " " + c["abstract"])), reverse=True)
    return out


def candidates_from_arxiv() -> list[dict]:
    cat = "+OR+".join(f"cat:{c}" for c in ARXIV_CATS)
    url = ("http://export.arxiv.org/api/query?"
           f"search_query={cat}&sortBy=submittedDate&sortOrder=descending&max_results=30")
    ns = {"a": "http://www.w3.org/2005/Atom"}
    out = []
    for e in ET.fromstring(_get(url)).findall("a:entry", ns):
        out.append({
            "id": _norm_id(e.find("a:id", ns).text),
            "title": " ".join(e.find("a:title", ns).text.split()),
            "abstract": " ".join(e.find("a:summary", ns).text.split()),
            "authors": [a.find("a:name", ns).text for a in e.findall("a:author", ns)],
            "upvotes": 0,
        })
    out.sort(key=lambda c: _llm_score(c["title"] + " " + c["abstract"]), reverse=True)
    return out


def _strip_html(h: str) -> str:
    h = re.sub(r"(?is)<(script|style|nav|header|footer)[^>]*>.*?</\1>", " ", h)
    h = re.sub(r"(?s)<[^>]+>", " ", h)
    return re.sub(r"\s+\n", "\n", re.sub(r"[ \t]+", " ", html.unescape(h))).strip()


def fetch_fulltext(arxiv_id: str) -> str | None:
    for url in (f"https://arxiv.org/html/{arxiv_id}",
                f"https://ar5iv.org/abs/{arxiv_id}"):
        try:
            text = _strip_html(_get(url))
        except Exception:  # noqa: BLE001
            continue
        if len(text) > 4000:  # a real rendered paper, not a stub/404
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

    out = {"date": date.today().isoformat(), "paper": chosen}
    (WORK / "sources.json").write_text(json.dumps(out, indent=2, ensure_ascii=False))
    print(f"wrote {WORK/'sources.json'}: {chosen['id']} — {chosen['title'][:70]} "
          f"({len(chosen['full_text'])} chars full text)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
