"""Render the submission PDF from recorded runs and browser evidence."""
import csv
import json
from pathlib import Path
import sys
from xml.sax.saxutils import escape

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
import numpy as np
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import Image, PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from .core import Trip, load
from .data import prefixes

R = Path("results")
F = R / "figures"
INK = "#15332b"
MUTED = "#4d655d"
GREEN = "#227a5a"
BLUE = "#4676ae"
VIOLET = "#8160a5"
MODELS = {
    "Logistic": ("Linear probability model", "Binary log loss with L2 penalty",
                 "Its signed coefficients provide a compact geometry baseline. Linear log odds cannot directly express interactions between heading, projection fraction and speed."),
    "Gaussian NB": ("Generative probabilistic model", "Class-conditional likelihood and Bayes rule",
                    "It is inexpensive to fit and provides an independence baseline. Current, previous and next distances are correlated, so treating them as independent can distort probability estimates."),
    "Decision tree": ("Single decision tree", "Greedy Gini impurity reduction",
                      "Threshold splits model such effects as bearing mattering more while moving. Leaf probabilities are coarse and a single tree is sensitive to split boundaries."),
    "Random forest": ("Bagged tree ensemble", "Per-tree Gini impurity reduction, aggregated probabilities",
                      "Averaging trees captures interactions while reducing split variance. More trees carry extra inference and storage cost."),
    "Histogram boosting": ("Gradient-boosted tree ensemble", "Binary log loss",
                           "Shallow additive trees can capture nonlinear feature interactions and refine ambiguous rankings. Capacity depends on iteration count and leaf size, and fit-time cost rises with both."),
    "KNN": ("Instance-based classifier", "Distance-weighted voting with no fitted training loss",
            "Distance-weighted Euclidean neighbours vote in standardised feature space. Prediction requires a neighbour search and can depend on coverage of rare road situations in the sample."),
    "MLP": ("Feed-forward neural classifier", "Binary log loss with L2 regularisation",
            "Adam optimises two hidden layers, initially 64 and 32 units, to represent interactions between movement and road geometry. Early stopping uses internal candidate-row accuracy, which can include rows from the same trips in both internal subsets."),
}


def read_csv(name):
    with (R / name).open() as file:
        return list(csv.DictReader(file))


def track_quality(root, inventory):
    quality, samples = {}, {}
    for partition in ("train", "student_test"):
        rows = [r for r in inventory if r["partition"] == partition]
        gaps, missing = [], 0
        for prefix in prefixes(root, partition):
            raw = load(prefix, ".track", 3)
            missing += int((~np.isfinite(raw)).sum())
            valid = (np.isfinite(raw).all(axis=1) & (abs(raw[:, 0]) <= 180)
                     & (abs(raw[:, 1]) <= 90))
            gaps.append(np.diff(np.sort(raw[valid, 2])))
        samples[partition] = np.concatenate(gaps)
        quality[partition] = [partition, sum(int(r["invalid"]) for r in rows), missing,
                              sum(int(r["duplicates"]) for r in rows),
                              sum(int(r["reversals"]) for r in rows),
                              int((samples[partition] > 10).sum())]
    return quality, samples


def fit_diagnostic(model, models):
    by_name = {row["model"]: row for row in models}
    name = model["model"]
    comparator, takeaway = {
        "Logistic": ("Decision tree", "The tree's higher CV score is consistent with the linear model missing useful feature interactions."),
        "Gaussian NB": ("Logistic", "The two simple models have similar CV F1, despite their different probability assumptions. Covered log loss checks how well the independence model ranks the correct arc."),
        "Decision tree": ("Random forest", "The forest's advantage measures the gain from using a larger ensemble under the same fold split."),
        "Random forest": ("Histogram boosting", "The two ensemble scores are close relative to their fold spreads, so their ranking is sensitive to trip composition."),
        "Histogram boosting": ("Decision tree", "The CV difference from a single tree measures the gain of additive trees. The small train-to-CV gap limits evidence of a large generalisation penalty."),
        "KNN": ("Decision tree", "The comparison includes a smaller KNN fitting sample. Its CV score therefore reflects both the neighbour rule and available sample coverage."),
        "MLP": ("Histogram boosting", "The internal accuracy curve guides early stopping; the trip-held-out F1 gives the more relevant generalisation estimate."),
    }[name]
    delta = model["cv_macro_f1"] - by_name[comparator]["cv_macro_f1"]
    gap = model["train_macro_f1"] - model["cv_macro_f1"]
    low, high = min(model["cv"]), max(model["cv"])
    return (f"Training minus CV F1 was {gap:+.3f}. The fold range was {low:.3f} to {high:.3f}. "
            f"The CV difference versus {comparator} was {delta:+.3f}. {takeaway}")


