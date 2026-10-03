import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("project", nargs="?", default=".")
    ap.add_argument("--force", action="store_true", help="regenerate existing audio files")
    ap.add_argument("--voice", default=None, help="override tts voice")
    args = ap.parse_args()

    root = Path(args.project).resolve()
    proj = json.loads((root / "project.json").read_text(encoding="utf-8"))

    if shutil.which("edge-tts") is None:
        sys.exit("edge-tts not found. Install with: pip3 install edge-tts")

    voice = args.voice or proj.get("tts", {}).get("voice", "zh-CN-YunxiNeural")
    rate = proj.get("tts", {}).get("rate", "+0%")
    print(f"voice: {voice} rate: {rate}")

    generated = 0
    for sc in proj.get("scenes", []):
        sid = sc["id"]
        text = (sc.get("tts_text") or sc.get("narration_zh", "")).strip()
        if not text:
            print(f"scene {sid}: skipped (no narration)")
            continue
        out = root / sc.get("audio", f"04_audio/scene-{sid}.mp3")
        out.parent.mkdir(parents=True, exist_ok=True)
        if out.exists() and not args.force:
            print(f"scene {sid}: exists, skip ({out.name}); use --force to regenerate")
            continue
        print(f"scene {sid}: {len(text)} chars -> {out.name}")
        r = subprocess.run(
            ["edge-tts", "--voice", voice, "--rate", rate, "--text", text, "--write-media", str(out)],
            capture_output=True,
            text=True,
        )
        if r.returncode != 0:
            print(r.stderr[-800:], file=sys.stderr)
            sys.exit(f"edge-tts failed for scene {sid}")
        generated += 1

    if generated == 0:
        print("nothing generated")
        return

    for sc in proj.get("scenes", []):
        out = root / sc.get("audio", f"04_audio/scene-{sc['id']}.mp3")
        if out.exists():
            r = subprocess.run(
                ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "json", str(out)],
                capture_output=True, text=True,
            )
            if r.returncode == 0:
                d = float(json.loads(r.stdout)["format"]["duration"])
                print(f"scene {sc['id']}: {d:.2f}s")
    print("done — re-run validate.py to check total duration")


if __name__ == "__main__":
    main()
