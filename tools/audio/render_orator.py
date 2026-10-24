#!/usr/bin/env python3
"""Render v2v chapter narration through the Orator TTS layer (2026-10-24, #ttsrepass). ACADEMIC VOICE ONLY.

Replaces render_all.py, which called F5 directly on whole paragraphs. This driver uses the same
Orator code the MC 427 videos use, so the book and the videos sound like one voice:

  * text: tts_lexicon.py (lexicon + notation), then simdad_phonetics, as one TTS-input string
    per segment. The chapters and the narration JSON are never changed.
  * chunks: orator.tts.split_into_sentence_chunks (floor 90, ceiling 350, max_pair 6,
    glue_limit 240), the 2026-09-21 settled values, asserted at start-up.
  * synthesis: orator.tts.synthesize_best_take per chunk with seed 1234 + i*97 and a 100 ms
    crossfade, i.e. synthesize_section(chunk_mode="sentence", seed=1234, takes=TAKES) unrolled
    so each chunk's duration can be audited (a short chunk that truncates is invisible in a
    whole-file average; see orator-voice-naturalness-diagnosis, 2026-09-21).
  * voice: --voice (default APLeith-n025, the owner's 2026-10-11 pick) with its speed.txt.

Every segment is cached under cache/<sha256>.wav keyed on everything that changes its audio
(TTS text, reference bytes, speed, seed, takes, tts.py bytes, checkpoint name), so the undergraduate
and graduate tracks share audio, a crash resumes where it stopped, and a later lexicon fix
re-renders only the segments it touches.

    render_orator.py --json DIR --out DIR --orator DIR --voices DIR --checkpoint FILE \
                     --phonetics SRC_DIR --preflight FILE [--device cpu] ch07 ch08 ...

PAUSE["heading"] = 0.85 s is the owner's pick (q-20261024-0025 = A, 2026-10-24).

Writes OUT/chNN-ug.wav, chNN-grad.wav (+ .mp3 at 64 kbps mono), OUT/segments.jsonl,
OUT/STATUS.txt, and runs gate_audio.py on each chapter as soon as its two tracks exist.
"""
import argparse, hashlib, json, logging, os, subprocess, sys, time
from pathlib import Path

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
os.environ.setdefault("PYTHONHASHSEED", "0")
sys.dont_write_bytecode = True

HERE = Path(__file__).resolve().parent
SR = 24000
SEED, TAKES, CROSSFADE_MS = 1234, 1, 100
PAUSE = {"heading": 0.85, "para": 0.45, "figure": 0.6}   # the book's own inter-segment pauses (render_all.py)
CHUNKER = {"floor": 90, "ceiling": 350, "max_pair": 6, "glue_limit": 240}   # settled 2026-09-21
FFMPEG = os.environ.get("FFMPEG", "ffmpeg")


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def case_sensitive_initialisms(simdad_phonetics):
    """Work around Lexicon.is_initialism matching token.upper(): it spells every lowercase "us"
    as "u s" (#llc-voice risk 2026-10-11, library unfixed). Only an all-caps token, or an all-caps
    stem with a plural s (KPIs), is an initialism. Patched in this process only; the library is
    untouched. Proven both ways at start-up."""
    from simdad_phonetics import lexicon as L
    orig = L.Lexicon.is_initialism

    def is_initialism(self, token):
        stem = token[:-1] if token.endswith("s") and token[:-1].isupper() else token
        return stem.isupper() and orig(self, token)

    L.Lexicon.is_initialism = is_initialism
    phon = simdad_phonetics.process
    assert "u s" not in phon("what would that account lead us to expect."), "lowercase us still respelled"
    assert "S P S S" in phon("SPSS and Excel"), "uppercase initialisms no longer respelled"
    return phon


