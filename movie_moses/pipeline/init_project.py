import argparse
import json
from pathlib import Path

DIRS = ["01_script", "02_storyboard", "03_visuals", "04_audio", "05_video"]

PROJECT_TEMPLATE = {
    "video_id": "",
    "title_zh": "",
    "title_en": "",
    "target_duration": 120,
    "chars_per_minute": 260,
    "scene_padding": 0.4,
    "fps": 30,
    "resolution": [1920, 1080],
    "vertical": False,
    "tts": {"voice": "zh-CN-YunxiNeural", "rate": "+0%"},
    "style_lock": "",
    "scenes": [],
}

SCRIPT_TEMPLATE = """# {title}

## Takeaway (one sentence)

> TODO

## Doctrine anchors

- Scripture: TODO
- CCC: TODO

## Narration (budget ~{budget} chars, Catholic terminology: 梅瑟/出谷纪/天主)

| Scene | Purpose | Narration (中文) | Notes |
| ----- | ------- | ---------------- | ----- |
| 01 | hook | TODO | |
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", default="movie_moses")
    ap.add_argument("--title-zh", default="")
    args = ap.parse_args()

    root = Path(args.dir)
    pipeline_src = Path(__file__).parent
    if root.resolve() == pipeline_src.parent.resolve():
        root = pipeline_src.parent

    for d in DIRS:
        (root / d).mkdir(parents=True, exist_ok=True)

    proj_path = root / "project.json"
    if not proj_path.exists():
        proj = dict(PROJECT_TEMPLATE)
        proj["video_id"] = root.name
        proj["title_zh"] = args.title_zh
        budget = int(proj["target_duration"] * proj["chars_per_minute"])
        proj_path.write_text(
            json.dumps(proj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
    else:
        proj = json.loads(proj_path.read_text(encoding="utf-8"))
        budget = int(proj["target_duration"] * proj.get("chars_per_minute", 260))

    script_path = root / "01_script" / "script.md"
    if not script_path.exists():
        script_path.write_text(
            SCRIPT_TEMPLATE.format(
                title=args.title_zh or proj["title_zh"] or root.name, budget=budget
            ),
            encoding="utf-8",
        )

    print(f"project ready: {root}")
    print(f"  manifest: {proj_path}")
    print(f"  script:   {script_path}")


if __name__ == "__main__":
    main()
