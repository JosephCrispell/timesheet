# Load packages
from pathlib import Path  # handling file paths

# Local imports
from timesheet import unittest_coverage_functions  # functions for running coverage


def main():

    # Run code coverage
    coverage_dataframe = unittest_coverage_functions.run_code_coverage()

    # Build badge
    coverage_badge_url = unittest_coverage_functions.make_coverage_badge_url(
        coverage_dataframe
    )

    # Update badger in README
    unittest_coverage_functions.replace_string_in_file(
        file_path=Path("README.md"),
        pattern_regex=r"\!\[Code Coverage\]\(.+\)",
        replacement=f"![Code Coverage]({coverage_badge_url})",
    )


if __name__ == "__main__":
    main()

# TODO Add unittests
