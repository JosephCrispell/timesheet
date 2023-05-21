# Load packages
import unittest  # running tests
from pathlib import Path  # handling file paths
import pandas as pd  # working with dummy data
from datetime import date  # working with dates

# Local imports
from timesheet import command_line_interface_functions  # cli functions
from timesheet import data_functions  # functions for working with data
from timesheet import timesheet  # timesheet class


class TestCommandLineInterfaceFunctions(unittest.TestCase):
    def test_build_command_line_interface(self):
        """Test command line parser is built"""

        # Build the command line interface parser
        parser = command_line_interface_functions.build_command_line_interface()

        # Check argument parser returned
        self.assertEqual(
            str(type(parser)),
            "<class 'argparse.ArgumentParser'>",
            "Check argument parser returned",
        )

    def test_parse_command_line_arguments(self):

        # Build the command line interface parser
        parser = command_line_interface_functions.build_command_line_interface()

        # Create the dummy data
        timesheet_file = Path("outputs/test_timesheet.csv")
        data_functions.create_dummy_timesheet(file_name=timesheet_file)

        # Define the command line arguments and parse
        start_time = "09:00"
        end_time = "11:45"
        arguments = [
            "--file",
            str(timesheet_file),
            "--start",
            start_time,
            "--end",
            end_time,
        ]
        command_line_interface_functions.parse_command_line_arguments(parser, arguments)

        # Load test timesheet
        my_timesheet = timesheet.Timesheet(file_name=timesheet_file)

        # Check today's date, start time, and end time added
        n_rows = my_timesheet.timesheet.shape[0]
        today = date.today().strftime("%Y-%m-%d")
        self.assertEqual(
            my_timesheet.timesheet.date[n_rows - 1],
            pd.Timestamp(today + " 00:00:00"),
            "Check today's date input correctly",
        )
        self.assertEqual(
            my_timesheet.timesheet.start_time[n_rows - 1],
            pd.Timestamp("1900-01-01 " + start_time + ":00"),
            "Check start time added",
        )
        self.assertEqual(
            my_timesheet.timesheet.end_time[n_rows - 1],
            pd.Timestamp("1900-01-01 " + end_time + ":00"),
            "Check end time added",
        )

        # Remove timesheet
        Path.unlink(timesheet_file)


# TODO add test for build_command_line_interface
# TODO add test for parse_command_line_arguments


if __name__ == "__main__":
    unittest.main()
