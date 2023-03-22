from pathlib import Path  # handling file paths
import pandas as pd  # working with data


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
        """Creates timesheet CSV file"""
        # Initialise dataframe
        self.timesheet = pd.DataFrame(
            columns=["date", "start_time", "end_time", "time_worked", "notes"]
        )

        # Write to file
        self.timesheet.to_csv(self.file_name, index=False)
        print(f"Created timesheet file at: {self.file_name}")

    def read_timesheet(self):

        # Check timesheet exists
        if Path.exists(self.file_name) == False:
            self.create_timesheet()

        # Read in timesheet
        self.timesheet = pd.read_csv(self.file_name)

        # Convert date and time columns to datetime objects
        self.timesheet["date"] = pd.to_datetime(self.timesheet["date"])
        self.timesheet["start_time"] = pd.to_datetime(
            self.timesheet["start_time"], format="%H:%M:%S"
        )
        self.timesheet["end_time"] = pd.to_datetime(
            self.timesheet["end_time"], format="%H:%M:%S"
        )
        self.timesheet["time_worked"] = pd.to_timedelta(self.timesheet["time_worked"])
