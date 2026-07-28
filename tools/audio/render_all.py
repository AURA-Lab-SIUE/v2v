#!/usr/bin/env python3
"""Batch-render every chapter narration JSON to two WAV tracks on CUDA.
Usage: render_all.py <json_dir>   (expects chNN.json; writes chNN-ug.wav / chNN-grad.wav)
Loads the F5-TTS model ONCE for the whole batch.
"""
import os, sys, json, time, glob
os.environ["PYTHONHASHSEED"] = "0"
# Windows console is cp1252; F5-TTS prints gen_text (may contain Unicode like the
# arrow U+2192), which crashes the process on encode. Force UTF-8 stdout/stderr.
for _s in (sys.stdout, sys.stderr):
    try: _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception: pass
TMP = r"C:\Users\alexl\orator-render-tmp"
CKPT = os.path.join(TMP, "model_slim.pt")
REF  = os.path.join(TMP, "APLeith.wav")
REFTXT = os.path.join(TMP, "APLeith.ref.txt")

import torch, numpy as np, soundfile as sf
import torchaudio
_orig = torchaudio.load
def _load(*a, **k):
    k.setdefault("backend", "soundfile")
    return _orig(*a, **k)
torchaudio.load = _load
try:
    from simdad_phonetics import process as phon
except Exception as e:
    print("WARN phonetics off:", e, flush=True); phon = lambda t: t
from f5_tts.api import F5TTS

SR = 24000
PAUSE = {"heading": 0.85, "para": 0.45, "figure": 0.6}
REF_TEXT = open(REFTXT, encoding="utf-8").read().strip()

dev = "cuda" if torch.cuda.is_available() else "cpu"
print("device", dev, torch.cuda.get_device_name(0) if dev == "cuda" else "", flush=True)
t0 = time.time()
model = F5TTS(ckpt_file=CKPT, device=dev)
print(f"model loaded in {time.time()-t0:.0f}s", flush=True)

_SYM = {"→": " to ", "←": " from ", "↔": " to ", "⤳": " to ",
        "▷": " ", "⭢": " to ", "⇒": " leads to "}
def sanitize(text):
    for k, v in _SYM.items():
        text = text.replace(k, v)
    return text

def synth(text, seed=0):
    text = sanitize(text)
    wav, sr, _ = model.infer(ref_file=REF, ref_text=REF_TEXT, gen_text=phon(text),
                             nfe_step=32, cfg_strength=2.0, speed=1.0,
                             remove_silence=False, seed=seed)
    w = wav.numpy() if hasattr(wav, "numpy") else np.asarray(wav)
    return w.astype(np.float32).squeeze()

def render_track(segments, out):
    t = time.time(); parts = []
    for s in segments:
        parts.append(synth(s["text"]))
        parts.append(np.zeros(int(PAUSE.get(s["type"], 0.4) * SR), dtype=np.float32))
    audio = np.concatenate(parts)
    sf.write(out, audio, SR)
    print(f"  WROTE {os.path.basename(out)} segs={len(segments)} {len(audio)/SR:.0f}s in {time.time()-t:.0f}s", flush=True)

json_dir = sys.argv[1]
files = sorted(glob.glob(os.path.join(json_dir, "ch*.json")))
print(f"batch: {len(files)} chapters", flush=True)
for jf in files:
    stem = os.path.splitext(os.path.basename(jf))[0]   # chNN
    ug_out = os.path.join(json_dir, f"{stem}-ug.wav")
    grad_out = os.path.join(json_dir, f"{stem}-grad.wav")
    data = json.load(open(jf, encoding="utf-8"))
    segs = data["segments"]
    ug = [s for s in segs if not s["grad"]]
    print(f"{stem}: ug={len(ug)} grad={len(segs)}", flush=True)
    if not os.path.exists(ug_out):
        render_track(ug, ug_out)
    if not os.path.exists(grad_out):
        render_track(segs, grad_out)
print("ALL DONE", flush=True)
