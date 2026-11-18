"""Laptop 1 inference API. Reference files are opened after prediction."""
from contextlib import asynccontextmanager
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


@asynccontextmanager
async def lifespan(app):
    root = Path(os.environ["PATHSNAP_TRIPS"])
    tracks = sorted(root.rglob("*.track"))
    trips = {p.stem: p.with_suffix("") for p in tracks}
    mode = os.environ.get("PATHSNAP_MODE", "evaluator")
    if mode not in {"demo", "evaluator"}:
        raise RuntimeError("PATHSNAP_MODE must be demo or evaluator")
    if len(trips) != 10 or len(tracks) != 10:
        raise RuntimeError("Trip directory must contain exactly ten uniquely named track files")
    for trip in trips.values():
        if any(not trip.with_suffix(extension).is_file() for extension in (".nodes", ".arcs")):
            raise RuntimeError(f"Missing road files for trip {trip.name}")
    app.state.trips = trips
    app.state.mode = mode
    app.state.references = Path(os.environ.get("PATHSNAP_REFERENCES", str(root)))
    bundle = joblib.load(os.environ.get("PATHSNAP_MODEL", "artifacts/model.joblib"))
    if bundle["features"] != FEATURES:
        raise RuntimeError("Saved model feature schema does not match this version")
    app.state.bundle = bundle
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
    return {"mode": state.mode, "trip_ids": sorted(state.trips)}


@app.get("/benchmark")
def benchmark(request: Request):
    import csv
    routes_csv = Path("results/routes.csv")
    if routes_csv.is_file():
        with routes_csv.open() as f:
            return {"status": "ok", "routes": list(csv.DictReader(f))}
    return {"status": "error", "message": "Benchmark data unavailable"}


def find_reference(root, trip_id):
    for candidate in (root / trip_id / trip_id, root / trip_id):
        if candidate.with_suffix(".route").is_file():
            return candidate
    return None


@app.post("/match")
def match(payload: MatchRequest, request: Request):
    state = request.app.state
    prefix = state.trips.get(payload.trip_id)
    if prefix is None:
        raise HTTPException(404, "Trip ID is unavailable")
    start = perf_counter()
    trip = Trip(prefix)
    ids, fractions, features = trip.candidates()
    params = state.bundle["decoder"]
    p = probabilities(state.bundle["model"], features)
    classifier_states = ids[np.arange(len(ids)), p.argmax(axis=1)]
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
