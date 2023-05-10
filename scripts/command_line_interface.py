# Load packages
import argparse  # parsing command line arguments

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
    parser = argparse.ArgumentParser(description=welcome_message)

    # Add arguments
    parser.add_argument(
        "-f",
        "--file",
        nargs="?",  # Accept 0 or 1 arguments
        const="outputs/timesheet.csv",  # Default value
        type=str,
        help="Provide file for timesheet. Defaults to outputs/timesheet.csv",
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
        const=None,
        type=str,
        help="Add start time (hh:mm) to timesheet file provided with file (-f/--file) argument. Defaults to current time.",
    )
    parser.add_argument(
        "-e",
        "--end",
        nargs="?",
        const=None,
        type=str,
        help="Add end time (hh:mm) to timesheet file provided with file (-f/--file) argument. Defaults to current time.",
    )

    return parser


def main():

    # Build interface
    parser = build_command_line_interface()

    # Get arguments
    args = parser.parse_args()

    if args.Output:
        print("Displaying Output as: % s" % args.Output)


if __name__ == "__main__":
    main()
