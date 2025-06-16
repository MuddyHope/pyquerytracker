#!/usr/bin/env python3
"""
Example demonstrating CSV export functionality in pyquerytracker.

This example shows how to:
1. Track multiple function executions
2. Export data to CSV format
3. Export data to JSON format
4. Get summary statistics
5. Clear tracked data
"""

import time
import random
from pathlib import Path
from pyquerytracker import TrackQuery, export_data, get_summary, clear_data, ExportType


@TrackQuery()
def fetch_users():
    """Simulate a database query to fetch users."""
    # Simulate varying query times
    time.sleep(random.uniform(0.05, 0.2))
    return "SELECT * FROM users;"


@TrackQuery()
def fetch_orders(user_id: int):
    """Simulate fetching orders for a specific user."""
    # Sometimes this query is slow
    sleep_time = 0.3 if random.random() < 0.3 else random.uniform(0.02, 0.1)
    time.sleep(sleep_time)
    return f"SELECT * FROM orders WHERE user_id = {user_id};"


@TrackQuery()
def create_report():
    """Simulate report generation that sometimes fails."""
    time.sleep(random.uniform(0.1, 0.4))
    
    # Simulate occasional failures
    if random.random() < 0.2:  # 20% chance of failure
        raise ValueError("Report generation failed: insufficient data")
    
    return "Report generated successfully"


class DatabaseService:
    """Example service class with tracked methods."""
    
    @TrackQuery()
    def connect(self):
        """Simulate database connection."""
        time.sleep(random.uniform(0.01, 0.05))
        return "Connected to database"
    
    @TrackQuery()
    def execute_query(self, query: str):
        """Execute a database query."""
        time.sleep(random.uniform(0.02, 0.15))
        return f"Executed: {query}"


def main():
    """Demonstrate CSV export functionality."""
    print("🐍 PyQueryTracker CSV Export Demo")
    print("=" * 40)
    
    # Clear any existing data
    clear_data()
    
    # Run some tracked functions
    print("Running tracked functions...")
    
    # Simple function calls
    for i in range(5):
        fetch_users()
    
    # Function with parameters
    for user_id in [1, 2, 3, 4, 5]:
        fetch_orders(user_id)
    
    # Function that may fail
    for i in range(8):
        try:
            create_report()
        except ValueError as e:
            print(f"  Report {i+1} failed: {e}")
    
    # Class method calls
    db_service = DatabaseService()
    for i in range(3):
        db_service.connect()
        db_service.execute_query(f"SELECT * FROM table_{i};")
    
    print(f"✅ Completed tracking {get_summary()['total_queries']} function calls")
    
    # Show summary statistics
    print("\n📊 Summary Statistics:")
    stats = get_summary()
    for key, value in stats.items():
        if isinstance(value, float):
            print(f"  {key}: {value:.2f}")
        else:
            print(f"  {key}: {value}")
    
    # Create exports directory
    exports_dir = Path("exports")
    exports_dir.mkdir(exist_ok=True)
    
    # Export to CSV
    csv_file = exports_dir / "query_tracking_export.csv"
    print(f"\n📄 Exporting to CSV: {csv_file}")
    export_data(ExportType.CSV, csv_file, include_summary=True)
    
    # Export to JSON
    json_file = exports_dir / "query_tracking_export.json"
    print(f"📄 Exporting to JSON: {json_file}")
    export_data(ExportType.JSON, json_file, include_summary=True)
    
    print("\n✨ Export completed!")
    print(f"📁 Check the '{exports_dir}' directory for exported files.")
    
    # Demonstrate clearing data
    print(f"\n🗑️  Current records: {len(get_summary())} -> Clearing...")
    clear_data()
    print(f"   After clearing: {get_summary()['total_queries']} records")


if __name__ == "__main__":
    main()