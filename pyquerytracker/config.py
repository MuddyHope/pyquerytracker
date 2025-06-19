from enum import Enum
from dataclasses import dataclass
from typing import Optional
import logging


class ExportType(str, Enum):
    """
    Enum representing supported export formats for query tracking logs.
    """

    JSON = "json"
    CSV = "csv"


@dataclass
class Config:
    """
    Configuration settings for the query tracking system.

    Attributes:
        slow_log_threshold_ms (float):
            Threshold in milliseconds above which a query is considered slow.
        slow_log_level (int):
            Logging level for slow query logs.
        export_type (ExportType):
            Format to export logs in.
        export_path (Optional[str]):
            File path to append exported logs to (if set).
    """

    slow_log_threshold_ms: float = 100.0
    slow_log_level: int = logging.WARNING
    export_type: Optional[ExportType] = None
    export_path: Optional[str] = None


_config: Config = Config()


def configure(
    *,
    slow_log_threshold_ms: Optional[float] = None,
    slow_log_level: Optional[int] = None,
    export_type: Optional[ExportType] = None,
    export_path: Optional[str] = None,
):
    """
    Configure global settings for query tracking.

    Keyword Args:
        slow_log_threshold_ms (Optional[float]):
            If set, override the default "slow" threshold.
        slow_log_level (Optional[int]):
            If set, override the default log level for "slow" events.
        export_type (Optional[ExportType]):
            If set, choose how logs are exported (e.g. JSON vs CSV).
        export_path (Optional[str]):
            If set, file path to append exported logs to.
    """
    if slow_log_threshold_ms is not None:
        _config.slow_log_threshold_ms = slow_log_threshold_ms

    if slow_log_level is not None:
        _config.slow_log_level = slow_log_level
    if export_type is not None:
        _config.export_type = export_type
    if export_path is not None:
        _config.export_path = export_path

    if export_type is not None:
        _config.export_type = export_type

    if export_path is not None:
        _config.export_path = export_path


def get_config() -> Config:
    """
    Retrieve the current query tracking configuration.
    """
    return _config
