#!/usr/bin/env python3
"""Insert a chapter-audio player block after each chapter's YAML front matter.
CRLF/LF tolerant, idempotent. Run AFTER quote edits + audio render."""
import re, pathlib
CH = pathlib.Path("/Volumes/One Touch/20-research/aura-lab/v2v-book/chapters")

BLOCK_TMPL = '''::: {{.chapter-audio}}
[Listen in Dr. Leith's voice]{{.audio-label}}

```{{=html}}
<audio class="v2v-audio v2v-audio-ug" controls preload="none"><source src="../audio/{stem}-ug.mp3" type="audio/mpeg">Your browser does not support audio.</audio>
<audio class="v2v-audio v2v-audio-grad" controls preload="none"><source src="../audio/{stem}-grad.mp3" type="audio/mpeg">Your browser does not support audio.</audio>
```

:::
'''

done, skip = [], []
for qmd in sorted(CH.glob("chapter*.qmd")):
    text = qmd.read_text(encoding="utf-8")
    if ".chapter-audio" in text:
        skip.append(qmd.name); continue
    nl = "\r\n" if "\r\n" in text else "\n"
    lines = text.split("\n")  # keep \r attached; we compare stripped
    if lines[0].rstrip("\r") != "---":
        print("no front matter, skip", qmd.name); continue
    end = next((i for i in range(1, len(lines)) if lines[i].rstrip("\r") == "---"), None)
    if end is None:
        print("unterminated front matter, skip", qmd.name); continue
    num = re.search(r"(\d+)", qmd.stem).group(1)
    block = BLOCK_TMPL.format(stem=f"ch{num}")
    block_lines = block.split("\n")
    if nl == "\r\n":
        block_lines = [ln + "\r" for ln in block_lines]
    new = lines[:end+1] + [("\r" if nl == "\r\n" else "")] + block_lines + lines[end+1:]
    qmd.write_text("\n".join(new), encoding="utf-8")
    done.append(qmd.name)
print("injected:", len(done), done)
print("already had player:", len(skip), skip)
