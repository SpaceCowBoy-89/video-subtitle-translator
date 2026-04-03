"""Load and save SRT/VTT subtitle files."""

from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import timedelta
from pathlib import Path


@dataclass
class SubtitleEntry:
    index: int
    start: timedelta
    end: timedelta
    text: str


def _parse_srt_time(s: str) -> timedelta:
    h, m, sec = s.strip().split(":")
    sec, ms = sec.split(",")
    return timedelta(hours=int(h), minutes=int(m), seconds=int(sec), milliseconds=int(ms))


def _format_srt_time(td: timedelta) -> str:
    total_seconds = int(td.total_seconds())
    ms = int(td.total_seconds() * 1000) % 1000
    h = total_seconds // 3600
    m = (total_seconds % 3600) // 60
    s = total_seconds % 60
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def _parse_vtt_time(s: str) -> timedelta:
    parts = s.strip().split(":")
    if len(parts) == 3:
        h, m, sec = parts
    else:
        h = "0"
        m, sec = parts
    sec, ms = sec.split(".")
    return timedelta(hours=int(h), minutes=int(m), seconds=int(sec), milliseconds=int(ms))


def _format_vtt_time(td: timedelta) -> str:
    total_seconds = int(td.total_seconds())
    ms = int(td.total_seconds() * 1000) % 1000
    h = total_seconds // 3600
    m = (total_seconds % 3600) // 60
    s = total_seconds % 60
    return f"{h:02d}:{m:02d}:{s:02d}.{ms:03d}"


def load_srt(path: str | Path) -> list[SubtitleEntry]:
    """Load subtitles from an SRT file."""
    import pysrt

    subs = pysrt.open(str(path), encoding="utf-8")
    entries = []
    for item in subs:
        start = timedelta(
            hours=item.start.hours,
            minutes=item.start.minutes,
            seconds=item.start.seconds,
            milliseconds=item.start.milliseconds,
        )
        end = timedelta(
            hours=item.end.hours,
            minutes=item.end.minutes,
            seconds=item.end.seconds,
            milliseconds=item.end.milliseconds,
        )
        entries.append(SubtitleEntry(index=item.index, start=start, end=end, text=item.text))
    return entries


def load_vtt(path: str | Path) -> list[SubtitleEntry]:
    """Load subtitles from a VTT file."""
    content = Path(path).read_text(encoding="utf-8")
    # Strip WEBVTT header
    content = re.sub(r"^WEBVTT.*?\n\n", "", content, count=1, flags=re.DOTALL)
    entries = []
    blocks = re.split(r"\n\n+", content.strip())
    for idx, block in enumerate(blocks, start=1):
        lines = block.strip().split("\n")
        # Skip optional cue identifier (numeric line)
        time_line_idx = 0
        for i, line in enumerate(lines):
            if "-->" in line:
                time_line_idx = i
                break
        time_parts = lines[time_line_idx].split("-->")
        start = _parse_vtt_time(time_parts[0])
        end = _parse_vtt_time(time_parts[1].split()[0])
        text = "\n".join(lines[time_line_idx + 1 :])
        entries.append(SubtitleEntry(index=idx, start=start, end=end, text=text))
    return entries


def load_subtitle(path: str | Path) -> list[SubtitleEntry]:
    """Load subtitles from SRT or VTT based on extension."""
    path = Path(path)
    ext = path.suffix.lower()
    if ext == ".srt":
        return load_srt(path)
    elif ext == ".vtt":
        return load_vtt(path)
    else:
        raise ValueError(f"Unsupported subtitle format: {ext}")


def save_srt(entries: list[SubtitleEntry], path: str | Path) -> None:
    """Save subtitles to an SRT file."""
    lines = []
    for entry in entries:
        lines.append(str(entry.index))
        lines.append(f"{_format_srt_time(entry.start)} --> {_format_srt_time(entry.end)}")
        lines.append(entry.text)
        lines.append("")
    Path(path).write_text("\n".join(lines), encoding="utf-8")


def save_vtt(entries: list[SubtitleEntry], path: str | Path) -> None:
    """Save subtitles to a VTT file."""
    lines = ["WEBVTT", ""]
    for entry in entries:
        lines.append(str(entry.index))
        lines.append(f"{_format_vtt_time(entry.start)} --> {_format_vtt_time(entry.end)}")
        lines.append(entry.text)
        lines.append("")
    Path(path).write_text("\n".join(lines), encoding="utf-8")


def save_subtitle(entries: list[SubtitleEntry], path: str | Path) -> None:
    """Save subtitles to SRT or VTT based on extension."""
    path = Path(path)
    ext = path.suffix.lower()
    if ext == ".srt":
        save_srt(entries, path)
    elif ext == ".vtt":
        save_vtt(entries, path)
    else:
        raise ValueError(f"Unsupported subtitle format: {ext}")
