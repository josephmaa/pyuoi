import matplotlib.pyplot as plt
import pandas as pd
import xarray as xr
import logging
import argparse
import sys

from collections import Counter
from typing import Optional
from multipledispatch import dispatch


def initialize_arg_parser():
    parser = argparse.ArgumentParser(
        description="Generate visualization of distributions for usage on the cluster."
    )

    parser.add_argument(
        "--input_files",
        help="Path to the input files.",
        default="/Users/josephgmaa/pyuoi/pyuoi/data/features/nolj_Recording_day7_overnight_636674151185633714_27_nolj.c3d.619.features.netcdf",
        nargs="+",
    )
    parser.add_argument(
        "--output_files",
        help="Path to the output files.",
        default="",
    )
    return parser


class Dataset:
    """
    Takes in a file as a full dataframe and returns metrics involving the distribution of the file.
    """

    def __init__(self):
        self.dataset: Optional[pd.DataFrame] = None

    @dispatch(str)
    def initialize_dataset(self, dataset):
        self.dataset = xr.load_dataset(dataset, engine="h5netcdf").to_dataframe()

    @dispatch(pd.DataFrame)
    def initialize_dataset(self, dataset):
        self.dataset = dataset

    def distribution(self, output_file: Optional[str] = None):
        """
        Outputs a matplotlib histogram of the distribution to the input file location.
        """
        if self.dataset is None:
            logging.warning("No dataset!")
            return

        counts = Counter(self.dataset["behavior_name"])
        fig, ax = plt.subplots()
        x, y = zip(*sorted(counts.items(), key=lambda x: x[1], reverse=True))
        bars = ax.bar(x, y)
        ax.bar_label(bars, [round(p / sum(y), 2) for p in y])
        plt.setp(ax.get_xticklabels(), rotation=90, horizontalalignment="right")
        if output_file:
            ax.set_title(output_file)
            plt.savefig(output_file, bbox_inches="tight", dpi=1000)
        else:
            plt.show()


if __name__ == "__main__":
    parser = initialize_arg_parser()
    ps = parser.parse_args(sys.argv[1:])
    ds = Dataset()
    ds.initialize_dataset(ps.input_files)
    ds.distribution(output_file=ps.output_files)
