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
    Downsamples a dataframe class on the column "behavior_name", reducing the highest count class to that of the second highest count class.
    """
    # The mapping is always sorted in descending order
    mapping_sorted_behavior_to_counts = dataframe_to_downsample["behavior_name"].value_counts().to_dict()

    counts = list(mapping_sorted_behavior_to_counts.values())
    if len(counts) > 1:
        logging.error("Downsample only when multiple behaviors are present.")
        return dataframe_to_downsample
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
        # Load the dataset.
        df = xr.load_dataset(os.path.join(ps.input_directory, 
        behavior_netcdf_file), engine="h5netcdf").to_dataframe()

        df = downsample_dataframe(dataframe_to_downsample=df)

        # Write the downsampled dataset to the output directory.
        xr.Dataset(df).to_netcdf(os.path.join(ps.output_directory, behavior_netcdf_file), engine="h5netcdf")


if __name__ == "__main__":
    main()
