# Chapter audio narration pipeline

Per-chapter AI narration in the author's voice (F5-TTS, `APLeith` clone), two
tracks each: `audio/chNN-ug.mp3` (undergraduate) and `audio/chNN-grad.mp3`
(graduate = includes the graduate-extension asides + quotes). The `<audio>`
players are injected after each chapter title; `custom.scss` swaps which one
shows on the graduate toggle (`body.show-grad-ext`).

## Rendering (since 2026-10-24: `render_orator.py`)

The chapters render through the same Orator TTS layer as the MC 427 videos, so the
book and the videos are one voice: sentence chunking (floor 90, ceiling 350),
fixed seeds, and the `APLeith-n025` reference with its `speed.txt` (0.8585).

1. `qmd_to_narration.py chapterNN.qmd > json/chNN.json` for every chapter.
2. `tts_lexicon.py check json` (exit 1 if a chapter-scoped rule matches nothing,
   meaning its sentence changed and the fix would silently stop applying).
3. `render_orator.py --json json --out OUT --orator ORATOR --voices VOICES
   --checkpoint model_6000.pt --phonetics SIMDAD_PHONETICS/src
   --preflight ORATOR/tools/preflight_voice.py ch07 ch08 ...` (CPU or CUDA via
   `--device`). Each segment is cached under `OUT/cache/`, keyed on everything that
   changes its audio, so both tracks share audio, an interrupted run resumes, and a
   lexicon fix re-renders only the segments it touches. It writes
   `OUT/chNN-ug.mp3` and `chNN-grad.mp3` and runs `gate_audio.py` on each chapter.
4. Copy a chapter's two mp3s into `audio/` only when its gate is PASS.
5. `cadence_check.py --out OUT --chapter chNN OUT/chNN-ug.wav` reports where chunk
   boundaries fall and the pause distribution against his real speech.

What the voice is asked to say comes from `tts_lexicon.tsv` (respellings and
heteronym rewrites, TTS input only) and `tts_lexicon.py` (spoken forms for code and
statistics notation). The chapter text and the narration JSON are never changed,
so the audio can differ from the page in those words (for example "is using" for a
verb "uses", which the voice mispronounces).

## Legacy rendering (`render_all.py`, July 2026; CUDA GPU host, ephemeral compute)

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
- Reference clip identity: the voice is `model_6000` + a pinned reference
  (`APLeith-n025.wav`, sha256 `05fd6b26...` since 2026-10-24; `APLeith.wav` in
  July), never the old 5-second clip. `render_orator.py` refuses any other bytes.
- simdad-phonetics spells a lowercase "us" as "u s"; `render_orator.py` patches
  initialism matching to all-caps tokens in its own process and asserts both
  directions at start-up.
