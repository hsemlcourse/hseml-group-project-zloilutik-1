from pathlib import Path

import pandas as pd
from sklearn.dummy import DummyClassifier
from sklearn.ensemble import (
    AdaBoostClassifier,
    ExtraTreesClassifier,
    GradientBoostingClassifier,
    RandomForestClassifier,
)
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score
from sklearn.model_selection import GridSearchCV
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from src.preprocessing import preprocess_dataset

RANDOM_SEED = 42


def evaluate_model(model, X_train, X_eval, y_train, y_eval):
    model.fit(X_train, y_train)

    y_pred = model.predict(X_eval)

    if hasattr(model, "predict_proba"):
        y_proba = model.predict_proba(X_eval)[:, 1]
        roc_auc = roc_auc_score(y_eval, y_proba)
    else:
        roc_auc = None

    return {
        "accuracy": accuracy_score(y_eval, y_pred),
        "f1": f1_score(y_eval, y_pred),
        "roc_auc": roc_auc,
    }


def tune_model(model, param_grid, X_train, y_train):
    grid = GridSearchCV(
        estimator=model,
        param_grid=param_grid,
        scoring="f1",
        cv=3,
        n_jobs=-1,
    )

    grid.fit(X_train, y_train)

    return grid.best_estimator_, grid.best_params_, grid.best_score_


def get_best_model_name(results_df: pd.DataFrame) -> str:
    best_row = results_df.sort_values(
        by="f1",
        ascending=False,
    ).iloc[0]

    return best_row["model"]


def run_experiments():
    dataset_path = Path("data/processed/battles_dataset.csv")

    X_train, X_val, X_test, y_train, y_val, y_test = preprocess_dataset(
        dataset_path
    )

    models = {
        "DummyClassifier": DummyClassifier(strategy="most_frequent"),
        "LogisticRegression": Pipeline([
            ("scaler", StandardScaler()),
            ("model", LogisticRegression(
                max_iter=1000,
                random_state=RANDOM_SEED
            )),
        ]),
        "KNN": Pipeline([
            ("scaler", StandardScaler()),
            ("model", KNeighborsClassifier(n_neighbors=5)),
        ]),
        "RandomForest": RandomForestClassifier(
            n_estimators=200,
            random_state=RANDOM_SEED,
        ),
        "GradientBoosting": GradientBoostingClassifier(
            random_state=RANDOM_SEED,
        ),
        "ExtraTrees": ExtraTreesClassifier(
            n_estimators=200,
            random_state=RANDOM_SEED,
        ),
        "AdaBoost": AdaBoostClassifier(
            n_estimators=100,
            random_state=RANDOM_SEED,
        ),
    }

    tuning_experiments = {
        "RandomForest_tuned": (
            RandomForestClassifier(random_state=RANDOM_SEED),
            {
                "n_estimators": [100, 200],
                "max_depth": [None, 5, 10],
                "min_samples_split": [2, 5],
            },
        ),
        "ExtraTrees_tuned": (
            ExtraTreesClassifier(random_state=RANDOM_SEED),
            {
                "n_estimators": [100, 200],
                "max_depth": [None, 5, 10],
                "min_samples_split": [2, 5],
            },
        ),
        "LogisticRegression_tuned": (
            Pipeline([
                ("scaler", StandardScaler()),
                ("model", LogisticRegression(
                    max_iter=1000,
                    random_state=RANDOM_SEED
                )),
            ]),
            {
                "model__C": [0.1, 1.0, 10.0],
            },
        ),
    }

    results = []
    trained_models = {}

    for model_name, model in models.items():
        metrics = evaluate_model(
            model,
            X_train,
            X_val,
            y_train,
            y_val,
        )

        trained_models[model_name] = model

        results.append({
            "model": model_name,
            "best_params": None,
            "best_cv_f1": None,
            **metrics,
        })

    for model_name, (model, param_grid) in tuning_experiments.items():
        best_model, best_params, best_cv_score = tune_model(
            model,
            param_grid,
            X_train,
            y_train,
        )

        metrics = evaluate_model(
            best_model,
            X_train,
            X_val,
            y_train,
            y_val,
        )

        trained_models[model_name] = best_model

        results.append({
            "model": model_name,
            "best_params": best_params,
            "best_cv_f1": best_cv_score,
            **metrics,
        })

    results_df = pd.DataFrame(results)
    results_df = results_df.sort_values(
        by="f1",
        ascending=False,
    )

    print("\n=== VALIDATION RESULTS ===")
    print(results_df)

    best_model_name = get_best_model_name(results_df)
    best_model = trained_models[best_model_name]

    print("\nBest validation model:", best_model_name)

    test_metrics = evaluate_model(
        best_model,
        X_train,
        X_test,
        y_train,
        y_test,
    )

    test_results = {
        "model": best_model_name,
        **test_metrics,
    }

    print("\n=== TEST RESULTS ===")
    print(test_results)

    output_path = Path("data/processed/model_results.csv")
    results_df.to_csv(output_path, index=False)

    test_output_path = Path("data/processed/test_results.csv")
    pd.DataFrame([test_results]).to_csv(test_output_path, index=False)

    print("\nValidation results saved to:", output_path)
    print("Test results saved to:", test_output_path)


if __name__ == "__main__":
    run_experiments()