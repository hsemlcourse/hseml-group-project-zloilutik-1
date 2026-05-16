from pathlib import Path

import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

from src.preprocessing import preprocess_dataset

DATASET_PATH = Path("data/processed/battles_dataset.csv")
OUTPUT_DIR = Path("report/images")


def run_pca():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    X_train, X_val, X_test, y_train, y_val, y_test = preprocess_dataset(
        DATASET_PATH
    )

    scaler = StandardScaler()

    X_scaled = scaler.fit_transform(X_train)

    pca = PCA(n_components=2, random_state=42)

    X_pca = pca.fit_transform(X_scaled)

    explained_variance = pca.explained_variance_ratio_

    print("Explained variance ratio:")
    print(explained_variance)

    plt.figure(figsize=(8, 6))

    scatter = plt.scatter(
        X_pca[:, 0],
        X_pca[:, 1],
        c=y_train,
        alpha=0.5
    )

    plt.title("PCA projection of battle dataset")
    plt.xlabel(
        f"PC1 ({explained_variance[0]:.2%} variance)"
    )
    plt.ylabel(
        f"PC2 ({explained_variance[1]:.2%} variance)"
    )

    plt.colorbar(scatter, label="Target")

    plt.tight_layout()

    output_path = OUTPUT_DIR / "pca_projection.png"

    plt.savefig(output_path)

    plt.close()

    print("\nPCA plot saved to:", output_path)


if __name__ == "__main__":
    run_pca()