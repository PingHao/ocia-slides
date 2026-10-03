---
description: Faith video — full pipeline end-to-end
---

Run the full faith-video pipeline for: $ARGUMENTS (idea, and optional project dir;
default `movie_moses` for the idea "Moses"). Read `movie_moses/pipeline/README.md` first.

Execute the six stages in order, pausing only at the two human gates:

1. `/video-new <idea>` — script + manifest → show the narration table.
2. **GATE 1 — human script approval.** Stop and wait.
3. `/video-storyboard <dir>` — prompts + motion → show the storyboard table.
4. `/video-visuals <dir>` — generate images, consistency review.
5. `/video-audio <dir>` — TTS per scene, terminology check, duration report.
6. `/video-assemble <dir>` — validate + assemble + review the final cut.
7. **GATE 2 — human approval of the cut** before any publishing.

Rules:

- Each stage's command file defines its steps and guardrails — follow them.
- If a stage fails validation, fix at the source (script text, TTS, image) and re-run;
  never hand-edit `timeline.json` or `subs.ass`.
- Audio drives timing: changing narration means regenerating that scene's audio,
  then re-running assembly.
- Keep the user informed with one concise status line per stage; no long narration.
