from pyquerytracker.config import Config, ExportType
from pyquerytracker.exporter.csv_exporter import CsvExporter
from pyquerytracker.exporter.base import Exporter


class ExporterManager:
    _exporter: Exporter = None

    @staticmethod
    def create_exporter(config: Config) -> Exporter:
        if config.export_type == ExportType.CSV:
            exporter = CsvExporter(config)
            ExporterManager.set(exporter)
            return exporter
        raise ValueError("Unsupported export type")

    @staticmethod
    def set(exporter: Exporter):
        ExporterManager._exporter = exporter

    @staticmethod
    def get() -> Exporter:
        if ExporterManager._exporter is None:
            raise RuntimeError("Exporter not set")
        return ExporterManager._exporter
