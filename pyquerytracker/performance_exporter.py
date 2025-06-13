import json
import csv
import os
import time

class PerformanceExporter:
    def __init__(self, export_path, export_format='json', frequency=None):
        """
        :param export_path: The path to export the file.
        :param export_format: 'json' or 'csv'.
        :param frequency: Optional frequency for writing data (in seconds).
        """
        self.export_path = export_path
        self.export_format = export_format.lower()
        self.frequency = frequency  # in seconds
        self.last_export_time = None

        if self.export_format not in ['json', 'csv']:
            raise ValueError("Unsupported export format. Choose 'json' or 'csv'.")

    def export(self, performance_stats):
        """
        Exports performance stats to the configured file if frequency allows it.
        """
        current_time = time.time()

        if self.frequency is not None:
            if self.last_export_time is not None:
                elapsed = current_time - self.last_export_time
                if elapsed < self.frequency:
                    print(f"Skipping export: only {elapsed:.2f}s elapsed, frequency is {self.frequency}s")
                    return

        os.makedirs(os.path.dirname(self.export_path), exist_ok=True)

        if self.export_format == 'json':
            self._export_json(performance_stats)
        elif self.export_format == 'csv':
            self._export_csv(performance_stats)

        self.last_export_time = current_time

    def _export_json(self, performance_stats):
        with open(self.export_path, 'w') as f:
            json.dump(performance_stats, f, indent=4)

    def _export_csv(self, performance_stats):
        with open(self.export_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Metric', 'Value'])
            for key, value in performance_stats.items():
                writer.writerow([key, value])
