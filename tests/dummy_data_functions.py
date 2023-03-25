from datetime import date, time, datetime, timedelta  # working with dates and times
from pathlib import Path  # handling file paths
import pandas as pd  # creating dummy data


def calculate_time_difference(start_time: time, end_time: time) -> timedelta:
    """Calculate difference between start and end time

    Args:
        start_time (datetime.time): start time
        end_time (datetime.time): end time

    Returns:
        datetime.time: difference between start and end time
    """

    # Calculate time difference
    difference = datetime.combine(date.today(), end_time) - datetime.combine(
        date.today(), start_time
    )

    # Check time difference is positive
    if difference.total_seconds() < 0:
        raise Exception(
            f"The end_time provided ({end_time}) is not after the start_time ({start_time})"
        )

    return difference


def calculate_time_differences(
    start_times: list[time], end_times: list[time]
) -> list[timedelta]:
    """Calculate difference between times

    Based on this stackoverflow answer: https://stackoverflow.com/questions/25346019/subtract-datetime-time-objects-stored-in-two-separate-lists

    Args:
        start_times (list[datetime.time]): list of start times
        end_times (list[datetime.time]): list of end times

    Returns:
        list[datetime.time]: list of time differences
    """

    # Calculate time differences
    differences = [
        calculate_time_difference(start_time, end_time)
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
