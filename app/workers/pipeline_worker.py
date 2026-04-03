"""Worker for running a single pipeline job in a thread."""

from __future__ import annotations

from app.core.pipeline import JobConfig, Pipeline
from app.workers.base_worker import BaseWorker


class PipelineWorker(BaseWorker):
    def __init__(self, api_key: str, config: JobConfig) -> None:
        super().__init__()
        self._api_key = api_key
        self._config = config

    def run(self) -> None:
        """Execute the pipeline job."""
        try:
            pipeline = Pipeline(self._api_key)

            def progress_callback(frac: float, msg: str) -> None:
                self.progress.emit(frac)
                self.status.emit(msg)

            result = pipeline.run(self._config, progress_callback=progress_callback)

            if result.success:
                self.finished.emit(
                    {
                        "subtitle_path": result.subtitle_path,
                        "video_path": result.video_path,
                    }
                )
            else:
                self.error.emit(result.error)

        except Exception as e:
            self.error.emit(str(e))
