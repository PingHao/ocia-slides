---
description: Audio — TTS per scene (audio is the clock)
---

Generate Chinese narration for the video project: $ARGUMENTS (project dir, default `movie_moses`).

Read `movie_moses/pipeline/README.md`. Audio drives all timing — one clip per scene.

## Steps

1. If `edge-tts` is missing: `pip3 install edge-tts` (ask before installing globally).
2. Run `python3 <dir>/pipeline/gen_tts.py <dir> --force`
   (`--voice` overrides `project.json` tts.voice; default zh-CN-YunxiNeural).
3. Review the printed per-scene durations vs the script plan. Flag scenes whose
   audio feels too fast/slow for their text length.
4. Terminology check before finalizing TTS text: 天主/上主, 梅瑟, 出谷纪, 梅瑟五书,
   圣神, 耶稣基督. If a narration still uses Protestant terms, fix the script and
   regenerate that scene.
5. Re-run `python3 <dir>/pipeline/validate.py <dir>` and report total narration time
   vs `target_duration` (audio + padding must land within ±10s).
6. Remind the user: scene timing is finalized only at assembly; nothing to hand-tune.

If the user supplies professionally recorded audio instead, just place files at the
scene `audio` paths and skip steps 1–2.
