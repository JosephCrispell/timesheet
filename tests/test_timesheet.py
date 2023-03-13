import unittest  # running tests
from pathlib import Path  # handling file paths

from timesheet import timesheet


class TestTimesheet(unittest.TestCase):
    def test_timesheet(self):

        # Get timesheet
        my_timesheet = timesheet.Timesheet(file_name=Path("outputs/test_timesheet.csv"))

        # Check timesheet file exists
        self.assertTrue(Path.exists(my_timesheet.file_name))


if __name__ == "__main__":
    unittest.main()
