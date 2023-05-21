# Load packages
import argparse  # parsing command line arguments
from pathlib import Path  # handling file paths
from datetime import datetime  # working with dates and times
import sys  # accessing command line arguments

# Local imports
from timesheet import timesheet


def build_command_line_interface() -> argparse.ArgumentParser:
    """Builds command line interface for timesheet

    Adds the following arguments:
    - Timesheet file: -f/--file
    - Reset: -r/--reset
    - Add start time: -s/--start
    - Add end time: -s/--end

    Returns:
        argparse.ArgumentParser: argument parser
    """

    # Write welcome message
    welcome_message = "Welcome to timesheet, a tool to help you log the hours you work. You are using the command line interface for timesheet."

    # Initialize parser
    parser = argparse.ArgumentParser(
        description=welcome_message,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,  # Shows default values for parameters
    )

    # Add arguments
    parser.add_argument(
        "-f",
        "--file",
        nargs="?",  # Accept 0 or 1 arguments
        default="outputs/timesheet.csv",  # Default value
        metavar="timesheet_file_path",
        type=str,
        help="Provide file for timesheet (note if note created this will create file).",
    )
    parser.add_argument(
        "-r",
        "--reset",
        action="store_true",
        help="Reset the timesheet file provided with file (-f/--file) argument.",
    )
    parser.add_argument(
        "-s",
        "--start",
        nargs="?",
        const=datetime.now().strftime(
            "%H:%M"
        ),  # Only used when no value provided but arg given. Note different to default, which is used when arg is absent
        metavar="hh:mm",
        type=str,
        help="Add start time (hh:mm) to timesheet file provided with file (-f/--file) argument.",
    )
    parser.add_argument(
        "-e",
        "--end",
        nargs="?",
        const=datetime.now().strftime("%H:%M"),
        metavar="hh:mm",
        type=str,
        help="Add end time (hh:mm) to timesheet file provided with file (-f/--file) argument.",
    )

    return parser


def parse_command_line_arguments(
    parser: argparse.ArgumentParser, arguments: list[str] = sys.argv[1:]
):
    """Parse command line arguments based on parser provided

    Args:
        parser (argparse.ArgumentParser): command line argument parser
        arguments (list[str]): list of command line arguments passed to parser.parse_args(), which isn't
            required normally but this measn we can unittest
            (see: https://stackoverflow.com/questions/18160078/how-do-you-write-tests-for-the-argparse-portion-of-a-python-module).
            Defaults to sys.argv[:1] (arguments minus script name).
    """

    # Get arguments
    args = parser.parse_args(arguments)

    # Load timesheet
    my_timesheet = timesheet.Timesheet(file_name=Path(args.file))

    # Check if resetting timesheet
    if args.reset:
        my_timesheet.reset_timesheet()

    # Check if adding start time
    if args.start:
        my_timesheet.add_start_time(start_time_string=args.start)

    # Check if adding end time
    if args.end:
        my_timesheet.add_end_time(end_time_string=args.end)
