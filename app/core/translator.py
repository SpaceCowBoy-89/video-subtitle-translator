"""Translation API wrapper supporting DeepL and Google Translate."""

from __future__ import annotations

from typing import Callable

from app.core.subtitle_parser import SubtitleEntry

BATCH_SIZE = 50


class SubtitleTranslator:
    def __init__(self, api_key: str = "", service: str = "deepl") -> None:
        """Initialize translator with specified service.

        Args:
            api_key: API key (required for DeepL, optional for Google)
            service: "deepl" or "google"
        """
        self._service = service.lower()
        self._api_key = api_key
        self._client = None

        if self._service == "deepl":
            import deepl
            if not api_key:
                raise ValueError("DeepL requires an API key")
            self._client = deepl.DeepLClient(api_key)
        elif self._service == "google":
            # Google Translate via deep-translator (free, no API key needed)
            from deep_translator import GoogleTranslator
            self._translator_class = GoogleTranslator
        else:
            raise ValueError(f"Unsupported translation service: {service}")

    def translate(
        self,
        entries: list[SubtitleEntry],
        target_lang: str,
        source_lang: str | None = None,
        progress_callback: Callable[[float], None] | None = None,
    ) -> list[SubtitleEntry]:
        """Translate subtitle entries, returning new entries with translated text."""
        if self._service == "deepl":
            return self._translate_deepl(entries, target_lang, source_lang, progress_callback)
        else:
            return self._translate_google(entries, target_lang, source_lang, progress_callback)

    def _translate_deepl(
        self,
        entries: list[SubtitleEntry],
        target_lang: str,
        source_lang: str | None,
        progress_callback: Callable[[float], None] | None,
    ) -> list[SubtitleEntry]:
        """Translate using DeepL API."""
        translated: list[SubtitleEntry] = []
        total = len(entries)

        for i in range(0, total, BATCH_SIZE):
            batch = entries[i : i + BATCH_SIZE]
            texts = [e.text for e in batch]

            results = self._client.translate_text(
                texts,
                target_lang=target_lang,
                source_lang=source_lang if source_lang else None,
            )

            for entry, result in zip(batch, results):
                translated.append(
                    SubtitleEntry(
                        index=entry.index,
                        start=entry.start,
                        end=entry.end,
                        text=result.text,
                    )
                )

            if progress_callback:
                progress_callback(min(i + len(batch), total) / total)

        return translated

    def _translate_google(
        self,
        entries: list[SubtitleEntry],
        target_lang: str,
        source_lang: str | None,
        progress_callback: Callable[[float], None] | None,
    ) -> list[SubtitleEntry]:
        """Translate using Google Translate (free)."""
        from app.languages import DEEPL_TO_GOOGLE

        # Convert DeepL language codes to Google codes
        target = DEEPL_TO_GOOGLE.get(target_lang.upper().split('-')[0], target_lang.lower())
        source = DEEPL_TO_GOOGLE.get(source_lang.upper(), 'auto') if source_lang else 'auto'

        translated: list[SubtitleEntry] = []
        total = len(entries)

        for i, entry in enumerate(entries):
            translator = self._translator_class(source=source, target=target)
            translated_text = translator.translate(entry.text)

            translated.append(
                SubtitleEntry(
                    index=entry.index,
                    start=entry.start,
                    end=entry.end,
                    text=translated_text,
                )
            )

            if progress_callback:
                progress_callback((i + 1) / total)

        return translated
