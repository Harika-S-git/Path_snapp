"""Road candidate generation and directed sequence decoding."""
from functools import lru_cache
from pathlib import Path
import heapq

import numpy as np
from scipy.spatial import cKDTree

FEATURES = ["distance_m", "heading_cos", "projection_fraction", "length_m",
            "speed_mps", "gap_s", "midpoint_distance_m", "previous_distance_m",
            "next_distance_m"]
DECODER = {"beta": 20.0, "reset_gap": 90.0, "max_distance": 2000.0}


def load(prefix, suffix, columns, dtype=float):
    path = Path(str(prefix) + suffix)
    values = np.loadtxt(path, dtype=dtype, ndmin=2)
    if values.shape[1] != columns:
        raise ValueError(f"{path.name} must contain {columns} columns")
    return values


def projection(points, start, delta):
    length_sq = np.sum(delta ** 2, axis=-1)
    fraction = np.clip(np.sum((points - start) * delta, axis=-1)
                       / np.maximum(length_sq, 1e-12), 0, 1)
    nearest = start + fraction[..., None] * delta
    return np.linalg.norm(points - nearest, axis=-1), fraction


class Trip:
    def __init__(self, prefix):
        raw = load(prefix, ".track", 3)
        valid = (np.isfinite(raw).all(axis=1) & (np.abs(raw[:, 0]) <= 180)
                 & (np.abs(raw[:, 1]) <= 90))
        raw = raw[valid]
        self.invalid = int((~valid).sum())
        self.raw_reversals = int((np.diff(raw[:, 2]) < 0).sum())
        raw = raw[np.argsort(raw[:, 2], kind="stable")]
        if not len(raw):
            raise ValueError("Track has no valid observations")
        self.track = raw
        self.nodes = load(prefix, ".nodes", 2)
        self.arcs = load(prefix, ".arcs", 2, int)
        if (not len(self.arcs) or self.arcs.min() < 0 or self.arcs.max() >= len(self.nodes)
                or not np.isfinite(self.nodes).all()):
            raise ValueError("Invalid road network")
        self.origin = raw[0, :2]
        self.scale = 111195 * np.array([np.cos(np.deg2rad(np.median(raw[:, 1]))), 1])
        self.xy = (raw[:, :2] - self.origin) * self.scale
        nodes = (self.nodes - self.origin) * self.scale
        self.start = nodes[self.arcs[:, 0]]
        self.delta = nodes[self.arcs[:, 1]] - self.start
        self.length = np.linalg.norm(self.delta, axis=1)
        self.paths = lru_cache(maxsize=384)(self._paths)
        self.adj = [[] for _ in nodes]
        for arc, (a, b) in enumerate(self.arcs):
            self.adj[a].append((b, float(self.length[arc]), arc))

    def candidates(self, k=8):
        # Sample long lines at <= 20 m so a close segment can be retrieved
        # even when its midpoint is far from the GPS observation.
        counts = np.maximum(1, np.ceil(self.length / 20).astype(int))
        owners = np.repeat(np.arange(len(counts)), counts)
        offsets = np.arange(len(owners)) - np.repeat(np.cumsum(counts) - counts, counts)
        samples = self.start[owners] + ((offsets + .5) / counts[owners])[:, None] * self.delta[owners]
        tree = cKDTree(samples)
        k = min(k, len(self.arcs))
        _, vicinity = tree.query(self.xy, k=np.arange(1, min(40, len(samples)) + 1))
        rows = []
        mid = self.start + .5 * self.delta
        for p, near in zip(self.xy, vicinity):
            ids = np.unique(owners[near])
            if len(ids) < k:
                ids = np.arange(len(self.arcs))
            ds, _ = projection(p, self.start[ids], self.delta[ids])
            rows.append(ids[np.argsort(ds, kind="stable")[:k]])
        ids = np.asarray(rows)
        start, delta = self.start[ids], self.delta[ids]
        distance, fraction = projection(self.xy[:, None], start, delta)
        prev = np.r_[0, np.arange(len(ids) - 1)]
        nxt = np.r_[np.arange(1, len(ids)), len(ids) - 1]
        motion = self.xy[nxt] - self.xy[prev]
        dt = self.track[nxt, 2] - self.track[prev, 2]
        norm = np.linalg.norm(motion, axis=1)
        heading = np.sum(motion[:, None] * delta, axis=-1) / np.maximum(norm[:, None] * self.length[ids], 1e-9)
        shape = distance.shape
        features = np.stack([
            distance, heading, fraction, self.length[ids],
            np.broadcast_to((norm / np.maximum(dt, 1))[:, None], shape),
            np.broadcast_to(np.diff(self.track[:, 2], prepend=self.track[0, 2])[:, None], shape),
            np.linalg.norm(self.xy[:, None] - mid[ids], axis=-1),
            projection(self.xy[prev, None], start, delta)[0],
            projection(self.xy[nxt, None], start, delta)[0],
        ], axis=-1)
        return ids, fraction, features

    def reference(self, prefix):
        route = load(prefix, ".route", 1, int).ravel()
        if not len(route) or route.min() < 0 or route.max() >= len(self.arcs):
            raise ValueError("Invalid reference route")
        # Monotone alignment to route positions with a soft penalty on
        # moving farther along the measured route than the GPS displacement.
        ds, fractions = projection(self.xy[:, None], self.start[route], self.delta[route])
        lengths = self.length[route]
        progress = (np.cumsum(lengths) - lengths) + fractions * lengths
        from .alignment import align
        steps = np.r_[0.0, np.linalg.norm(np.diff(self.xy, axis=0), axis=1)]
        return route, route[align(ds, progress, steps)]

    def _paths(self, source, limit):
        distance = {source: 0.0}
        parent = {}
        queue = [(0.0, source)]
        while queue:
            length, node = heapq.heappop(queue)
            if length != distance[node]:
                continue
            for other, edge, arc in self.adj[node]:
                candidate = length + edge
                if candidate <= limit and candidate < distance.get(other, np.inf):
                    distance[other] = candidate
                    parent[other] = (node, arc)
                    heapq.heappush(queue, (candidate, other))
        return distance, parent

    def decode(self, ids, fractions, probabilities, beta=20, reset_gap=90, max_distance=2000):
        return self.decode_betas(ids, fractions, probabilities, (beta,), reset_gap, max_distance)[0]

    def decode_betas(self, ids, fractions, probabilities, betas, reset_gap=90, max_distance=2000):
        """Reuse the directed transition distances across decoder calibrations."""
        log_emission = np.log(np.clip(probabilities, 1e-12, 1))
        betas = np.asarray(betas)
        n, k = ids.shape
        back = np.zeros((n, len(betas), k), dtype=np.intp)
        score = np.broadcast_to(log_emission[0], (len(betas), k))
        batch = np.arange(len(betas))
        candidates = np.arange(k)
        for i in range(1, n):
            gap = self.track[i, 2] - self.track[i - 1, 2]
            if gap > reset_gap:
                back[i] = score.argmax(axis=1)[:, None]
                score = np.broadcast_to(log_emission[i], score.shape)
                continue
            step = np.linalg.norm(self.xy[i] - self.xy[i - 1])
            previous, current = ids[i - 1], ids[i]
            cap = min(max_distance, max(120.0, step * 3 + 70, gap * 35))
            heads = self.arcs[current, 0]
            offset = fractions[i] * self.length[current]
            forward = np.empty((k, k))
            for a, arc in enumerate(previous):
                distances, _ = self.paths(int(self.arcs[arc, 1]), max_distance)
                remainder = (1 - fractions[i - 1, a]) * self.length[arc]
                network = np.fromiter((distances.get(head, np.inf) for head in heads), float, count=k)
                direct = abs(fractions[i] - fractions[i - 1, a]) * self.length[arc]
                via_network = (network + remainder) + offset
                forward[a] = np.where(current == arc, np.minimum(via_network, direct), via_network)
            cost = np.where(forward <= cap,
                            -abs(forward - step) / (betas[:, None, None] + .3 * gap), -8.0)
            cost -= np.logaddexp.reduce(cost, axis=2)[:, :, None]
            joint = score[:, :, None] + cost
            back[i] = joint.argmax(axis=1)
            score = joint[batch[:, None], back[i], candidates] + log_emission[i]
        index = score.argmax(axis=1)
        paths = np.empty((len(betas), n), dtype=int)
        for i in range(n - 1, -1, -1):
            paths[:, i] = ids[i, index]
            index = back[i, batch, index]
        return paths

    def route_geometry(self, states, max_distance=2000, reset_gap=90):
        route = [int(states[0])]
        breaks = []
        for i, (a, b) in enumerate(zip(states, states[1:]), start=1):
            if a == b:
                continue
            source, target = self.arcs[a, 1], self.arcs[b, 0]
            distance, parent = self.paths(int(source), max_distance)
            if target in distance and self.track[i, 2] - self.track[i - 1, 2] <= reset_gap:
                bridge = []
                while source != target:
                    target, arc = parent[target]
                    bridge.append(arc)
                route.extend(reversed(bridge))
            else:
                breaks.append(len(route))
            route.append(int(b))
        return route, breaks


def probabilities(model, features):
    n, k, d = features.shape
    p = model.predict_proba(features.reshape(-1, d))[:, 1].reshape(n, k)
    p = np.clip(p, 1e-8, 1 - 1e-8)
    odds = p / (1 - p)
    return odds / odds.sum(axis=1, keepdims=True)
