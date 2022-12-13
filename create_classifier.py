import pandas as pd
import sqlite3
from pyuoi import UoI_L1Logistic
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import numpy as np
from sklearn.metrics import accuracy_score
import argparse
from sklearn.preprocessing import Normalizer


def main(args):
    conn = sqlite3.connect(args.database_path)
    df = pd.read_sql(sql="SELECT * FROM features", con=conn)

    y = df["behavior_name"].to_numpy()
    le = LabelEncoder()
    le.fit(y)

    X = df.loc[:, df.dtypes == np.float64].to_numpy()
    transformer = Normalizer()
    input_data = transformer.transform(X)

    # We only use dtypes of float64 in training for columns.
    x_train, x_test, y_train, y_test = train_test_split(
        input_data,
        le.transform(y),
        random_state=1,
    )

    print(
        f"label encoder output {le.transform(y).shape}, actual output {le.transform(y)}"
    )

    pd.set_option("display.max_rows", None, "display.max_columns", None)
    print(
        f"arrays: {df.loc[0, df.dtypes == np.float64]}, shape: {df.loc[:, df.dtypes == np.float64].shape}"
    )

    print(f"x train: {x_train}, x_test: {x_test}")

    print(f"y test: {y_test}, y_train: {y_train}")

    l1log = UoI_L1Logistic(random_state=1, multi_class="multinomial").fit(
        x_train, y_train, verbose=True
    )

    y_hat = l1log.predict(x_test)

    accuracy = accuracy_score(y_test, y_hat)
    print("y_test: ", y_test)
    print("y_hat: ", y_hat)
    y_test_freq = np.bincount(y_test)
    y_hat_freq = np.bincount(y_hat)
    print("y_test_freq: ", y_test_freq)
    print("y_hat_freq: ", y_hat_freq)

    print(f"Accuracy: {accuracy}")
    print(f"Resulting values: {y_hat}")
    print(f"selection values: {l1log._selection_lm}")
    print(f"estimation values: {l1log._estimation_lm}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--database_path", help="path to the database")
    args = parser.parse_args()
    main(args)
