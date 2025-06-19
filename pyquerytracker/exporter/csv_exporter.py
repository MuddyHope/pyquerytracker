import atexit
import csv
import os
from threading import Lock

from pyquerytracker.utils.logger import QueryLogger
from pyquerytracker.exporter.base import Exporter

logger = QueryLogger.get_logger()


class CsvExporter(Exporter):
    def __init__(self, config):
        super().__init__(config)
        self._lock = Lock()
        self._buffer = []
        self._header_written = os.path.exists(self.config.export_path)
        # Ensure logs are flushed when program exits.
        atexit.register(self.flush)

    def append(self, data: dict):
        with self._lock:
            self._buffer.append(data)

    def flush(self):

        with self._lock:
            if not self._buffer:
                return

            os.makedirs(os.path.dirname(self.config.export_path), exist_ok=True)

            # Gather all possible fieldnames (union of keys)
            all_keys = set()
            for entry in self._buffer:
                all_keys.update(entry.keys())
            fieldnames = sorted(all_keys)  # consistent ordering

            with open(self.config.export_path, "a", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)

                if not self._header_written:
                    writer.writeheader()
                    self._header_written = True

                for row in self._buffer:
                    # Fill missing keys with None
                    full_row = {key: row.get(key) for key in fieldnames}
                    writer.writerow(full_row)

                logger.info("Flushed %d logs to CSV", len(self._buffer))
                self._buffer.clear()
