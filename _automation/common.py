"""Shared helpers for the Research Radar fetchers (paper / repo)."""
import os
import time
import urllib.error
import urllib.request
from pathlib import Path

UA = {"User-Agent": "research-radar/0.3 (personal digest; +https://hyeonjongjang.github.io)"}
WORK = Path(__file__).parent / "work"

# Soft LLM preference (NOT a hard filter): matching items float up; the author is
# a researcher *and* a developer, so general dev/ML items still appear.
LLM_KW = ["llm", "language model", "large language model", "gpt", "llama",
          "transformer", "rag", "retrieval-augmented", "agent", "fine-tun",
          "instruction", "chatbot", "prompt", "mixture-of-experts", "moe",
          "attention", "inference", "serving", "reasoning", "diffusion"]


def get(url: str, timeout: int = 30) -> str:
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


def llm_score(text: str) -> int:
    t = text.lower()
    return sum(1 for k in LLM_KW if k in t)
