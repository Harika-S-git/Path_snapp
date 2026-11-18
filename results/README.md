# Recorded development evidence

- `inventory.csv` describes all 90 supplied trips, including missing/invalid observations, timestamps, geometry bounds, file sizes and weak connectivity.
- `models.json` contains seven baseline configurations, training and grouped CV scores, student-test metrics, candidate confusion matrices and durations. The tuned model uses the same protocol.
- `search.csv` logs Bayesian trials and durations. `decoder_search.csv` logs all 320 out-of-fold training-trip and beta combinations.
- `mlp_history.csv` records the MLP training loss and internal validation accuracy per epoch. `data_quality.csv` summarises raw track checks by partition.
- `routes.csv` contains per-trip classifier and Viterbi metrics. `decoder_config.json` matches the deployed transition parameters.
- `api_smoke.txt` contains HTTP integration output for all ten student-test trips. `receiver.log` records the corresponding FastAPI receiving console. `evaluator_mode_fixture.txt` exercises evaluator-mode wiring using those same student-test inputs and a separate reference directory.
- `figures/` contains the visual evidence used in the technical report. Interactive Folium maps for trips 00000052 and 00000056 are the two `student_trip_map_*.html` files.

Per-trip macro F1 averages across the union of predicted and reference arc labels. Across the three CV folds, every trip appears in exactly one validation fold. A new fit uses the fold's training trips only and reruns feature scaling inside the applicable model pipeline. All timed results are hardware dependent.
