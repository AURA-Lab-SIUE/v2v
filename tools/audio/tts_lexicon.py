"""v2v chapter TTS lexicon: turn a narration segment's text into what the voice is asked to say.

Applied ONLY to the TTS input at render time (render_orator.py). The chapters, the narration
JSON and everything a reader sees are untouched. Adapted 2026-10-24 from the MC 427 kit's
tts_lexicon.py (m4:~/mc427-rerender/), whose two global rules and red/reed pins were measured
by phoneme read on 2026-10-12; the heteronym rewrites follow the owner's 2026-09-20 ear
verdicts (uses -> is using, separate (verb) -> draw a line between, record (verb) rewritten).

Two layers, in this order:
  1. tts_lexicon.tsv: literal, case-sensitive, word-bounded rules, scoped to a chapter (chNN)
     or every chapter (*). A chapter-scoped rule that matches nothing fails that chapter,
     because its sentence drifted and the fix would silently stop applying.
  2. NORMALIZE below: regex rules for code and statistics notation the voice cannot read
     (snake_case, pkg::fn(), <dbl>, p <.001). Global, counted, never required to match.

    python3 tts_lexicon.py check JSON_DIR    every rule against every chNN.json; exit 1 on a dead scoped rule
    python3 tts_lexicon.py text CHNN "text"   print the TTS text for one string
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Callable

LEXICON = Path(__file__).with_name("tts_lexicon.tsv")

_DIGIT = {"0": "zero", "1": "one", "2": "two", "3": "three", "4": "four",
          "5": "five", "6": "six", "7": "seven", "8": "eight", "9": "nine"}


def _point(m: re.Match) -> str:
    return "point " + " ".join(_DIGIT[d] for d in m.group(1))


# (pattern, replacement, why). Order matters: identifiers first, then symbols, then numbers.
NORMALIZE: list[tuple[str, str | Callable[[re.Match], str], str]] = [
    (r"\?(?=v2v::)", "question mark ", "the ?topic help call"),
    (r"\bv2v::(?!\w)", "v2v colon colon", "the prefix named on its own"),
    (r",\s*<-\s*,", ",", "the assignment arrow named in prose ('The arrow, <-, is')"),
    (r"\bt\.test\b", "t dot test", "base R function name"),
    (r"\s~\s", " tilde ", "R formula"),
    (r"(?<![\w.])\+(?=\d)", "plus ", "signed number (+0.15)"),
    (r"\s*>=\s*", " greater than or equal to ", "comparison operator"),
    (r"\s*≥\s*", " at least ", "comparison symbol"),
    (r"\s*≤\s*", " at most ", "comparison symbol"),
    (r"α", "alpha", "statistic symbol"),
    (r"\s/\s", " divided by ", "division in a code call"),
    (r"(?<=\w)::(?=\w)", " ", "pkg::fn reads as 'pkg fn'"),
    (r"(?<=\w)\(\)", "", "fn() reads as 'fn'"),
    (r"(?<=[A-Za-z0-9])_(?=[A-Za-z0-9])", " ", "snake_case reads as words"),
    (r"<dbl>", "double", "tibble column type"),
    (r"<dttm>", "date time", "tibble column type"),
    (r"<chr>", "character", "tibble column type"),
    (r"<int>", "integer", "tibble column type"),
    (r"<lgl>", "logical", "tibble column type"),
    (r"\s*%in%\s*", " in ", "R membership operator"),
    (r"(?<=\w)\$(?=\w)", " dollar ", "R column accessor, as R users say it"),
    (r"\\n", " backslash n ", "a literal newline escape"),
    (r"\bA/B\b", "A B", "A/B testing"),
    (r"\binclusion/exclusion\b", "inclusion and exclusion", "slashed pair"),
    (r"(?<=[a-z])/(?=[a-z]|\s|$)", " slash ", "folder path (data/raw/, codebook/codebook.qmd)"),
    (r"(?<=\w)\.qmd\b", " dot Q M D", "file extension"),
    (r"(?<=\w)\.csv\b", " dot C S V", "file extension"),
    (r"(?<=\w)\.rds\b", " dot R D S", "file extension"),
    (r"(?<=\w)\.lock\b", " dot lock", "file extension"),
    (r"χ²", "chi-square ", "statistic symbol"),
    (r"κ", "kappa", "statistic symbol"),
    (r"\s*<\s*(?=\.?\d)", " less than ", "p <.001"),
    (r"\s*>\s*(?=\.?\d)", " greater than ", "inequality"),
    (r"\s*(?<![<>=!])=(?!=)\s*", " equals ", "statistic = value, also unspaced (α =.05)"),
    (r"\[(-?\.?\d[\d.]*),\s*(-?\.?\d[\d.]*)\]", r"from \1 to \2", "confidence interval bounds"),
    (r"(?<![\w.])-(?=\.?\d)", "minus ", "negative number"),
    (r"(?<![\d.])\.(\d+)", lambda m: " " + _point(m), "leading-dot decimal (.001, is.35, The.05)"),
]
_NORMALIZE = [(re.compile(p), r, why) for p, r, why in NORMALIZE]


def load(path: Path = LEXICON) -> list[tuple[str, str, str, str]]:
    rules = []
    for n, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip() or line.startswith("#"):
            continue
        parts = line.split("\t")
        if len(parts) != 4 or not all(p.strip() for p in parts[:3]):
            raise ValueError(f"{path.name} line {n}: need scope<TAB>find<TAB>replace<TAB>why")
        rules.append(tuple(parts))
    return rules


def _pattern(find: str) -> re.Pattern:
    return re.compile(r"(?<![\w'])" + re.escape(find) + r"(?![\w])")


def apply(text: str, chapter: str, rules=None) -> tuple[str, list[tuple[str, str, int]]]:
    """Return (tts_text, [(scope, rule, count)]) for the lexicon rules then NORMALIZE."""
    rules = load() if rules is None else rules
    counts = []
    for scope, find, repl, _why in rules:
        if scope not in ("*", chapter):
            continue
        text, k = _pattern(find).subn(repl.replace("\\", "\\\\"), text)
        counts.append((scope, find, k))
    for pat, repl, _why in _NORMALIZE:
        text, k = pat.subn(repl, text)
        counts.append(("norm", pat.pattern, k))
    return re.sub(r"\s{2,}", " ", text).strip(), counts


def dead_rules(chapter: str, counts) -> list[str]:
    return [f for s, f, k in counts if s == chapter and k == 0]


def check(json_dir: Path) -> int:
    rules = load()
    hits: dict[tuple, int] = {}
    for jf in sorted(json_dir.glob("ch[0-9][0-9].json")):
        ch = jf.stem
        for seg in json.loads(jf.read_text(encoding="utf-8"))["segments"]:
            for s, f, k in apply(seg["text"], ch, rules)[1]:
                if s != "norm":
                    hits[(s, f)] = hits.get((s, f), 0) + k
    bad = 0
    for scope, find, repl, _why in rules:
        k = hits.get((scope, find), 0)
        if scope != "*" and k == 0:
            bad += 1
            print(f"FAIL {scope}: '{find}' matches nothing")
        else:
            print(f"ok   {scope}: '{find}' -> '{repl}' x{k}")
    print(f"{len(rules)} rules, {bad} failures")
    return 1 if bad else 0


def main(argv: list[str]) -> int:
    if argv[:1] == ["check"] and len(argv) == 2:
        return check(Path(argv[1]))
    if argv[:1] == ["text"] and len(argv) == 3:
        print(apply(argv[2], argv[1])[0])
        return 0
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
