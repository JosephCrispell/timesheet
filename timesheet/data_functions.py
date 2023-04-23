from datetime import date, time, datetime, timedelta  # working with dates and times
from pathlib import Path  # handling file paths
import pandas as pd  # creating dummy data
import re  # string matching


def check_string_pattern_match(string: str, pattern: str):
    """Check string matches pattern and throw error if not

    Args:
        string (str): input string to match against pattern
        pattern (str): input pattern to match against string

    Raises:
        Exception: if string doesn't match pattern
    """

    if not re.match(pattern, string):
        raise Exception(
            f"String provided ({string}) doesn't match pattern ({pattern})!"
        )


def format_datetime_columns_to_strings(my_timesheet: pd.DataFrame) -> pd.DataFrame:
    """Formats the date and time columns in timesheet as strings

    Input timesheet derived from timesheet.py

    date: YYYY-mm-dd
    start_time: hh:mm
    end_time: hh:mm
    time_worked: hh:mm
    Args:
        my_timesheet (pd.DataFrame): dataframe containing timesheet

    Returns:
        pd.DataFrame: timesheet dataframe with datetime columns as strings
    """

    # Format the date and time columns as strings
    my_timesheet.date = my_timesheet.date.dt.strftime("%Y-%m-%d")
    my_timesheet.start_time = my_timesheet.start_time.dt.strftime("%H:%M")
    my_timesheet.end_time = my_timesheet.end_time.dt.strftime("%H:%M")
    my_timesheet.time_worked = my_timesheet.time_worked.astype(str).str[
        -8:-3
    ]  # strips out number days

    # Replace oddly subsetted values in time_worked column with 00:00
    # occurs when zero times sent through
    my_timesheet.time_worked = my_timesheet.time_worked.replace("0 d", "00:00")

    return my_timesheet


def calculate_time_difference(start_time: datetime, end_time: datetime) -> timedelta:
    """Calculate difference between start and end time

    Args:
        start_time (datetime.time): start time
        end_time (datetime.time): end time

    Returns:
        datetime.time: difference between start and end time
    """

    # Calculate time difference
    difference = end_time - start_time

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

    # Check the same number of start and end times provided
    if len(start_times) != len(end_times):
        raise Exception(
            f"The number of start ({len(start_times)}) and end ({len(end_times)}) times provided don't match!"
        )

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
    dates = [
        date(year=2023, month=3, day=13),
        date(year=2023, month=3, day=13),
        date(year=2023, month=3, day=14),
        date(year=2023, month=3, day=14),
        date(year=2023, month=3, day=15),
        date(year=2023, month=3, day=15),
        date(year=2023, month=3, day=16),
        date(year=2023, month=3, day=16),
    ]
    start_times = [
        datetime.combine(dates[0], time(hour=8, minute=24)),
        datetime.combine(dates[1], time(hour=12, minute=24)),
        datetime.combine(dates[2], time(hour=8, minute=35)),
        datetime.combine(dates[3], time(hour=12, minute=45)),
        datetime.combine(dates[4], time(hour=8, minute=22)),
        datetime.combine(dates[5], time(hour=12, minute=15)),
        datetime.combine(dates[6], time(hour=8, minute=36)),
        datetime.combine(dates[7], time(hour=12, minute=56)),
    ]
    end_times = [
        datetime.combine(dates[0], time(hour=12, minute=0)),
        datetime.combine(dates[1], time(hour=16, minute=24)),
        datetime.combine(dates[2], time(hour=12, minute=5)),
        datetime.combine(dates[3], time(hour=16, minute=55)),
        datetime.combine(dates[4], time(hour=11, minute=51)),
        datetime.combine(dates[5], time(hour=17, minute=5)),
        datetime.combine(dates[6], time(hour=12, minute=6)),
        datetime.combine(dates[7], time(hour=17, minute=3)),
    ]
    dummy_timesheet_data = {
        "date": dates,
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

    # Convert columns to pandas datetimes to be consistent with how they are read in
    dummy_timesheet_data.date = pd.to_datetime(dummy_timesheet_data.date)
    dummy_timesheet_data.start_time = pd.to_datetime(dummy_timesheet_data.start_time)
    dummy_timesheet_data.end_time = pd.to_datetime(dummy_timesheet_data.end_time)
    dummy_timesheet_data.time_worked = pd.to_timedelta(dummy_timesheet_data.time_worked)

    # Format the date and time columns as strings
    dummy_timesheet_data = format_datetime_columns_to_strings(dummy_timesheet_data)

    # Write data to file
    dummy_timesheet_data.to_csv(file_name, index=False)
