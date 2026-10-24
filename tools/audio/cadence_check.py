#!/usr/bin/env python3
"""Cadence spot-check for re-rendered v2v chapter audio (2026-10-24, #ttsrepass).

The standing complaint is cadence, not timbre (orator-voice-naturalness-diagnosis, 2026-09-20):
89% of paragraphs were cut into independently synthesized chunks at ARBITRARY points, so the
voice reset its prosody mid-paragraph, and the pause structure ran too-short ordinary pauses
under too-long structural ones (render max 3.82 s vs his real 1.99 s; median 0.34 vs 0.42 s).

Two measures, for each audio file given:
  text   (needs --out): share of paragraphs synthesized as 2+ chunks, and share of chunk
         boundaries that fall on a sentence end. Sentence mode is meant to make every reset
         land on a full stop; a boundary anywhere else is the old defect.
  audio  pauses >= 0.15 s on an adaptive floor (10th-percentile frame energy, 6 dB above,
         10 ms frames): count per minute, median, p90, max, and how many run >= 1.5 s.

    cadence_check.py [--out DIR --chapter chNN] FILE.wav|.mp3 [...]
"""
import argparse, json, os, re, statistics, subprocess, sys, tempfile
from pathlib import Path

import numpy as np
import soundfile as sf

FFMPEG = os.environ.get("FFMPEG", "ffmpeg")
REAL = {"median_s": 0.42, "max_s": 1.99}   # APLeith-30min.wav, his own read (2026-09-20)


def load(path: Path):
    if path.suffix.lower() == ".wav":
        return sf.read(str(path), dtype="float32")
    with tempfile.TemporaryDirectory() as td:
        w = Path(td) / "d.wav"
        subprocess.run([FFMPEG, "-y", "-loglevel", "error", "-i", str(path), "-ac", "1", "-ar", "24000", str(w)],
                       check=True)
        return sf.read(str(w), dtype="float32")


def pauses(x, sr, min_s=0.15):
    hop = int(0.010 * sr)
    n = len(x) // hop
    rms = np.sqrt(np.mean(x[: n * hop].reshape(n, hop).astype(np.float64) ** 2, axis=1))
    thr = max(float(np.percentile(rms, 10)) * 2.0, float(rms.max()) * 0.01)
    voiced = rms >= thr
    idx = np.where(voiced)[0]
    out, run = [], 0
    for q in ~voiced[idx[0]: idx[-1] + 1]:
        if q:
            run += 1
        elif run:
            out.append(run * 0.010)
            run = 0
    return [p for p in out if p >= min_s], n * 0.010


def text_side(out: Path, chap: str):
    man = json.loads((out / f"{chap}-grad.segments.json").read_text(encoding="utf-8"))
    paras = multi = bounds = on_stop = 0
    for key in man:
        m = json.loads((out / "cache" / f"{key}.json").read_text(encoding="utf-8"))
        if m["type"] != "para":
            continue
        paras += 1
        multi += len(m["chunks"]) > 1
        for c in m["chunks"][:-1]:
            bounds += 1
            on_stop += bool(re.search(r"[.!?][\"')\]]*$", c.strip()))
    return {"paragraphs": paras, "multi_chunk_pct": round(100 * multi / paras, 1) if paras else 0,
            "boundaries": bounds, "on_sentence_end_pct": round(100 * on_stop / bounds, 1) if bounds else 100.0}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out")
    ap.add_argument("--chapter")
    ap.add_argument("files", nargs="+")
    a = ap.parse_args()
    res = {"real_speech_reference": REAL}
    if a.out and a.chapter:
        res["text"] = text_side(Path(a.out), a.chapter)
    for f in a.files:
        x, sr = load(Path(f))
        p, dur = pauses(x, sr)
        res[Path(f).name] = {"minutes": round(dur / 60, 2), "pauses_per_min": round(len(p) / (dur / 60), 1),
                             "median_s": round(statistics.median(p), 2), "p90_s": round(float(np.percentile(p, 90)), 2),
                             "max_s": round(max(p), 2), "n_ge_1_5s": sum(q >= 1.5 for q in p)}
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    sys.exit(main())
