"""Five baseline experiments, Bayesian search, and model export."""
import csv
import json
from pathlib import Path
import sys
from time import perf_counter

import joblib
import numpy as np
import optuna
from sklearn.ensemble import HistGradientBoostingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, precision_recall_fscore_support
from sklearn.model_selection import GroupKFold
from sklearn.naive_bayes import GaussianNB
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier

from .core import FEATURES, DECODER, probabilities

SEED = 352
BASE = {
    "Logistic": {"C": 1.0},
    "Gaussian NB": {"var_smoothing": 1e-8},
    "Decision tree": {"max_depth": 9, "min_samples_leaf": 50},
    "Random forest": {"n_estimators": 48, "max_depth": 13, "min_samples_leaf": 25},
    "Histogram boosting": {"max_iter": 100, "max_leaf_nodes": 23, "learning_rate": .10,
                           "min_samples_leaf": 40, "l2_regularization": 1.0},
}


def classifier(name, config):
    if name == "Logistic":
        return make_pipeline(StandardScaler(), LogisticRegression(max_iter=250, **config))
    if name == "Gaussian NB":
        return make_pipeline(StandardScaler(), GaussianNB(**config))
    if name == "Decision tree":
        return DecisionTreeClassifier(random_state=SEED, **config)
    if name == "Random forest":
        return RandomForestClassifier(random_state=SEED, n_jobs=4, **config)
    return HistGradientBoostingClassifier(random_state=SEED, early_stopping=False, **config)


def load_partition(cache, partition):
    return [(p.stem.split("-")[1], dict(np.load(p)))
            for p in sorted(Path(cache).glob(f"{partition}-*.npz"))]


def fit(name, config, trips):
    x = np.concatenate([t["features"].reshape(-1, len(FEATURES)) for _, t in trips])
    y = np.concatenate([(t["ids"] == t["truth"][:, None]).ravel() for _, t in trips])
    if len(y) > 180000:
        idx = np.random.default_rng(SEED).choice(len(y), 180000, replace=False)
        x, y = x[idx], y[idx]
    return classifier(name, config).fit(x, y)


def observation_stats(truth, predicted):
    precision, recall, f1, _ = precision_recall_fscore_support(
        truth, predicted, average="macro", zero_division=0)
    return dict(top1=float(np.mean(truth == predicted)), macro_f1=f1,
                macro_precision=precision, macro_recall=recall)


def evaluate(model, trips, networks=None):
    scores, confusion = [], np.zeros((2, 2), dtype=int)
    for label, t in trips:
        start = perf_counter()
        p = probabilities(model, t["features"])
        duration = (perf_counter() - start) * 1000
        ids, truth = t["ids"], t["truth"]
        matches = ids == truth[:, None]
        pred = ids[np.arange(len(ids)), p.argmax(axis=1)]
        covered = matches.any(axis=1)
        loss = -np.log(np.clip((p * matches).sum(axis=1)[covered], 1e-12, 1))
        pick = np.zeros_like(matches)
        pick[np.arange(len(ids)), p.argmax(axis=1)] = True
        confusion += confusion_matrix(matches.ravel(), pick.ravel(), labels=[False, True])
        scores.append(dict(**observation_stats(truth, pred), log_loss=float(loss.mean()),
                           miss_rate=float(1 - covered.mean()), inference_ms=duration))
        if networks is not None:
            arcs = networks[label]
            scores[-1]["continuity"] = float(np.mean((pred[1:] == pred[:-1]) |
                                                    (arcs[pred[:-1], 1] == arcs[pred[1:], 0])))
    return {k: float(np.mean([row[k] for row in scores])) for k in scores[0]}, confusion.tolist()


