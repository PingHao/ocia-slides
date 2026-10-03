---
description: Start a faith video — idea → Chinese script → project.json scenes
---

Start a new Catholic faith short video in this repo's audio-length-driven pipeline.

**Input:** $ARGUMENTS (idea or topic; if empty, ask the user for one idea only).

First read `movie_moses/pipeline/README.md` for conventions and the `project.json` schema.

## Steps

1. If the project folder for this idea does not exist, run:
   `python3 movie_moses/pipeline/init_project.py --dir <video_id> --title-zh "<中文标题>"`
   (inside the repo root; pipeline scripts can live in `movie_moses/pipeline/` and target other dirs via `--dir`).
2. Write the script to `01_script/script.md`:
   - Budget: `target_duration × chars_per_minute` (~260 字/分钟 → ~520 chars for 2 min).
   - Structure: hook (10s) → story (75s) → reflection/application (25s) → closing prayer (10s).
   - Spoken, warm, reverent Chinese; short sentences (they shape TTS pacing); keep punctuation.
3. Create one scene per beat in `project.json` (10–14 scenes for 2 min), each with
   `id`, `title`, `narration_zh`, `image` path (`03_visuals/scene-XX.png`), `audio` path
   (`04_audio/scene-XX.mp3`). Leave `image_prompt`/`motion` empty for /video-storyboard.
4. Set `title_zh`, `title_en`, and `style_lock` (one paragraph: palette, era, composition,
   reverent tone — this is prepended to every image prompt later).
5. Run `python3 movie_moses/pipeline/validate.py <dir>` and report the char-budget estimate.

## Guardrails

- Catholic Chinese terminology: 天主/上主, 梅瑟 (NOT 摩西), 出谷纪 (NOT 出埃及记),
  梅瑟五书, 圣神 (NOT 圣灵), 感恩祭/圣体, 玛利亚.
- Every doctrinal claim must trace to Scripture or the Catechism (CCC); cite the anchor
  in script.md under "Doctrine anchors". No invented private revelations.
- Do not proceed to visuals/audio. Stop after validation and show the narration table.
