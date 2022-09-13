import sys
import argparse
import os
import pandas as pd
import xarray as xr

from collections import Counter
from visualize_dataset_distribution import Dataset


def initialize_arg_parser():
    parser = argparse.ArgumentParser(description="Generate compiled dataset.")

    parser.add_argument(
        "--input_directory",
        help="Path to the input directory. Assumes that all .netcdf files in the directory will be used for the final dataset",
        default="features.all",
    )
    parser.add_argument(
        "--output_files",
        help="Optional argument for the output directory of the files",
        default="",
    )
    parser.add_argument(
        "--aggregate",
        help="Speed up computations by loading behaviors into dict instead.",
        default=False,
    )
    return parser


def main():
    parser = initialize_arg_parser()
    ps = parser.parse_args(sys.argv[1:])
    ds = Dataset()
    df = pd.DataFrame()
    num_files = len(os.listdir(ps.input_directory))

    if ps.aggregate:
        counts = Counter()

    for i, input_file in enumerate(os.listdir(ps.input_directory)):
        print(f"Processing {i} of {num_files}")
        print(counts)
        if input_file.endswith(".netcdf"):
            new_dataframe = xr.load_dataset(
                os.path.join(os.getcwd(), "features.all", input_file),
                engine="h5netcdf",
            ).to_dataframe()
            if ps.aggregate:
                counts.update(Counter(new_dataframe["behavior_name"]))
            else:
                df = pd.concat([df, new_dataframe])

    ds.initialize_dataset(df)
    ds.distribution(output_file=ps.output_files)

    if ps.aggregate:
        print(counts)


if __name__ == "__main__":
    main()
