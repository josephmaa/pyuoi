from classifier.filter_dataset import downsample_dataframe
import unittest
import pandas as pd
import xarray as xr

class TestDownsample(unittest.TestCase):
    def test_downsample_dataframe(self):
        df = xr.open_dataset("features.all/nolj_Recording_day7_overnight_636674151185633714_1_nolj.c3d.205.features.netcdf").to_dataframe()

        downsampled = downsample_dataframe(df)

        self.assertEqual(len(df), 5884)
        self.assertEqual(len(downsampled), 2643)

        original_counts = df["behavior_name"].value_counts()
        downsampled_counts = downsampled["behavior_name"].value_counts()

        self.assertFalse(original_counts["Rear"] == original_counts["AdjustPosture"])
        self.assertTrue(downsampled_counts["Rear"] == downsampled_counts["AdjustPosture"])



        