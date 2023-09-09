# Load packages
from pathlib import Path  # handling file paths
import pandas as pd  # working with data
from datetime import time, datetime  # working with dates and times
import warnings  # writing warnings

# Local imports
from timesheet import (
    data_functions as ts_data,
)  # general functions for working with data


class Timesheet:
    def __init__(self, file_name: str = Path("outputs/timesheet.csv")):
        """Create Timesheet object

        Args:
            file_name (str, optional): path to timesheet file.
                Defaults to Path("outputs/timesheet.csv").
        """
        self.file_name = file_name
        self.start_time = None
        self.end_time = None
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

        # Check if no end time
        if self.timesheet["end_time"].isnull().all():
            self.timesheet["end_time"] = pd.to_datetime(self.timesheet["end_time"])
        else:
            self.timesheet["end_time"] = pd.to_datetime(
                self.timesheet["end_time"], format="%H:%M"
            )

        # Convert timedelta column
        self.timesheet["time_worked"] = pd.to_timedelta(
            self.timesheet["time_worked"] + ":00"
        )

        # Check if any timesheet data present
        if self.timesheet.shape[0] > 0:

            # Set current start and end times
            last_row = self.timesheet.iloc[-1:]
            time = last_row["start_time"].item()
            self.start_time = None if pd.isnull(time) else time
            time = last_row["end_time"].item()
            self.end_time = None if pd.isnull(time) else time

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

            # Check string format
            ts_data.check_string_pattern_match(
                start_time_string, pattern=r"[0-9][0-9]:[0-9][0-9]"
            )

            # Convert to time
            hours, minutes = map(int, start_time_string.split(":"))
            start_time = datetime.combine(
                current_date, time(hour=hours, minute=minutes)
            )

        # Check if a current end_time exists
        if self.end_time == None:
            warnings.warn(
                f"Adding new start time when current end_time is None. (Please review and edit timesheet file)"
            )

        # Check current start is after end_time
        elif self.end_time >= start_time:
            raise Exception(
                f"The start_time provided ({start_time}) is not after the current end_time ({self.end_time})"
            )

        # Add date and start time to timesheet
        new_timesheet_record = {
            "date": pd.Timestamp(current_date),
            "start_time": pd.Timestamp(start_time),
            "end_time": pd.Timestamp("nat"),
            "time_worked": pd.Timedelta(15, "s"),
            "notes": "",
        }
        new_timesheet_record = pd.DataFrame([new_timesheet_record])
        self.timesheet = pd.concat([self.timesheet, new_timesheet_record])

        # Reset dataframe index
        self.timesheet = self.timesheet.reset_index(drop=True)

        # Write updated timesheet to file
        self.write_timesheet()

        # Set current start and end times
        self.start_time = start_time
        self.end_time = None

    def write_timesheet(self):
        """Write timesheet to file

        Timesheet written to self.file_name (set in __init__), overwrites current content
        """

        # Create a copy of the dataframe
        my_timesheet = self.timesheet.copy()

        # Format the date and time columns as strings
        my_timesheet = ts_data.format_datetime_columns_to_strings(my_timesheet)

        # Write to file
        my_timesheet.to_csv(self.file_name, index=False)

    def add_end_time(self, end_time_string: str = None):
        """Add end time to timesheet

        Args:
            end_time_string (str, optional): time (format: hh:mm) to use for end time
                Defaults to None (will use current time).
        """

        # Get datetime object for now
        current_datetime = datetime.now()
        current_date = current_datetime.date()

        # Get current time
        end_time = current_datetime

        # Check if a end time provided
        if end_time_string != None:

            # Check string format
            ts_data.check_string_pattern_match(
                end_time_string, pattern=r"[0-9][0-9]:[0-9][0-9]"
            )

            # Convert to time
            hours, minutes = map(int, end_time_string.split(":"))
            end_time = datetime.combine(current_date, time(hour=hours, minute=minutes))

        # Check if a current start_time exists
        if self.start_time == None:
            raise Exception(
                f"Trying to add end time when start time is None (doesn't exist). (Please review and edit timesheet file)"
            )

        # Check current end is after start_time
        elif self.start_time >= end_time:
            raise Exception(
                f"The end_time provided ({end_time}) is not after the current start_time ({self.start_time})"
            )

        # Add end_time to timesheet
        # Note using .loc here so change is made directly on dataframe rather than on copy/slice
        # which would be done if used indices/names with [] or .
        self.timesheet.loc[self.timesheet.index[-1], "end_time"] = pd.Timestamp(
            end_time
        )

        # Write updated timesheet to file
        self.write_timesheet()

        # Set current start and end times
        self.start_time = None
        self.end_time = end_time

    def reset_timesheet(self):
        """Reset and empty timesheet"""

        # Create new empty timesheet
        self.create_timesheet()

        # Reset start and end times
        self.start_time = None
        self.end_time = None
