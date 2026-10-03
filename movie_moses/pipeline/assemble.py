import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

FFMPEG = "ffmpeg"
FFPROBE = "ffprobe"

PUNCT_RE = re.compile(r"([，。！？；：、…—,.!?;:]+)")
PUNCT_ONLY_RE = re.compile(r"[，。！？；：、…—,.!?;:]+")


def run(cmd, cwd, dry=False):
    printable = " ".join(str(c) for c in cmd)
    if dry:
        print(f"  [dry] {printable}")
        return
    print(f"  $ {printable}")
    r = subprocess.run([str(c) for c in cmd], cwd=cwd, capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stderr[-3000:], file=sys.stderr)
        sys.exit(f"command failed: {printable}")


def has_filter(name):
    r = subprocess.run(
        [FFMPEG, "-hide_banner", "-filters"], capture_output=True, text=True
    )
    return re.search(rf"^\s*\S+\s+{re.escape(name)}\s", r.stdout, re.M) is not None


def probe_duration(path, cwd):
    r = subprocess.run(
        [FFPROBE, "-v", "error", "-show_entries", "format=duration", "-of", "json", str(path)],
        cwd=cwd,
        capture_output=True,
        text=True,
    )
    if r.returncode != 0:
        sys.exit(f"ffprobe failed for {path}: {r.stderr[-500:]}")
    return float(json.loads(r.stdout)["format"]["duration"])


def split_segments(text, max_len=16):
    parts = PUNCT_RE.split(text)
    segs, buf = [], ""
    for p in parts:
        if not p:
            continue
        if PUNCT_ONLY_RE.fullmatch(p):
            buf += p
            if buf.strip():
                segs.append(buf)
                buf = ""
        else:
            buf += p
            while len(buf) > max_len:
                segs.append(buf[:max_len])
                buf = buf[max_len:]
    if buf.strip():
        segs.append(buf)
    return [s.strip() for s in segs if s.strip()]


