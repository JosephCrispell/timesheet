import unittest  # running tests
from pathlib import Path  # handling file paths
import pandas as pd  # creating dummy data
from datetime import date, time, datetime  # working with dates and times

from timesheet import timesheet


def calculate_time_differences(
    start_times: list[datetime.time], end_times: list[datetime.time]
) -> list[datetime.time]:
    """Calculate difference between times

    Based on this staackoverflow answer: https://stackoverflow.com/questions/25346019/subtract-datetime-time-objects-stored-in-two-separate-lists

    Args:
        start_times (list[datetime.time]): list of start times
        end_times (list[datetime.time]): list of end times

    Returns:
        list[datetime.time]: list of time differences
    """

    # Calculate time differences
    differences = [
        datetime.combine(date.today(), end_time)
        - datetime.combine(date.today(), start_time)
        for start_time, end_time in zip(start_times, end_times)
    ]

    return differences


def create_dummy_timesheet(file_name: Path):

    """Creates timesheet with dummy data in it

    Args:
        file_name (Path): path to file where dummy data are written
    """

    # Create some dummy timesheet data
    start_times = [
        time(hour=8, minute=24),
        time(hour=12, minute=24),
        time(hour=8, minute=35),
        time(hour=12, minute=45),
        time(hour=8, minute=22),
        time(hour=12, minute=15),
        time(hour=8, minute=36),
        time(hour=12, minute=56),
    ]
    end_times = [
        time(hour=12, minute=0),
        time(hour=16, minute=24),
        time(hour=12, minute=5),
        time(hour=16, minute=55),
        time(hour=11, minute=51),
        time(hour=17, minute=5),
        time(hour=12, minute=6),
        time(hour=17, minute=3),
    ]
    dummy_timesheet_data = {
        "date": [
            date(year=2023, month=3, day=13),
            date(year=2023, month=3, day=13),
            date(year=2023, month=3, day=14),
            date(year=2023, month=3, day=14),
            date(year=2023, month=3, day=15),
            date(year=2023, month=3, day=15),
            date(year=2023, month=3, day=16),
            date(year=2023, month=3, day=16),
        ],
        "start_time": start_times,
        "end_time": end_times,
        "time_worked": map(str, calculate_time_differences(start_times, end_times)),
        "notes": [
            "nothing off note",
            "",
            "nothing off note",
            "nothing off note",
            "nothing off note",
            "nothing off note",
            "a simple note",
            "nothing off note",
        ],
    }
    dummy_timesheet_data = pd.DataFrame(dummy_timesheet_data)

    # Write data to file
    dummy_timesheet_data.to_csv(file_name, index=False)


class TestTimesheet(unittest.TestCase):
    def test_timesheet_creation(self):
        """Test the creation of a timesheet file"""

        # Get timesheet
        timesheet_file = Path("outputs/test_timesheet.csv")
        my_timesheet = timesheet.Timesheet(file_name=timesheet_file)

        # Check timesheet file exists
        self.assertTrue(
            Path.exists(my_timesheet.file_name),
            f"Timesheet file ({timesheet_file}) exist",
        )

        # Remove timesheet
        Path.unlink(timesheet_file)

    def test_timesheet_loading(self):
        """Creates dummy timesheet data and checks read in correctly"""

        # Create a dummy timesheet
        timesheet_file = Path("outputs/test_timesheet.csv")
        create_dummy_timesheet(file_name=timesheet_file)

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


if __name__ == "__main__":
    unittest.main()
