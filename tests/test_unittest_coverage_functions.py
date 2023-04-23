# Load packages
import unittest  # running tests
from pathlib import Path  # handling file paths

# Local imports
from timesheet import unittest_coverage_functions  # functions for running coverage


class TestUnittestCoverageFunctions(unittest.TestCase):
    def test_replace_string_in_file(self):
        """Test replacing of pattern in file with string"""

        # Create temporary file
        temporary_file_path = Path("outputs/test_README.md")
        file_lines = ["I", "am", "a", "really", "simple", "file", "\n"]
        with open(temporary_file_path, "w") as file:
            file.write("\n".join(file_lines))

        # Replace string in temporary file
        unittest_coverage_functions.replace_string_in_file(
            file_path=temporary_file_path, pattern_regex=r"s.m.+e", replacement="great"
        )

        # Read in temporary file lines
        file_lines = []
        with open(temporary_file_path) as file:
            file_lines = file.read().splitlines()

        # Check temporary file lines have changed
        self.assertEqual(
            file_lines[4],
            "great",
            "Check string was replaced in file",
        )

        # Remove temporary file
        Path.unlink(temporary_file_path)

    def test_parse_coverage_report(self):
        """Test parse of coverage byte string into coverage report"""

        # Create dummy coverage report data in byte string
        byte_string = "Name                                        Stmts   Miss  Cover\n---------------------------------------------------------------\nsetup.py                                        3      3     0%\ntests/__init__.py                               1      0   100%\ntests/test_data_functions.py                   19      1    95%\ntests/test_timesheet.py                        46      1    98%\ntests/test_unittest_coverage_functions.py      13      1    92%\ntimesheet/__init__.py                           2      0   100%\ntimesheet/data_functions.py                    32      2    94%\ntimesheet/timesheet.py                         53      1    98%\ntimesheet/unittest_coverage_functions.py       41     23    44%\nupdate_test_coverage_badge.py                   8      8     0%\n---------------------------------------------------------------\nTOTAL                                         218     40    82%\n"
        byte_string = bytes(byte_string, "utf-8")

        # Parse the report byte string
        coverage_dataframe = unittest_coverage_functions.parse_coverage_report(
            byte_string
        )

        # Check dataframe returned
        self.assertEqual(
            str(type(coverage_dataframe)),
            "<class 'pandas.core.frame.DataFrame'>",
            "Check start_time column contains datetimes",
        )

        # Check correct columns are present
        column_names = ["Name", "Stmts", "Miss", "Cover"]
        self.assertTrue(
            all(
                [
                    column_name in coverage_dataframe.columns
                    for column_name in column_names
                ]
            ),
            "Check expected columns present after parsing coverage report",
        )

        # Check some selected values
        self.assertEqual(
            coverage_dataframe.Cover[1],
            float("100.0"),
            "Check second value in Cover column",
        )
        self.assertEqual(
            coverage_dataframe.Name[2],
            "tests/test_data_functions.py",
            "Check third value in Name column",
        )
        self.assertEqual(
            coverage_dataframe.Stmts[7],
            float("53.0"),
            "Check eighth value in Stmts column",
        )

    def test_make_coverage_badge_url(self):
        """Test that shields io coverage badge url created correctly"""

        # Create dummy coverage report data in byte string
        byte_string = "Name                                        Stmts   Miss  Cover\n---------------------------------------------------------------\nsetup.py                                        3      3     0%\ntests/__init__.py                               1      0   100%\ntests/test_data_functions.py                   19      1    95%\ntests/test_timesheet.py                        46      1    98%\ntests/test_unittest_coverage_functions.py      13      1    92%\ntimesheet/__init__.py                           2      0   100%\ntimesheet/data_functions.py                    32      2    94%\ntimesheet/timesheet.py                         53      1    98%\ntimesheet/unittest_coverage_functions.py       41     23    44%\nupdate_test_coverage_badge.py                   8      8     0%\n---------------------------------------------------------------\nTOTAL                                         218     40    82%\n"
        byte_string = bytes(byte_string, "utf-8")

        # Parse the report byte string
        coverage_dataframe = unittest_coverage_functions.parse_coverage_report(
            byte_string
        )

        # Create badge url
        badge_url = unittest_coverage_functions.make_coverage_badge_url(
            coverage_dataframe
        )

        # Check url
        self.assertEqual(
            badge_url,
            "https://img.shields.io/badge/coverage-81.7%25-green",
            "Check expected shields io badger url produced",
        )

    def test_get_badge_colour(self):
        """Test that correct badger colour returned"""

        # Set value thresholds
        poor_max_threshold = 25
        medium_max_threshold = 75

        # Check badge is red when value lower than poor max threshold
        self.assertEqual(
            "red",
            unittest_coverage_functions.get_badge_colour(
                value=15,
                poor_max_threshold=poor_max_threshold,
                medium_max_threshold=medium_max_threshold,
            ),
            f"Badge is red when value lower than {poor_max_threshold}",
        )

        # Check badge is orange when value more than poor max threshold but lower than medium_max_threshold
        self.assertEqual(
            "orange",
            unittest_coverage_functions.get_badge_colour(
                value=47,
                poor_max_threshold=poor_max_threshold,
                medium_max_threshold=medium_max_threshold,
            ),
            f"Badge is orange when value more than {poor_max_threshold} but lower than {medium_max_threshold}",
        )

        # Check badge is green when value more than medium max threshold
        self.assertEqual(
            "green",
            unittest_coverage_functions.get_badge_colour(
                value=85,
                poor_max_threshold=poor_max_threshold,
                medium_max_threshold=medium_max_threshold,
            ),
            f"Badge is green when value more than {medium_max_threshold}",
        )


if __name__ == "__main__":
    unittest.main()
