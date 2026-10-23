#!/usr/bin/env python3
"""Strip model chatter / code fences before the YAML front matter.

The generate/translate passes sometimes wrap output in prose ("Here is the
post:"), a ```markdown fence, and/or a stray `---` separator before the real
front matter — all of which break Jekyll parsing. This finds the first genuine
front-matter key, backs up to its opening `---`, and keeps the document from
there.

Usage: sanitize.py <file>   (edits in place)
"""
import re
import sys

KEY = re.compile(
    r"^(title|date|lang|excerpt|tags|header|translated_url|"
    r"categories|category|permalink|author|read_time|comments):"
)

p = sys.argv[1]
lines = open(p, encoding="utf-8").read().splitlines()
lines = [l for l in lines if not re.match(r"^```[A-Za-z0-9_-]*[ \t]*$", l)]  # drop fences

start = 0
for j, l in enumerate(lines):
    if KEY.match(l):
        k = j
        while k >= 0 and lines[k].strip() != "---":   # back up to opening ---
            k -= 1
        start = k if k >= 0 else j
        break

body = "\n".join(lines[start:]).strip()

# Normalize math delimiters to $$…$$ so kramdown renders them. kramdown does NOT
# process \( … \) / \[ … \] by default (they leak through as literal text);
# $$…$$ renders inline within a line and as a display block on its own line.
for a, b in (("\\(", "$$"), ("\\)", "$$"), ("\\[", "$$"), ("\\]", "$$")):
    body = body.replace(a, b)

open(p, "w", encoding="utf-8").write(body + "\n")
