# Shared lens library: literature matrix and run record

Date: 2026-09-18; UTC verification/deposit date: 2026-09-19. **Deep, bounded decision support; not a systematic review or behavioral validation.**

[Design synthesis](2026-09-18-v7-lens-library-assessment.md) · [Structured matrix and run record](2026-09-18-v7-lens-literature.json)

## Framed question

Which reusable methods should a shared lens library retain, refine, combine, relocate or add to improve evidence-sensitive reasoning without unnecessary process?

The target outcomes are useful distinct findings, accurate claims, feasible alternatives and proportionate effort. Human studies inform hypotheses about methods; they do not establish transfer to LLM agents. The unit of study varies: experimental participants, model evaluations, datasets, methods and a case study. Reanalysis and publication versions do not add independent evidence.

## Search, reception and durability

- Consensus: 13 question-led queries, first result pages only; all 20 selected records fetched. Rich response and quota fields inspected, with no free-tier/sign-in degradation observed. The reported page totals are not a census of the literature.
- Scite: signed-in collections canary passed. All selected DOI coordinates resolved; 19 supplied live tallies, one did not. Retraction, concern, correction and erratum filters applied to the selected papers and their two alternate coordinates.
- Reception follow-ups: perspective accuracy, reference-class forecasting and disagreeing-perspective estimation. Initial combined graph was capped; separate incoming graphs and targeted critique retrieval supplied the cited follow-ups. Other papers received tallies/notice checks, not exhaustive reception review.
- Prior holdings: the relevant skill-theory collection contained eight items; none of the selected twenty were already there. This does not establish absence from every other library.
- Deposit: a private scite collection named `epistemic-skills-v7-lens-library-2026-09-18` holds all 20 selected papers and two corrections, verified by paginated DOI membership (22/22). A synthesis note was added. This is the equivalent durable substrate; no directly callable Zotero connection or Zotero deposit is claimed.
- Two correction notices were examined: prior-publication disclosure for P13 and missing PDF figure arrows for P14. Neither retracts the cited result. No indexed retraction or concern matched the queried coordinates.
- Stop: **capped-by-budget**, meaning the preset deep-mode paper scope. Further general searching would not establish whether the proposed prompts work; no saturation claimed.

## Counterevidence and interpretation changes

- P05 and P06 prevent a blanket claim that role prompting either works or fails. Use task methods and relevant attributes, then assess behavior in context.
- P07 reports debate benefits; P08 attributes much tested benefit to independent sampling/voting. Neither establishes that every task requires a panel, a particular model family, or no discussion.
- P09 is **contested** by P19. Scite reported zero contrasting statements for P09, so that count would have missed the retrieved methodological critique.
- P20 extends perspective accuracy through target-specific feedback. Mixed citation labels do not make it a blanket refutation of P03.
- P17 describes a boundary on reference-class forecasting in an institutional setting, rather than a universal refutation of P11.
- P12 reports no significant transfer effect, but the transfer measure had low reliability. Do not turn a weak measure into evidence that transfer is impossible.

## Paper-level matrix

Verification labels identify what was inspected, not a quality score. `full-text` means the selected body sections identified below, not cover-to-cover reading. Tallies are live citation-statement counts, not independent studies or votes. All rows are cross-index confirmed and deposited this run.

### P01 — Devil's advocate versus authentic dissent: stimulating quantity and quality

