 # PathSnap – Intelligent GPS Map Matching Using Machine Learning

PathSnap is a machine-learning-powered GPS map-matching system that reconstructs realistic travel routes from noisy and time-stamped GPS observations. It identifies the most likely directed road segments for each GPS point and combines supervised machine learning with probabilistic sequence decoding to generate continuous, network-consistent routes.

The system uses a Random Forest classifier to estimate candidate road-segment emission scores and a Viterbi decoder to identify the most likely sequence of road arcs based on spatial proximity, road-network connectivity, network distances, and elapsed travel time.

PathSnap provides a FastAPI-based inference backend and an interactive browser interface for route visualization, prediction analysis, and accuracy evaluation.

## 1. Key Features

- GPS Map Matching: Converts noisy GPS observations into meaningful road-network routes.
- Machine Learning Classification: Uses a supervised Random Forest model to rank candidate road segments.
- Candidate Generation: Identifies potential road arcs for each GPS observation.
- Viterbi Decoding: Finds the most likely continuous route using spatial and temporal transition constraints.
- Network-Aware Route Reconstruction: Considers directed road connectivity and network distances.
- Feature Engineering: Extracts spatial, geometric, temporal, and network-based features.
- FastAPI Backend: Provides REST APIs for route inference and evaluation.
- Interactive Web Interface: Displays GPS observations, predicted routes, and aggregate accuracy.
- Two-Laptop Deployment: Supports inference on one laptop and visualization on another over a local network.
- Offline Map Rendering: Draws map layers locally without requiring an external map-tile provider.

## 2. System Architecture

The PathSnap pipeline consists of the following stages:

1. GPS Data Input: Receives noisy, time-stamped GPS observations.
2. Candidate Generation: Finds nearby directed road arcs for each GPS observation.
3. Feature Extraction: Calculates relevant spatial, geometric, temporal, and network features.
4. ML Classification: Random Forest generates candidate emission scores.
5. Sequence Decoding: Viterbi combines emission scores with transition probabilities and network constraints.
6. Route Reconstruction: Produces the most likely sequence of directed road arcs.
7. Evaluation: Compares predictions against reference routes and calculates performance metrics.
8. Visualization: Displays reconstructed routes and evaluation results in the browser.

### Architecture Flow

```text
GPS Observations
       |
       v
Candidate Generation
       |
       v
Feature Extraction
       |
       v
Random Forest Model
       |
       v
Emission Scores
       |
       v
Viterbi Decoder
       |
       v
Route Reconstruction
       |
       v
Accuracy Evaluation
       |
       v
FastAPI Backend
       |
       v
Interactive Web UI
```

## 3. Technology Stack

| Component | Technology |
|---|---|
| Programming Language | Python 3.12 |
| Machine Learning | Scikit-learn |
| Classification Model | Random Forest |
| Optimization | Tree-structured Parzen Estimator (TPE) |
| Sequence Decoding | Viterbi Algorithm |
| Backend | FastAPI |
| API Server | Uvicorn |
| Frontend | HTML, CSS, JavaScript |
| Map Visualization | Local browser rendering |
| Route Visualization | Folium |
| Browser Testing | Playwright |
| Data Processing | NumPy, Pandas |

## 4. Machine Learning Methodology

### 4.1 Data Preprocessing

The GPS trajectory dataset is processed to prepare observations and road-network information for model training.

The preprocessing pipeline includes:

- Reading GPS trajectory observations.
- Processing node and directed arc information.
- Handling spatial coordinates and timestamps.
- Generating candidate road segments.
- Extracting relevant features.
- Creating training labels through monotone alignment between GPS observations and reference routes.

### 4.2 Feature Engineering

PathSnap extracts features that help distinguish between candidate road arcs.

These include:

- GPS-to-road spatial distance.
- Road-segment geometry.
- Direction and orientation information.
- Temporal information from consecutive GPS observations.
- Road-network connectivity.
- Network distance and transition-related features.

