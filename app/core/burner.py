"""Burn subtitles into video using ffmpeg."""

from __future__ import annotations

import re
import subprocess
from typing import Callable


def _get_duration(video_path: str) -> float:
    """Get video duration in seconds via ffprobe."""
    cmd = [
        "ffprobe",
        "-v", "quiet",
        "-print_format", "json",
        "-show_format",
        str(video_path),
    ]
    import json

    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    data = json.loads(result.stdout)
    return float(data["format"]["duration"])


def burn_subtitles(
    video_path: str,
    subtitle_path: str,
    output_path: str,
    progress_callback: Callable[[float], None] | None = None,
) -> None:
    """Burn subtitles into video using ffmpeg's subtitles filter.

    Uses styled font rendering. Reports progress by parsing ffmpeg stderr.
    """
    duration = _get_duration(video_path)

    # Escape special characters in subtitle path for ffmpeg filter
    escaped_sub = subtitle_path.replace("\\", "\\\\").replace(":", "\\:").replace("'", "\\'")

    cmd = [
        "ffmpeg",
        "-y",
        "-i", video_path,
        "-vf", f"subtitles='{escaped_sub}':force_style='FontSize=22,PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,Outline=2'",
        "-c:a", "copy",
        "-progress", "pipe:1",
        output_path,
    ]

    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    time_pattern = re.compile(r"out_time_us=(\d+)")

    if process.stdout:
        for line in process.stdout:
            match = time_pattern.search(line)
            if match and progress_callback and duration > 0:
                current_us = int(match.group(1))
                current_s = current_us / 1_000_000
                progress_callback(min(current_s / duration, 1.0))

    process.wait()
    if process.returncode != 0:
        stderr = process.stderr.read() if process.stderr else ""
        raise RuntimeError(f"ffmpeg burn failed (exit {process.returncode}): {stderr}")
