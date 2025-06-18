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
        if not self._enabled or not self._buffer:
            return

        self._path.parent.mkdir(parents=True, exist_ok=True)

        # load existing array (or start fresh)
        try:
            with self._path.open("r", encoding="utf-8") as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            data = []

        # extend and rewrite
        data.extend(self._buffer)
        with _lock, self._path.open("w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        self._buffer.clear()
