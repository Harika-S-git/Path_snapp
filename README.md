# PathSnap

PathSnap matches noisy, time-stamped GPS observations to directed road arcs. A supervised candidate classifier supplies emission scores, then a Viterbi decoder uses network distances and elapsed time to reconstruct the route. FastAPI runs inference and scoring on the receiving laptop. The browser displays the prediction and aggregate accuracy.

## Run locally with the supplied student-test data

Use Python 3.12. Extract the original `Student folder.zip` into the project directory. The repository ships the trained model and experiment output. After installing `requirements-api.txt`, run `python -m pathsnap.demo` and open http://localhost:8080. Pass the extracted dataset folder as a command-line argument if it lives elsewhere. To run the two servers separately, use the commands below.

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-api.txt
PATHSNAP_MODE=demo PATHSNAP_TRIPS="Student folder/student_test" python -m uvicorn pathsnap.api:app --host 0.0.0.0 --port 8000
```

Windows PowerShell

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements-api.txt
$env:PATHSNAP_MODE = "demo"
$env:PATHSNAP_TRIPS = "Student folder/student_test"
python -m uvicorn pathsnap.api:app --host 0.0.0.0 --port 8000
```

Start the interface in a second terminal with `python -m http.server 8080 --directory ui`. Open http://localhost:8080 and select a trip. The UI uses the API for every reconstruction and draws both map layers locally without relying on a tile provider.

## Evaluator deployment on two laptops

1. On laptop 1, install the API dependencies, then set `PATHSNAP_MODE=evaluator`. Point `PATHSNAP_TRIPS` to the reserved folder with exactly ten unique IDs. Each ID needs matching `.track`, `.nodes`, and `.arcs` files, either directly in the folder or inside a per-trip subdirectory.
2. Set `PATHSNAP_REFERENCES` to a server-only directory with `<id>.route` or `<id>/<id>.route` files. If omitted, scoring looks in the trip directory. Reference files are read after the decoder produces a prediction.
3. Start the API on `0.0.0.0:8000` using the command above. Use the receiving laptop's LAN IPv4 address on laptop 2. Allow TCP 8000 on the private network if the OS firewall prompts.
4. Copy `ui/` to laptop 2 and run the static server there. Open http://localhost:8080, enter `http://<laptop-1-address>:8000` in **Inference server**, click **Connect**, and pick any displayed trip. The receiving terminal logs the trip ID, inferred observation count, prediction time, and accuracy. To restrict cross-origin calls, set `PATHSNAP_UI_ORIGINS=http://localhost:8080` on laptop 1 before starting the API.
5. For diagnostics, GET `/health`, then GET `/trips`. POST `/match` with a JSON body containing `trip_id`. See `/docs` for the live OpenAPI interface.

The source data has route-level arc labels. Server accuracy uses per-observation pseudo-labels derived by monotone alignment to that reference route. Geometry is longitude/latitude in JSON. The download contains predicted arc IDs and geometry, GPS observations, break positions, and aggregate accuracy.

## Reproduce the experiments

Run from the project root with the extracted student dataset.

```bash
python -m pip install -r requirements.txt
export OMP_NUM_THREADS=2 OPENBLAS_NUM_THREADS=2
python -m pathsnap.data "Student folder" cache
python -m pathsnap.train cache "Student folder"
python -m pathsnap.routes "Student folder"
# With the demo running, capture the actual integration evidence.
python -m pathsnap.smoke http://127.0.0.1:8000 > results/api_smoke.txt
python -m playwright install chromium
python -m pathsnap.evidence http://localhost:8080 http://127.0.0.1:8000
python -m pathsnap.report "Student folder"
```

- `pathsnap/core.py` contains the local metric projection, candidate generation, features, directed transition graph, Viterbi recurrence, and route stitching.
- `pathsnap/alignment.py` contains the monotone dynamic program for assigning pseudo-labels to observations.
- `results/inventory.csv` records file availability, coordinate ranges, sampling, and network connectivity for each development trip.
- `results/models.json` records model configuration, grouped CV scores, test metrics, candidate confusion matrices, and timing. `results/search.csv` records the nine TPE trials.
- `results/routes.csv` records the classifier and decoder comparison per student-test trip. `results/decoder_search.csv` records the training-only beta sweep.
- Run the route comparison to generate `results/student_trip_map.html` for the Folium visualisation. Leaflet resources and the optional OpenStreetMap basemap use network access.

All trip splits come from the organizers. Timing varies by hardware. Training uses at most 180,000 candidate rows per fit with a fixed seed. Candidate log loss is conditional on the pseudo-label being in the shortlist. Observation-level macro metrics average over road arc labels within each trip and then over trips, since arc IDs are local to each network.

## Recorded student-test results

| Method | Pointwise accuracy | Macro F1 | Route continuity | Route arc Jaccard |
| --- | ---: | ---: | ---: | ---: |
| Random forest | 88.60% | 77.89% | 93.86% | 65.75% |
| Random forest + Viterbi | 91.87% | 87.21% | 97.66% | 85.70% |

Three-fold grouped CV selected the random forest (macro F1 74.74%). The nine-trial Bayesian search retained the original forest configuration. The `results/` directory contains per-trip outcomes. The project archive and technical report are available with the release. [PathSnap v1.0.0](https://github.com/Harika-S-git/Path_snapp/releases/tag/v1.0.0)

## Submission provenance

The implementation and report draft were produced with Codex assistance. Figures and metrics come from the code and recorded experiment runs. Use the report together with the run logs and source when reviewing and explaining the submission. The reserved data and a physical two-laptop test were unavailable during development.
