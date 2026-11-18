"""Exercise every trip through the deployed HTTP API."""
import json
import sys
from urllib.error import HTTPError
from urllib.request import Request, urlopen


def read(endpoint, path, payload=None):
    request = Request(endpoint + path)
    if payload is not None:
        request = Request(endpoint + path, data=json.dumps(payload).encode(),
                          headers={"Content-Type": "application/json"})
    with urlopen(request, timeout=180) as response:
        return json.load(response)


def run(endpoint):
    print("GET /health", read(endpoint, "/health"), flush=True)
    trips = read(endpoint, "/trips")
    ids = trips["trip_ids"]
    assert len(ids) == len(set(ids)) == 10
    print("GET /trips", json.dumps(trips), flush=True)
    try:
        read(endpoint, "/match", {"trip_id": "../unavailable"})
    except HTTPError as error:
        assert error.code == 404
    else:
        raise AssertionError("An unavailable trip was accepted")
    for trip in ids:
        data = read(endpoint, "/match", {"trip_id": trip})
        assert set(data) == {"trip_id", "observations", "accuracy", "prediction_ms",
                             "observation_arc_ids", "route_arc_ids", "breaks", "gps", "route_segments"}
        assert data["trip_id"] == trip
        assert len(data["observation_arc_ids"]) == len(data["gps"]) == data["observations"] > 0
        assert len(data["route_arc_ids"]) == len(data["route_segments"]) > 0
        assert data["accuracy"] is None or 0 <= data["accuracy"] <= 1
        print("POST /match 200", trip, data["observations"], "observations",
              f"accuracy={data['accuracy']}", f"prediction_ms={data['prediction_ms']}", flush=True)


if __name__ == "__main__":
    run(sys.argv[1])
