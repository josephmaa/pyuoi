import sys
import argparse
import os
import pandas as pd
import xarray as xr
import datetime
from collections import Counter

from hashlib import sha256
from visualize_dataset_distribution import Dataset
from logging.log_writer import DatasetLog


def initialize_arg_parser():
    parser = argparse.ArgumentParser(description="Generate compiled dataset.")

    parser.add_argument(
        "--input_directory",
        help="Path to the input directory. Assumes that all .netcdf files in the directory will be used for the final dataset",
        default="features.all",
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
    ds = Dataset()
    df = pd.DataFrame()
    num_files = len(os.listdir(ps.input_directory))

    time = str(datetime.datetime.now().strftime("%Y_%m_%d_%I_%M_%S"))
    behavior_output_directory = os.path.join(ps.output_directory, time, "behaviors")
    counts_output_directory = os.path.join(ps.output_directory, time, "counts")

    print(behavior_output_directory
    )
    os.makedirs(behavior_output_directory, exist_ok=True)
    os.makedirs(counts_output_directory, exist_ok=True)

    for i, input_file in enumerate(os.listdir(ps.input_directory)):
        print(f"Processing {i} of {num_files}")
        if input_file.endswith(".netcdf"):
            hash_filename = f"{sha256(input_file.encode('utf-8')).hexdigest()}.txt"

            # Get the frame and behavior name from the dataframe
            behaviors_dataframe = xr.load_dataset(
                os.path.join(os.getcwd(), "features.all", input_file),
                engine="h5netcdf",
            ).to_dataframe()[["vid_framenum", "behavior_name"]]
            dataset_behaviors_log = DatasetLog(data = behaviors_dataframe)

            dataset_behaviors_log.write(behavior_output_directory, hash_filename)
            
            # Get the counts of the behaviors
            counts = Counter(behaviors_dataframe["behavior_name"])
            counts_dataframe = pd.DataFrame.from_records(list(counts.items()), columns=['behavior_name','count'])
            counts_dataframe.sort_values(by=["behavior_name"], inplace=True)
            dataset_counts_log = DatasetLog(data = counts_dataframe)
            dataset_counts_log.write(counts_output_directory, hash_filename)



if __name__ == "__main__":
    main()