These features help the classifier identify road segments that are geographically and structurally consistent with the observed trajectory.

### 4.3 Random Forest Classification

A supervised Random Forest classifier predicts the likelihood of candidate road arcs for each GPS observation.

The classifier produces emission scores that represent how well each candidate matches the observed GPS point.

Three-fold grouped cross-validation was used for model selection to reduce the risk of trip-level data leakage.

### 4.4 Viterbi Decoding

Individual GPS observations can produce incorrect or disconnected road predictions.

To improve route consistency, PathSnap applies the Viterbi algorithm.

The decoder considers:

- Candidate emission scores.
- Directed road-network transitions.
- Network distances.
- Elapsed time between observations.
- Transition scoring controlled by a calibrated beta parameter.

It identifies the most likely sequence of road arcs instead of independently predicting each GPS observation.

### 4.5 Route Reconstruction

The final output is a continuous, network-aware route consisting of predicted directed road arc IDs and their associated geometries.

## 5. Model Evaluation and Results

PathSnap evaluates the performance of the Random Forest classifier before and after applying Viterbi decoding.

### Recorded Student-Test Results

| Evaluation Metric | Random Forest | Random Forest + Viterbi |
|---|---:|---:|
| Pointwise Accuracy | 88.56% | 92.13% |
| Macro F1 | 78.20% | 87.46% |
| Route Continuity | 93.82% | 97.62% |
| Route Arc Jaccard | 67.35% | 86.52% |

### Performance Improvement

- Pointwise accuracy improved by 3.57 percentage points.
- Macro F1 improved by 9.26 percentage points.
- Route continuity improved by 3.80 percentage points.
- Route arc Jaccard improved by 19.17 percentage points.

The results demonstrate that combining machine learning with sequence decoding improves both individual road-arc predictions and overall route consistency.

### Model Selection and Optimization

- Three-fold grouped cross-validation selected Random Forest as the baseline model.
- Baseline grouped-CV Macro F1: 74.74%.
- Best of 40 TPE trials: 74.76%.
- Deployment retained the tuned configuration based on cross-validation.
- Out-of-fold training calibration selected beta = 8.

The reported student-test results are recorded experiment outputs and should not be confused with results from the reserved evaluator dataset.

## 6. Project Structure

```text
PathSnap/
|
├── pathsnap/
│   ├── __init__.py
│   ├── api.py
│   ├── core.py
│   ├── alignment.py
│   ├── data.py
│   ├── train.py
│   ├── routes.py
│   ├── demo.py
│   ├── smoke.py
│   ├── evidence.py
│   └── report.py
│
├── ui/
│   ├── index.html
│   ├── style.css
│   └── script.js
│
├── results/
│   ├── inventory.csv
│   ├── models.json
│   ├── search.csv
│   ├── mlp_history.csv
│   ├── routes.csv
│   ├── decoder_search.csv
│   ├── api_smoke.txt
│   ├── receiver.log
│   └── student_trip_map_*.html
│
├── report/
│   └── PathSnap-Technical-Report.pdf
│
├── requirements-api.txt
└── README.md
```

The structure summarizes the main project components. Additional model, cache, and experiment artifacts may also be present.

## 7. Installation and Setup

### Prerequisites

- Python 3.12
- Git
- Windows, Linux, or macOS environment
- Extracted student-test dataset

### Step 1: Clone the Repository

```bash
git clone https://github.com/Harika-S-git/Path_snapp.git
cd Path_snapp
```

### Step 2: Extract the Dataset

Extract the original `Student folder.zip` into the project root.

Expected structure:

```text
PathSnap/
└── Student folder/
    └── student_test/
```

### Step 3: Create a Virtual Environment

Windows PowerShell:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Linux / macOS:

```bash
python3.12 -m venv .venv
source .venv/bin/activate
```

### Step 4: Install Dependencies

```bash
python -m pip install -r requirements-api.txt
```

