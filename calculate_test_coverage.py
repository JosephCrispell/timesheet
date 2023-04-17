# See second answer here for code to get coverage from unitttest: https://stackoverflow.com/questions/29295965/python-coverage-badges-how-to-get-them
# See video here for how to create manual shields.io badge: https://www.youtube.com/watch?v=bNVRxb-MKGo&ab_channel=glebbahmutov
# - Note that will need specific script to set colour thresholds
# - For example: https://img.shields.io/badge/coverage-75%25-green url gives great looking badge

# Generate coverage report: pythontutorial.net/python-unit-testing/python-unittest-coverage/

# See existing tool: https://pypi.org/project/readme-coverage-badger/

# Load required libraries
import subprocess  # command line commands
import coverage  # not used directly but run in command line
from io import BytesIO  # reading byte string (returned by coverage)
from statistics import median, mean
import pandas as pd


def parse_coverage_report(coverage_report_byte_string: bytes) -> pd.DataFrame:

    # Convert the byte string into pandas dataframe
    coverage_dataframe = pd.read_csv(BytesIO(coverage_report_byte_string), sep="\s+")

    # Remove empty rows
    coverage_dataframe = coverage_dataframe[1:-2]
    coverage_dataframe = coverage_dataframe.reset_index(drop=True)

    # Remove percent sign from coverage column and convert to float
    coverage_dataframe.Cover = coverage_dataframe.Cover.str[:-1].astype(float)

    return coverage_dataframe


def run_code_coverage() -> pd.DataFrame:

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


def main():

    # Run code coverage
    coverage_dataframe = run_code_coverage()

    # Build badge
    coverage_badge_url = make_coverage_badge_url(coverage_dataframe)

    print(coverage_badge_url)


if __name__ == "__main__":
    main()

# TODO Figure out how to edit README
# Replace ![Coverage](...)
# https://stackoverflow.com/questions/4128144/replace-string-within-file-contents

# TODO Tidy and create functions
