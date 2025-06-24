import atexit
import json
import os
from threading import Lock

from pyquerytracker.exporter.base import Exporter
from pyquerytracker.utils.logger import QueryLogger

logger = QueryLogger.get_logger()


class JsonExporter(Exporter):
    def __init__(self, config):
        super().__init__(config)
        self.config = config
        self._lock = Lock()
        self._buffer = []
        atexit.register(self.flush)

    def append(self, data: dict):
        with self._lock:
            self._buffer.append(data)

    def flush(self):
        with self._lock:
            if not self._buffer:
                return

            os.makedirs(os.path.dirname(self.config.export_path), exist_ok=True)

            existing_data = []
            if os.path.exists(self.config.export_path):
                try:
                    with open(self.config.export_path, "r", encoding="utf-8") as f:
                        existing_data = json.load(f)
                        if not isinstance(existing_data, list):
                            existing_data = []
                except json.JSONDecodeError:
                    pass

            existing_data.extend(self._buffer)

            with open(self.config.export_path, "w", encoding="utf-8") as f:
                json.dump(existing_data, f, indent=2)

            logger.info(f"Flushed {len(self._buffer)} logs to JSON")
            self._buffer.clear()