## 8. Running PathSnap Locally

The easiest way to start the complete demo is:

```bash
python -m pathsnap.demo
```

Open your browser:

http://localhost:8080

Select a student-test trip to view its GPS observations and reconstructed route.

### Running the API and UI Separately

Terminal 1 – Start the FastAPI backend.

Windows PowerShell:

```powershell
$env:PATHSNAP_MODE = "demo"
$env:PATHSNAP_TRIPS = "Student folder/student_test"

python -m uvicorn pathsnap.api:app --host 0.0.0.0 --port 8000
```

Linux / macOS:

```bash
export PATHSNAP_MODE=demo
export PATHSNAP_TRIPS="Student folder/student_test"

python -m uvicorn pathsnap.api:app --host 0.0.0.0 --port 8000
```

Terminal 2 – Start the frontend.

```bash
python -m http.server 8080 --directory ui
```

Open:

http://localhost:8080

## 9. Two-Laptop Evaluator Deployment

PathSnap supports a client-server deployment in which inference runs on one laptop and the visualization interface runs on another.

### Laptop 1 – Inference Server

1. Install Python dependencies.
2. Set the evaluator mode.
3. Configure the reserved evaluator trip directory.
4. Configure the server-only reference directory.
5. Start the FastAPI server.

Windows PowerShell:

```powershell
$env:PATHSNAP_MODE = "evaluator"
$env:PATHSNAP_TRIPS = "PATH_TO_EVALUATOR_TRIPS"
$env:PATHSNAP_REFERENCES = "PATH_TO_REFERENCE_FILES"

python -m uvicorn pathsnap.api:app --host 0.0.0.0 --port 8000
```

The evaluator dataset must contain exactly ten unique trip IDs. Each trip requires matching `.track`, `.nodes`, and `.arcs` files.

Reference routes must be available as `.route` files in the configured server-only directory.

### Laptop 2 – Receiving Interface

1. Copy the `ui/` directory.
2. Start the static server:

```bash
python -m http.server 8080 --directory ui
```

3. Open:

http://localhost:8080

4. Enter the inference server address:

```text
http://<LAPTOP-1-LAN-IP>:8000
```

5. Click Connect.
6. Select a trip and run reconstruction.
7. Capture the displayed predictions and evaluation results.

On Laptop 1, use `ipconfig` to identify the active network adapter's IPv4 address. Allow TCP port 8000 through the private-network firewall if prompted.

For additional CORS restrictions, configure:

```powershell
$env:PATHSNAP_UI_ORIGINS = "http://localhost:8080"
```

### API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/health` | Check server health |
| GET | `/trips` | Retrieve available trips |
| POST | `/match` | Reconstruct a selected trip |
| GET | `/docs` | Interactive API documentation |

Example POST request:

```json
{
  "trip_id": "student_trip_00000052"
}
```

The exact trip ID should be selected from the `/trips` response.

## 10. Reproducing Experiments

Run the following commands from the project root after extracting the student dataset.

### Step 1: Install Dependencies

```bash
python -m pip install -r requirements-api.txt
```

For experiment reproduction, ensure the required training and visualization dependencies are also installed.

### Step 2: Configure Computational Threads

Linux / macOS:

```bash
export OMP_NUM_THREADS=2
export OPENBLAS_NUM_THREADS=2
```

Windows PowerShell:

```powershell
$env:OMP_NUM_THREADS = "2"
$env:OPENBLAS_NUM_THREADS = "2"
```

### Step 3: Generate Feature Cache

```bash
python -m pathsnap.data "Student folder" cache
```

### Step 4: Train the Models

```bash
python -m pathsnap.train cache "Student folder"
```

### Step 5: Generate Route Experiments

```bash
python -m pathsnap.routes "Student folder" cache
```

### Step 6: Run API Integration Tests

With the API and frontend running:

```bash
python -m pathsnap.smoke http://127.0.0.1:8000
```

