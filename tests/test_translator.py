"""Tests for translator (with mocked DeepL)."""

from datetime import timedelta
from unittest.mock import MagicMock, patch

from app.core.subtitle_parser import SubtitleEntry
from app.core.translator import SubtitleTranslator


def test_translator_batch():
    """Test translator batches requests correctly."""
    entries = [
        SubtitleEntry(i, timedelta(seconds=i), timedelta(seconds=i + 1), f"Text {i}")
        for i in range(1, 101)
    ]

    mock_result = MagicMock()
    mock_result.text = "Translated"

    with patch("deepl.DeepLClient") as mock_client:
        mock_instance = mock_client.return_value
        mock_instance.translate_text.return_value = [mock_result] * 50

        translator = SubtitleTranslator("fake-api-key")
        translated = translator.translate(entries, target_lang="DE", source_lang="EN")

        # Should make 2 calls (100 entries / 50 per batch)
        assert mock_instance.translate_text.call_count == 2
        assert len(translated) == 100
        assert all(e.text == "Translated" for e in translated)


def test_translator_progress():
    """Test progress callback is called."""
    entries = [
        SubtitleEntry(i, timedelta(seconds=i), timedelta(seconds=i + 1), f"Text {i}")
        for i in range(1, 51)
    ]

    mock_result = MagicMock()
    mock_result.text = "Translated"

    progress_values = []

    def progress_callback(frac):
        progress_values.append(frac)

    with patch("deepl.DeepLClient") as mock_client:
        mock_instance = mock_client.return_value
        mock_instance.translate_text.return_value = [mock_result] * 50

        translator = SubtitleTranslator("fake-api-key")
        translator.translate(
            entries,
            target_lang="DE",
            progress_callback=progress_callback,
        )

        assert len(progress_values) == 1
        assert progress_values[0] == 1.0
