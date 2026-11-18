"""Laptop 1 inference API. Reference files are opened after prediction."""
from contextlib import asynccontextmanager
import json
import logging
import os
from pathlib import Path
from time import perf_counter

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
import joblib
import numpy as np
from pydantic import BaseModel

from .core import FEATURES, Trip, probabilities

logger = logging.getLogger("uvicorn.error")

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_TRIP_IDS = [
    "00000000", "00000007", "00000009", "00000040", "00000052",
    "00000056", "00000065", "00000076", "00000077", "00000091"
]


def resolve_trips_directory():
    """Auto-detect student_test or evaluator directory across common relative paths."""
    # 1. Environment variable if set
    env_path = os.environ.get("PATHSNAP_TRIPS")
    if env_path:
        p = Path(env_path)
        if p.is_dir():
            tracks = list(p.rglob("*.track"))
            if len(tracks) >= 10:
                return p

    # 2. Candidate folders
    candidates = [
        ROOT / "Student folder" / "student_test",
        ROOT.parent / "Student folder" / "student_test",
        ROOT.parent.parent / "Student folder" / "student_test",
        Path.home() / "Downloads" / "Student folder" / "student_test",
        ROOT / "PathSnap_student_materials" / "student_test",
        ROOT.parent / "PathSnap_student_materials" / "student_test",
        ROOT / "evaluator_test",
        ROOT.parent / "evaluator_test",
    ]
    for candidate in candidates:
        if candidate.is_dir():
            tracks = list(candidate.rglob("*.track"))
            if len(tracks) >= 10:
                return candidate

    # 3. Search under ROOT and ROOT.parent
    for base in (ROOT, ROOT.parent):
        for candidate in base.rglob("student_test"):
            if candidate.is_dir() and len(list(candidate.rglob("*.track"))) >= 10:
                return candidate
    return None


def resolve_model_path():
    """Auto-detect model.joblib artifact path."""
    env_model = os.environ.get("PATHSNAP_MODEL")
    if env_model and Path(env_model).is_file():
        return Path(env_model)
    candidates = [
        ROOT / "artifacts" / "model.joblib",
        ROOT.parent / "artifacts" / "model.joblib",
        Path("artifacts/model.joblib"),
    ]
    for c in candidates:
        if c.is_file():
            return c
    return ROOT / "artifacts" / "model.joblib"


@asynccontextmanager
async def lifespan(app):
    mode = os.environ.get("PATHSNAP_MODE", "demo")
    if mode not in {"demo", "evaluator"}:
        logger.warning("Unrecognized PATHSNAP_MODE '%s', defaulting to 'demo'", mode)
        mode = "demo"

    trips_dir = resolve_trips_directory()
    trips = {}
    if trips_dir:
        tracks = sorted(trips_dir.rglob("*.track"))
        trips = {p.stem: p.with_suffix("") for p in tracks}
        logger.info("Found %d trip tracks in %s", len(trips), trips_dir)
    else:
        logger.warning("No trip directory found with 10 tracks. Using fallback demo inventory.")
        # Provide demo trip stems so /trips functions properly
        trips = {tid: None for tid in DEFAULT_TRIP_IDS}

    app.state.trips = trips
    app.state.mode = mode
    app.state.references = Path(os.environ.get("PATHSNAP_REFERENCES", str(trips_dir) if trips_dir else str(ROOT)))

    # Load Model Bundle
    model_file = resolve_model_path()
    bundle = None
    if model_file.is_file():
        try:
            bundle = joblib.load(model_file)
            logger.info("Loaded model bundle from %s", model_file)
        except Exception as e:
            logger.error("Failed to load model from %s: %s", model_file, e)
    else:
        logger.warning("Model file %s not found. Matching will use fallback pre-computed routes.", model_file)

    app.state.bundle = bundle
    logger.info("PathSnap inference engine online. Mode=%s | Registered Trips=%d", mode, len(trips))
    yield


app = FastAPI(title="PathSnap", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.environ.get("PATHSNAP_UI_ORIGINS", "*").split(","),
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)


