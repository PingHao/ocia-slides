---
description: Assemble — timeline, subtitles, final mp4
---

Assemble the final video: $ARGUMENTS (project dir, default `movie_moses`; optional flags
like `--vertical 1`, `--dry-run`).

## Steps

1. `python3 <dir>/pipeline/validate.py <dir>` — must PASS before assembly.
2. Run `python3 <dir>/pipeline/assemble.py <dir>`:
   - probes every scene's audio → writes `02_storyboard/timeline.json` (exact start/end),
   - writes `02_storyboard/subs.ass` (hard-burned, PingFang SC, bottom center),
   - renders per-scene clips with Ken Burns motion, concatenates, muxes audio,
   - output: `05_video/<video_id>.mp4` (use `--vertical 1` for 1080×1920 Shorts crop).
3. Verify with ffprobe: total duration vs `target_duration` (warn if off >10s).
   Note: if the local ffmpeg lacks libass, assembly automatically falls back to soft
   subtitles + `.srt` sidecar and prints a `brew reinstall ffmpeg` hint — mention
   this to the user rather than treating it as a failure.
4. Review the cut: open the output, check subtitle sync on 2–3 scenes, image motion,
   and any audio clipping. List concrete issues if found (e.g. "scene 03 subtitle ends
   late") — fixes are script/TTS edits + re-run, never manual timeline edits.
5. Report final duration, file size, and path.

Human approval gate: publishing is a separate, explicit user decision.
