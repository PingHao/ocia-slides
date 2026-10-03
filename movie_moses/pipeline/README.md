# Faith Video Pipeline — Conventions

Agent-driven workflow that turns a Catholic faith idea into a ~2-minute Chinese
narrated video. Deterministic stages are scripts; creative stages are done by
the agent via Kilo commands.

## Core principle: audio-length-driven timing

Audio is the clock. Each scene's duration = probed length of its audio clip +
`scene_padding`. Images/motion are stretched to fit; subtitles get exact
start/end times from the probed audio. Never hand-tune timings — generate audio,
re-run `assemble.py`.

## Directory layout (per video project)

```
<video_id>/
├── project.json          # SSOT manifest — scenes, paths, settings
├── pipeline/             # this package (shared, copy per repo root project)
├── 01_script/script.md   # narration table: scene id, purpose, 中文旁白
├── 02_storyboard/
│   ├── storyboard.md     # per-scene image prompts + motion (agent writes)
│   ├── timeline.json     # generated: exact scene start/end from audio
│   └── subs.ass          # generated: burned subtitles
├── 03_visuals/scene-XX.png
├── 04_audio/scene-XX.mp3
└── 05_video/
    ├── <video_id>.mp4    # final output (1920x1080, hard-burned subs)
    └── tmp/              # build artifacts (deleted after assemble)
```

## project.json schema

```jsonc
{
  "video_id": "movie_moses",        // also output filename
  "title_zh": "…",                   // required
  "title_en": "…",
  "target_duration": 120,            // seconds; script budget = target * chars_per_minute
  "chars_per_minute": 260,           // zh narration pace → ~520 chars for 2 min
  "scene_padding": 0.4,              // silence gap after each scene's audio
  "fps": 30,
  "resolution": [1920, 1080],        // source frames; see "vertical"
  "vertical": false,                 // true → final crop to 1080x1920 (Shorts/抖音)
  "tts": { "voice": "zh-CN-YunxiNeural", "rate": "+0%" },
  "style_lock": "…one paragraph prepended to every image prompt…",
  "scenes": [
    {
      "id": "01",
      "title": "hook",
      "narration_zh": "…",           // TTS text; keep punctuation — it shapes TTS pauses
      "subtitle_zh": "",             // optional short on-screen text; falls back to narration
      "image": "03_visuals/scene-01.png",
      "image_prompt": "…full prompt including style_lock…",
      "motion": { "type": "zoom-in", "zoom_from": 1.0, "zoom_to": 1.1 },
      "audio": "04_audio/scene-01.mp3"
    }
  ]
}
```

Motion types: `still` | `zoom-in` | `zoom-out` | `pan-left` | `pan-right`.
Use i2v (image-to-video) clips for 3–5 hero shots by placing the generated clip
at `03_visuals/scene-XX-anim.mp4` and pointing `image` at it — the pipeline
treats it as a video source the same way.

## Scripts

| Script | Purpose |
| ------ | ------- |
| `init_project.py --dir <video_id> --title-zh …` | scaffold folders + templates |
| `validate.py <dir>` | schema check, char budget vs target, asset existence, audio totals |
| `gen_tts.py <dir>` [--force] [--voice …] | per-scene TTS via edge-tts (audio-driven timing) |
| `assemble.py <dir>` [--dry-run] [--vertical 1\|0] [--no-subs] | probe audio → timeline.json + subs.ass → per-scene clips → concat → mux → final mp4 |

`assemble.py` burns subtitles if the ffmpeg build has the `subtitles` filter (libass).
If not, it falls back automatically: soft `mov_text` subtitle track inside the mp4 plus
an `.srt` sidecar in `05_video/`, with a warning to `brew reinstall ffmpeg` for
hard-burned Chinese subtitles. `--vertical 1` crops to 1080×1920 in both modes.

## Stage order (audio-length-driven)

1. `/video-new` — idea → `01_script/script.md` + `project.json` scenes skeleton
2. `/video-storyboard` — fill scenes: image prompts, motion; human review
3. `/video-visuals` — generate `03_visuals/scene-XX.png`; consistency review
4. `/video-audio` — `gen_tts.py`; listen, fix pronunciation/terminology, regenerate
5. `/video-assemble` — `validate.py` → `assemble.py` → review final cut
6. Human approval gate → publish

## Guardrails

- **Terminology**: Catholic Chinese — 天主/上主, 梅瑟 (not 摩西), 出谷纪 (not 出埃及记),
  梅瑟五书, 圣神 (not 圣灵), 耶稣基督. Traditional Catholic phrasing throughout.
- **Doctrine**: every claim traces to Scripture or CCC; no invented private revelation.
- **Visuals**: reverent framing; consistent style via `style_lock`; no grotesque
  or mocking depictions of sacred figures.
- Always end with a human review before publishing.
