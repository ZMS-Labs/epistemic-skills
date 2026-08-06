# Collection-hook pressure evaluation

Five fresh-context repetitions per arm used the same adapter-failure pressure
scenario. The old snapshot passed the five assertions at counts **5, 5, 3, 0,
5**; the candidate passed **5, 5, 5, 5, 5**. Overall, the old snapshot passed
0/5 runs and the candidate passed 5/5.

Candidate behavior converged with no assertion variance. The old snapshot was
mixed only on adapter non-blocking behavior and never supplied eligibility-map
semantics. The public aggregate contains only counts, a scenario hash, and a
model-family label; raw outputs remain local-only.
