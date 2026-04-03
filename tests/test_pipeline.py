"""Tests for pipeline orchestration."""

import tempfile
from datetime import timedelta
from pathlib import Path
from unittest.mock import MagicMock, patch

from app.core.pipeline import JobConfig, Pipeline
from app.core.subtitle_parser import SubtitleEntry, save_srt


def test_pipeline_subtitle_input():
    """Test pipeline with subtitle file input."""
    entries = [
        SubtitleEntry(1, timedelta(seconds=1), timedelta(seconds=3), "Hello"),
        SubtitleEntry(2, timedelta(seconds=5), timedelta(seconds=7), "World"),
    ]

    with tempfile.TemporaryDirectory() as tmpdir:
        input_srt = Path(tmpdir) / "input.srt"
        save_srt(entries, input_srt)

        translated_entries = [
            SubtitleEntry(1, timedelta(seconds=1), timedelta(seconds=3), "Hallo"),
            SubtitleEntry(2, timedelta(seconds=5), timedelta(seconds=7), "Welt"),
        ]

        with patch("app.core.pipeline.SubtitleTranslator") as mock_translator_class:
            mock_translator = mock_translator_class.return_value
            mock_translator.translate.return_value = translated_entries

            pipeline = Pipeline("fake-api-key")
            config = JobConfig(
                input_path=str(input_srt),
                target_lang="DE",
                source_lang="EN",
                output_dir=tmpdir,
            )

            result = pipeline.run(config)

            assert result.success
            assert result.subtitle_path
            assert Path(result.subtitle_path).exists()

            # Verify output was saved
            from app.core.subtitle_parser import load_srt
            output = load_srt(result.subtitle_path)
            assert len(output) == 2
            assert output[0].text == "Hallo"


def test_pipeline_error_handling():
    """Test pipeline handles errors gracefully."""
    with tempfile.TemporaryDirectory() as tmpdir:
        input_file = Path(tmpdir) / "nonexistent.srt"

        pipeline = Pipeline("fake-api-key")
        config = JobConfig(
            input_path=str(input_file),
            target_lang="DE",
        )

        result = pipeline.run(config)

        assert not result.success
        assert result.error
