#!/usr/bin/env python3
"""Extract TTS narration segments from a v2v chapter .qmd.

Emits JSON: {"chapter","title","segments":[{"type","text","grad"}]}
  type: "heading" | "para" | "figure"
  grad: True if the segment lives inside a .graduate-extension div
Rules:
  - YAML front matter dropped; title -> first heading segment.
  - ## References and everything after it -> dropped (both tracks).
  - Graduate-extension asides -> emitted with grad=True (undergrad track filters
    them out; grad track keeps them). A "Graduate readings" subsection (the
    reference list) is dropped from audio entirely.
  - Fenced code blocks -> dropped (the prose already carries the concept).
  - Figures -> read from caption (fallback fig-alt), prefixed "Figure.".
  - Callout divs -> read as prose.
  - Inline: parenthetical citations, markdown emphasis, links, URLs stripped.
Two tracks from one parse:
  undergrad = [s for s in segments if not s["grad"]]
  grad      = segments (all)
"""
import json, re, sys, pathlib

def clean(t: str) -> str:
    # Operators that appear in prose read as gibberish aloud ("percent greater
    # than percent"), so name them instead.
    t = t.replace('`%>%`', 'pipe symbol').replace('`|>`', 'pipe symbol')
    t = t.replace('%>%', 'pipe symbol').replace('|>', 'pipe symbol')
    t = re.sub(r'!\[[^\]]*\]\([^)]*\)\{[^}]*\}', '', t)          # stray inline image
    t = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', t)                # [text](url) -> text
    t = re.sub(r'\s*\((?:[^()]*?\b(?:19|20)\d{2}[a-z]?)[^()]*\)', '', t)  # (Author, 2017a)
    t = re.sub(r'\*\*([^*]+)\*\*', r'\1', t)                      # bold
    t = re.sub(r'(?<!\w)\*([^*]+)\*(?!\w)', r'\1', t)             # italic
    t = re.sub(r'`([^`]+)`', r'\1', t)                           # inline code
    t = re.sub(r'https?://\S+', '', t)                           # bare URL/DOI
    t = re.sub(r'\s+([,.;:!?])', r'\1', t)
    t = re.sub(r'\s+', ' ', t).strip()
    return t

def fig_text(block: str) -> str:
    cap = re.match(r'!\[([^\]]*)\]', block)
    caption = cap.group(1).strip() if cap else ''
    if not caption:
        m = re.search(r'fig-alt="([^"]*)"', block)
        caption = m.group(1).strip() if m else ''
    caption = clean(caption)
    if not caption:
        return ''
    if not caption.endswith(('.', '!', '?')):
        caption += '.'
    return 'Figure. ' + caption

def parse(path: pathlib.Path):
    raw = path.read_text(encoding='utf-8')
    # front matter
    title = path.stem
    m = re.match(r'^---\n(.*?)\n---\n', raw, re.S)
    if m:
        tm = re.search(r'^title:\s*"?(.*?)"?\s*$', m.group(1), re.M)
        if tm:
            title = tm.group(1).strip()
        raw = raw[m.end():]

    lines = raw.split('\n')
    segments = [{"type": "heading", "text": clean(title), "grad": False}]
    i, n = 0, len(lines)
    div_stack = []                 # classes of open ::: divs
    in_code = False
    skip_rest = False
    skip_grad_readings = False     # inside a "Graduate readings" block
    buf = []

    def in_grad():
        return any('graduate-extension' in c for c in div_stack)

    def flush():
        if not buf:
            return
        text = clean(' '.join(buf))
        buf.clear()
        if text and len(text.split()) >= 2:
            segments.append({"type": "para", "text": text, "grad": in_grad()})

    while i < n and not skip_rest:
        ln = lines[i]
        stripped = ln.strip()

        # fenced code toggle (``` or more)
        if re.match(r'^\s*`{3,}', ln):
            flush()
            in_code = not in_code
            i += 1
            continue
        if in_code:
            i += 1
            continue

        # div fence
        if re.match(r'^:{3,}\s*\{', ln):        # opening with attrs
            flush()
            cls = re.findall(r'\.([A-Za-z0-9_-]+)', ln)
            div_stack.append(' '.join(cls))
            i += 1
            continue
        if re.match(r'^:{3,}\s*$', ln):         # closing
            flush()
            if div_stack:
                popped = div_stack.pop()
                if 'graduate-extension' in popped:
                    skip_grad_readings = False
            i += 1
            continue

        # headings
        hm = re.match(r'^(#{1,6})\s+(.*)$', ln)
        if hm:
            flush()
            htext = clean(hm.group(2))
            low = htext.lower()
            if low.startswith('references'):
                skip_rest = True
                break
            if 'graduate readings' in low:
                skip_grad_readings = True
                i += 1
                continue
            if not skip_grad_readings:
                segments.append({"type": "heading", "text": htext, "grad": in_grad()})
            i += 1
            continue

        if skip_grad_readings:
            i += 1
            continue

        # figure (own paragraph, starts with ![)
        if stripped.startswith('!['):
            flush()
            ft = fig_text(stripped)
            if ft:
                segments.append({"type": "figure", "text": ft, "grad": in_grad()})
            i += 1
            continue

        # blockquote (direct quote): narrate the quoted text, drop the '>' markers
        # and the trailing attribution line ("Author (Year, p. N)").
        if stripped.startswith('>'):
            flush()
            qlines = []
            while i < n and lines[i].strip().startswith('>'):
                c = lines[i].strip()[1:].strip()   # strip leading '>'
                qlines.append(c)
                i += 1
            quote_parts = []
            for c in qlines:
                if c == '':          # blank line separates quote from attribution
                    break
                quote_parts.append(c)
            qtext = clean(' '.join(quote_parts))
            if qtext and len(qtext.split()) >= 2:
                segments.append({"type": "para", "text": qtext, "grad": in_grad()})
            continue

        # bullet list item -> its own sentence
        bm = re.match(r'^\s*[-*+]\s+(.*)$', ln)
        if bm:
            flush()
            bt = clean(bm.group(1))
            if bt and len(bt.split()) >= 2:
                if not bt.endswith(('.', '!', '?', ':')):
                    bt += '.'
                segments.append({"type": "para", "text": bt, "grad": in_grad()})
            i += 1
            continue

        # blank line ends a block
        if stripped == '':
            flush()
            i += 1
            continue

        buf.append(stripped)
        i += 1

    flush()
    return {"chapter": path.stem, "title": title, "segments": segments}

if __name__ == '__main__':
    out = parse(pathlib.Path(sys.argv[1]))
    if len(sys.argv) > 2 and sys.argv[2] == '--stats':
        ug = [s for s in out['segments'] if not s['grad']]
        gr = out['segments']
        wc = lambda segs: sum(len(s['text'].split()) for s in segs)
        print(f"{out['chapter']}: {len(gr)} segs ({len(ug)} ug / {len(gr)-len(ug)} grad-only); "
              f"words ug={wc(ug)} grad={wc(gr)}; "
              f"types={{h:{sum(1 for s in gr if s['type']=='heading')}, "
              f"fig:{sum(1 for s in gr if s['type']=='figure')}}}")
    else:
        print(json.dumps(out, indent=2, ensure_ascii=False))
