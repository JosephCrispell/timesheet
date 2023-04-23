# Load required libraries
import subprocess  # command line commands
import coverage  # not used directly but run in command line
from io import BytesIO  # reading byte string (returned by coverage)
import pandas as pd  # working with dataframes
from pathlib import Path  # handling file paths
import re  # working with regular expressions


def parse_coverage_report(coverage_report_byte_string: bytes) -> pd.DataFrame:
    """Parses byte string returned by coverage report into pandas dataframe

    Args:
        coverage_report_byte_string (bytes): byte string version of coverage report

    Returns:
        pd.DataFrame: coverage report as dataframe
    """

    # Convert the byte string into pandas dataframe
    coverage_dataframe = pd.read_csv(BytesIO(coverage_report_byte_string), sep="\s+")

    # Remove empty rows
    coverage_dataframe = coverage_dataframe[1:-2]
    coverage_dataframe = coverage_dataframe.reset_index(drop=True)

    # Remove percent sign from coverage column and convert to float
    coverage_dataframe.Cover = coverage_dataframe.Cover.str[:-1].astype(float)

    return coverage_dataframe


def run_code_coverage() -> pd.DataFrame:
    """Runs coverage tool in command line and returns report

    Returns:
        pd.DataFrame: coverage report as dataframe
    """

    # Run code coverage calculation
    subprocess.run(["python3", "-m", "coverage", "run", "--source=.", "-m", "unittest"])

    # Generate the report
    coverage_report = subprocess.check_output(["python3", "-m", "coverage", "report"])

    # Convert coverage report output to dataframe
    report_dataframe = parse_coverage_report(coverage_report)

    return report_dataframe


def get_badge_colour(
    value: float,
    poor_max_threshold: float,
    medium_max_threshold: float,
    poor_colour: str = "red",
    medium_colour: str = "orange",
    good_colour: str = "green",
) -> str:
    """Gets coverage badger colour based on value and thresholds

    Args:
        value (float): coverage value
        poor_max_threshold (float): threshold below which badge colour is poor_colour
        medium_max_threshold (float): threshold below which badge colour is medium_colour
        poor_colour (str, optional): colour for badge when value <= poor_max_threshold. Defaults to "red".
        medium_colour (str, optional): colour for badge when value <= medium_max_threshold but more than poor_max_threshold. Defaults to "orange".
        good_colour (str, optional): colour for badge when value > medium_max_threshold. Defaults to "green".

    Returns:
        str: colour for badge
    """

    badge_colour = None
    if value < poor_max_threshold:
        badge_colour = poor_colour
    elif value < medium_max_threshold:
        badge_colour = medium_colour
    else:
        badge_colour = good_colour

    return badge_colour


def make_coverage_badge_url(
    coverage_dataframe: pd.DataFrame,
    poor_max_threshold: float = 25,
    medium_max_threshold: float = 75,
) -> str:
    """Uses shields io to build coverage badge

    Args:
        coverage_dataframe (pd.DataFrame): coverage report as dataframe
        poor_max_threshold (float, optional): threshold below which badge colour is red. Defaults to 25.
        medium_max_threshold (float, optional): threshold below which badge colour is orange. Defaults to 75.

    Returns:
        str: _description_
    """

    # Calculate the average code coverage
    total_statements = sum(coverage_dataframe.Stmts)
    total_statements_missed = sum(coverage_dataframe.Miss)
    average_coverage = (total_statements - total_statements_missed) / total_statements

    # Convert to percentage and round
    average_coverage = round(average_coverage * 100, 1)

    # Note badger colour
    badge_colour = get_badge_colour(
        average_coverage, poor_max_threshold, medium_max_threshold
    )

    # Build badge
    badge_url = (
        f"https://img.shields.io/badge/coverage-{average_coverage}%25-{badge_colour}"
    )

    return badge_url


def replace_string_in_file(file_path: Path, pattern_regex: str, replacement: str):
    """Replace pattern in file with string

    Args:
        file_path (Path): path to file
        pattern_regex (str): pattern to find
        replacement (str): string to replace pattern when found
    """

    # Read in file contents
    file_lines = []
    with open(file_path) as file:
        file_lines = file.read().splitlines()

    # Replace string in each line
    file_lines = [re.sub(pattern_regex, replacement, line) for line in file_lines]

    # Write file lines back to file
    file_lines.append("\n")
    with open(file_path, "w") as file:
        file.write("\n".join(file_lines))
