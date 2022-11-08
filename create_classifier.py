import pandas as pd
import sqlite3
from pyuoi import UoI_L1Logistic
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import numpy as np
from sklearn.metrics import accuracy_score


# DB_FILE_PATH = "/wynton/home/manoli/josephgmaa/pyuoi/test_small.db"
DB_FILE_PATH = "/wynton/home/manoli/josephgmaa/pyuoi/test.db"


def main():
    conn = sqlite3.connect(DB_FILE_PATH)
    df = pd.read_sql(sql="SELECT * FROM features", con=conn)

    y = df["behavior_name"].to_numpy()
    le = LabelEncoder()
    le.fit(y)

    # We only use dtypes of float64 in training for columns.
    x_train, x_test, y_train, y_test = train_test_split(
        df.loc[:, df.dtypes == np.float64].to_numpy(),
        le.transform(y),
        random_state=1,
    )

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


if __name__ == "__main__":
    main()
