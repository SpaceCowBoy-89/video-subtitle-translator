"""Extract embedded subtitles from video files using ffmpeg."""

from __future__ import annotations

import json
import subprocess
import tempfile
from pathlib import Path

from app.core.subtitle_parser import SubtitleEntry, load_srt


def probe_subtitles(video_path: str) -> list[dict]:
    """Probe a video file for embedded subtitle streams.

    Returns a list of dicts with keys: index, codec_name, language (if tagged).
    """
    cmd = [
        "ffprobe",
        "-v", "quiet",
        "-print_format", "json",
        "-show_streams",
        "-select_streams", "s",
        str(video_path),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    data = json.loads(result.stdout)
    streams = []
    for stream in data.get("streams", []):
        info = {
            "index": stream["index"],
            "codec_name": stream.get("codec_name", "unknown"),
        }
        tags = stream.get("tags", {})
        if "language" in tags:
            info["language"] = tags["language"]
        streams.append(info)
    return streams


def extract_subtitle(
    video_path: str, stream_index: int = 0
) -> list[SubtitleEntry]:
    """Extract a subtitle stream from a video file and return parsed entries."""
    with tempfile.NamedTemporaryFile(suffix=".srt", delete=False) as tmp:
        tmp_path = tmp.name

    cmd = [
        "ffmpeg",
        "-y",
        "-i", str(video_path),
        "-map", f"0:s:{stream_index}",
        "-c:s", "srt",
        tmp_path,
    ]
    subprocess.run(cmd, capture_output=True, text=True, check=True)

    try:
        entries = load_srt(tmp_path)
    finally:
        Path(tmp_path).unlink(missing_ok=True)

    return entries
