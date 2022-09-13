import unittest
import pandas as pd
import os
import sys

from logging.log_writer import DatasetLog
from logging.test_utils import create_temp_dir, delete_temp_dir, object_logging_dir
from parameterized import parameterized

class TestLogWriter(unittest.TestCase):
    def setUp(self):
        create_temp_dir()

    def tearDown(self):
        delete_temp_dir()

    @parameterized.expand(
        [
            {"col1": [0, 1, 2, 3], "col2": pd.Series([2, 3], index=[2, 3])},
        ]
    )
    def test_log_writer(self, df: pd.DataFrame):
        """
        >>> df = {'col1': [0, 1, 2, 3], 'col2': pd.Series([2, 3], index=[2, 3])}
        >>> df = pd.DataFrame(data=df, index=[0, 1, 2, 3])
        col1  col2
        0     0   NaN
        1     1   NaN
        2     2   2.0
        3     3   3.0
        >>> log = DatasetLog(df)
        >>> log.write("/Users/josephgmaa/pyuoi", "log1.txt")
        >>> DatasetLog.read("/Users/josephgmaa/pyuoi/log1.txt")
        col1  col2
        0     0   N
        1     1   NaN
        2     2   2.0
        3     3   3.0
        """
        expected_df = pd.DataFrame(data=df, index=[0, 1, 2, 3])

        log = DatasetLog(df)
        log.write(object_logging_dir(), "log1.txt")

        output_df = DatasetLog.read(
            os.path.join(object_logging_dir, "log1.txt")
        )

        self.assertTrue(pd.DataFrame.equals(expected_df, output_df))

if __name__ == "__main__":
    unittest.main()