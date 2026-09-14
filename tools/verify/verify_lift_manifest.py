"""Confirm a v4 consolidation preserved the owner's prose exactly.

Builders that lift paragraphs out of an existing chapter write a manifest naming
every anchor they lifted and whether they declared a repair on it. This checks
each one against both files: an unrepaired paragraph must appear byte-identical
in the output, and a paragraph declared repaired must NOT, or the repair was a
no-op and the declaration is lying.

    python3 tools/verify/verify_lift_manifest.py data-raw/v3/ch25_lift_manifest.json
"""
import json
import pathlib
import re
import sys

ROOT = pathlib.Path("/Volumes/One Touch/20-research/aura-lab/v2v")


def paragraph(src, anchor):
    body = re.sub(r"^```.*?^```", "", src, flags=re.S | re.M)
    hits = [p.strip() for p in body.split("\n\n") if anchor in p]
    if len(hits) != 1:
        sys.exit("anchor matched %d paragraphs in source: %r" % (len(hits), anchor[:60]))
    return hits[0]


def check(manifest_path):
    m = json.loads(pathlib.Path(manifest_path).read_text(encoding="utf-8"))
    # a builder may lift from one source ("source") or several ("sources", with
    # each lifted item naming which one it came from)
    if "sources" in m:
        srcs = {k: (ROOT / v).read_text(encoding="utf-8") for k, v in m["sources"].items()}
    else:
        srcs = {None: (ROOT / m["source"]).read_text(encoding="utf-8")}
    new = (ROOT / m["output"]).read_text(encoding="utf-8")

    identical, repaired, drift = 0, [], []
    for item in m["lifted"]:
        anchor, is_rep = item["anchor"], item["repaired"]
        p = paragraph(srcs[item.get("source")], anchor)
        if p in new:
            identical += 1
            if is_rep:
                drift.append((anchor, "declared a repair but lifted unchanged"))
        elif is_rep:
            repaired.append(anchor)
        else:
            drift.append((anchor, "NOT FOUND and no repair was declared"))

    print("%s -> %s" % (m.get("source") or ", ".join(m["sources"].values()), m["output"]))
    print("  paragraphs lifted byte-identical  : %d" % identical)
    print("  paragraphs changed by declared repair: %d" % len(repaired))
    for a in repaired:
        print("     %s..." % a[:62])
    if drift:
        print("\n  ** UNDECLARED DRIFT, %d paragraph(s):" % len(drift))
        for a, why in drift:
            print("     %s\n         %s" % (a[:72], why))
        return False
    print("  OK: no undeclared drift.")
    return True


if __name__ == "__main__":
    args = sys.argv[1:] or sorted(str(p) for p in (ROOT / "data-raw/v3").glob("*_lift_manifest.json"))
    if not args:
        sys.exit("no manifests found")
    ok = all(check(a) for a in args)
    sys.exit(0 if ok else 1)
