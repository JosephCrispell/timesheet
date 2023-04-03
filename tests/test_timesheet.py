# Load packages
import unittest  # running tests
from pathlib import Path  # handling file paths
import pandas as pd  # creating dummy data

# Local imports
from timesheet import timesheet  # timesheet class
from timesheet import data_functions  # functions for working with data


class TestTimesheet(unittest.TestCase):
    def test_timesheet_creation(self):
        """Test the creation of a timesheet file"""

        # Get timesheet
        timesheet_file = Path("outputs/test_timesheet.csv")
        my_timesheet = timesheet.Timesheet(file_name=timesheet_file)

        # Check timesheet file exists
        self.assertTrue(
            Path.exists(my_timesheet.file_name),
            f"Timesheet file ({my_timesheet.file_name}) exist",
        )

        # Remove timesheet
        Path.unlink(my_timesheet.file_name)

    def test_timesheet_loading(self):
        """Creates dummy timesheet data and checks read in correctly"""

        # Create a dummy timesheet
        timesheet_file = Path("outputs/test_timesheet.csv")
        data_functions.create_dummy_timesheet(file_name=timesheet_file)

        # Load dummy timesheet
        my_timesheet = timesheet.Timesheet(file_name=timesheet_file)

        # Check column types
        self.assertEqual(
            my_timesheet.timesheet.date.dtype,
            "datetime64[ns]",
            "Check date column contains datetimes",
        )
        self.assertEqual(
            my_timesheet.timesheet.start_time.dtype,
            "datetime64[ns]",
            "Check start_time column contains datetimes",
        )
        self.assertEqual(
            my_timesheet.timesheet.end_time.dtype,
            "datetime64[ns]",
            "Check end_time column contains datetimes",
        )
        self.assertEqual(
            my_timesheet.timesheet.time_worked.dtype,
            "timedelta64[ns]",
            "Check time_worked column contains timedeltas",
        )
        self.assertIsInstance(
            my_timesheet.timesheet.notes[0], str, "Check note column contains strings"
        )

        # Check some column values
        self.assertEqual(
            my_timesheet.timesheet.date[0],
            pd.Timestamp("2023-03-13 00:00:00"),
            "Check first value in date column",
        )
        self.assertEqual(
            my_timesheet.timesheet.start_time[2],
            pd.Timestamp("1900-01-01 08:35:00"),
            "Check third value in start time column",
        )
        self.assertEqual(
            my_timesheet.timesheet.notes[6],
            "a simple note",
            "Check seventh value in notes column",
        )

        # Remove timesheet
        Path.unlink(timesheet_file)

    # TODO add test for add start time

    # TODO add tests for empty timesheet


if __name__ == "__main__":
    unittest.main()
