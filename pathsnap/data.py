"""Inventory and prepare the two permitted development partitions."""
import csv
from pathlib import Path
import sys

import numpy as np
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components

from .core import Trip


def prefixes(root, partition):
    for path in sorted((Path(root) / partition).rglob("*.track")):
        yield path.with_suffix("")


def prepare(root, cache):
    cache = Path(cache)
    cache.mkdir(parents=True, exist_ok=True)
    rows = []
    for partition, expected in [("train", 80), ("student_test", 10)]:
        trips = list(prefixes(root, partition))
        if len(trips) != expected:
            raise ValueError(f"{partition}: expected {expected} trips, found {len(trips)}")
        for p in trips:
            trip = Trip(p)
            ids, fraction, features = trip.candidates()
            route, truth = trip.reference(p)
            graph = coo_matrix((np.ones(len(trip.arcs)),
                                (trip.arcs[:, 0], trip.arcs[:, 1])),
                               shape=(len(trip.nodes),) * 2).tocsr()
            gaps = np.diff(trip.track[:, 2])
            rows.append(dict(partition=partition, trip=p.name, observations=len(ids),
                             invalid=trip.invalid, reversals=trip.raw_reversals,
                             one_second=int((gaps == 1).sum()), duplicates=int((gaps == 0).sum()),
                             maximum_gap=float(max(gaps, default=0)), nodes=len(trip.nodes),
                             arcs=len(trip.arcs), isolated=int(len(trip.nodes) - len(np.unique(trip.arcs))),
                             weak_components=connected_components(graph, directed=False)[0],
                             route_arcs=len(route),
                             reference_breaks=int((trip.arcs[route[:-1], 1] != trip.arcs[route[1:], 0]).sum()),
                             longitude_min=trip.track[:, 0].min(), longitude_max=trip.track[:, 0].max(),
                             latitude_min=trip.track[:, 1].min(), latitude_max=trip.track[:, 1].max(),
                             **{f"{ext}_bytes": p.with_suffix("." + ext).stat().st_size
                                for ext in ("track", "nodes", "arcs", "route")}))
            np.savez_compressed(cache / f"{partition}-{p.name}.npz", ids=ids, features=features,
                                truth=truth, fraction=fraction)
    with Path("results/inventory.csv").open("w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    prepare(*sys.argv[1:])
