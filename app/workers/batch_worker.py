"""Worker for running multiple pipeline jobs sequentially."""

from __future__ import annotations

from app.core.pipeline import JobConfig, Pipeline
from app.core.transcriber import VideoTranscriber
from app.workers.base_worker import BaseWorker


class BatchWorker(BaseWorker):
    def __init__(
        self,
        api_key: str,
        configs: list[JobConfig],
        whisper_model: str,
        translation_service: str = "deepl"
    ) -> None:
        super().__init__()
        self._api_key = api_key
        self._configs = configs
        self._whisper_model = whisper_model
        self._translation_service = translation_service
        self._cancelled = False

    def cancel(self) -> None:
        """Request cancellation of the batch."""
        self._cancelled = True

    def run(self) -> None:
        """Execute all jobs sequentially."""
        results = []
        try:
            # Reuse Whisper model across all jobs
            transcriber = VideoTranscriber(model_size=self._whisper_model)
            pipeline = Pipeline(
                self._api_key,
                transcriber=transcriber,
                translation_service=self._translation_service
            )

            total = len(self._configs)

            for i, config in enumerate(self._configs):
                if self._cancelled:
                    self.status.emit("Cancelled")
                    break

                self.status.emit(f"Processing {i + 1}/{total}: {config.input_path}")

                # Fix: capture i by value via default argument to avoid closure bug
                def job_progress(frac: float, msg: str, _i: int = i, _total: int = total) -> None:
                    self.progress.emit((_i + frac) / _total)
                    self.status.emit(f"[{_i + 1}/{_total}] {msg}")

                result = pipeline.run(config, progress_callback=job_progress)
                results.append(result)

        except Exception as e:
            self.error.emit(str(e))

        # Always emit finished so the UI can clean up, even after an error
        self.finished.emit({
            "results": [
                {
                    "input": r.input_path,
                    "subtitle_path": r.subtitle_path,
                    "video_path": r.video_path,
                    "success": r.success,
                    "error": r.error,
                }
                for r in results
            ],
            "completed": sum(1 for r in results if r.success),
            "failed": sum(1 for r in results if not r.success),
        })