[C. Nemeth, Keith S. Brown, J. D. Rogers (2001)](https://doi.org/10.1002/ejsp.58)

- **Design/population:** Human group experiment comparing authentic minority dissent with three assigned-advocate conditions.
- **Finding and relation:** Authentic dissent produced more and better alternatives in the tested tasks. supports method distinction.
- **Limits:** Assigned disagreement is not independent conviction or evidence; human laboratory results do not validate LLM personas.
- **Verification:** abstract-level. Metadata and abstract; primary publication metadata checked where noted.
- **Reception:** supporting 2, contrasting 0, mentioning 121; total statements 127, citing publications 227.
- **Notice:** none indexed in queried filters.
- **Cross-index / holdings:** confirmed / deposited-this-run. Evidence family: `authentic-dissent-2001`.

### P02 — Considering the opposite: a corrective strategy for social judgment.

[Charles G. Lord, Mark R. Lepper, Elizabeth L. Preston (1984)](https://doi.org/10.1037/0022-3514.47.6.1231)

- **Design/population:** Two human social-judgment experiments.
- **Finding and relation:** A concrete consider-the-opposite instruction reduced targeted judgment biases more than generic impartiality instructions. supports bounded counter-testing.
- **Limits:** Task-specific human result; not a universal debiasing cure or a test of this library.
- **Verification:** abstract-level. Metadata and abstract; primary publication metadata checked where noted.
- **Reception:** supporting 17, contrasting 3, mentioning 455; total statements 482, citing publications 694.
- **Notice:** none indexed in queried filters.
- **Cross-index / holdings:** confirmed / deposited-this-run. Evidence family: `consider-opposite-1984`.
- **Metadata/version notes:** Canonical single-slash APA DOI used; double-slash alias has a separate tally. Do not add the counts.
- **Alternate coordinates:** `10.1037//0022-3514.47.6.1231`. Do not sum version tallies.

### P03 — Perspective Mistaking: Accurately Understanding the Mind of Another Requires Getting Perspective, Not Taking Perspective

[Tal Eyal, Mary Steffel, Nicholas Epley (2018)](https://doi.org/10.1037/pspa0000115)

- **Design/population:** Twenty-five human experiments on interpersonal accuracy.
- **Finding and relation:** Imagined perspective taking did not consistently improve accuracy; direct conversation improved accuracy in the final experiment. supports stakeholder grounding.
- **Limits:** Some confidence increased without accuracy; conversation does not guarantee accurate representation. See P20 for feedback-based extension.
- **Verification:** abstract-level. Metadata and abstract; primary publication metadata checked where noted.
- **Reception:** supporting 17, contrasting 2, mentioning 209; total statements 234, citing publications 276.
- **Notice:** none indexed in queried filters.
- **Cross-index / holdings:** confirmed / deposited-this-run. Evidence family: `perspective-accuracy-2018`.

### P04 — Creating More and Better Alternatives for Decisions Using Objectives

[J. Siebert, R. Keeney (2015)](https://doi.org/10.1287/opre.2015.1411)

- **Design/population:** Five studies of personally relevant decisions and objective-driven alternative generation.
- **Finding and relation:** Working from objectives improved the quantity and quality of alternatives in the reported settings. supports constructive method.
- **Limits:** Human decision tasks; does not establish a morphological generator or LLM prompt is effective.
- **Verification:** abstract-level. Metadata and abstract; primary publication metadata checked where noted.
- **Reception:** supporting 0, contrasting 0, mentioning 49; total statements 51, citing publications 100.
- **Notice:** none indexed in queried filters.
- **Cross-index / holdings:** confirmed / deposited-this-run. Evidence family: `objective-generation-2015`.

### P05 — When"A Helpful Assistant"Is Not Really Helpful: Personas in System Prompts Do Not Improve Performances of Large Language Models

[Mingqian Zheng, Jiaxin Pei, Lajanugen Logeswaran, Moontae Lee, David Jurgens (2024)](https://doi.org/10.18653/v1/2024.findings-emnlp.888) · [Primary publication](https://aclanthology.org/2024.findings-emnlp.888/)

- **Design/population:** 162 roles, four model families and 2,410 factual questions.
- **Finding and relation:** Adding persona descriptions did not improve average factual performance in these tests. limits persona claims.
- **Limits:** Factual QA and tested prompts/models; not evidence that every specialist method or persona is ineffective.
- **Verification:** abstract-level. Metadata and abstract; primary publication metadata checked where noted.
- **Reception:** supporting 1, contrasting 0, mentioning 26; total statements 27, citing publications 69.
- **Notice:** none indexed in queried filters.
- **Cross-index / holdings:** confirmed / deposited-this-run. Evidence family: `persona-factual-2024`.
- **Metadata/version notes:** Published ACL record replaces the earlier preprint metadata; version tallies are not summed.
- **Alternate coordinates:** `10.48550/arxiv.2311.10054`. Do not sum version tallies.

### P06 — Principled Personas: Defining and Measuring the Intended Effects of Persona Prompting on Task Performance

[Pedro Henrique Luz de Araujo, Paul Röttger, Dirk Hovy, Benjamin Roth (2025)](https://doi.org/10.18653/v1/2025.emnlp-main.1364) · [Primary publication](https://aclanthology.org/2025.emnlp-main.1364/)

- **Design/population:** Nine models and 27 objective tasks; controlled intended and irrelevant persona attributes.
- **Finding and relation:** Expert personas often helped or had no significant effect; irrelevant attributes could impair performance. qualifies P05.
- **Limits:** Single-persona objective tasks; cannot establish value of a multi-lens open-ended review. Model size and attributes matter.
- **Verification:** full-text. Selected results and limitations sections; not cover-to-cover.
- **Reception:** UNVERIFIED (tallies unavailable for this indexed DOI).
- **Notice:** none indexed in queried filters.
- **Cross-index / holdings:** confirmed / deposited-this-run. Evidence family: `principled-personas-2025`.
- **Metadata/version notes:** Consensus venue was ArXiv despite the published DOI; use ACL primary record. Scite indexed this DOI but supplied no tally.

### P07 — Improving Factuality and Reasoning in Language Models through Multiagent Debate

[Yilun Du, Shuang Li, A. Torralba, J. Tenenbaum, Igor Mordatch (2024)](https://doi.org/10.48550/arxiv.2305.14325) · [Primary publication](https://proceedings.mlr.press/v235/du24e.html)

- **Design/population:** LLM multiagent debate experiments on reasoning and factual tasks.
- **Finding and relation:** Reported improvements in tested debate configurations. supports possible debate benefit.
- **Limits:** Protocol/task specific; compare P08 before attributing gains to debate rather than extra samples.
- **Verification:** abstract-level. Metadata and abstract; primary publication metadata checked where noted.
- **Reception:** supporting 3, contrasting 0, mentioning 342; total statements 346, citing publications 272.
- **Notice:** none indexed in queried filters.
- **Cross-index / holdings:** confirmed / deposited-this-run. Evidence family: `multiagent-debate-2024`.
- **Metadata/version notes:** Published conference identity verified; reception coordinate is the 2023 arXiv DOI, not a second evidence unit.

### P08 — Debate or Vote: Which Yields Better Decisions in Multi-Agent Large Language Models?

[Hyeong Kyu Choi, Xiaojin Zhu, Yixuan Li (2025)](https://doi.org/10.48550/arxiv.2508.17536) · [Primary publication](https://arxiv.org/html/2508.17536v1)

- **Design/population:** Seven NLP benchmarks plus analysis under explicit assumptions.
- **Finding and relation:** Independent voting explained much of the tested multiagent gain; selective debate interventions could help. qualifies P07.
- **Limits:** Preprint and mainly simultaneous-talk setting; the martingale analysis is conditional, not proof that discussion never helps.
- **Verification:** full-text. Selected results and limitations sections; not cover-to-cover.
- **Reception:** supporting 2, contrasting 0, mentioning 31; total statements 33, citing publications 6.
- **Notice:** none indexed in queried filters.
- **Cross-index / holdings:** confirmed / deposited-this-run. Evidence family: `debate-vote-2025`.
- **Metadata/version notes:** Selected full-text reasoning refers to version 1.

### P09 — Taking a Disagreeing Perspective Improves the Accuracy of People’s Quantitative Estimates

[Philippe P. F. M. van de Calseyde, Emir Efendić (2022)](https://doi.org/10.1177/09567976211061321)

- **Design/population:** Five preregistered human estimation experiments; 6,425 adults and 53,086 estimates as reported.
- **Finding and relation:** Reported benefit from aggregating an initial estimate with a disagreeing-perspective estimate. contested by P19.
- **Limits:** Later critique questions generalization from the statistical model; do not use as settled support for simulated diversity.
- **Verification:** abstract-level. Metadata and abstract; primary publication metadata checked where noted.
- **Reception:** supporting 1, contrasting 0, mentioning 31; total statements 32, citing publications 17.
- **Notice:** none indexed in queried filters.
- **Cross-index / holdings:** confirmed / deposited-this-run. Evidence family: `quantitative-perspective-2022`.
- **Metadata/version notes:** Scite author metadata was inconsistent; publisher/university record used. Zero indexed contrasting tally did not expose P19, which was found by targeted discovery.

### P10 — Group decision making in hidden profile situations: dissent as a facilitator for decision quality.

[S. Schulz-Hardt, F. Brodbeck, A. Mojzisch, Rudolf Kerschreiter, D. Frey (2006)](https://doi.org/10.1037/0022-3514.91.6.1080)

- **Design/population:** 135 three-person human groups with distributed hidden-profile information.
- **Finding and relation:** Dissent increased discovery of the better alternative; the degree of preference diversity did not differentiate outcomes. supports information-focused dissent.
- **Limits:** Unique information in human laboratory groups differs from agents sharing one model and evidence packet.
- **Verification:** abstract-level. Metadata and abstract; primary publication metadata checked where noted.
- **Reception:** supporting 10, contrasting 2, mentioning 287; total statements 309, citing publications 397.
- **Notice:** none indexed in queried filters.
- **Cross-index / holdings:** confirmed / deposited-this-run. Evidence family: `hidden-profile-2006`.

### P11 — Practical Application and Empirical Evaluation of Reference Class Forecasting for Project Management

[Jordy Batselier, M. Vanhoucke (2016)](https://doi.org/10.1177/875697281604700504)

- **Design/population:** Empirical project-management forecasting comparison using real project data.
- **Finding and relation:** Reference-class forecasting performed well in the reported comparison. supports qualified reference classes.
- **Limits:** Reference-class selection and organizational implementation matter; P17 is a case-study boundary, not a direct replication.
- **Verification:** abstract-level. Metadata and abstract; primary publication metadata checked where noted.
- **Reception:** supporting 0, contrasting 1, mentioning 48; total statements 49, citing publications 60.
- **Notice:** none indexed in queried filters.
- **Cross-index / holdings:** confirmed / deposited-this-run. Evidence family: `reference-class-projects-2016`.

### P12 — ‘Consider the Opposite’ – Effects of elaborative feedback and correct answer feedback on reducing confirmation bias – A pre-registered study

[Suzan van Brussel, M. Timmermans, P. Verkoeijen, F. Paas (2020)](https://doi.org/10.1016/j.cedpsych.2020.101844)

- **Design/population:** Preregistered university experiment on hypothesis-testing instruction, practice and feedback.
- **Finding and relation:** Feedback improved trained-task performance; no significant transfer effects were detected. supports bounded practice; limits transfer claim.
- **Limits:** Transfer-test reliability was low. No detected transfer is not proof of no transfer; longer-term persistence was not established.
- **Verification:** full-text. Scite full-text introduction, results/discussion and limitations excerpts (offsets 0, 40000, 48000). Transfer reliability limitation checked in the body.
- **Reception:** supporting 1, contrasting 0, mentioning 12; total statements 13, citing publications 25.
- **Notice:** none indexed in queried filters.
- **Cross-index / holdings:** confirmed / deposited-this-run. Evidence family: `consider-opposite-feedback-2020`.

### P13 — Many Analysts, One Data Set: Making Transparent How Variations in Analytic Choices Affect Results

[R. Silberzahn, E. Uhlmann, D. P. Martin, P. Anselmi, F. Aust, E. Awtrey, Š. Bahník, F. Bai, Colin Bannard, E. Bonnier, Rickard Carlsson, F. Cheung, G. Christensen, R. Clay, M. A. Craig, A. D. Rosa, Lammertjan Dam, Mathew H. Evans, I. F. Cervantes, N. Fong, M. Gamez-Djokic, A. Glenz, S. Gordon-McKeon, T. Heaton, K. Hederos, M. Heene, A. Mohr, F. Högden, K. Hui, M. Johannesson, J. Kalodimos, E. Kaszubowski, D. Kennedy, R. Lei, Thomas Lindsay, S. Liverani, C. Madan, Daniel C. Molden, E. Molleman, R. Morey, L. Mulder, B. Nijstad, N. Pope, B. Pope, J. Prenoveau, F. Rink, E. Robusto, H. Roderique, Anna Sandberg, E. Schlüter, F. Schönbrodt, M. Sherman, S. A. Sommer, K. Sotak, S. Spain, C. Spörlein, T. Stafford, L. Stefanutti, Susanne Täuber, J. Ullrich, M. Vianello, E. Wagenmakers, M. Witkowiak, S. Yoon, Brian A. Nosek (2018)](https://doi.org/10.1177/2515245917747646)

- **Design/population:** 29 analyst teams, 61 analysts and one shared football dataset.
- **Finding and relation:** Reasonable analytic choices produced materially different results. supports analysis sensitivity.
- **Limits:** Analysts shared one dataset; count it once, not as 29 independent studies. Correction concerns prior-publication disclosure.
- **Verification:** abstract-level. Metadata and abstract; primary publication metadata checked where noted.
- **Reception:** supporting 15, contrasting 0, mentioning 813; total statements 833, citing publications 975.
- **Notice:** correction. [10.1177/2515245918810511](https://doi.org/10.1177/2515245918810511): Adds omitted citation/disclosure of earlier Nature commentary and preprint publicity; not a result retraction. Full correction text inspected.
- **Cross-index / holdings:** confirmed / deposited-this-run. Evidence family: `many-analysts-2018`.

### P14 — Specification curve analysis

[U. Simonsohn, J. Simmons, Leif D. Nelson (2020)](https://doi.org/10.1038/s41562-020-0912-z)

- **Design/population:** Specification-curve method with three empirical examples.
- **Finding and relation:** Examines results across reasonable, valid, nonredundant specifications with joint inference. supports structured sensitivity.
- **Limits:** Reasonable-specification choices require justification; robustness across specifications does not establish causality or transport.
- **Verification:** abstract-level. Metadata and abstract; primary publication metadata checked where noted.
- **Reception:** supporting 8, contrasting 0, mentioning 829; total statements 837, citing publications 753.
- **Notice:** correction. [10.1038/s41562-020-00974-w](https://doi.org/10.1038/s41562-020-00974-w): Corrects missing bidirectional arrows in PDF figure; HTML was correct. Notice abstract inspected; primary webpage access failed.
- **Cross-index / holdings:** confirmed / deposited-this-run. Evidence family: `specification-curve-2020`.

### P15 — Judging LLM-as-a-judge with MT-Bench and Chatbot Arena

[Lianmin Zheng et al. (2023)](https://doi.org/10.52202/075280-2020) · [Primary publication](https://proceedings.neurips.cc/paper_files/paper/2023/hash/91f18a1287b398d378ef22505bf41832-Abstract-Datasets_and_Benchmarks.html)

- **Design/population:** LLM judge evaluation against human preferences on MT-Bench and Chatbot Arena.
- **Finding and relation:** Reported useful agreement alongside position, verbosity and self-enhancement biases. supports judging safeguards.
- **Limits:** Preference agreement is not factual validity; results are specific to evaluated models, tasks and prompts.
- **Verification:** abstract-level. Metadata and abstract; primary publication metadata checked where noted.
- **Reception:** supporting 0, contrasting 0, mentioning 38; total statements 38, citing publications 1013.
- **Notice:** none indexed in queried filters.
- **Cross-index / holdings:** confirmed / deposited-this-run. Evidence family: `llm-judge-2023`.
- **Metadata/version notes:** Primary NeurIPS authors/venue used because connector author/venue fields disagreed.

### P16 — Fixing dependency errors for Python build reproducibility

[S. Mukherjee, Abigail Almanza, Cindy Rubio-González (2021)](https://doi.org/10.1145/3460319.3464797)

- **Design/population:** 2,702 Python builds from BugSwarm and BugsInPy.
- **Finding and relation:** 1,921 builds had dependency-related unreproducibility; the method completely fixed 859 and partially fixed 632. supports dependency-closure method.
- **Limits:** Selected build datasets, not a software-population prevalence estimate. The 71.1% figure is failure prevalence here, not improvement.
- **Verification:** abstract-level. Metadata and abstract; primary publication metadata checked where noted.
- **Reception:** supporting 0, contrasting 0, mentioning 13; total statements 13, citing publications 68.
- **Notice:** none indexed in queried filters.
- **Cross-index / holdings:** confirmed / deposited-this-run. Evidence family: `python-builds-2021`.
- **Metadata/version notes:** Generated discovery takeaway mislabeled 71.10% as improvement; checked abstract instead.

### P17 — The processes of public megaproject cost estimation: The inaccuracy of reference class forecasting

[T. Themsen (2019)](https://doi.org/10.1111/faam.12210)

- **Design/population:** Longitudinal Danish megaproject case study.
- **Finding and relation:** Reference-class forecasting did not achieve its intended results amid organizational estimation processes. qualifies P11.
- **Limits:** One institutional setting; not a universal refutation of reference-class forecasting.
- **Verification:** abstract-level. Metadata and abstract; primary publication metadata checked where noted.
- **Reception:** supporting 0, contrasting 0, mentioning 21; total statements 24, citing publications 32.
- **Notice:** none indexed in queried filters.
- **Cross-index / holdings:** confirmed / deposited-this-run. Evidence family: `megaproject-process-2019`.

### P18 — Evaluating meta-analytic methods to detect selective reporting in the presence of dependent effect sizes.

[Melissa A. Rodgers, J. Pustejovsky (2021)](https://doi.org/10.1037/met0000300) · [Primary publication](https://jepusto.com/publications/selective-reporting-with-dependent-effects/)

- **Design/population:** Monte Carlo evaluation of selective-reporting detection with dependent effect sizes.
- **Finding and relation:** Ignoring dependence could inflate false positives; examined methods had limited power in some conditions. supports evidence-synthesis distinction.
- **Limits:** Simulation under specified conditions; no method certifies an unbiased evidence base.
- **Verification:** abstract-level. Metadata and abstract; primary publication metadata checked where noted.
- **Reception:** supporting 3, contrasting 1, mentioning 431; total statements 435, citing publications 555.
- **Notice:** none indexed in queried filters.
- **Cross-index / holdings:** confirmed / deposited-this-run. Evidence family: `selective-reporting-simulation-2021`.
- **Metadata/version notes:** Published volume 26(2), 2021; online publication 2020-07-12.

### P19 — Drawing Generalizable Conclusions From Multilevel Models: Commentary on Van de Calseyde and Efendić (2022)

[Joshua L. Fiechter (2024)](https://doi.org/10.1177/09567976241245411)

- **Design/population:** Statistical commentary/reanalysis of P09.
- **Finding and relation:** Argues the original model omitted relevant item-level variation and could support anti-conservative generalization. contests P09.
- **Limits:** A methodological critique, not a new independent experiment; disputed result retained with uncertainty.
- **Verification:** abstract-level. Metadata and abstract; primary publication metadata checked where noted.
- **Reception:** supporting 0, contrasting 0, mentioning 1; total statements 1, citing publications 5.
- **Notice:** none indexed in queried filters.
- **Cross-index / holdings:** confirmed / deposited-this-run. Evidence family: `quantitative-perspective-2022`.

### P20 — Nuancing Perspective

[Jacob Israelashvili, Anat Perry (2021)](https://doi.org/10.1027/1864-9335/a000452)

- **Design/population:** Two human emotion-inference experiments, one preregistered; total N=398.
- **Finding and relation:** Feedback about a target's past emotions improved inference about that person's future emotions. extends P03.
- **Limits:** Target-specific feedback, not proof that unaided imagining works. Mixed scite labels require reading the actual claim.
- **Verification:** abstract-level. Metadata and abstract; primary publication metadata checked where noted.
- **Reception:** supporting 0, contrasting 0, mentioning 3; total statements 3, citing publications 7.
- **Notice:** none indexed in queried filters.
- **Cross-index / holdings:** confirmed / deposited-this-run. Evidence family: `emotion-feedback-2021`.

## Query log

No publication-year restriction was used. Inclusion was judgment-led for the pending design questions. Secondary graph leads were followed where a result could change the recommendation. Unselected discovery records were not judged low quality; this was not formal full-text screening.

| # | Consensus query | Returned on page |
|---|---|---:|
| 1 | Do structured dissent, devil's advocacy and considering the opposite improve decision quality? | 20 |
| 2 | Does persona prompting or assigning expert roles improve factual accuracy of large language models compared with task instructions? | 19 |
| 3 | When does multi-agent debate improve large language model reasoning compared with majority voting and independent sampling? failure confirmation bias | 20 |
| 4 | Does considering the opposite reduce biased judgment? Lord Lepper Preston 1984 | 20 |
| 5 | Does taking another person's perspective improve accuracy compared with getting their perspective? Eyal Steffel Epley 2018 | 20 |
| 6 | Do premortem prospective hindsight and reference class forecasting improve prediction and planning accuracy? experiments limitations | 20 |
| 7 | Do value focused thinking and structured alternative generation improve decision quality? experiments | 20 |
| 8 | Many analysts one data set how variations in analytic choices affect results specification curve analysis | 19 |
| 9 | Large language model judges position bias verbosity self preference evaluation MT Bench Chatbot Arena | 20 |
| 10 | Reproducible builds undeclared dependencies computational reproducibility empirical study software | 20 |
| 11 | evidence synthesis selective reporting dependent studies transportability publication bias meta-analysis methods | 20 |
| 12 | Drawing Generalizable Conclusions From Multilevel Models Commentary Van de Calseyde Efendic Fiechter 2024 | 20 |
| 13 | 10.1027/1864-9335/a000452 Nuancing Perspective | 20 |

## Connector observations and limits

- Consensus structured response carries richer data and quota information than the compact text result.
- Consensus fetch metadata and generated takeaways are not automatically authoritative.
- Scite search may return fewer hits than requested; pagination verified the entire deposit.
- Scite zero filtered matches used misleading unindexed wording although unfiltered DOI lookups resolved.
- Citation graph type arrays included contradicting as well as mentioning/supporting; some edges lacked type.
- Missing tally treated as unavailable, not zero.
- Primary metadata resolved publication version/venue and author discrepancies.

No public artifact includes private access links, account metadata or local runtime bindings. The full source-decision record is kept with this research run and recorded through the scite citation-report connection. These notes remain local and uncommitted; the verified private collection is the off-machine scholarly deposit.