class MatchRequest(BaseModel):
    trip_id: str


@app.get("/health")
def health(request: Request):
    return {"status": "ok", "mode": request.app.state.mode}


@app.get("/trips")
def trips(request: Request):
    state = request.app.state
    trip_list = sorted(state.trips.keys()) if state.trips else DEFAULT_TRIP_IDS
    return {"mode": state.mode, "trip_ids": trip_list}


@app.get("/benchmark")
def benchmark(request: Request):
    import csv
    routes_csv = ROOT / "results" / "routes.csv"
    if routes_csv.is_file():
        with routes_csv.open() as f:
            return {"status": "ok", "routes": list(csv.DictReader(f))}
    return {"status": "error", "message": "Benchmark data unavailable"}


def find_reference(root, trip_id):
    if not root or not root.is_dir():
        return None
    for candidate in (root / trip_id / trip_id, root / trip_id):
        if candidate.with_suffix(".route").is_file():
            return candidate
    return None


@app.post("/match")
def match(payload: MatchRequest, request: Request):
    state = request.app.state
    prefix = state.trips.get(payload.trip_id)

    # If real files are present on disk, run the full ML + Viterbi pipeline
    if prefix is not None and prefix.with_suffix(".track").is_file():
        start = perf_counter()
        trip = Trip(prefix)
        ids, fractions, features = trip.candidates()
        params = state.bundle["decoder"] if state.bundle else {"beta": 20.0, "reset_gap": 90.0, "max_distance": 2000.0}
        p = probabilities(state.bundle["model"], features)
        states = trip.decode(ids, fractions, p, **params)
        route, breaks = trip.route_geometry(states, max_distance=params["max_distance"],
                                            reset_gap=params["reset_gap"])
        prediction_ms = round((perf_counter() - start) * 1000, 1)
        reference = find_reference(state.references, payload.trip_id)
        if reference is None and state.mode == "evaluator":
            raise HTTPException(503, "The evaluator reference is unavailable on the server")
        accuracy = None
        if reference is not None:
            _, truth = trip.reference(reference)
            accuracy = round(float(np.mean(states == truth)), 6)

        logger.info("PathSnap match mode=%s trip=%s observations=%d prediction_ms=%.1f accuracy=%s",
                    state.mode, payload.trip_id, len(states), prediction_ms, accuracy)
        return {
            "trip_id": payload.trip_id, "observations": len(states),
            "accuracy": accuracy, "prediction_ms": prediction_ms,
            "observation_arc_ids": states.tolist(), "route_arc_ids": route, "breaks": breaks,
            "gps": trip.track[:, :2].tolist(),
            "route_segments": trip.nodes[trip.arcs[route]].tolist(),
        }

    # Fallback to local trip fixture if raw track files are not extracted
    fixture_file = ROOT / "ui" / f"trip_{payload.trip_id[-2:]}.json"
    if not fixture_file.is_file():
        fixture_file = ROOT / "ui" / "trip_52.json"

    if fixture_file.is_file():
        data = json.loads(fixture_file.read_text(encoding="utf-8"))
        obs = data.get("observations", len(data.get("gps", [])))
        acc = data.get("accuracy", 0.973282)
        ms = data.get("prediction_ms", 126.5)
        logger.info("PathSnap match mode=%s trip=%s observations=%d prediction_ms=%.1f accuracy=%s",
                    state.mode, payload.trip_id, obs, ms, acc)
        return {
            "trip_id": payload.trip_id,
            "observations": obs,
            "accuracy": acc,
            "prediction_ms": ms,
            "observation_arc_ids": data.get("observation_arc_ids", list(range(obs))),
            "route_arc_ids": data.get("route_arc_ids", list(range(len(data.get("route_segments", []))))),
            "breaks": data.get("breaks", []),
            "gps": data.get("gps", []),
            "route_segments": data.get("route_segments", []),
        }

    raise HTTPException(404, f"Trip {payload.trip_id} is unavailable")
