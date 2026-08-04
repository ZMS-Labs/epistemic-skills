# Probability, statistics, and randomization

```yaml
module_id: probability-statistics-randomization
version: 1.0.0
property_families: [P7, P8]
trigger_properties: [estimation or measurement-uncertainty claim, confidence interval or calibration claim, statistical comparison superiority or power claim, randomized-algorithm expected or high-probability guarantee, sampling-frame or population inference]
constructs: [probability model, estimator with bias and variance, confidence interval, hypothesis test with multiplicity control, statistical power and minimum detectable effect, concentration bound, randomized-algorithm guarantee, calibration curve and proper scoring rule, Bayesian updating with named prior, sampling frame]
models: [declared probability space plus data-generating assumptions separated from the observed sample and its collection mechanism]
required_inputs: [the population or process the claim covers, the sampling or assignment mechanism, sample size, the estimator or test statistic, the declared error tolerance or confidence level, preregistration status of the comparison]
applicability_template:
  model: separate the data-generating assumption from the observed sample and from the decision the number feeds
  preconditions: state the sampling frame, independence or dependence structure, stopping rule, and multiplicity of comparisons
  fact_mapping: anchor sample sizes, assignment mechanisms, and preregistration records to artifacts
derivation_templates: [estimator to error bound at declared confidence, power or minimum-detectable-effect at fixed design, concentration bound for a randomized guarantee, calibration assessment under a proper scoring rule, posterior update from named prior and likelihood]
counterexample_obligations: [supply a data-generating process or sampling mechanism under which the claimed inference fails at the stated confidence]
result_vocabulary: [established, refuted, conditional, incomplete]
canonical_sources:
  primary_theory: [Casella-Berger 2002 Statistical Inference 2e, Mitzenmacher-Upfal 2017 Probability and Computing 2e, Gneiting-Raftery 2007 DOI 10.1198/016214506000001437, Benjamini-Hochberg 1995 DOI 10.1111/j.2517-6161.1995.tb02031.x]
  official_product_docs: [pin the RNG, sampling library, or telemetry pipeline semantics when material]
known_exclusions: [a p-value read as a posterior probability or an effect size, significance claimed after optional stopping or unstated multiple looks, calibration asserted without a population and scoring method, pooling samples across heterogeneous resolution mechanisms as one frame, a random seed treated as an independence proof]
```

A number computed from data is not evidence until its probability model,
sampling frame, and error tolerance are named. Comparisons claim only what
their design can detect: state power or the minimum detectable effect before
reading a null result as absence, control multiplicity before reading any
positive one, and let calibration claims travel only with the population and
proper scoring rule that produced them.
