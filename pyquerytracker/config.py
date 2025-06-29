import logging
from dataclasses import dataclass
from enum import Enum
from typing import Optional


class ExportType(str, Enum):
    """
    Enum representing supported export formats for query tracking logs.

    Attributes:
        JSON: Export logs in JSON format.
        CSV: Export logs in CSV format.
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
            Defaults to 100.0 ms.

        slow_log_level (int):
            Logging level for slow query logs (e.g., logging.WARNING, logging.INFO).
            Defaults to logging.WARNING.
    """

    # TODO: Adding export functionality
    slow_log_threshold_ms: float = 100.0
    slow_log_level: int = logging.WARNING
    export_type: Optional[ExportType] = None
    export_path: Optional[str] = None
    dashboard_enabled: bool = True  # ← set to False in real deployments
    persist_to_db: bool = True


_config: Config = Config()


def configure(
    slow_log_threshold_ms: Optional[float] = None,
    slow_log_level: Optional[int] = None,
    export_type: Optional[ExportType] = None,
    export_path: Optional[str] = None,
):
    """
    Configure global settings for query tracking.

    Args:
        slow_log_threshold_ms (Optional[float]):
            Threshold in milliseconds to log a query as "slow".
            If not provided, defaults to 100.0 ms.

        slow_log_level (Optional[int]):
            Logging level for slow queries (e.g., logging.INFO, logging.WARNING).
            If not provided, defaults to logging.WARNING.
    """
    if slow_log_threshold_ms is not None:
        _config.slow_log_threshold_ms = slow_log_threshold_ms
    if slow_log_level is not None:
        _config.slow_log_level = slow_log_level
    if export_type is not None:
        _config.export_type = export_type
    if export_path is not None:
        _config.export_path = export_path


def get_config() -> Config:
    """
    Retrieve the current query tracking configuration.

    Returns:
        TrackerConfig: The current configuration settings.
    """
    return _config
