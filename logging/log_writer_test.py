import unittest
import pandas as pd
import os
import sys

from logging.log_writer import DatasetLog
import logging.test_utils 
from parameterized import parameterized

class TestLogWriter(unittest.TestCase):
    def setUp(self):
        logging.test_utils.create_temp_dir()

    def tearDown(self):
        logging.test_utils.delete_temp_dir()

    @parameterized.expand(
        [
            ({"col1": [0, 1, 2, 3], "col2": pd.Series([2, 3], index=[2, 3])},),
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

        log = DatasetLog(expected_df)
        log.write(os.path.join(os.getcwd(), logging.test_utils.object_logging_dir()), "log1.txt")

        output_df = DatasetLog.read(
            os.path.join(os.path.join(os.getcwd(), logging.test_utils.object_logging_dir()), "log1.txt")
        )

        self.assertTrue(pd.DataFrame.equals(expected_df, output_df))

if __name__ == "__main__":
    unittest.main()