def plots(root, models, inventory, comparison, samples):
    F.mkdir(exist_ok=True)
    plt.rcParams.update({"font.size": 10, "axes.spines.top": False,
                         "axes.spines.right": False, "figure.dpi": 145})
    for partition, color in [("train", GREEN), ("student_test", BLUE)]:
        rows = [r for r in inventory if r["partition"] == partition]
        plt.scatter([int(r["observations"]) for r in rows], [int(r["arcs"]) for r in rows],
                    s=22, alpha=.7, c=color, label=partition)
    plt.xscale("log")
    plt.yscale("log")
    plt.xlabel("GPS observations per trip (log scale)")
    plt.ylabel("Road arcs per trip (log scale)")
    plt.legend(frameon=False)
    plt.tight_layout()
    plt.savefig(F / "inventory.png")
    plt.close()

    fig, (components, network) = plt.subplots(1, 2, figsize=(9, 3.2))
    fig_gap, gap_ax = plt.subplots(figsize=(9, 2.9))
    component_max = max(int(row["weak_components"]) for row in inventory)
    gap_max = max(float(values.max()) for values in samples.values())
    bins = np.geomspace(min(values[values > 0].min() for values in samples.values()), gap_max, 28)
    for partition, color in (("train", GREEN), ("student_test", BLUE)):
        rows = [r for r in inventory if r["partition"] == partition]
        components.hist([int(row["weak_components"]) for row in rows],
                        bins=np.geomspace(1, component_max + 1, 19), histtype="step",
                        color=color, label=partition)
        network.scatter([int(row["nodes"]) for row in rows], [int(row["arcs"]) for row in rows],
                        s=17, alpha=.65, color=color, label=partition)
        gap_ax.hist(samples[partition][samples[partition] > 0], bins=bins,
                    histtype="step", color=color, label=partition)
    components.set(xscale="log", xlabel="Weak components per trip", ylabel="Trips")
    network.set(xscale="log", yscale="log", xlabel="Nodes per trip", ylabel="Directed arcs per trip")
    gap_ax.set(xscale="log", yscale="log", xlabel="Positive sampling gap (seconds)", ylabel="Intervals")
    for ax in (components, network, gap_ax):
        ax.legend(frameon=False)
    for fig, name in ((fig, "connectivity.png"), (fig_gap, "sampling_gaps.png")):
        fig.tight_layout()
        fig.savefig(F / name)
        plt.close(fig)

    fig, (loss, accuracy) = plt.subplots(1, 2, figsize=(9, 3))
    history = read_csv("mlp_history.csv")
    for variant in dict.fromkeys(row["variant"] for row in history):
        rows = [row for row in history if row["variant"] == variant]
        epochs = [int(row["epoch"]) for row in rows]
        loss.plot(epochs, [float(row["training_loss"]) for row in rows], label=variant)
        accuracy.plot(epochs, [float(row["validation_accuracy"]) for row in rows], label=variant)
    for ax, label in ((loss, "Training loss"), (accuracy, "Validation accuracy")):
        ax.set(xlabel="Epoch", ylabel=label)
        ax.legend(frameon=False)
    fig.tight_layout()
    fig.savefig(F / "mlp_history.png")
    plt.close(fig)

    trip = Trip(next(p for p in prefixes(root, "student_test") if p.name == "00000052"))
    fig, ax = plt.subplots(figsize=(8, 3.8))
    geometry = trip.nodes[trip.arcs]
    low, high = trip.track[:, :2].min(axis=0), trip.track[:, :2].max(axis=0)
    keep = ((geometry >= low - .003) & (geometry <= high + .003)).all(axis=(1, 2))
    ax.add_collection(LineCollection(geometry[keep], colors="#9faba7", linewidths=.6))
    ax.scatter(*trip.track[:, :2].T, c=np.arange(len(trip.track)), cmap="viridis", s=9, zorder=3)
    ax.set(xlabel="Longitude", ylabel="Latitude", xlim=(low[0]-.002, high[0]+.002),
           ylim=(low[1]-.002, high[1]+.002))
    ax.set_aspect(1 / np.cos(np.deg2rad(trip.track[:, 1].mean())))
    fig.tight_layout()
    fig.savefig(F / "trajectory.png")
    plt.close(fig)

    labels = [m["model"].replace("Histogram ", "Hist.\n").replace("Random ", "Random\n") for m in models]
    fig, axes = plt.subplots(1, 3, figsize=(11.3, 3.2))
    x = np.arange(len(models))
    axes[0].bar(x, [m["cv_macro_f1"] for m in models], color=GREEN)
    for i, model in enumerate(models):
        axes[0].scatter([i] * len(model["cv"]), model["cv"], color=INK, s=12)
    axes[0].set_title("Grouped CV macro F1")
    for offset, key, name, color in [(-.18, "top1", "Top-1", GREEN), (.18, "macro_f1", "Macro F1", BLUE)]:
        axes[1].bar(x + offset, [m[key] for m in models], .34, label=name, color=color)
    axes[1].legend(frameon=False, fontsize=8)
    axes[1].set_title("Student-test ranking")
    axes[2].bar(x, [m["log_loss"] for m in models], color=VIOLET)
    axes[2].set_title("Student-test covered log loss")
    for ax in axes:
        ax.set_xticks(x, labels, fontsize=7)
        ax.set_ylim(bottom=0)
    fig.tight_layout()
    fig.savefig(F / "models.png")
    plt.close(fig)

    fig, axes = plt.subplots(1, len(models), figsize=(14, 2.6))
    for ax, model in zip(axes, models):
        matrix = np.asarray(model["confusion"])
        ax.imshow(matrix, cmap="Greens")
        for (i, j), count in np.ndenumerate(matrix):
            ax.text(j, i, f"{count:,}", fontsize=8, ha="center", va="center",
                    color="white" if count > matrix.max() * .6 else INK)
        ax.set_xticks([0, 1], ["Other", "Picked"], fontsize=7)
        ax.set_yticks([0, 1], ["Other", "True"], fontsize=7)
        ax.set_title(model["model"], fontsize=8)
    fig.tight_layout()
    fig.savefig(F / "confusion.png")
    plt.close(fig)

    trials = read_csv("search.csv")
    x = [int(t["trial"]) + 1 for t in trials]
    y = [float(t["macro_f1"]) for t in trials]
    plt.figure(figsize=(7, 2.6))
    plt.plot(x, np.maximum.accumulate(y), color=GREEN, label="Best so far")
    plt.scatter(x, y, color=BLUE, label="Trial")
    plt.xlabel("Trial")
    plt.ylabel("CV macro F1")
    plt.legend(frameon=False)
    plt.tight_layout()
    plt.savefig(F / "search.png")
    plt.close()

    by_method = {method: [r for r in comparison if r["method"] == method]
                 for method in ("Classifier", "Viterbi")}
    plt.figure(figsize=(8, 3.2))
    x = np.arange(len(by_method["Classifier"]))
    for offset, (method, rows) in zip((-.17, .17), by_method.items()):
        plt.bar(x + offset, [float(r["top1"]) for r in rows], .34, label=method,
                color=BLUE if method == "Classifier" else GREEN)
    plt.xticks(x, [r["trip"][-2:] for r in by_method["Classifier"]])
    plt.xlabel("Student-test trip ID (last two digits)")
    plt.ylabel("Pointwise top-1 accuracy")
    plt.legend(frameon=False)
    plt.tight_layout()
    plt.savefig(F / "route_accuracy.png")
    plt.close()


