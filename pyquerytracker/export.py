import csv
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
from dataclasses import dataclass, asdict
from .config import ExportType

logger = logging.getLogger("pyquerytracker.export")


@dataclass
class QueryRecord:
    """
    Represents a single query execution record for export.
    """

    timestamp: str
    function_name: str
    class_name: Optional[str]
    duration_ms: float
    status: str  # 'success' or 'error'
    error_message: Optional[str] = None
    args_count: int = 0
    kwargs_count: int = 0


class QueryTracker:
    """
    Collects and manages query execution records for export.
    """

    def __init__(self):
        self._records: List[QueryRecord] = []

    def add_record(
        self,
        function_name: str,
        class_name: Optional[str],
        duration_ms: float,
        status: str,
        error_message: Optional[str] = None,
        args_count: int = 0,
        kwargs_count: int = 0,
    ):
        """Add a new query execution record."""
        record = QueryRecord(
            timestamp=datetime.now().isoformat(),
            function_name=function_name,
            class_name=class_name,
            duration_ms=duration_ms,
            status=status,
            error_message=error_message,
            args_count=args_count,
            kwargs_count=kwargs_count,
        )
        self._records.append(record)

    def get_records(self) -> List[QueryRecord]:
        """Get all collected records."""
        return self._records.copy()

    def clear_records(self):
        """Clear all collected records."""
        self._records.clear()

    def get_summary_stats(self) -> Dict[str, Any]:
        """Get summary statistics of tracked queries."""
        if not self._records:
            return {
                "total_queries": 0,
                "successful_queries": 0,
                "failed_queries": 0,
                "average_duration_ms": 0.0,
                "min_duration_ms": 0.0,
                "max_duration_ms": 0.0,
            }

        successful_records = [r for r in self._records if r.status == "success"]
        failed_records = [r for r in self._records if r.status == "error"]
        durations = [r.duration_ms for r in self._records]

        return {
            "total_queries": len(self._records),
            "successful_queries": len(successful_records),
            "failed_queries": len(failed_records),
            "average_duration_ms": sum(durations) / len(durations),
            "min_duration_ms": min(durations),
            "max_duration_ms": max(durations),
        }


class CSVExporter:
    """
    Exports query tracking data to CSV format.
    """

    @staticmethod
    def export_to_csv(
        records: List[QueryRecord],
        filepath: Union[str, Path],
        include_summary: bool = True,
    ) -> None:
        """
        Export query records to CSV file.

        Args:
            records: List of QueryRecord objects to export
            filepath: Path where to save the CSV file
            include_summary: Whether to include summary statistics in a separate CSV section
        """
        filepath = Path(filepath)
        filepath.parent.mkdir(parents=True, exist_ok=True)

        if not records:
            logger.warning("No records to export")
            return

        # Write main records
        with open(filepath, "w", newline="", encoding="utf-8") as csvfile:
            fieldnames = [
                "timestamp",
                "function_name",
                "class_name",
                "duration_ms",
                "status",
                "error_message",
                "args_count",
                "kwargs_count",
            ]

            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for record in records:
                writer.writerow(asdict(record))

            # Add summary section if requested
            if include_summary:
                tracker = QueryTracker()
                for record in records:
                    tracker.add_record(
                        record.function_name,
                        record.class_name,
                        record.duration_ms,
                        record.status,
                        record.error_message,
                        record.args_count,
                        record.kwargs_count,
                    )

                stats = tracker.get_summary_stats()

                # Add empty rows for separation
                writer.writerow({})
                writer.writerow({})

                # Write summary header
                writer.writerow({"timestamp": "SUMMARY STATISTICS"})

                # Write summary data
                for key, value in stats.items():
                    writer.writerow({"timestamp": key, "function_name": str(value)})

        logger.info(f"Exported {len(records)} records to {filepath}")

    @staticmethod
    def export_to_json(
        records: List[QueryRecord],
        filepath: Union[str, Path],
        include_summary: bool = True,
    ) -> None:
        """
        Export query records to JSON file.

        Args:
            records: List of QueryRecord objects to export
            filepath: Path where to save the JSON file
            include_summary: Whether to include summary statistics
        """
        filepath = Path(filepath)
        filepath.parent.mkdir(parents=True, exist_ok=True)

        if not records:
            logger.warning("No records to export")
            return

        data = {
            "records": [asdict(record) for record in records],
            "export_timestamp": datetime.now().isoformat(),
            "total_records": len(records),
        }

        if include_summary:
            tracker = QueryTracker()
            for record in records:
                tracker.add_record(
                    record.function_name,
                    record.class_name,
                    record.duration_ms,
                    record.status,
                    record.error_message,
                    record.args_count,
                    record.kwargs_count,
                )
            data["summary"] = tracker.get_summary_stats()

        with open(filepath, "w", encoding="utf-8") as jsonfile:
            json.dump(data, jsonfile, indent=2, ensure_ascii=False)

        logger.info(f"Exported {len(records)} records to {filepath}")


# Global tracker instance
_global_tracker = QueryTracker()


def get_tracker() -> QueryTracker:
    """Get the global query tracker instance."""
    return _global_tracker


def export_data(
    export_type: ExportType,
    filepath: Union[str, Path],
    include_summary: bool = True,
    clear_after_export: bool = False,
) -> None:
    """
    Export collected query data to file.

    Args:
        export_type: Format to export (CSV or JSON)
        filepath: Path where to save the file
        include_summary: Whether to include summary statistics
        clear_after_export: Whether to clear records after export
    """
    records = _global_tracker.get_records()

    if export_type == ExportType.CSV:
        CSVExporter.export_to_csv(records, filepath, include_summary)
    elif export_type == ExportType.JSON:
        CSVExporter.export_to_json(records, filepath, include_summary)
    else:
        raise ValueError(f"Unsupported export type: {export_type}")

    if clear_after_export:
        _global_tracker.clear_records()


def get_summary() -> Dict[str, Any]:
    """Get summary statistics of tracked queries."""
    return _global_tracker.get_summary_stats()


def clear_data() -> None:
    """Clear all collected query data."""
    _global_tracker.clear_records()
