#!/usr/bin/env python3
"""Post-render gate for v2v chapter audio (2026-10-24, #ttsrepass). Exit 1 on any FAIL.

preflight_voice.py guards the input before a render; this guards each rendered chapter. A
render that completes is not a render that worked (orator-render-pipeline-gates, 2026-07-29),
so every check reads the audio, never the exit code:

  G2 duration  per CHUNK, rendered length within LEN_TOL of F5's own expected length for that text
               (ref frames per ref byte x chunk bytes / speed; the driver records it), which fails a
               render off the wrong reference or speed (the 2.1-4.3x 2026-07-29 signature) chunk by
               chunk instead of averaging it away; and the file speaking rate (words / voiced-segment
               seconds) inside RATE_BAND. Chunks far off the corpus median wpm are LISTED, not failed:
               F5 sets length per byte, so per-chunk wpm mostly tracks word length.
  G3 integrity every segment the track names exists in the cache; no empty, NaN or clipped audio;
               the mp3 decodes to the wav's length within 0.3 s.
  info         micro-gap count (orator suspicious_gaps, 0.05-0.12 s); audibility is unknown, so
               it is reported, never failed.

    gate_audio.py --out DIR chNN [chNN ...]     writes DIR/gate-chNN.json
"""
import argparse, json, os, statistics, subprocess, sys, tempfile
from pathlib import Path

import numpy as np
import soundfile as sf

RATE_BAND = (110.0, 210.0)   # n025 at 0.8585: 169 wpm on the refeval passage, 137 on long-worded book prose (smoke 10-24)
LEN_TOL = 0.03
STRETCH, FAST = 0.6, 1.6
FFMPEG = os.environ.get("FFMPEG", "ffmpeg")


def chunk_rates(cache: Path):
    rates = []
    for m in cache.glob("*.json"):
        for c in json.loads(m.read_text(encoding="utf-8"))["chunk_meta"]:
            if c["seconds"] > 0:
                rates.append(c["words"] / c["seconds"] * 60)
    return rates


def mp3_seconds(mp3: Path) -> float:
    with tempfile.TemporaryDirectory() as td:
        wav = Path(td) / "d.wav"
        subprocess.run([FFMPEG, "-y", "-loglevel", "error", "-i", str(mp3), str(wav)], check=True)
        return sf.info(str(wav)).duration


def gate(out: Path, chap: str, median: float) -> dict:
    cache = out / "cache"
    res = {"chapter": chap, "median_chunk_wpm_corpus": round(median, 1), "tracks": {}, "fails": []}
    for track in ("ug", "grad"):
        wav_p, man_p = out / f"{chap}-{track}.wav", out / f"{chap}-{track}.segments.json"
        r = {"fails": [], "fast_chunks": [], "gaps": 0}
        if not (wav_p.exists() and man_p.exists()):
            res["fails"].append(f"{track}: track or manifest missing")
            continue
        words = speech = 0.0
        for key in json.loads(man_p.read_text(encoding="utf-8")):
            mp = cache / f"{key}.json"
            if not (mp.exists() and (cache / f"{key}.wav").exists()):
                r["fails"].append(f"G3 segment {key[:12]} missing from cache")
                continue
            m = json.loads(mp.read_text(encoding="utf-8"))
            words += len(m["text"].split())
            speech += m["seconds"]
            for i, c in enumerate(m["chunk_meta"]):
                wpm = c["words"] / c["seconds"] * 60 if c["seconds"] else 0
                r["gaps"] += len(c["gaps"])
                exp = c.get("expected_s")
                if not exp:
                    r["fails"].append(f"G2 seg {m['seg']} chunk {i}: no expected length recorded")
                elif abs(c["seconds"] / exp - 1) > LEN_TOL:
                    r["fails"].append(f"G2 seg {m['seg']} chunk {i}: {c['seconds']} s vs F5 expected {exp} s: "
                                      f"{m['chunks'][i][:70]}")
                if not (STRETCH * median <= wpm <= FAST * median):
                    r["fast_chunks"].append({"seg": m["seg"], "chunk": i, "wpm": round(wpm), "chars": c["chars"],
                                             "text": m["chunks"][i][:90]})
        x, sr = sf.read(str(wav_p), dtype="float32")
        r["seconds"] = round(len(x) / sr, 2)
        r["speech_seconds"] = round(speech, 2)
        r["words"] = int(words)
        r["wpm"] = round(words / speech * 60, 1) if speech else 0
        r["peak"] = round(float(np.max(np.abs(x))) if x.size else 0.0, 4)
        if not (RATE_BAND[0] <= r["wpm"] <= RATE_BAND[1]):
            r["fails"].append(f"G2 file rate {r['wpm']} wpm outside {RATE_BAND}")
        if x.size == 0 or not np.isfinite(x).all():
            r["fails"].append("G3 empty or non-finite audio")
        if r["peak"] >= 0.999:
            r["fails"].append(f"G3 clipped (peak {r['peak']})")
        mp3 = wav_p.with_suffix(".mp3")
        if not mp3.exists():
            r["fails"].append("G3 mp3 missing")
        else:
            r["mp3_seconds"] = round(mp3_seconds(mp3), 2)
            if abs(r["mp3_seconds"] - r["seconds"]) > 0.3:
                r["fails"].append(f"G3 mp3 {r['mp3_seconds']} s vs wav {r['seconds']} s")
        res["tracks"][track] = r
        res["fails"] += [f"{track}: {f}" for f in r["fails"]]
    res["verdict"] = "FAIL" if res["fails"] else "PASS"
    (out / f"gate-{chap}.json").write_text(json.dumps(res, indent=1, ensure_ascii=False), encoding="utf-8")
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("chapters", nargs="+")
    a = ap.parse_args()
    out = Path(a.out)
    median = statistics.median(chunk_rates(out / "cache"))
    bad = 0
    for chap in a.chapters:
        r = gate(out, chap, median)
        t = r["tracks"]
        print(f"GATE {chap} {r['verdict']}  " + "  ".join(
            f"{k}: {v.get('seconds')}s {v.get('wpm')}wpm fast={len(v['fast_chunks'])} gaps={v['gaps']}"
            for k, v in t.items()) + (f"  FAILS: {r['fails']}" if r["fails"] else ""))
        bad += r["verdict"] == "FAIL"
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
