# Load packages
import unittest  # running tests
from pathlib import Path  # handling file paths
import pandas as pd  # creating dummy data
from datetime import time, datetime  # working with dates and times

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

    def add_start_time_and_test(self, timesheet_file: Path):
        """Function to add start time to timesheet file and test

        Args:
            timesheet_file (Path): path to timesheet file
        """

        # Load dummy timesheet
        my_timesheet = timesheet.Timesheet(file_name=timesheet_file)

        # Create a start time
        start_time_string = "08:34"
        current_datetime = datetime.now()
        current_date = current_datetime.date()
        hours, minutes = map(int, start_time_string.split(":"))
        start_time_datetime = datetime.combine(
            current_date, time(hour=hours, minute=minutes)
        )
        my_timesheet.add_start_time(start_time_string)

        # Check start time added
        self.assertEqual(
            my_timesheet.start_time,
            start_time_datetime,
            "Check start time added matches start time provided",
        )

        # Check start time written to file
        my_timesheet_data = pd.read_csv(timesheet_file)
        self.assertEqual(
            start_time_string,
            my_timesheet_data.iloc[-1:].start_time.item(),
            "Check start time written to file",
        )

        # Check timesheet loading
        my_timesheet = timesheet.Timesheet(file_name=timesheet_file)

        # Remove timesheet
        Path.unlink(timesheet_file)

    def test_add_start_time_with_dummy_timesheet(self):
        """Creates dummy timesheet data and then tests adding a start time"""

        # Create a dummy timesheet
        timesheet_file = Path("outputs/test_timesheet.csv")
        data_functions.create_dummy_timesheet(file_name=timesheet_file)

        # Add start time and test
        self.add_start_time_and_test(timesheet_file=timesheet_file)

    def test_add_start_time_with_empty_timesheet(self):
        """Tests adding a start time to empty tiemsheet"""

        # Add start time and test to empty timesheet
        self.add_start_time_and_test(timesheet_file=Path("outputs/test_timesheet.csv"))

    def test_reset_timesheet(self):
        """Test timesheet is reset correctly"""

        # Create a dummy timesheet
        timesheet_file = Path("outputs/test_timesheet.csv")
        data_functions.create_dummy_timesheet(file_name=timesheet_file)

        # Load dummy timesheet
        my_timesheet = timesheet.Timesheet(file_name=timesheet_file)

        # Reset timesheet
        my_timesheet.reset_timesheet()

        # Check timesheet empty
        self.assertEqual(
            0,
            my_timesheet.timesheet.shape[0],
            "Resetted timesheet is empty",
        )

        # Check no start and end times
        self.assertEqual(
            None,
            my_timesheet.start_time,
            "No start time after reset",
        )
        self.assertEqual(
            None,
            my_timesheet.end_time,
            "No end time after reset",
        )

        # Remove timesheet
        Path.unlink(timesheet_file)

    def test_add_end_time_with_dummy_timesheet(self):
        """Test adding end time time to timesheet"""

        # Create a dummy timesheet
        timesheet_file = Path("outputs/test_timesheet.csv")
        data_functions.create_dummy_timesheet(file_name=timesheet_file)

        # Load dummy timesheet
        my_timesheet = timesheet.Timesheet(file_name=timesheet_file)

        # Add a start time
        start_time_string = "08:34"
        current_datetime = datetime.now()
        current_date = current_datetime.date()
        hours, minutes = map(int, start_time_string.split(":"))
        my_timesheet.add_start_time(start_time_string)

        # Add end time
        end_time_string = "11:34"
        current_datetime = datetime.now()
        current_date = current_datetime.date()
        hours, minutes = map(int, end_time_string.split(":"))
        end_time_datetime = datetime.combine(
            current_date, time(hour=hours, minute=minutes)
        )
        my_timesheet.add_end_time(end_time_string)

        # Check start time is now None
        self.assertEqual(
            None,
            my_timesheet.start_time,
            "No start time after adding end time",
        )

        # Check end time added
        self.assertEqual(
            my_timesheet.end_time,
            end_time_datetime,
            "Check end time added matches end time provided",
        )

        # Check end time written to file
        my_timesheet_data = pd.read_csv(timesheet_file)
        self.assertEqual(
            end_time_string,
            my_timesheet_data.iloc[-1:].end_time.item(),
            "Check end time written to file",
        )

        # Check timesheet loading
        my_timesheet = timesheet.Timesheet(file_name=timesheet_file)

        # Remove timesheet
        Path.unlink(timesheet_file)

    def test_add_end_time_with_empty_timesheet(self):

        # Create empty timesheet
        timesheet_file = Path("outputs/test_timesheet.csv")
        my_timesheet = timesheet.Timesheet(file_name=timesheet_file)

        # Check raises exception when try to add end time without start time
        with self.assertRaises(Exception):
            my_timesheet.add_end_time()

        # Remove timesheet
        Path.unlink(timesheet_file)


if __name__ == "__main__":
    unittest.main()
