from pathlib import Path  # handling file paths
import pandas as pd  # working with data
from datetime import time, datetime  # working with dates and times


class Timesheet:
    def __init__(self, file_name: str = Path("outputs/timesheet.csv")):
        """Create Timesheet object

        Args:
            file_name (str, optional): path to timesheet file.
                Defaults to Path("outputs/timesheet.csv").
        """
        self.file_name = file_name
        self.read_timesheet()

    def create_timesheet(self):
        """Creates timesheet CSV file

        Timesheet saved to self.file_name (set in __init__)
        """
        # Initialise dataframe
        self.timesheet = pd.DataFrame(
            columns=["date", "start_time", "end_time", "time_worked", "notes"]
        )

        # Write to file
        self.timesheet.to_csv(self.file_name, index=False)
        print(f"Created timesheet file at: {self.file_name}")

    def read_timesheet(self):
        """Read in the timesheet

        Timesheet read from self.file_name (set in __init__)
        """

        # Check timesheet exists
        if Path.exists(self.file_name) == False:
            self.create_timesheet()

        # Read in timesheet
        self.timesheet = pd.read_csv(self.file_name)

        # Convert date and time columns to datetime objects
        self.timesheet["date"] = pd.to_datetime(self.timesheet["date"])
        self.timesheet["start_time"] = pd.to_datetime(
            self.timesheet["start_time"], format="%H:%M"
        )
        self.timesheet["end_time"] = pd.to_datetime(
            self.timesheet["end_time"], format="%H:%M"
        )
        self.timesheet["time_worked"] = pd.to_timedelta(
            self.timesheet["time_worked"] + ":00"
        )

    def add_start_time(self, start_time_string: str = None):
        """Add start time to timesheet

        Args:
            start_time_string (str, optional): time (format: hh:mm) to use for start time
                Defaults to None (will use current time).
        """

        # Get datetime object for now
        current_datetime = datetime.now()
        current_date = current_datetime.date()

        # Get current time
        start_time = current_datetime

        # Check if a start time provided
        if start_time_string != None:

            hours, minutes = map(int, start_time_string.split(":"))
            start_time = datetime.combine(
                current_date, time(hour=hours, minute=minutes)
            )

        # Add date and start time to timesheet
        new_timesheet_record = {
            "date": pd.Timestamp(current_date),
            "start_time": pd.Timestamp(start_time),
            "end_time": None,
            "time_worked": None,
            "notes": "",
        }
        new_timesheet_record = pd.DataFrame([new_timesheet_record])
        self.timesheet = pd.concat([self.timesheet, new_timesheet_record])

        # Reset dataframe index
        self.timesheet = self.timesheet.reset_index(drop=True)

        # Write updated timesheet to file
        self.write_timesheet()

    def write_timesheet(self):
        """Write timesheet to file

        Timesheet written to self.file_name (set in __init__), overwrites current content
        """

        # Create a copy of the dataframe
        my_timesheet = self.timesheet.copy()

        # Format the date and time columns as strings
        my_timesheet.date = my_timesheet.date.dt.strftime("%Y-%m-%d")
        my_timesheet.start_time = my_timesheet.start_time.dt.strftime("%H:%M")
        my_timesheet.end_time = my_timesheet.end_time.dt.strftime("%H:%M")
        my_timesheet.time_worked = my_timesheet.time_worked.astype(str).str[
            -8:-3
        ]  # strips out number days

        # Write to file
        my_timesheet.to_csv(self.file_name, index=False)
