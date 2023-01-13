from database_metrics import generate_sql_database_distribution
import os


def main():
    # Get the downsampled databases.
    for file in os.listdir(os.getcwd()):
        if file.startswith("downsampled") and file.endswith(".db"):
            print(file)
            print(generate_sql_database_distribution(file))


if __name__ == "__main__":
    main()