def search_params(trial, name):
    if name == "Logistic":
        return {"C": trial.suggest_float("C", .001, 100, log=True)}
    if name == "Gaussian NB":
        return {"var_smoothing": trial.suggest_float("var_smoothing", 1e-11, .2, log=True)}
    if name == "Decision tree":
        return {"max_depth": trial.suggest_int("max_depth", 5, 24),
                "min_samples_leaf": trial.suggest_int("min_samples_leaf", 8, 180, log=True)}
    if name == "Random forest":
        return {"n_estimators": trial.suggest_int("n_estimators", 35, 90),
                "max_depth": trial.suggest_int("max_depth", 8, 23),
                "min_samples_leaf": trial.suggest_int("min_samples_leaf", 6, 100, log=True)}
    return {"max_iter": trial.suggest_int("max_iter", 65, 185),
            "max_leaf_nodes": trial.suggest_int("max_leaf_nodes", 12, 55),
            "learning_rate": trial.suggest_float("learning_rate", .04, .24, log=True),
            "min_samples_leaf": trial.suggest_int("min_samples_leaf", 16, 120, log=True),
            "l2_regularization": trial.suggest_float("l2_regularization", .05, 10, log=True)}


def experiment(cache, root):
    train, test = (load_partition(cache, p) for p in ("train", "student_test"))
    groups = [label for label, _ in train]
    if len(train) != 80 or len(test) != 10 or set(groups) & {label for label, _ in test}:
        raise ValueError("Expected 80 training and 10 disjoint student-test trips")
    folds = list(GroupKFold(n_splits=3).split(train, groups=groups))
    networks = {label: np.loadtxt(Path(root) / "student_test" / label / (label + ".arcs"),
                                 dtype=int, ndmin=2) for label, _ in test}

    def cv(name, config):
        return [evaluate(fit(name, config, [train[i] for i in a]),
                         [train[i] for i in b])[0]["macro_f1"] for a, b in folds]

    def record(name, config, fold_scores):
        start = perf_counter()
        model = fit(name, config, train)
        seconds = perf_counter() - start
        metrics, matrix = evaluate(model, test, networks)
        training_metrics, _ = evaluate(model, train)
        row = dict(model=name, config=config, cv=list(fold_scores),
                   cv_macro_f1=float(np.mean(fold_scores)), train_macro_f1=training_metrics["macro_f1"],
                   fit_seconds=seconds, confusion=matrix, **metrics)
        print(json.dumps(row), flush=True)
        return model, row

    results = []
    for name, config in BASE.items():
        _, row = record(name, config, cv(name, config))
        results.append(row)
    best = max(results, key=lambda row: row["cv_macro_f1"])
    name = best["model"]
    study = optuna.create_study(direction="maximize", sampler=optuna.samplers.TPESampler(seed=SEED, n_startup_trials=3))
    study.enqueue_trial(BASE[name])

    def objective(trial):
        scores = cv(name, search_params(trial, name))
        trial.set_user_attr("fold_macro_f1", scores)
        return float(np.mean(scores))

    start = perf_counter()
    study.optimize(objective, n_trials=9)
    seconds = perf_counter() - start
    model, tuned = record(name, study.best_params, study.best_trial.user_attrs["fold_macro_f1"])
    joblib.dump({"model": model, "features": FEATURES, "decoder": DECODER,
                 "name": name}, "artifacts/model.joblib", compress=3)
    with Path("results/search.csv").open("w", newline="") as file:
        writer = csv.writer(file, lineterminator="\n")
        writer.writerow(["trial", "macro_f1", "seconds", "parameters", "fold_macro_f1"])
        for trial in study.trials:
            writer.writerow([trial.number, trial.value, trial.duration.total_seconds(),
                             json.dumps(trial.params), json.dumps(trial.user_attrs["fold_macro_f1"])])
    Path("results/models.json").write_text(json.dumps(
        dict(baselines=results, tuned=tuned, search_seconds=seconds,
             seed=SEED, folds=[[groups[i] for i in b] for _, b in folds],
             search_space={key: str(value) for key, value in study.best_trial.distributions.items()}),
        indent=2))


if __name__ == "__main__":
    experiment(*sys.argv[1:])
