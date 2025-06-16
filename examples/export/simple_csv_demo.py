#!/usr/bin/env python3
"""
Simple demonstration of CSV export functionality.
"""

import time
from pyquerytracker import TrackQuery, export_data, get_summary, ExportType


@TrackQuery()
def slow_query():
    """A slow database query simulation."""
    time.sleep(0.25)  # 250ms - will be logged as slow
    return "SELECT * FROM large_table;"


@TrackQuery()
def fast_query():
    """A fast database query simulation."""
    time.sleep(0.05)  # 50ms - normal execution
    return "SELECT id FROM users LIMIT 10;"


def main():
    print("Simple CSV Export Demo")
    print("-" * 25)
    
    # Execute some tracked functions
    for i in range(3):
        fast_query()
        slow_query()
    
    # Show summary
    stats = get_summary()
    print(f"Tracked {stats['total_queries']} queries")
    print(f"Average duration: {stats['average_duration_ms']:.2f}ms")
    
    # Export to CSV
    export_data(ExportType.CSV, "simple_export.csv")
    print("✅ Exported to simple_export.csv")


if __name__ == "__main__":
    main()