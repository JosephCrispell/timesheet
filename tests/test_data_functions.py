# Load packages
import unittest  # running tests
from pathlib import Path  # handling file paths
from datetime import datetime  # working with dates and times

# Local imports
from timesheet import data_functions  # functions for working with data


class TestDataFunctions(unittest.TestCase):
    def test_create_dummy_timesheet(self):
        """Test that dummy data file created

        Note more thoroughly tested (column types and values) in test_timesheet.py:test_timesheet_loading
        """
        # Create the dummy data
        timesheet_file = Path("outputs/test_timesheet.csv")
        data_functions.create_dummy_timesheet(file_name=timesheet_file)

        # Check timesheet file exists
        self.assertTrue(
            Path.exists(timesheet_file),
            f"Dummy data file ({timesheet_file}) exists",
        )

        # Remove timesheet
        Path.unlink(timesheet_file)

    def test_calculate_time_differences(self):
        """Test function that calculates differences between two datetime lists"""

        # Create start and end datetimes
        start_times = [
            datetime(year=2023, month=6, day=1, hour=12, minute=0, second=0),
            datetime(year=2023, month=3, day=16, hour=2, minute=0, second=0),
        ]
        end_times = [
            datetime(year=2023, month=6, day=1, hour=12, minute=0, second=10),
            datetime(year=2023, month=3, day=16, hour=2, minute=0, second=55),
        ]

        # Calculate time differences
        time_differences = data_functions.calculate_time_differences(
            start_times, end_times
        )

        # Check time differences
        self.assertEqual(
            time_differences[0].total_seconds(),
            10,
            "Check time difference calculation",
        )
        self.assertEqual(
            time_differences[1].total_seconds(),
            55,
            "Check time difference calculation",
        )

        # Check number of time differences provided
        self.assertEqual(
            len(time_differences),
            len(start_times),
            "Check time difference calculation",
        )

    def test_check_string_pattern_match(self):

        # Check raises exception when string format wrong
        with self.assertRaises(Exception):
            data_functions.check_string_pattern_match(
                string="08:00", patten=r"[0-9]-[0-9]"
            ),


if __name__ == "__main__":
    unittest.main()
