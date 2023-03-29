import pandas as pd  # working with data


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

    return my_timesheet
