import os
import argparse
import sys
import pandas as pd
from dataset_distribution_metrics import Dataset
import numpy as np
from tqdm import tqdm
import xarray as xr

def initialize_arg_parser():
    parser = argparse.ArgumentParser(description="Generate compiled dataset.")

    parser.add_argument("--input_directory_features", help="Path to the input feature directory.", default="features.all")
    parser.add_argument(
        "--input_directory_counts",
        help="Path to the input directory. Assumes that all .netcdf files in the directory will be used for the final dataset",
        default="2022_09_27_02_20_52/counts",
    )
    parser.add_argument(
        "--input_directory_behaviors",
        help="Path to the input directory. Assumes that all .netcdf files in the directory will be used for the final dataset",
        default="2022_09_27_02_20_52/behaviors",
    )
    parser.add_argument(
        "--output_directory",
        help="Argument for the output directory of the files",
        default=os.getcwd(),
    )
    return parser


def main():
    parser = initialize_arg_parser()
    ps = parser.parse_args(sys.argv[1:])

    counts_df = pd.DataFrame()
    # Read in all the datasets counts.
    print("Read in dataset counts.")
    for file in tqdm(os.listdir(ps.input_directory_counts)):
        intermediate_df = pd.read_csv(os.path.join(os.getcwd(), ps.input_directory_counts, file))
        counts_df = pd.concat([counts_df, intermediate_df], axis=0, ignore_index=True)

    counts_df.reset_index(inplace=True)
    counts_df.drop(columns=["index", "Unnamed: 0"], inplace=True)
    grouped_counts = counts_df.groupby("behavior_name", as_index=False)["count"].sum()
    ds = Dataset()
    ds.initialize_dataset(grouped_counts)
    counts = ds.distribution()

    # Read in all the indices of the datasets with frame numbers.
    sorted_behavior_counts = list(sorted(counts.values(), reverse=True))

    # Group by highest behavior count to downsample and create a list of indices to randomly downsample frames from the max.
    count_downsampled_behaviors = sorted_behavior_counts[0] - sorted_behavior_counts[1]

    # Re-open netcdfs and filter by available frames.
    behavior_frames_df = pd.DataFrame()
    print("Read in behavior dataframe indices.")
    for file in tqdm(os.listdir(ps.input_directory_behaviors)):
        intermediate_df = pd.read_csv(os.path.join(os.getcwd(), ps.input_directory_behaviors, file))
        behavior_frames_df = pd.concat([behavior_frames_df, intermediate_df], axis=0) 

    walk_frame_indices = behavior_frames_df.loc[behavior_frames_df["behavior_name"] == "Walk", "vid_framenum"].to_numpy()

    # Downsample indices
    np.random.seed(1)
    np.random.shuffle(walk_frame_indices)

    downsampled_walk_frame_indices = walk_frame_indices[count_downsampled_behaviors:]
    np.save("/Users/josephgmaa/pyuoi/2022_09_27_02_20_52/test.npy", downsampled_walk_frame_indices)
    arr = sorted(np.load("/Users/josephgmaa/pyuoi/2022_09_27_02_20_52/test.npy"))

    write_filtered_netcdfs(ps.input_directory_features)

    # Re-evaluate counts to confirm downsampling worked successfully.

def write_filtered_netcdfs(input_directory_features: str):
    # Re-write netcdfs to output directory.
    for file in os.listdir(input_directory_features):
        unfiltered_dataframe = xr.load_dataset(os.path.join(os.getcwd(), input_directory_features, file))
        start, end = unfiltered_dataframe.iloc[0: "vid_framenum"], unfiltered_dataframe.iloc[len(unfiltered_dataframe) - 1: "vid_framenum"]
        print(start, end)
        break

if __name__ == "__main__":
    main()