---
description: Storyboard — fill scenes with image prompts and motion
---

Storyboard the video project: $ARGUMENTS (project dir, default `movie_moses`).

Read `movie_moses/pipeline/README.md` (schema + guardrails) and `01_script/script.md`.

## Steps

1. For every scene in `project.json`, write:
   - `image_prompt`: full standalone prompt = `style_lock` + scene-specific description.
     Describe composition, light, and emotion; one subject focus per scene.
   - `motion`: `still` | `zoom-in` | `zoom-out` | `pan-left` | `pan-right` with
     `zoom_from`/`zoom_to` (e.g. 1.0→1.12). Vary motion across scenes.
   - `subtitle_zh`: optional short on-screen line (≤16 chars) if narration is long.
2. Mark 3–5 hero shots (e.g. the parting of the sea, Sinai) as candidates for
   image-to-video: note them in the response and set `03_visuals/scene-XX-anim.mp4`
   as the expected i2v output path in the scene notes of `storyboard.md`.
3. Write `02_storyboard/storyboard.md`: per-scene table (id, prompt, motion, i2v?, notes).
4. If existing slide art in the repo matches a scene (e.g. `moses/*.png`), propose
   reusing/regenerating from it instead of starting from scratch.
5. Run `python3 <dir>/pipeline/validate.py <dir>` and fix structural issues only.

## Visual guardrails

- Reverent framing only; never grotesque or mocking depictions of sacred figures.
- Photoreal-uncanny faces of Christ/Moses → prefer distant silhouettes, hands, staffs,
  landscapes, light. Consistency via `style_lock` in every prompt.
- Stop after the storyboard table; wait for human review before generating images.
