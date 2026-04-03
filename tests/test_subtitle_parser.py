"""Tests for subtitle parser."""

import tempfile
from datetime import timedelta
from pathlib import Path

from app.core.subtitle_parser import (
    SubtitleEntry,
    load_srt,
    load_vtt,
    save_srt,
    save_vtt,
)


def test_srt_roundtrip():
    """Test loading and saving SRT files."""
    entries = [
        SubtitleEntry(1, timedelta(seconds=1), timedelta(seconds=3), "Hello world"),
        SubtitleEntry(2, timedelta(seconds=5), timedelta(seconds=7), "Second line\nWith newline"),
    ]

    with tempfile.NamedTemporaryFile(mode="w", suffix=".srt", delete=False) as f:
        tmp_path = f.name

    try:
        save_srt(entries, tmp_path)
        loaded = load_srt(tmp_path)

        assert len(loaded) == len(entries)
        for orig, loaded_entry in zip(entries, loaded):
            assert orig.index == loaded_entry.index
            assert orig.start == loaded_entry.start
            assert orig.end == loaded_entry.end
            assert orig.text == loaded_entry.text
    finally:
        Path(tmp_path).unlink(missing_ok=True)


def test_vtt_roundtrip():
    """Test loading and saving VTT files."""
    entries = [
        SubtitleEntry(1, timedelta(seconds=1, milliseconds=500), timedelta(seconds=3), "Hello VTT"),
        SubtitleEntry(2, timedelta(seconds=5), timedelta(seconds=7, milliseconds=250), "Second line"),
    ]

    with tempfile.NamedTemporaryFile(mode="w", suffix=".vtt", delete=False) as f:
        tmp_path = f.name

    try:
        save_vtt(entries, tmp_path)
        loaded = load_vtt(tmp_path)

        assert len(loaded) == len(entries)
        for orig, loaded_entry in zip(entries, loaded):
            assert orig.start == loaded_entry.start
            assert orig.end == loaded_entry.end
            assert orig.text == loaded_entry.text
    finally:
        Path(tmp_path).unlink(missing_ok=True)


def test_time_formatting():
    """Test time format conversions."""
    entries = [
        SubtitleEntry(
            1,
            timedelta(hours=1, minutes=23, seconds=45, milliseconds=678),
            timedelta(hours=1, minutes=23, seconds=47, milliseconds=890),
            "Test",
        ),
    ]

    with tempfile.NamedTemporaryFile(mode="w", suffix=".srt", delete=False) as f:
        tmp_path = f.name

    try:
        save_srt(entries, tmp_path)
        content = Path(tmp_path).read_text()
        assert "01:23:45,678" in content
        assert "01:23:47,890" in content
    finally:
        Path(tmp_path).unlink(missing_ok=True)
