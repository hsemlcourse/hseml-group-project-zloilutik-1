from pathlib import Path

import pandas as pd
from sklearn.model_selection import train_test_split


RANDOM_SEED = 42


def load_dataset(path: str | Path) -> pd.DataFrame:
    return pd.read_csv(path)


def clean_dataset(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    print("Initial shape:", df.shape)

    print("\nMissing values:")
    print(df.isnull().sum())

    duplicates = df.duplicated().sum()
    print("\nDuplicates:", duplicates)

    df = df.drop_duplicates()

    print("Shape after duplicate removal:", df.shape)

    return df


def encode_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    categorical_columns = df.select_dtypes(include=["object", "string"]).columns.tolist()

    if "winner" in categorical_columns:
        categorical_columns.remove("winner")

    df = pd.get_dummies(
        df,
        columns=categorical_columns,
        drop_first=False
    )

    return df


def split_dataset(df: pd.DataFrame):
    df = df.copy()

    X = df.drop(columns=["target", "winner"])
    y = df["target"]

    X_train, X_temp, y_train, y_temp = train_test_split(
        X,
        y,
        test_size=0.30,
        random_state=RANDOM_SEED,
        stratify=y
    )

    X_val, X_test, y_val, y_test = train_test_split(
        X_temp,
        y_temp,
        test_size=0.50,
        random_state=RANDOM_SEED,
        stratify=y_temp
    )

    print("\nTrain shape:", X_train.shape)
    print("Validation shape:", X_val.shape)
    print("Test shape:", X_test.shape)

    print("\nTarget distribution:")
    print("Train:")
    print(y_train.value_counts(normalize=True))
    print("Validation:")
    print(y_val.value_counts(normalize=True))
    print("Test:")
    print(y_test.value_counts(normalize=True))

    return X_train, X_val, X_test, y_train, y_val, y_test


def preprocess_dataset(path: str | Path):
    df = load_dataset(path)
    df = clean_dataset(df)
    df = encode_features(df)

    return split_dataset(df)


if __name__ == "__main__":
    dataset_path = Path("data/processed/battles_dataset.csv")
    preprocess_dataset(dataset_path)