"""Orchestrates a single translation job end-to-end."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable

from app.core.subtitle_parser import (
    SubtitleEntry,
    load_subtitle,
    save_subtitle,
)
from app.core.translator import SubtitleTranslator
from app.core.transcriber import VideoTranscriber
from app.core.extractor import extract_subtitle, probe_subtitles
from app.core.burner import burn_subtitles
from app.languages import DEEPL_TO_WHISPER

VIDEO_EXTENSIONS = {".mp4", ".mkv", ".avi", ".mov", ".webm", ".flv", ".wmv"}
SUBTITLE_EXTENSIONS = {".srt", ".vtt"}


@dataclass
class JobConfig:
    input_path: str
    target_lang: str  # DeepL target code, e.g. "DE"
    source_lang: str = ""  # DeepL source code, empty for auto-detect
    subtitle_source: str = "auto"  # "auto", "whisper", "embedded"
    burn: bool = False
    output_format: str = "srt"  # "srt" or "vtt"
    output_dir: str = ""  # Empty means same directory as input
    whisper_model: str = "base"


@dataclass
class JobResult:
    input_path: str
    subtitle_path: str = ""
    video_path: str = ""
    success: bool = True
    error: str = ""


class Pipeline:
    def __init__(
        self,
        api_key: str = "",
        transcriber: VideoTranscriber | None = None,
        translation_service: str = "deepl",
    ) -> None:
        self._translator = SubtitleTranslator(api_key, service=translation_service)
        self._transcriber = transcriber

    def run(
        self,
        config: JobConfig,
        progress_callback: Callable[[float, str], None] | None = None,
    ) -> JobResult:
        """Run the full pipeline for a single job.

        progress_callback receives (fraction 0-1, status_message).
        """
        result = JobResult(input_path=config.input_path)

        def report(frac: float, msg: str) -> None:
            if progress_callback:
                progress_callback(frac, msg)

        try:
            input_path = Path(config.input_path)
            ext = input_path.suffix.lower()
            is_video = ext in VIDEO_EXTENSIONS
            is_subtitle = ext in SUBTITLE_EXTENSIONS

            # Step 1: Obtain subtitles
            report(0.0, "Obtaining subtitles...")
            entries = self._obtain_subtitles(config, is_video, is_subtitle)

            if not entries:
                raise RuntimeError("No subtitles found or generated.")

            # Step 2: Translate
            report(0.3, "Translating subtitles...")
            src = config.source_lang if config.source_lang else None

            def translate_progress(frac: float) -> None:
                report(0.3 + frac * 0.4, "Translating subtitles...")

            translated = self._translator.translate(
                entries,
                target_lang=config.target_lang,
                source_lang=src,
                progress_callback=translate_progress,
            )

            # Step 3: Save subtitle file
            report(0.7, "Saving subtitle file...")
            out_dir = Path(config.output_dir) if config.output_dir else input_path.parent
            out_dir.mkdir(parents=True, exist_ok=True)

            # Target lang code for filename (lowercase, strip variant)
            lang_tag = config.target_lang.lower().replace("-", "_")
            stem = input_path.stem
            # Strip existing lang tag if re-translating
            if is_subtitle:
                stem = Path(stem).stem if "." in stem else stem

            sub_ext = f".{config.output_format}"
            sub_filename = f"{stem}.{lang_tag}{sub_ext}"
            sub_path = out_dir / sub_filename
            save_subtitle(translated, sub_path)
            result.subtitle_path = str(sub_path)

            # Step 4: Optionally burn subtitles into video
            if config.burn and is_video:
                report(0.75, "Burning subtitles into video...")
                video_out = out_dir / f"{stem}.{lang_tag}{ext}"

                def burn_progress(frac: float) -> None:
                    report(0.75 + frac * 0.25, "Burning subtitles...")

                burn_subtitles(
                    str(input_path),
                    str(sub_path),
                    str(video_out),
                    progress_callback=burn_progress,
                )
                result.video_path = str(video_out)

            report(1.0, "Done")

        except Exception as e:
            result.success = False
            result.error = str(e)
            report(1.0, f"Error: {e}")

        return result

    def _obtain_subtitles(
        self, config: JobConfig, is_video: bool, is_subtitle: bool
    ) -> list[SubtitleEntry]:
        if is_subtitle:
            return load_subtitle(config.input_path)

        if not is_video:
            raise ValueError(f"Unsupported file type: {Path(config.input_path).suffix}")

        source = config.subtitle_source

        if source == "auto":
            # Try embedded first, fall back to Whisper
            streams = probe_subtitles(config.input_path)
            if streams:
                return extract_subtitle(config.input_path, stream_index=0)
            return self._whisper_transcribe(config)

        if source == "embedded":
            return extract_subtitle(config.input_path, stream_index=0)

        if source == "whisper":
            return self._whisper_transcribe(config)

        raise ValueError(f"Unknown subtitle source: {source}")

    def _whisper_transcribe(self, config: JobConfig) -> list[SubtitleEntry]:
        if self._transcriber is None:
            self._transcriber = VideoTranscriber(model_size=config.whisper_model)

        whisper_lang = None
        if config.source_lang:
            whisper_lang = DEEPL_TO_WHISPER.get(config.source_lang.upper())

        return self._transcriber.transcribe(config.input_path, language=whisper_lang)
