import argparse
import json
import subprocess
import sys
from pathlib import Path


def probe_duration(path):
    r = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "json", str(path)],
        capture_output=True,
        text=True,
    )
    if r.returncode != 0:
        return None
    return float(json.loads(r.stdout)["format"]["duration"])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("project", nargs="?", default=".")
    args = ap.parse_args()

    root = Path(args.project).resolve()
    proj_path = root / "project.json"
    if not proj_path.exists():
        sys.exit(f"no project.json in {root}")
    proj = json.loads(proj_path.read_text(encoding="utf-8"))

    errors, warnings, notes = [], [], []

    for key in ("video_id", "title_zh", "target_duration"):
        if not proj.get(key):
            errors.append(f"missing required field: {key}")

    scenes = proj.get("scenes", [])
    if not scenes:
        errors.append("no scenes defined")
    ids = [s.get("id") for s in scenes]
    if len(ids) != len(set(ids)):
        errors.append("duplicate scene ids")

    cpm = proj.get("chars_per_minute", 260)
    target = proj.get("target_duration", 120)
    total_chars = 0
    total_audio = 0.0
    for s in scenes:
        sid = s.get("id", "?")
        narration = s.get("narration_zh", "")
        if not narration:
            errors.append(f"scene {sid}: narration_zh empty")
        total_chars += len(narration.replace(" ", ""))

        img = s.get("image")
        if not img:
            warnings.append(f"scene {sid}: no image set")
        elif not (root / img).exists():
            warnings.append(f"scene {sid}: image not found: {img}")

        audio = s.get("audio")
        if not audio:
            notes.append(f"scene {sid}: no audio yet")
        elif not (root / audio).exists():
            warnings.append(f"scene {sid}: audio file missing: {audio}")
        else:
            d = probe_duration(root / audio)
            if d:
                total_audio += d

    est = total_chars / cpm * 60
    notes.append(f"narration: {total_chars} chars -> est {est:.0f}s (target {target}s)")
    if est < target * 0.9:
        warnings.append(f"script looks short: est {est:.0f}s vs target {target}s")
    if est > target * 1.1:
        warnings.append(f"script looks long: est {est:.0f}s vs target {target}s")

    if total_audio > 0:
        pad = proj.get("scene_padding", 0.4) * len(scenes)
        notes.append(f"audio present for all/partial scenes: {total_audio:.1f}s (+{pad:.1f}s padding = {total_audio + pad:.1f}s)")
        if total_audio + pad < target - 10:
            warnings.append(f"audio total {total_audio + pad:.1f}s is well below target {target}s")

    print("=== validate ===")
    for label, items in (("ERROR", errors), ("WARN", warnings), ("INFO", notes)):
        for it in items:
            print(f"[{label}] {it}")
    if errors:
        print(f"result: FAIL ({len(errors)} errors)")
        sys.exit(1)
    print("result: PASS")


if __name__ == "__main__":
    main()