def report(root, output="results/PathSnap-Technical-Report.pdf"):
    inventory = read_csv("inventory.csv")
    logging = json.loads((R / "models.json").read_text())
    models, tuned = logging["baselines"], logging["tuned"]
    comparison = read_csv("routes.csv")
    settings = json.loads((R / "decoder_config.json").read_text())
    team = json.loads(Path("report/team.json").read_text())
    authors = ", ".join(team["members"])
    quality, samples = track_quality(root, inventory)
    with (R / "data_quality.csv").open("w", newline="") as file:
        writer = csv.writer(file, lineterminator="\n")
        writer.writerow(["partition", "invalid_rows", "non_finite_cells", "duplicate_timestamps",
                         "timestamp_reversals", "gaps_over_10_seconds"])
        writer.writerows(quality.values())
    plots(root, models, inventory, comparison, samples)
    style = getSampleStyleSheet()
    style["Normal"].fontName = "Helvetica"
    style["Normal"].textColor = colors.HexColor(INK)
    style["Normal"].fontSize = 10
    style["Normal"].leading = 13
    style["Heading1"].fontSize = 22
    style["Heading1"].leading = 26
    style["Heading1"].textColor = colors.HexColor(INK)
    style["Heading2"].textColor = colors.HexColor(GREEN)
    cap = ParagraphStyle("caption", parent=style["Normal"], fontSize=8, leading=11,
                         textColor=colors.HexColor(MUTED))
    story = []

    def para(text):
        story.extend([Paragraph(escape(text), style["Normal"]), Spacer(1, 6)])

    def heading(text, level=1):
        story.append(Paragraph(escape(text), style[f"Heading{level}"]))

    def picture(name, caption, width=166*mm, maximum=95*mm):
        img = Image(str(F / name))
        scale = min(width / img.imageWidth, maximum / img.imageHeight)
        img.drawWidth, img.drawHeight = img.imageWidth * scale, img.imageHeight * scale
        story.extend([img, Paragraph(escape(caption), cap), Spacer(1, 9)])

    def table(headers, data, widths):
        t = Table([headers] + data, colWidths=[x * mm for x in widths], repeatRows=1)
        t.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor(INK)),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.HexColor("#edf5f1"), colors.white]),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 8),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ("TOPPADDING", (0, 0), (-1, -1), 5),
            ("LEFTPADDING", (0, 0), (-1, -1), 6)]))
        story.extend([t, Spacer(1, 10)])

    def page():
        story.append(PageBreak())

    heading("PathSnap technical report")
    para(f"{team['name']} | {authors}")
    para("Directed road matching with learned candidate probabilities and sequential decoding. UE24CS352A Machine Learning hackathon.")
    heading("2.2 Dataset and exploratory analysis", 2)
    para("The supplied development package contains 80 training trips and ten student-test trips. Every trip has a GPS track (longitude, latitude, seconds), node coordinates, directed arcs indexed by row and an ordered reference route of arc IDs. The reserved evaluator partition was absent and excluded from development.")
    counts = []
    for p in ("train", "student_test"):
        data = [r for r in inventory if r["partition"] == p]
        obs = sum(int(r["observations"]) for r in data)
        gaps = obs - len(data)
        counts.append([p, len(data), f"{obs:,}", sum(int(r["invalid"]) for r in data),
                       f"{sum(int(r['one_second']) for r in data)/gaps:.1%}",
                       f"{max(float(r['maximum_gap']) for r in data):g} s",
                       max(int(r["weak_components"]) for r in data)])
    table(["Partition", "Trips", "GPS rows", "Invalid", "1 s gaps", "Max gap", "Max components"],
          counts, [31, 16, 24, 20, 22, 23, 33])
    reversals = sum(int(r["reversals"]) for r in inventory)
    duplicates = sum(int(r["duplicates"]) for r in inventory)
    isolated = sum(int(r["isolated"]) for r in inventory)
    breaks = sum(int(r["reference_breaks"]) for r in inventory)
    worst = max(inventory, key=lambda r: float(r["maximum_gap"]))
    para(f"Across both development partitions, the inventory recorded {reversals:,} timestamp reversals, {duplicates:,} zero-second intervals, {isolated:,} isolated nodes summed over trip graphs and {breaks:,} non-adjacent steps in supplied routes. The largest gap was {float(worst['maximum_gap']):,.0f} seconds in {worst['partition']} trip {worst['trip']}. The decoder resets beyond 90 seconds. The {breaks:,} non-adjacent reference steps remain in the supplied route for alignment and are counted as reference discontinuities. The inventory includes per-file sizes and coordinate bounds.")
    para("Preprocessing drops non-finite or out-of-range GPS readings, preserves duplicate timestamps, stable-sorts valid readings and validates arc endpoints. A trip-centred equirectangular projection scales longitude by the cosine of the median latitude, giving locally meaningful metric distances for the observed extents.")
    picture("inventory.png", "Figure 1. Trip size and road-network size in both permitted development partitions.", maximum=81*mm)
    page()

    heading("2.2 Data quality and connectivity")
    table(["Partition", "Invalid rows", "Non-finite cells", "0 s gaps", "Reversals", "Gaps >10 s"],
          list(quality.values()), [30, 26, 31, 25, 25, 29])
    picture("connectivity.png", "Weak components and graph sizes, by development partition.", maximum=63*mm)
    picture("sampling_gaps.png", "Positive intervals after sorting valid timestamps within trips. Zero intervals are counted in the table.", maximum=60*mm)
    page()

    heading("2.2 Geometry, features and labels")
    picture("trajectory.png", "Figure 2. Student-test trip 00000052. The colour ramp marks observation order over its nearby road network.", maximum=101*mm)
    para("A spatial tree indexes arc samples spaced at most 20 metres apart. The pipeline retrieves nearby samples, deduplicates owner arcs and ranks these by exact point-to-segment distance to retain up to eight arcs. When sample retrieval yields fewer than eight distinct arcs, it evaluates all arcs. This approximation makes the candidate miss rate a necessary diagnostic.")
    para("Nine features describe distance to the arc, direction agreement with local GPS motion, fractional position on the arc, arc length, local speed, preceding time gap, midpoint distance, and point-to-segment distances at the previous and next observations. Distances convey proximity, bearing helps distinguish opposite directions, and neighbouring points carry context when GPS jitter produces locally ambiguous matches. Candidate features do not use trip IDs, arc IDs or reference labels.")
    para("The provided route is a sequence of arc IDs. A monotone dynamic program aligns observations to successive route positions using projected distance plus 0.35 times the mismatch between projected route progress and observed displacement. Each aligned arc becomes the observation's pseudo-label. This can be ambiguous near intersections, overlapping roads, discontinuous references and sparse samples.")
    para(f"On student-test trips the mean candidate miss rate was {tuned['miss_rate']:.2%}. Missing labels remain wrong in Top-1 and contribute to the macro metrics. Covered log loss uses the normalised probability of the correct shortlist member only. Labels are evaluated per trip before aggregation because arc IDs are local to a trip.")
    para("Continuity counts adjacent inferred observations that stay on the same arc or share the directed end-to-start node. Inference timing covers classifier scoring of cached features, averaged across test trips. The classifier comparison excludes feature-generation and Viterbi time.")
    page()

    heading("3.1 Model comparison")
    para("All seven baselines used identical features and the same three GroupKFold splits of the 80 training trips. Grouping is by trip ID. Fits use up to 180,000 deterministically sampled candidate rows. KNN uses at most 12,000 to bound prediction cost. The selected model maximises mean grouped-CV observation-level macro F1, which gives infrequent arcs a voice in model selection.")
    table(["Model", "CV F1", "Test top-1", "Test F1", "Continuity", "Log loss", "Infer ms"],
          [[m["model"], f"{m['cv_macro_f1']:.3f}", f"{m['top1']:.3f}", f"{m['macro_f1']:.3f}",
            f"{m['continuity']:.3f}", f"{m['log_loss']:.3f}", f"{m['inference_ms']:.1f}"] for m in models],
          [43, 19, 23, 19, 23, 20, 22])
    picture("models.png", "Figure 3. Baseline model comparison. Dots in the first panel are actual fold scores.", maximum=43*mm)
    page()
    heading("3.1 Student-test candidate diagnostics")
    table(["Model", "Test macro precision", "Test macro recall", "Full fit seconds"],
          [[m["model"], f"{m['macro_precision']:.3f}", f"{m['macro_recall']:.3f}",
            f"{m['fit_seconds']:.2f}"] for m in models], [53, 39, 37, 40])
    picture("confusion.png", "Figure 4. Candidate-level confusion matrices. One arc per observation is selected; the target is positive only for a correct shortlist member.", maximum=39*mm)
    winner = max(models, key=lambda m: m["cv_macro_f1"])
    runner = sorted(models, key=lambda m: m["cv_macro_f1"])[-2]
    para(f"{winner['model']} led {runner['model']} by {winner['cv_macro_f1']-runner['cv_macro_f1']:.4f} mean CV F1. The fold scores in Figure 3 show how rankings vary with the validation trips.")
    page()

    heading("3.2 Individual model experiments")
    for index, m in enumerate(models):
        if index and index % 3 == 0:
            page()
            heading("3.2 Individual model experiments")
        family, objective, why = MODELS[m["model"]]
        heading(m["model"], 2)
        para(f"{family}. The training objective is {objective.lower()}. {why}")
        config = ", ".join(f"{key}={value:g}" for key, value in m["config"].items())
        para(f"The initial configuration used {config}. Student-test Top-1 was {m['top1']:.3f}, macro F1 was {m['macro_f1']:.3f}, and covered log loss was {m['log_loss']:.3f}. Full-training F1 was {m['train_macro_f1']:.3f} and grouped CV F1 was {m['cv_macro_f1']:.3f}.")
        para(fit_diagnostic(m, models))
    picture("mlp_history.png", "MLP full-fit epoch history. Validation accuracy is on its internal training-row split. Grouped CV remains trip-disjoint.", maximum=68*mm)
    page()

    heading("4 Bayesian hyperparameter optimisation")
    base = next(m for m in models if m["model"] == tuned["model"])
    para(f"{tuned['model']} led the baseline comparison at CV macro F1 {base['cv_macro_f1']:.4f}. Optuna's Tree-structured Parzen Estimator ran {len(read_csv('search.csv'))} trials with seed {logging['seed']} and ten startup trials. The baseline was evaluated separately. It maximised mean macro F1 over the same three trip-grouped folds. Total search time was {logging['search_seconds']:.1f} s.")
    for name, space in logging["search_space"].items():
        para(f"The search used {space} for {name} and selected {tuned['config'][name]:.5g}.")
    table(["Variant", "CV F1", "Test top-1", "Test F1", "Test log loss", "Infer ms"],
          [[label, f"{m['cv_macro_f1']:.4f}", f"{m['top1']:.4f}", f"{m['macro_f1']:.4f}",
            f"{m['log_loss']:.4f}", f"{m['inference_ms']:.2f}"]
           for label, m in [("Untuned", base), ("Tuned", tuned)]], [35, 25, 28, 25, 31, 25])
    para(f"Tuning changed CV macro F1 by {tuned['cv_macro_f1']-base['cv_macro_f1']:+.4f} and student-test macro F1 by {tuned['macro_f1']-base['macro_f1']:+.4f}. The deployed variant was {logging['deployed_variant']}, selected by training-only CV macro F1. A CV tie favours the tuned variant. Student-test scores were excluded from the deployment decision.")
    picture("search.png", "Figure 5. Bayesian trials in execution order. Parameters, fold scores and durations are preserved in results/search.csv.")
    page()

    heading("5 HMM and Viterbi route reconstruction")
    para("A hidden state is a directed candidate arc for one GPS observation. The positive-class probability of each candidate becomes odds p/(1-p), then is normalised across shortlisted arcs. The Viterbi score combines log emission with the best previous state and its normalised log transition score. Backpointers recover one hidden state per observation.")
    para(f"Directed shortest paths join the previous projected position to the next. The transition kernel penalises discrepancy between network travel distance and observed GPS displacement using a scale of {settings['beta']:g} + 0.3 times the sampling gap in seconds. Directed search is capped at {settings['max_distance']:g} m. Transitions outside a gap-dependent cap receive a finite fallback penalty, and gaps beyond {settings['reset_gap']:g} seconds reset the dynamic program. Repeated arc states can absorb small along-arc jitter. Output geometry stitches traversable gaps with intermediate arcs and records unresolved breaks.")
    para("The shortlist falls back to the available road arcs on sparse graphs. An invalid or empty network fails validation. Beta was selected from 8, 14, 20 and 35 by mean macro F1 on all 80 training trips. Each trip was decoded using probabilities from a classifier fitted on the other two grouped folds. Classifier configuration was selected using these same folds. The calibration avoids fitting on a held-out trip, while shared model selection means this score is not a fully independent estimate. Final decoder evaluation used the ten separate student-test trips.")
    calibration = read_csv("decoder_search.csv")
    beta_scores = {beta: np.mean([float(r["macro_f1"]) for r in calibration if r["beta"] == beta])
                   for beta in dict.fromkeys(r["beta"] for r in calibration)}
    para("The training out-of-fold scores were " +
         ", ".join(f"{score:.4f} at beta {float(beta):g}" for beta, score in beta_scores.items()) + ".")
    agg = []
    for method in ("Classifier", "Viterbi"):
        data = [row for row in comparison if row["method"] == method]
        avg = {key: np.mean([float(row[key]) for row in data])
               for key in ("top1", "macro_f1", "continuity", "arc_jaccard", "seconds", "breaks")}
        agg.append([method] + [f"{avg[k]:.3f}" for k in ("top1", "macro_f1", "continuity", "arc_jaccard", "seconds", "breaks")])
    table(["Method", "Top-1", "Macro F1", "Continuity", "Arc Jaccard", "Sec/trip", "Breaks/trip"],
          agg, [32, 19, 22, 24, 27, 21, 24])
    improved, degraded = [], []
    for a, b in zip(comparison[::2], comparison[1::2]):
        if float(b["top1"]) > float(a["top1"]):
            improved.append(a["trip"][-2:])
        elif float(b["top1"]) < float(a["top1"]):
            degraded.append(a["trip"][-2:])
    para("Viterbi improved pointwise accuracy on " + str(len(improved)) + " trips and reduced it on "
         + str(len(degraded)) + ". The reduced-score trip suffixes were " + (", ".join(degraded) or "none")
         + ". Arc Jaccard measures set overlap after stitching. Exact sequence matches were "
         + ", ".join(f"{method} {sum(int(r['exact_route']) for r in comparison if r['method']==method)}/10"
                     for method in ("Classifier", "Viterbi")) + ".")
    baseline_pts, decoded_pts = [[float(r["top1"]) for r in comparison if r["method"] == method]
                                 for method in ("Classifier", "Viterbi")]
    deltas = np.asarray(decoded_pts) - baseline_pts
    worst_trip = comparison[2 * int(deltas.argmin())]["trip"]
    worst_gap = next(row["maximum_gap"] for row in inventory
                     if row["partition"] == "student_test" and row["trip"] == worst_trip)
    para(f"The mean pointwise change was {deltas.mean():+.2%}. Trip {worst_trip} had the smallest change ({deltas.min():+.2%}) and a maximum sampling gap of {float(worst_gap):g} seconds. A transition can favour a connected detour over an isolated, higher-scoring candidate; the table and per-trip plot distinguish these objectives.")
    picture("route_accuracy.png", "Figure 6. Per-trip comparison using aligned student-test reference labels.", maximum=65*mm)
    page()

    heading("6 Geographical visualisation using Folium")
    para("The generated Folium map adds nearby road segments, original GPS points, the reference and reconstructed route as separately toggleable layers. Bounds fit the GPS and reconstructed geometry. The optional OpenStreetMap basemap is initially off.")
    for index, trip in enumerate(("00000056", "00000052")):
        if index:
            page()
            heading("6 Geographical visualisation using Folium")
        a, b = [r for r in comparison if r["trip"] == trip]
        picture(f"folium_{trip}.png", f"Student-test trip {trip}. Interactive map in results/student_trip_map_{trip}.html.", maximum=118*mm)
        para(f"For {trip}, the classifier had {a['breaks']} route breaks and Viterbi had {b['breaks']}. Pointwise accuracy changed from {float(a['top1']):.2%} to {float(b['top1']):.2%}. Route arc Jaccard changed from {float(a['arc_jaccard']):.2%} to {float(b['arc_jaccard']):.2%}.")
        para("A reconstruction can rank fewer observation-level labels correctly while still connecting adjacent arcs. Breaks, overlap and pointwise accuracy capture different effects of decoding.")
    page()

    heading("7 API, UI and deployment")
    para("Laptop 1 serves FastAPI with the trained model and private scoring references. Laptop 2 serves a static UI. GET /trips enumerates ten inputs and POST /match scores the selected trip. The receiving console logs match requests.")
    picture("api.png", "Receiving Uvicorn log from the actual development API run, rendered from results/receiver.log.", maximum=85*mm)
    picture("ui_00000052.png", "Live student-test inference for trip 00000052.", maximum=103*mm)
    para("All ten student-test trips were exercised through the browser and directly over HTTP in the cloud workspace. A separate evaluator-mode development fixture isolates the reference files. Physical two-laptop operation and reserved evaluator trips require a live run on the team equipment.")
    page()
    heading("7 Browser evidence")
    for trip in ("00000056", "00000076"):
        picture(f"ui_{trip}.png", f"Live student-test inference for trip {trip}.", maximum=107*mm)
    page()
    heading("Reproducibility and authorship")
    para("The repository contains the source pipeline, saved model, configuration, logged results, plots, and commands for recreating the Folium map and this report. Raw dataset files and private evaluator references belong on the team machines.")
    para("The team supplied project requirements, author details and revision requests, and ran the initial demo on Windows. Codex implemented the pipeline and interface, ran the recorded experiments and integration tests, and prepared the report and figures. All reported metrics are computed from recorded runs. The team is responsible for analysing and explaining the results and confirming that its submission meets the organiser's independent-work and disclosure requirements.")
    para("This report follows the supplied PathSnap Main Guidelines, Dataset Exploration, Models and Training Guidelines, Deliverables, and Assessment and Plagiarism Policy. These are the supplied hackathon documents. The video attachment exceeded the workspace transfer limit and was unavailable for review.")

    def footer(canvas, doc):
        canvas.setStrokeColor(colors.HexColor("#d0ded8"))
        canvas.line(20*mm, 15*mm, 190*mm, 15*mm)
        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(colors.HexColor(MUTED))
        canvas.drawString(20*mm, 10*mm, "PATHSNAP  /  TECHNICAL REPORT")
        canvas.drawRightString(190*mm, 10*mm, str(doc.page))

    pdf = SimpleDocTemplate(output, pagesize=(210*mm, 297*mm), rightMargin=20*mm, leftMargin=20*mm,
                            topMargin=17*mm, bottomMargin=21*mm, title="PathSnap Technical Report", author=f"{team['name']} ({authors})")
    pdf.build(story, onFirstPage=footer, onLaterPages=footer)


if __name__ == "__main__":
    report(*sys.argv[1:])
