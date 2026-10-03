---
description: Visuals — generate per-scene images for the video
---

Generate visuals for the video project: $ARGUMENTS (project dir, default `movie_moses`).

Read `movie_moses/pipeline/README.md` and `02_storyboard/storyboard.md`.

## Steps

1. For each scene with an `image_prompt` and no image yet, generate
   `03_visuals/scene-XX.png` at the manifest `resolution` (landscape) using the
   image generation tools available in this environment.
2. Prepend `style_lock` from `project.json` to every prompt — no exceptions.
   Generate hero shots first; check consistency (palette, era, character look)
   before batch-generating the rest.
3. For the 3–5 hero shots, also produce i2v clips as `03_visuals/scene-XX-anim.mp4`
   and point the scene's `image` field at them (the pipeline accepts video sources).
4. Self-review each image against the guardrails (reverence, style consistency,
   no uncanny sacred faces). Regenerate any that fail.
5. Update `project.json` paths if any output names differ, then run
   `python3 <dir>/pipeline/validate.py <dir>`.

Report: per-scene generated/skipped/failure list. Audio is the next stage, not this one.
