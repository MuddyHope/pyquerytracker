from pyquerytracker.exporter import JsonExporter


class _ExporterManager:
    _instance: JsonExporter | None = None

    @classmethod
    def set(cls, exporter: JsonExporter) -> None:
        cls._instance = exporter

    @classmethod
    def flush(cls) -> None:
        if cls._instance is not None:
            cls._instance.flush()


def flush_exported_logs() -> None:
    """
    Manually flushes the JSON exporter buffer to disk, if initialized.
    Always returns None.
    """
    _ExporterManager.flush()
