from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


DATASET_PATH = Path("data/processed/battles_dataset.csv")
OUTPUT_DIR = Path("report/images")


def load_dataset() -> pd.DataFrame:
    return pd.read_csv(DATASET_PATH)


def save_target_distribution(df: pd.DataFrame):
    counts = df["winner"].value_counts()

    plt.figure()
    counts.plot(kind="bar")
    plt.title("Battle winner distribution")
    plt.xlabel("Winner")
    plt.ylabel("Count")
    plt.tight_layout()

    plt.savefig(OUTPUT_DIR / "winner_distribution.png")
    plt.close()


def save_rounds_distribution(df: pd.DataFrame):
    plt.figure()
    df["rounds"].hist(bins=30)
    plt.title("Rounds distribution")
    plt.xlabel("Rounds")
    plt.ylabel("Count")
    plt.tight_layout()

    plt.savefig(OUTPUT_DIR / "rounds_distribution.png")
    plt.close()


def save_army_health_comparison(df: pd.DataFrame):
    plt.figure()
    plt.scatter(
        df["army_a_total_health"],
        df["army_b_total_health"],
        alpha=0.3
    )
    plt.title("Army A vs Army B total health")
    plt.xlabel("Army A total health")
    plt.ylabel("Army B total health")
    plt.tight_layout()

    plt.savefig(OUTPUT_DIR / "army_health_comparison.png")
    plt.close()


def save_attack_difference_by_target(df: pd.DataFrame):
    df = df.copy()
    df["attack_diff"] = (
        df["army_a_total_attack"] - df["army_b_total_attack"]
    )

    plt.figure()
    df.boxplot(column="attack_diff", by="target")
    plt.title("Attack difference by target")
    plt.suptitle("")
    plt.xlabel("Target: 1 = Army A wins, 0 = Army B wins")
    plt.ylabel("Army A attack - Army B attack")
    plt.tight_layout()

    plt.savefig(OUTPUT_DIR / "attack_difference_by_target.png")
    plt.close()


def save_correlation_heatmap(df: pd.DataFrame):
    numeric_df = df.select_dtypes(include=["number"])

    corr = numeric_df.corr()

    plt.figure(figsize=(12, 10))
    plt.imshow(corr, aspect="auto")
    plt.colorbar()
    plt.title("Feature correlation heatmap")
    plt.xticks(range(len(corr.columns)), corr.columns, rotation=90, fontsize=6)
    plt.yticks(range(len(corr.columns)), corr.columns, fontsize=6)
    plt.tight_layout()

    plt.savefig(OUTPUT_DIR / "correlation_heatmap.png")
    plt.close()


def run_eda():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    df = load_dataset()

    print("Dataset shape:", df.shape)
    print("\nTarget distribution:")
    print(df["target"].value_counts(normalize=True))

    save_target_distribution(df)
    save_rounds_distribution(df)
    save_army_health_comparison(df)
    save_attack_difference_by_target(df)
    save_correlation_heatmap(df)

    print("\nEDA plots saved to:", OUTPUT_DIR)


if __name__ == "__main__":
    run_eda()