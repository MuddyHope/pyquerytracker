import unittest
import tempfile
import csv
import json
from pathlib import Path
from unittest.mock import patch
from pyquerytracker.export import (
    QueryRecord, QueryTracker, CSVExporter, 
    export_data, get_summary, clear_data, get_tracker
)
from pyquerytracker.config import ExportType
from pyquerytracker import TrackQuery


class TestQueryRecord(unittest.TestCase):
    """Test QueryRecord dataclass."""
    
    def test_query_record_creation(self):
        """Test creating a QueryRecord."""
        record = QueryRecord(
            timestamp="2023-01-01T12:00:00",
            function_name="test_func",
            class_name="TestClass",
            duration_ms=150.5,
            status="success"
        )
        
        self.assertEqual(record.function_name, "test_func")
        self.assertEqual(record.class_name, "TestClass")
        self.assertEqual(record.duration_ms, 150.5)
        self.assertEqual(record.status, "success")


class TestQueryTracker(unittest.TestCase):
    """Test QueryTracker functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.tracker = QueryTracker()
    
    def test_add_and_get_records(self):
        """Test adding and retrieving records."""
        self.tracker.add_record("func1", None, 100.0, "success")
        self.tracker.add_record("func2", "Class1", 200.0, "error", "Test error")
        
        records = self.tracker.get_records()
        self.assertEqual(len(records), 2)
        self.assertEqual(records[0].function_name, "func1")
        self.assertEqual(records[1].function_name, "func2")
        self.assertEqual(records[1].error_message, "Test error")
    
    def test_clear_records(self):
        """Test clearing records."""
        self.tracker.add_record("func1", None, 100.0, "success")
        self.assertEqual(len(self.tracker.get_records()), 1)
        
        self.tracker.clear_records()
        self.assertEqual(len(self.tracker.get_records()), 0)
    
    def test_summary_stats_empty(self):
        """Test summary statistics with no records."""
        stats = self.tracker.get_summary_stats()
        expected = {
            "total_queries": 0,
            "successful_queries": 0,
            "failed_queries": 0,
            "average_duration_ms": 0.0,
            "min_duration_ms": 0.0,
            "max_duration_ms": 0.0,
        }
        self.assertEqual(stats, expected)
    
    def test_summary_stats_with_records(self):
        """Test summary statistics with records."""
        self.tracker.add_record("func1", None, 100.0, "success")
        self.tracker.add_record("func2", None, 200.0, "success")
        self.tracker.add_record("func3", None, 150.0, "error", "Test error")
        
        stats = self.tracker.get_summary_stats()
        
        self.assertEqual(stats["total_queries"], 3)
        self.assertEqual(stats["successful_queries"], 2)
        self.assertEqual(stats["failed_queries"], 1)
        self.assertEqual(stats["average_duration_ms"], 150.0)
        self.assertEqual(stats["min_duration_ms"], 100.0)
        self.assertEqual(stats["max_duration_ms"], 200.0)


class TestCSVExporter(unittest.TestCase):
    """Test CSV export functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.temp_path = Path(self.temp_dir)
        
        # Create test records
        self.records = [
            QueryRecord("2023-01-01T12:00:00", "func1", None, 100.0, "success"),
            QueryRecord("2023-01-01T12:01:00", "func2", "TestClass", 200.0, "error", "Test error"),
        ]
    
    def test_export_to_csv(self):
        """Test exporting records to CSV."""
        csv_file = self.temp_path / "test.csv"
        CSVExporter.export_to_csv(self.records, csv_file, include_summary=False)
        
        self.assertTrue(csv_file.exists())
        
        # Read and verify CSV content
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0]['function_name'], 'func1')
        self.assertEqual(rows[1]['function_name'], 'func2')
        self.assertEqual(rows[1]['error_message'], 'Test error')
    
    def test_export_to_csv_with_summary(self):
        """Test exporting records to CSV with summary."""
        csv_file = self.temp_path / "test_summary.csv"
        CSVExporter.export_to_csv(self.records, csv_file, include_summary=True)
        
        self.assertTrue(csv_file.exists())
        
        # Read CSV content
        with open(csv_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check that summary section exists
        self.assertIn("SUMMARY STATISTICS", content)
        self.assertIn("total_queries", content)
    
    def test_export_to_json(self):
        """Test exporting records to JSON."""
        json_file = self.temp_path / "test.json"
        CSVExporter.export_to_json(self.records, json_file, include_summary=True)
        
        self.assertTrue(json_file.exists())
        
        # Read and verify JSON content
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        self.assertEqual(len(data['records']), 2)
        self.assertEqual(data['total_records'], 2)
        self.assertIn('summary', data)
        self.assertEqual(data['records'][0]['function_name'], 'func1')


class TestExportIntegration(unittest.TestCase):
    """Test integration with TrackQuery decorator."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.temp_path = Path(self.temp_dir)
        clear_data()  # Clear any existing data
    
    def test_trackquery_integration(self):
        """Test that TrackQuery decorator populates export data."""
        @TrackQuery()
        def test_function():
            return "test result"
        
        # Execute tracked function
        result = test_function()
        self.assertEqual(result, "test result")
        
        # Check that data was recorded
        summary = get_summary()
        self.assertEqual(summary['total_queries'], 1)
        self.assertEqual(summary['successful_queries'], 1)
        self.assertEqual(summary['failed_queries'], 0)
    
    def test_trackquery_with_error(self):
        """Test TrackQuery decorator with function that raises error."""
        @TrackQuery()
        def failing_function():
            raise ValueError("Test error")
        
        # Execute tracked function that fails
        with self.assertRaises(ValueError):
            failing_function()
        
        # Check that error was recorded
        summary = get_summary()
        self.assertEqual(summary['total_queries'], 1)
        self.assertEqual(summary['successful_queries'], 0)
        self.assertEqual(summary['failed_queries'], 1)
    
    def test_full_export_workflow(self):
        """Test complete workflow from tracking to export."""
        @TrackQuery()
        def sample_query():
            return "SELECT * FROM test;"
        
        # Execute some functions
        for _ in range(3):
            sample_query()
        
        # Export to CSV
        csv_file = self.temp_path / "workflow_test.csv"
        export_data(ExportType.CSV, csv_file)
        
        self.assertTrue(csv_file.exists())
        
        # Verify CSV contains correct data
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        
        # Should have 3 records (excluding summary and empty rows)
        # Data rows have actual timestamps (ISO format starting with year)
        data_rows = [row for row in rows if (
            row['timestamp'] and
            row['timestamp'] != 'SUMMARY STATISTICS' and
            not row['timestamp'].startswith('total_queries') and
            not row['timestamp'].startswith('successful_queries') and
            not row['timestamp'].startswith('failed_queries') and
            not row['timestamp'].startswith('average_duration_ms') and
            not row['timestamp'].startswith('min_duration_ms') and
            not row['timestamp'].startswith('max_duration_ms') and
            row['function_name']  # Must have a function name
        )]
        self.assertEqual(len(data_rows), 3)
        
        for row in data_rows:
            self.assertEqual(row['function_name'], 'sample_query')
            self.assertEqual(row['status'], 'success')


if __name__ == '__main__':
    unittest.main()