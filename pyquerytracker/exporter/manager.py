from pyquerytracker.config import Config, ExportType
from pyquerytracker.exporter.base import Exporter
from pyquerytracker.exporter.csv_exporter import CsvExporter
from pyquerytracker.exporter.json_exporter import JsonExporter


class ExporterManager:
    _exporter: Exporter = None

    _exporter_classes = {
        ExportType.CSV: CsvExporter,
        ExportType.JSON: JsonExporter,
    }

    @classmethod
    def create_exporter(cls, config: Config) -> Exporter:
        exporter_cls = cls._exporter_classes.get(config.export_type)
        if not exporter_cls:
            raise ValueError(f"Unsupported export type: {config.export_type}")
        exporter = exporter_cls(config)
        cls.set(exporter)
        return exporter

    @staticmethod
    def set(exporter: Exporter):
        ExporterManager._exporter = exporter

    @staticmethod
    def get() -> Exporter:
        if ExporterManager._exporter is None:
            raise RuntimeError("Exporter not set")
        return ExporterManager._exporter