def main():
    ap = argparse.ArgumentParser()
    for a in ("--json", "--out", "--orator", "--voices", "--checkpoint", "--phonetics"):
        ap.add_argument(a, required=True)
    ap.add_argument("--preflight", required=True, help="Orator's tools/preflight_voice.py (not vendored here)")
    ap.add_argument("--voice", default="APLeith-n025")
    ap.add_argument("--voice-sha256", default="05fd6b26b393f176888505571bdc9b1a7cd15843b6c2ec4a843140984d0c1ca1")
    ap.add_argument("--device", default="cpu")
    ap.add_argument("--no-gate", action="store_true")
    ap.add_argument("chapters", nargs="+")
    a = ap.parse_args()

    out = Path(a.out)
    cache = out / "cache"
    cache.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(name)s %(message)s", stream=sys.stdout)

    sys.path.insert(0, a.orator)
    sys.path.insert(0, a.phonetics)
    sys.path.insert(0, str(HERE))
    import numpy as np, soundfile as sf
    import simdad_phonetics
    import orator.config as C
    import orator.tts as T
    import tts_lexicon

    C.VOICES_DIR = T.VOICES_DIR = Path(a.voices)
    phon = case_sensitive_initialisms(simdad_phonetics)
    sig = T.split_into_sentence_chunks.__defaults__
    assert sig == (CHUNKER["floor"], CHUNKER["ceiling"], CHUNKER["max_pair"], CHUNKER["glue_limit"]), sig

    ref_audio, ref_text = T.get_voice_ref(a.voice)
    ref_bytes = Path(ref_audio).read_bytes()
    if sha(ref_bytes) != a.voice_sha256:
        sys.exit(f"BLOCK voice {a.voice}: sha256 {sha(ref_bytes)} is not the pinned {a.voice_sha256}")
    speed = T.get_voice_speed(ref_audio)
    if os.environ.get("TTSREPASS_GATE_TOGGLE") == "ignore-speed":
        # Gate self-test only: the engine renders at 1.0 as if speed.txt were missing, while the
        # expected length still uses the pinned speed. gate_audio.py must FAIL this render.
        T.get_voice_speed = lambda _p: 1.0
        print("TOGGLE: engine speed forced to 1.0", flush=True)
    tts_py = Path(T.__file__).read_bytes()
    fixed = {"voice": a.voice, "ref_sha256": sha(ref_bytes), "ref_text": ref_text, "speed": speed,
             "seed": SEED, "takes": TAKES, "crossfade_ms": CROSSFADE_MS, "chunker": CHUNKER,
             "tts_py_sha256": sha(tts_py), "checkpoint": Path(a.checkpoint).name}
    pre = subprocess.run([sys.executable, a.preflight, "--voices", a.voices,
                          "--voice", a.voice], capture_output=True, text=True)
    print(pre.stdout + pre.stderr, flush=True)
    if pre.returncode != 0:
        sys.exit("BLOCK preflight_voice failed")
    (out / "render-config.json").write_text(json.dumps(fixed, indent=1), encoding="utf-8")
    print("config", json.dumps(fixed), flush=True)

    eng = T.F5TTSEngine(checkpoint=a.checkpoint)
    t0 = time.time()
    eng.load(a.device)
    print(f"model loaded in {time.time() - t0:.0f}s on {a.device}", flush=True)

    status = out / "STATUS.txt"
    seglog = (out / "segments.jsonl").open("a", encoding="utf-8")
    done_chunks = 0

    def expected_seconds(chunk):
        """F5's own length for this chunk (f5_tts 1.1.22 utils_infer.py:505, hop 256): ref frames per ref
        byte x chunk bytes / speed. A render off this by more than a few percent did not use the pinned
        reference and speed, which is the 2026-07-29 failure class."""
        audio, sr_ref, processed = eng._ref_cache[str(ref_audio)]
        rt = processed + " " if len(processed[-1].encode("utf-8")) == 1 else processed
        frames = (audio.shape[-1] * SR // sr_ref) // 256
        sp = 0.3 if len(chunk.encode("utf-8")) < 10 else speed
        return int(frames / len(rt.encode("utf-8")) * len(chunk.encode("utf-8")) / sp) * 256 / SR

    def render_segment(tts_text):
        nonlocal done_chunks
        chunks = T.split_into_sentence_chunks(tts_text)
        wavs, meta = [], []
        for i, ch in enumerate(chunks):
            t = time.time()
            w = T.synthesize_best_take(eng, ch, ref_audio, ref_text, seed=SEED + i * 97, takes=TAKES, sr=SR)
            if w.size == 0:
                raise RuntimeError(f"empty chunk {i}: {ch[:60]}")
            wavs.append(w)
            meta.append({"chars": len(ch), "words": len(ch.split()), "seconds": round(len(w) / SR, 3),
                         "expected_s": round(expected_seconds(ch), 3),
                         "gaps": T.suspicious_gaps(w, SR), "render_s": round(time.time() - t, 1)})
            done_chunks += 1
        combined = wavs[0]
        for w in wavs[1:]:
            combined = T.crossfade(combined, w, int(CROSSFADE_MS / 1000 * SR))
        return combined, chunks, meta

    for chap in a.chapters:
        data = json.loads((Path(a.json) / f"{chap}.json").read_text(encoding="utf-8"))
        segs, counts_all, prepared = data["segments"], [], []
        for s in segs:
            lexed, counts = tts_lexicon.apply(s["text"], chap)
            counts_all += counts
            prepared.append(phon(lexed))
        dead = [f for sc, f, k in _sum(counts_all) if sc == chap and k == 0]
        if dead:
            print(f"FAIL {chap} lexicon rules match nothing (chapter text drifted?): {dead}", flush=True)
            continue
        audio = {}
        for idx, (s, tts_text) in enumerate(zip(segs, prepared)):
            key = sha(json.dumps({"tts": tts_text, **fixed}, sort_keys=True).encode())
            wav_p, meta_p = cache / f"{key}.wav", cache / f"{key}.json"
            if not (wav_p.exists() and meta_p.exists()):
                status.write_text(f"{time.strftime('%Y-%m-%d %H:%M:%S')} {chap} seg {idx + 1}/{len(segs)} "
                                  f"chunks_done={done_chunks}\n", encoding="utf-8")
                t = time.time()
                wav, chunks, meta = render_segment(tts_text)
                sf.write(wav_p.with_suffix(".tmp.wav"), wav, SR)
                os.replace(wav_p.with_suffix(".tmp.wav"), wav_p)
                rec = {"chapter": chap, "seg": idx, "type": s["type"], "grad": s["grad"], "text": s["text"],
                       "tts": tts_text, "chunks": chunks, "chunk_meta": meta, "seconds": round(len(wav) / SR, 3),
                       "render_s": round(time.time() - t, 1), "key": key}
                meta_p.write_text(json.dumps(rec, ensure_ascii=False), encoding="utf-8")
                seglog.write(json.dumps({k: rec[k] for k in ("chapter", "seg", "seconds", "render_s", "key")}) + "\n")
                seglog.flush()
                print(f"{chap} seg {idx + 1}/{len(segs)} {rec['seconds']}s audio in {rec['render_s']}s", flush=True)
            audio[idx] = (wav_p, json.loads(meta_p.read_text(encoding="utf-8")))
        for track, keep in (("ug", lambda s: not s["grad"]), ("grad", lambda s: True)):
            parts, manifest = [], []
            for idx, s in enumerate(segs):
                if not keep(s):
                    continue
                w, _ = sf.read(audio[idx][0], dtype="float32")
                parts += [w, np.zeros(int(PAUSE.get(s["type"], 0.4) * SR), dtype=np.float32)]
                manifest.append(audio[idx][1]["key"])
            full = np.concatenate(parts)
            wav_out = out / f"{chap}-{track}.wav"
            sf.write(wav_out, full, SR)
            subprocess.run([FFMPEG, "-y", "-loglevel", "error", "-i", str(wav_out), "-c:a", "libmp3lame",
                            "-b:a", "64k", "-ac", "1", str(wav_out.with_suffix(".mp3"))], check=True)
            (out / f"{chap}-{track}.segments.json").write_text(json.dumps(manifest), encoding="utf-8")
            print(f"WROTE {chap}-{track} {len(full) / SR:.1f}s", flush=True)
        if not a.no_gate:
            g = subprocess.run([sys.executable, str(HERE / "gate_audio.py"), "--out", str(out), chap],
                               capture_output=True, text=True)
            print(g.stdout + g.stderr, flush=True)
    status.write_text(f"{time.strftime('%Y-%m-%d %H:%M:%S')} COMPLETE chunks_done={done_chunks}\n", encoding="utf-8")
    print("ALL DONE", flush=True)


def _sum(counts):
    tot = {}
    for sc, f, k in counts:
        tot[(sc, f)] = tot.get((sc, f), 0) + k
    return [(sc, f, k) for (sc, f), k in tot.items()]


if __name__ == "__main__":
    main()
