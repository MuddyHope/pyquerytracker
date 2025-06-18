import json
from pathlib import Path
from threading import Lock
from typing import Dict
from pyquerytracker.config import Config, ExportType

_lock = Lock()


class JsonExporter:
    """
    Handles appending JSON objects to a file in a thread-safe way.
    """

    def __init__(self, config: Config):
        self._enabled = bool(config.export_path) and (
            config.export_type == ExportType.JSON
        )
        self._path = Path(config.export_path) if config.export_path else None
        self._buffer = []

    def append(self, record: Dict) -> None:
        if self._enabled:
            self._buffer.append(record)

    def flush(self) -> None:
        if self._enabled and self._buffer:
            self._path.parent.mkdir(parents=True, exist_ok=True)
            with _lock, self._path.open("a", encoding="utf-8") as f:
                json.dump(self._buffer, f, indent=2)
