# Local imports
from timesheet import timesheet  # time sheet class


def main():

    # Get timesheet
    my_timesheet = timesheet.Timesheet()

    # Add start time
    my_timesheet.add_start_time()

    # Add end time
    my_timesheet.add_end_time()


if __name__ == "__main__":
    main()