### Step 7: Capture Browser Evidence

Install Playwright and Chromium:

```bash
python -m pip install playwright
python -m playwright install chromium
```

Run:

```bash
python -m pathsnap.evidence http://localhost:8080 http://127.0.0.1:8000
```

### Step 8: Generate the Technical Report

```bash
python -m pathsnap.report "Student folder"
```

## 11. Experiment Outputs

The `results/` directory contains experiment configurations, model comparisons, evaluation metrics, and visualization outputs.

| File | Description |
|---|---|
| `inventory.csv` | Dataset availability, coordinate ranges, sampling, and network connectivity |
| `models.json` | Model configuration, cross-validation scores, test metrics, and timing |
| `search.csv` | Results of 40 TPE optimization trials |
| `mlp_history.csv` | MLP training loss and internal validation accuracy |
| `routes.csv` | Classifier and decoder comparisons for student-test trips |
| `decoder_search.csv` | Training-only beta parameter search |
| `api_smoke.txt` | API integration test output |
| `receiver.log` | Receiving-server execution logs |
| `student_trip_map_*.html` | Folium route visualizations |

## 12. Route Visualization

PathSnap provides visual representations of:

- Original GPS observations.
- Predicted directed road arcs.
- Reconstructed route geometry.
- Route-level evaluation results.

The generated Folium maps can be opened using a web browser.

Example visualizations:

- `results/student_trip_map_00000052.html`
- `results/student_trip_map_00000056.html`

Folium visualizations and optional OpenStreetMap basemaps may require an internet connection to load external map resources.

## 13. Evaluation Methodology

The source dataset contains route-level arc labels. Observation-level reference labels are generated through monotone alignment between GPS observations and the reference route.

Evaluation includes:

- Pointwise Accuracy: Measures the percentage of GPS observations assigned the correct road arc.
- Macro F1: Measures classification performance while giving equal importance to individual road-arc classes.
- Route Continuity: Evaluates whether consecutive predicted road arcs form a connected route.
- Route Arc Jaccard: Measures the overlap between predicted and reference road-arc sets.

Observation-level macro metrics are calculated within each trip and then averaged across trips because road arc IDs are local to individual road networks.

Candidate log loss is conditional on the pseudo-label being present in the candidate shortlist.

## 14. Limitations and Evaluation Considerations

- GPS observations may contain significant positional noise.
- Candidate generation may exclude the correct road arc.
- Performance depends on road-network quality and connectivity.
- Route-level pseudo-labels are derived using monotone alignment.
- The reported student-test results do not establish performance on unseen evaluator trips.
- The reserved evaluator dataset and physical two-laptop test were unavailable during development.
- External Folium basemap resources require network access.

## 15. Documentation and Resources

For additional technical details, experimental methodology, implementation decisions, and evaluation results, refer to:

- [PathSnap Technical Report (PDF)](https://github.com/Harika-S-git/Path_snapp/blob/main/report/PathSnap-Technical-Report.pdf)
- [Project Archive – v1.1.0](https://github.com/Harika-S-git/Path_snapp/archive/refs/tags/v1.1.0.zip)

## 16. Project Credits and Submission Provenance

The Gradient Gang provided the project requirements, revision requests, and initial Windows execution demonstration.

Codex assisted with pipeline implementation, experimental execution, integration checks, visualizations, and technical report preparation.

All reported figures and metrics originate from the implementation and recorded experiment outputs. The technical report, source code, and execution logs should be considered together when reviewing and evaluating the project.

## 17. Project Objective

PathSnap aims to demonstrate how supervised machine learning and probabilistic sequence decoding can work together to solve GPS map matching more effectively.

Rather than treating GPS observations as independent classification problems, PathSnap considers the underlying road network and movement sequence to reconstruct routes that are both geographically plausible and topologically consistent.

**PathSnap – From Noisy GPS Points to Intelligent Route Reconstruction.**