def ass_time(sec):
    sec = max(0.0, sec)
    h = int(sec // 3600)
    m = int((sec % 3600) // 60)
    s = sec % 60
    return f"{h}:{m:02d}:{s:05.2f}"


def write_subs(proj, timeline, path):
    w, h = proj["resolution"]
    fontsize = round(h * 0.052)
    margin = round(h * 0.07)
    lines = [
        "[Script Info]",
        "ScriptType: v4.00+",
        f"PlayResX: {w}",
        f"PlayResY: {h}",
        "WrapStyle: 0",
        "",
        "[V4+ Styles]",
        "Format: Name, Fontname, Fontsize, PrimaryColour, OutlineColour, BackColour, Bold, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, BorderStyle",
        f"Style: Default,PingFang SC,{fontsize},&H00FFFFFF,&H00101010,&HAA000000,-1,3,1,2,{margin},{margin},{margin},1",
        "",
        "[Events]",
        "Format: Layer, Start, End, Style, Text",
    ]
    total_pad = sum(
        t["duration"] - t["audio_duration"] for t in timeline["scenes"]
    )
    for sc in timeline["scenes"]:
        text = sc["subtitle_text"]
        segs = split_segments(text)
        if not segs:
            continue
        window = sc["audio_duration"]
        weights = [len(s) for s in segs]
        total = sum(weights)
        cursor = sc["start"]
        for seg, wgt in zip(segs, weights):
            span = window * wgt / total
            lines.append(
                f"Dialogue: 0,{ass_time(cursor)},{ass_time(cursor + span)},Default,,,0,0,0,,{seg}"
            )
            cursor += span
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def motion_filter(motion, w, h, n, fps):
    motion = motion or {}
    t = motion.get("type", "zoom-in")
    z0 = motion.get("zoom_from", 1.0)
    z1 = motion.get("zoom_to", 1.1)
    cx = "iw/2-(iw/zoom/2)"
    cy = "ih/2-(ih/zoom/2)"

    def zpan(z, x, y):
        return f"zoompan=z='{z}':x='{x}':y='{y}':d=1:s={w}x{h}:fps={fps}"

    if t == "still":
        return f"scale={w}:{h}:force_original_aspect_ratio=increase,crop={w}:{h},setsar=1"
    if t == "zoom-in":
        return f"scale={w * 4}:-2,{zpan(f'{z0}+({z1}-{z0})*on/{n}', cx, cy)},setsar=1"
    if t == "zoom-out":
        return f"scale={w * 4}:-2,{zpan(f'{z1}-({z1}-{z0})*on/{n}', cx, cy)},setsar=1"
    if t in ("pan-left", "pan-right"):
        z = max(z1, 1.05)
        xf = f"(iw-iw/zoom)*(1-on/{n})" if t == "pan-left" else f"(iw-iw/zoom)*(on/{n})"
        return f"scale={w * 4}:-2,{zpan(f'{z}', xf, cy)},setsar=1"
    sys.exit(f"unknown motion type: {t}")


def build_timeline(proj, cwd):
    pad = proj.get("scene_padding", 0.4)
    timeline_scenes = []
    missing = []
    cursor = 0.0
    for sc in proj["scenes"]:
        audio = sc.get("audio")
        if not audio or not (cwd / audio).exists():
            missing.append(f"scene {sc['id']}: audio missing ({audio})")
            continue
        raw = probe_duration(audio, cwd)
        dur = raw + pad
        subtitle_text = sc.get("subtitle_zh") or sc.get("narration_zh", "")
        timeline_scenes.append(
            {
                "id": sc["id"],
                "start": round(cursor, 3),
                "end": round(cursor + dur, 3),
                "audio_duration": round(raw, 3),
                "duration": round(dur, 3),
                "image": sc.get("image"),
                "subtitle_text": subtitle_text,
            }
        )
        cursor += dur
    if missing:
        sys.exit("audio-driven timing requires audio for every scene:\n  " + "\n  ".join(missing))
    return {
        "video_id": proj["video_id"],
        "fps": proj.get("fps", 30),
        "resolution": proj["resolution"],
        "padding": pad,
        "total_duration": round(cursor, 3),
        "scenes": timeline_scenes,
    }


def srt_time(sec):
    sec = max(0.0, sec)
    h = int(sec // 3600)
    m = int((sec % 3600) // 60)
    s = sec % 60
    return f"{h:02d}:{m:02d}:{s:06.3f}".replace(".", ",")


def write_srt(timeline, path):
    idx = 0
    lines = []
    for sc in timeline["scenes"]:
        segs = split_segments(sc["subtitle_text"])
        if not segs:
            continue
        weights = [len(s) for s in segs]
        total = sum(weights)
        cursor = sc["start"]
        for seg, wgt in zip(segs, weights):
            span = sc["audio_duration"] * wgt / total
            idx += 1
            lines += [str(idx), f"{srt_time(cursor)} --> {srt_time(cursor + span)}", seg, ""]
            cursor += span
    path.write_text("\n".join(lines), encoding="utf-8")


def assemble(proj, args, cwd):
    fps = proj.get("fps", 30)
    w, h = proj["resolution"]
    tmp = cwd / "05_video" / "tmp"
    (tmp / "video").mkdir(parents=True, exist_ok=True)
    (tmp / "audio").mkdir(parents=True, exist_ok=True)

    timeline = build_timeline(proj, cwd)
    tl_path = cwd / "02_storyboard" / "timeline.json"
    tl_path.write_text(json.dumps(timeline, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"timeline: {tl_path} (total {timeline['total_duration']:.2f}s)")

    subs_path = cwd / "02_storyboard" / "subs.ass"
    write_subs(proj, timeline, subs_path)
    print(f"subtitles: {subs_path}")

    for sc, tl in zip(proj["scenes"], timeline["scenes"]):
        n = max(1, round(tl["duration"] * fps))
        vf = motion_filter(sc.get("motion"), w, h, n, fps)
        run(
            [
                FFMPEG, "-y", "-loglevel", "error", "-loop", "1", "-framerate", fps,
                "-i", sc["image"], "-t", f"{tl['duration']:.3f}", "-vf", vf,
                "-c:v", "libx264", "-preset", "fast", "-crf", "18",
                "-pix_fmt", "yuv420p", tmp / "video" / f"scene-{sc['id']}.mp4",
            ],
            cwd,
            args.dry_run,
        )
        run(
            [
                FFMPEG, "-y", "-loglevel", "error", "-i", sc["audio"],
                "-af", f"apad=pad_dur={proj.get('scene_padding', 0.4)}",
                "-ar", "48000", "-ac", "2", "-c:a", "pcm_s16le",
                tmp / "audio" / f"scene-{sc['id']}.wav",
            ],
            cwd,
            args.dry_run,
        )

    vlist = tmp / "video" / "list.txt"
    vlist.write_text(
        "\n".join(f"file 'scene-{tl['id']}.mp4'" for tl in timeline["scenes"]) + "\n",
        encoding="utf-8",
    )
    alist = tmp / "audio" / "list.txt"
    alist.write_text(
        "\n".join(f"file 'scene-{tl['id']}.wav'" for tl in timeline["scenes"]) + "\n",
        encoding="utf-8",
    )

    run([FFMPEG, "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", vlist, "-c", "copy", tmp / "concat.mp4"], cwd, args.dry_run)
    run([FFMPEG, "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", alist, "-c", "copy", tmp / "audio.wav"], cwd, args.dry_run)

    vertical = args.vertical if args.vertical is not None else proj.get("vertical", False)
    out = cwd / "05_video" / f"{proj['video_id']}.mp4"

    if has_filter("subtitles"):
        vf = f"subtitles={subs_path.relative_to(cwd)}"
        if vertical:
            vf = f"scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,{vf}"
        run(
            [
                FFMPEG, "-y", "-loglevel", "error", "-i", tmp / "concat.mp4",
                "-i", tmp / "audio.wav", "-vf", vf, "-map", "0:v", "-map", "1:a",
                "-c:v", "libx264", "-preset", "medium", "-crf", "19",
                "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
                "-movflags", "+faststart", out,
            ],
            cwd,
            args.dry_run,
        )
    else:
        print(
            "WARNING: this ffmpeg build has no 'subtitles' filter (libass missing).\n"
            "  Falling back to soft subtitles + sidecar files.\n"
            "  For hard-burned Chinese subtitles install libass ffmpeg: brew reinstall ffmpeg"
        )
        srt_path = cwd / "05_video" / f"{proj['video_id']}.srt"
        write_srt(timeline, srt_path)
        vfilters = [
            "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920"
        ] if vertical else None
        cmd = [
            FFMPEG, "-y", "-loglevel", "error", "-i", tmp / "concat.mp4",
            "-i", tmp / "audio.wav", "-i", subs_path, "-map", "0:v", "-map", "1:a",
            "-map", "2:0",
        ]
        if vfilters:
            cmd += ["-vf", vfilters[0], "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-pix_fmt", "yuv420p"]
        else:
            cmd += ["-c:v", "copy"]
        cmd += [
            "-c:a", "aac", "-b:a", "192k",
            "-c:s", "mov_text", "-metadata:s:s:0", "language=chi",
            "-movflags", "+faststart", out,
        ]
        run(cmd, cwd, args.dry_run)
        print(f"sidecar subtitles: {srt_path}")

    if not args.dry_run:
        dur = probe_duration(out, cwd)
        print(f"output: {out} ({dur:.2f}s, target {proj['target_duration']}s)")
        if abs(dur - proj["target_duration"]) > 10:
            print("WARNING: duration deviates more than 10s from target")
    if not args.keep_tmp:
        import shutil

        shutil.rmtree(tmp, ignore_errors=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("project", nargs="?", default=".", help="project dir containing project.json")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--no-subs", action="store_true")
    ap.add_argument("--keep-tmp", action="store_true")
    ap.add_argument("--vertical", type=lambda v: v.lower() in ("1", "true", "yes"), default=None)
    args = ap.parse_args()

    cwd = Path(args.project).resolve()
    proj = json.loads((cwd / "project.json").read_text(encoding="utf-8"))
    if args.no_subs:
        (cwd / "02_storyboard" / "subs.ass").write_text("", encoding="utf-8")
    assemble(proj, args, cwd)


if __name__ == "__main__":
    main()
