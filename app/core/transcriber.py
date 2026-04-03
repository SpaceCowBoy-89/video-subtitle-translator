"""Whisper speech recognition wrapper."""

from __future__ import annotations

from datetime import timedelta
from typing import Callable

from app.core.subtitle_parser import SubtitleEntry


class VideoTranscriber:
    def __init__(self, model_size: str = "base") -> None:
        self._model_size = model_size
        self._model = None

    def _ensure_model(self) -> None:
        if self._model is None:
            import whisper

            self._model = whisper.load_model(self._model_size)

    def transcribe(
        self,
        video_path: str,
        language: str | None = None,
        progress_callback: Callable[[float], None] | None = None,
    ) -> list[SubtitleEntry]:
        """Transcribe audio from video file, returning subtitle entries."""
        self._ensure_model()

        options: dict = {"verbose": False}
        if language:
            options["language"] = language

        result = self._model.transcribe(str(video_path), **options)

        entries: list[SubtitleEntry] = []
        segments = result.get("segments", [])
        for idx, seg in enumerate(segments, start=1):
            entries.append(
                SubtitleEntry(
                    index=idx,
                    start=timedelta(seconds=seg["start"]),
                    end=timedelta(seconds=seg["end"]),
                    text=seg["text"].strip(),
                )
            )
            if progress_callback:
                progress_callback(idx / len(segments))

        return entries
