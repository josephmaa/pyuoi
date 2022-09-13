import os
import pandas as pd
from typing import Optional


class DatasetLog:
    """
    Class that outputs log files. Data should be pre-processed prior to writing to log file. The write method has to be explicitly called in order to write a log file. The filename is standardized to the date and time.
    """

    def __init__(self, data: Optional[pd.DataFrame] = None):
        if not isinstance(data, pd.DataFrame):
            raise NotImplementedError("Dataset must be a pandas dataframe.")
        self._data = data

    def write(self, output_path: str, filename: str):
        if not filename.endswith(".txt"):
            raise NotImplementedError("Filename must be a text file.")
        with open(os.path.join(output_path, filename), "w") as file:
            file.write(self._data.to_csv())

    def read(input_file_path: str):
        if not input_file_path.endswith(".txt"):
            raise NotImplementedError("Input file must be a text file.")
        return pd.read_csv(input_file_path, index_col=0)
