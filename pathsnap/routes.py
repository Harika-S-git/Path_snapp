"""Decoder tuning, held-out comparison, and reproducible Folium maps."""
import csv
import json
from pathlib import Path
import sys
from time import perf_counter

import folium
import joblib
import numpy as np

from .core import Trip, probabilities
from .data import prefixes
from .train import observation_stats


def measure(trip, truth, route, states, config):
    rebuilt, breaks = trip.route_geometry(states, max_distance=config["max_distance"],
                                         reset_gap=config["reset_gap"])
    arcs = trip.arcs
    repeated = states[1:] == states[:-1]
    connected = arcs[states[:-1], 1] == arcs[states[1:], 0]
    ref, pred = set(route), set(rebuilt)
    return dict(**observation_stats(truth, states), continuity=float(np.mean(repeated | connected)),
                arc_jaccard=len(ref & pred) / len(ref | pred), breaks=len(breaks),
                exact_route=int(list(route) == rebuilt))


def map_for(trip, route, predicted):
    center = trip.track[:, :2].mean(axis=0)[::-1]
    result = folium.Map(location=center, tiles=None, control_scale=True, zoom_start=14)
    folium.TileLayer("OpenStreetMap", name="Street basemap", show=False).add_to(result)
    bounds = np.vstack([trip.track[:, :2], trip.nodes[trip.arcs[predicted]].reshape(-1, 2)])
    low, high = bounds.min(axis=0), bounds.max(axis=0)
    line = trip.nodes[trip.arcs]
    inside = ((line >= low - .003) & (line <= high + .003)).all(axis=(1, 2))
    layers = [
        ("Road network", "#a3b0ae", 1, line[inside]),
        ("Reference route", "#843bd1", 5, line[route]),
        ("Predicted route", "#008455", 3, line[predicted]),
    ]
    for label, color, weight, data in layers:
        group = folium.FeatureGroup(name=label).add_to(result)
        folium.PolyLine(data[..., ::-1].tolist(), color=color, weight=weight, opacity=.8).add_to(group)
    gps = folium.FeatureGroup(name="GPS observations").add_to(result)
    for point in trip.track[:, :2]:
        folium.CircleMarker(point[::-1].tolist(), radius=2, color="#2878da", fill=True,
                            fill_opacity=.85, weight=1).add_to(gps)
    folium.LayerControl(collapsed=False).add_to(result)
    legend = """<div style="position:fixed;bottom:53px;left:22px;z-index:9999;background:white;
    padding:12px 16px;border-radius:6px;color:#162720;font:14px system-ui">
    <b>PathSnap · student-test trip</b><br><span style="color:#2878da">●</span> GPS
    &nbsp;<span style="color:#843bd1">━</span> Reference
    &nbsp;<span style="color:#008455">━</span> Predicted
    &nbsp;<span style="color:#71817e">━</span> Network</div>"""
    result.get_root().html.add_child(folium.Element(legend))
    result.fit_bounds([low[::-1].tolist(), high[::-1].tolist()])
    return result


def write_csv(path, rows):
    with Path(path).open("w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def compare(root):
    bundle = joblib.load("artifacts/model.joblib")
    model, config = bundle["model"], bundle["decoder"]
    # Tune on deterministic training-route samples only. Model selection and
    # classifier hyperparameter tuning have already completed at this point.
    sample = sorted(prefixes(root, "train"), key=lambda p: (p.with_suffix(".track").stat().st_size, p.name))[:8]
    tuning = []
    for prefix in sample:
        trip = Trip(prefix)
        ids, fractions, features = trip.candidates()
        p = probabilities(model, features)
        reference, truth = trip.reference(prefix)
        for beta in (8.0, 14.0, 20.0, 35.0):
            settings = dict(config, beta=beta)
            decoded = trip.decode(ids, fractions, p, **settings)
            tuning.append(dict(trip=prefix.name, beta=beta, **measure(trip, truth, reference, decoded, settings)))
    write_csv("results/decoder_search.csv", tuning)
    selected = max((8., 14., 20., 35.), key=lambda beta: np.mean(
        [r["macro_f1"] for r in tuning if r["beta"] == beta]))
    settings = dict(config, beta=selected)
    bundle["decoder"] = settings
    joblib.dump(bundle, "artifacts/model.joblib", compress=3)
    Path("results/decoder_config.json").write_text(json.dumps(settings, indent=2))
    rows = []
    for prefix in prefixes(root, "student_test"):
        start = perf_counter()
        trip = Trip(prefix)
        ids, fractions, features = trip.candidates()
        p = probabilities(model, features)
        classifier = ids[np.arange(len(ids)), p.argmax(axis=1)]
        base_seconds = perf_counter() - start
        decoded = trip.decode(ids, fractions, p, **settings)
        decode_seconds = perf_counter() - start
        reference, truth = trip.reference(prefix)
        for name, states, seconds in (("Classifier", classifier, base_seconds), ("Viterbi", decoded, decode_seconds)):
            rows.append(dict(trip=prefix.name, method=name, seconds=seconds,
                             **measure(trip, truth, reference, states, settings)))
        if prefix.name == "00000052":
            reconstructed, _ = trip.route_geometry(decoded, max_distance=settings["max_distance"],
                                                   reset_gap=settings["reset_gap"])
            map_for(trip, reference, reconstructed).save("results/student_trip_map.html")
        print(prefix.name, round(decode_seconds, 2), flush=True)
    write_csv("results/routes.csv", rows)


if __name__ == "__main__":
    compare(sys.argv[1])
