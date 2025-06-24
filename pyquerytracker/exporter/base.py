from abc import ABC, abstractmethod

from pyquerytracker.config import Config


class Exporter(ABC):
    def __init__(self, config: Config):
        self.config = config

    @abstractmethod
    def append(self, data: dict) -> None:
        pass

    @abstractmethod
    def flush(self) -> None:
        pass


class NullExporter:

    def append(self, log_data):
        pass

    def flush(self):
        pass
