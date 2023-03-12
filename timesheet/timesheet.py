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
        self.timesheet = self.read_timesheet()

    def create_timesheet(self):
        """Creates timesheet CSV file"""
        # Initialise dataframe
        self.timesheet = pd.DataFrame(
            columns=["date", "start_time", "end_time", "hh:mm", "notes"]
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
