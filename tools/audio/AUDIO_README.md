# Chapter audio narration pipeline

Per-chapter AI narration in the author's voice (F5-TTS, `APLeith` clone), two
tracks each: `audio/chNN-ug.mp3` (undergraduate) and `audio/chNN-grad.mp3`
(graduate = includes the graduate-extension asides + quotes). The `<audio>`
players are injected after each chapter title; `custom.scss` swaps which one
shows on the graduate toggle (`body.show-grad-ext`).

## Rendering (on a CUDA GPU host, e.g. nsf-leith RTX 3090, ephemeral compute)

Stage transiently, render, pull the audio back here, then delete the staging dir
(nsf-leith holds no resident data):

1. Stage to `C:\Users\alexl\orator-render-tmp\`: `model_slim.pt` (EMA-only slim of
   Orator's `model_6000.pt`, ~1.3 GB), `voices/APLeith.wav` + `APLeith.ref.txt`,
   a CUDA venv with `f5-tts` + `simdad-phonetics`, plus `render_all.py`.
2. `qmd_to_narration.py chapterNN.qmd > json/chNN.json` for every chapter
   (two tracks fall out: undergrad = non-grad segments, grad = all).
3. `render_all.py json` (loads the model once, renders both tracks per chapter,
   idempotent per-track resume).
4. `ffmpeg -i chNN-track.wav -c:a libmp3lame -b:a 64k -ac 1 audio/chNN-track.mp3`.
5. `inject_audio.py` (idempotent) inserts the players; commit `audio/` + chapters.

## Gotchas baked into these scripts (do not regress)

- Force UTF-8 stdout: F5-TTS prints each line; a Unicode char (e.g. the arrow
  U+2192) crashes on the cp1252 Windows console otherwise.
- `PYTHONHASHSEED=0` + an in-range `seed`: F5 writes a 64-bit seed into
  PYTHONHASHSEED before spawning a worker; the default overflows the 32-bit max.
- torchaudio 2.x defaults to torchcodec (needs ffmpeg libs), so force
  `backend="soundfile"` for WAV loads.
- The narration parser strips `>` blockquote markers and drops the trailing
  citation line, and speaks symbols (arrows read as "to").
- Reference clip identity: the voice is `model_6000` + the lecture-register
  reference `APLeith.wav`, not the old 5-second clip.
