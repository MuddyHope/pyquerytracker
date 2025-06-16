import json
from pathlib import Path
from threading import Lock
from typing import Optional, Dict
from pyquerytracker.config import Config, ExportType

_lock = Lock()


class JsonExporter:
    """
    Handles appending JSON‐lines to a file in a threadsafe way.
    """

    def __init__(self, config: Config):
        self._path: Optional[Path] = (
            Path(config.export_path) if config.export_path else None
        )
        self._enabled = bool(self._path) and config.export_type == ExportType.JSON

    def append(self, record: Dict) -> None:
        if not self._enabled:
            return
        # ensure directory exists
        self._path.parent.mkdir(parents=True, exist_ok=True)
        # threadsafe append
        with _lock, self._path.open("a", encoding="utf-8") as f:
            json.dump(record, f)
            f.write("\n")
