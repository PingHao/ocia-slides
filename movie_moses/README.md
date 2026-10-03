# movie_moses — Catholic faith short video (Chinese, ~2 min)

Audio-length-driven pipeline: see `pipeline/README.md` for the full conventions
and `project.json` schema.

## Operating loop (Kilo commands)

```
/video-new            # idea → script.md + project.json scenes
/video-storyboard     # scenes: image prompts + motion
/video-visuals        # generate 03_visuals/scene-XX.png
/video-audio          # TTS per scene → 04_audio/
/video-assemble       # timeline + subtitles + final mp4
/video-build          # run all stages end-to-end
```

## Manual equivalent

```bash
python3 pipeline/validate.py .
python3 pipeline/gen_tts.py .
python3 pipeline/assemble.py .            # add --vertical 1 for Shorts
```
