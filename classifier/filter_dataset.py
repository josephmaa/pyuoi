import os
import argparse
import sys
import numpy as np
from tqdm import tqdm
import xarray as xr
import pandas as pd
import logging

def initialize_arg_parser():
    parser = argparse.ArgumentParser(description="Generate compiled dataset.")

    parser.add_argument("--input_directory", help="Path to the input feature directory.", default="features.all")
    parser.add_argument(
        "--output_directory",
        help="Argument for the output directory of the files",
        default=os.path.join(os.getcwd(), "local_downsampled_netcdfs"),
    )
    return parser

def downsample_dataframe(dataframe_to_downsample: pd.DataFrame) -> pd.DataFrame:
    """
    Downsamples a dataframe class on the column "behavior_name", reducing the highest count class to that of the second highest count class. Assumes that the number of unique behavior names is greater than one.
    """
    assert len(pd.unique(dataframe_to_downsample["behavior_name"])) > 1, "The number of behaviors must be greater than one."

    # The mapping is always sorted in descending order
    mapping_sorted_behavior_to_counts = dataframe_to_downsample["behavior_name"].value_counts().to_dict()

    counts = list(mapping_sorted_behavior_to_counts.values())
    majority_class = next(iter(mapping_sorted_behavior_to_counts))
    count_downsample_majority_class = counts[0] - counts[1]

    # Get the indices of the majority class
    indices = np.array(dataframe_to_downsample["behavior_name"].loc[lambda x: x == majority_class].index)
    np.random.seed(1)
    np.random.shuffle(indices)
    negative_indices_mask = indices[:count_downsample_majority_class]
    downsampled = dataframe_to_downsample.drop(index=negative_indices_mask)

    return downsampled       

def main():
    parser = initialize_arg_parser()
    ps = parser.parse_args(sys.argv[1:])
    os.makedirs(ps.output_directory, exist_ok=True)

    for behavior_netcdf_file in tqdm(os.listdir(ps.input_directory)):
        input_file_full_path = os.path.join(ps.input_directory, 
        behavior_netcdf_file)
        # Skip directories
        if not os.path.isfile(input_file_full_path) or not input_file_full_path.endswith(".netcdf"):
            continue
        # Load the dataset.
        df = xr.load_dataset(input_file_full_path, engine="h5netcdf").to_dataframe()

        if len(pd.unique(df["behavior_name"])) > 1:
            df = downsample_dataframe(dataframe_to_downsample=df)

        # Write the downsampled dataset to the output directory.
        xr.Dataset(df).to_netcdf(input_file_full_path, engine="h5netcdf")


if __name__ == "__main__":
    main()
