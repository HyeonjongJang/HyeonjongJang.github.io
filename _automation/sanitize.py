#!/usr/bin/env python3
r"""Normalize a generated draft into a single valid Jekyll post.

Fixes three ways the generate/translate passes can malform output:
  1. Preamble / code fences before the front matter.
  2. A second post appended (e.g. a Korean copy after the English one) — EN and KO
     are separate files, so keep only the first post.
  3. Math delimiters kramdown won't render ( \( \) / \[ \] ) -> $$ … $$.
Usage: sanitize.py <file>  (edits in place)
"""
import re
import sys

KEY = re.compile(
    r"^(title|date|lang|excerpt|tags|header|translated_url|"
    r"categories|category|permalink|author|read_time|comments):"
)

p = sys.argv[1]
lines = [l for l in open(p, encoding="utf-8").read().splitlines()
         if not re.match(r"^```[A-Za-z0-9_-]*[ \t]*$", l)]  # drop ``` fence lines

# Start at the first front-matter key, backed up to its opening '---'.
start = 0
for j, l in enumerate(lines):
    if KEY.match(l):
        k = j
        while k >= 0 and lines[k].strip() != "---":
            k -= 1
        start = k if k >= 0 else j
        break
seg = lines[start:]

# Truncate a second post appended after the first (e.g. an extra KO copy).
cut = len(seg)
dashes = [i for i, l in enumerate(seg) if l.strip() == "---"]
for di in dashes[2:]:  # dashes[0:2] bound the first front matter
    nxt = next((seg[k].strip() for k in range(di + 1, min(di + 4, len(seg))) if seg[k].strip()), "")
    if KEY.match(nxt):   # a '---' opening a new front matter = a second post
        cut = di
        break
for i in range(min(cut, len(seg))):  # or an explicit "KO post" / "Korean" marker
    if re.match(r"^\s*(\*\*|#+)\s*(KO|Korean|한국어)\b", seg[i]):
        cut = i
        break

out = seg[:cut]
while out and (not out[-1].strip() or out[-1].strip() in ("---", "***", "___")):
    out.pop()  # drop trailing blank lines / horizontal rules

body = "\n".join(out).strip()
for a, b in (("\\(", "$$"), ("\\)", "$$"), ("\\[", "$$"), ("\\]", "$$")):
    body = body.replace(a, b)
open(p, "w", encoding="utf-8").write(body + "\n")
