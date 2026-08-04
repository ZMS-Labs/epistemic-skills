# Queueing, capacity, and parallelism

```yaml
module_id: queueing-capacity-parallelism
version: 1.0.0
property_families: [P5, P7, P8]
trigger_properties: [throughput latency backlog saturation backpressure or parallel-speedup claim]
constructs: [arrival rate, service rate, utilization, Little's Law, queue stability, backpressure, Amdahl limit, tail latency]
models: [declared arrival and service processes, bounded queues, parallel workload fractions]
required_inputs: [arrival process, sustainable service capacity, concurrency, buffer and rejection policy, measurement window]
applicability_template:
  model: define arrivals service resources queues and horizon
  preconditions: state stationarity stability and independence assumptions used
  fact_mapping: anchor measured rates and topology to a time window and revision
derivation_templates: [lambda versus mu stability test, L equals lambda W under stated conditions, serial-fraction speedup bound]
counterexample_obligations: [give an overload interval or workload composition that violates the capacity claim]
result_vocabulary: [established, refuted, conditional, incomplete]
canonical_sources:
  primary_theory: [Little 1961 DOI 10.1287/opre.9.3.383, Amdahl 1967 DOI 10.1145/1465482.1465560]
  official_product_docs: [pin runtime autoscaling and queue semantics by product and version]
known_exclusions: [O(1) per-request work as proof of aggregate stability, unmeasured workload assumptions]
```

Constant per-request complexity does not establish system scalability. If a
sustained arrival rate `λ` exceeds sustainable service rate `μ`, expected
backlog grows while that condition persists. Measurements require a pinned
window and preregistered interpretation; assumed hit rate or service capacity
is not observed evidence.
