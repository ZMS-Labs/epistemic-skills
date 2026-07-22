# Evidence basis for `write-goal`

## Scope and epistemic status

This reference records why the skill differs from a generic SMART-goal template. It is a
design synthesis, not a claim that one goal format is universally optimal.

Research was run on 2026-07-20 in `standard` evidence-research mode. Consensus supplied
discovery and paper-level summaries. Primary publisher, proceedings, or author pages were
used for integrity checks where available. Scite reception checks could not run because
the configured trial quota was exhausted until 2026-07-24 UTC, so every reception field
below is **UNVERIFIED**. No Zotero tool was available; holdings are **UNVERIFIED** and
deposit was skipped. Those missing layers limit confidence and are not silently treated as
negative findings.

Follow-up: re-run the reception pass (evidence-research, standard mode) after 2026-07-24
UTC and flip the UNVERIFIED reception stamps (the basis ran with Scite quota exhausted
until that date).

## Claim-evidence matrix

| ID | Design claim | Evidence | Application in the skill | Reception | Holdings |
|---|---|---|---|---|---|
| C1 | Specific, challenging goals and feedback often improve performance relative to vague exhortation. | Mento, Steel, & Karren (1987); Neubert (1998) | require an observable end state and feedback-producing proof | UNVERIFIED | UNVERIFIED |
| C2 | Task complexity moderates goal effects; complex or novel work can benefit from learning goals before outcome goals. | Wood, Mento, & Locke (1987); Winters & Latham (1996) | classify performance vs learning-first goals | UNVERIFIED | UNVERIFIED |
| C3 | Implementation intentions can help translate intent into action, but rigid or nonplanned responses can be harmful when conditions vary. | Gollwitzer & Brandstätter (1997); Webb & Sheeran (2008); Bieleke, Legrand, Mignon, & Gollwitzer (2018) | define a loop and critical blocker policy without scripting every contingency | UNVERIFIED | UNVERIFIED |
| C4 | Narrow goals can induce gaming, neglect, or unethical behavior when proxies diverge from intent. | Ordóñez et al. (2009); Amodei et al. (2016); Manheim & Garrabrant (2019) | require a three-layer proof bundle and anti-proxy review | UNVERIFIED | UNVERIFIED |
| C5 | Safe interruption and deference require explicit design; objective uncertainty alone does not guarantee off-switch behavior. | Orseau & Armstrong (2016); Hadfield-Menell et al. (2016) | preserve operator interrupt authority and name stop/escalation conditions | UNVERIFIED | UNVERIFIED |

## Counterevidence and boundary conditions

| Challenge | Evidence | Consequence for the method | Reception | Holdings |
|---|---|---|---|---|
| Strong warnings about goal setting may overstate the case; goal-setting theory already includes moderators and safeguards. | Locke & Latham (2009) | do not reject goals wholesale; make the contract context-sensitive and guarded | UNVERIFIED | UNVERIFIED |
| Implementation intentions show useful average effects, but effect size and mechanism vary. | Bélanger-Gravel, Godin, & Amireault (2013) | treat if-then planning as a bounded aid, not a universal completion contract | UNVERIFIED | UNVERIFIED |
| Learning goals are not automatically superior for every complex setting; interdependent teams can respond differently. | Nahrgang et al. (2013) | make goal type a classification decision, not a complexity-only rule | UNVERIFIED | UNVERIFIED |
| Off-switching is not guaranteed merely by uncertainty about the objective. | Neth (2025) | state user interrupt authority and escalation behavior explicitly | UNVERIFIED | UNVERIFIED |

## Coverage and design synthesis

- **Observed consensus:** specificity, difficulty, feedback, task complexity, and planning
  all matter, but none licenses a one-size-fits-all goal template.
- **Key translation:** use direct outcome evidence plus integrity and provenance checks so
  that an agent cannot satisfy the words by optimizing a weak proxy.
- **Boundary condition:** novel tasks may need a bounded learning-first contract, followed
  by an explicit conversion to a performance contract. This is a decision rule, not a
  universal preference for learning goals.
- **Safety condition:** detailed plans are subordinate to the completion contract. The
  user retains interrupt, redirect, pause, and cancel authority.
- **Unresolved:** reception, retraction, and durable-library status remain unverified for
  this run because Scite and Zotero were unavailable.

## Provenance of the adapted method

The starting method was Kimi Code 0.28.1's logical built-in skill
`builtin://write-goal`. Its payload was recovered from a Kimi session trace under
`%USERPROFILE%\.kimi-code\sessions\...\agents\main\wire.jsonl`.
The installed package is `@moonshot-ai/kimi-code` under
`%APPDATA%\npm\node_modules\@moonshot-ai\kimi-code`.

Retained concepts: end state, proof, boundaries, execution loop, stop rule, separate draft
and start actions, opt-in budgets, and queue-shaped-goal recognition. Additions: goal-type
classification, proof bundles, proxy-resistance, uncertainty policy, operator
interruptibility, epistemic boundary, and runtime adapters.

## References

1. Mento, A. J., Steel, R. P., & Karren, R. J. (1987). A meta-analytic study of the effects of goal setting on task performance: 1966-1984. *Organizational Behavior and Human Decision Processes, 39*(1), 52-83. https://doi.org/10.1016/0749-5978(87)90045-8
2. Neubert, M. J. (1998). The value of feedback and goal setting over goal setting alone and potential moderators of this effect: A meta-analysis. *Human Performance, 11*(4), 321-335. https://doi.org/10.1207/s15327043hup1104_2
3. Wood, R. E., Mento, A. J., & Locke, E. A. (1987). Task complexity as a moderator of goal effects: A meta-analysis. *Journal of Applied Psychology, 72*(3), 416-425. https://doi.org/10.1037/0021-9010.72.3.416
4. Winters, D., & Latham, G. P. (1996). The effect of learning versus outcome goals on a simple versus a complex task. *Group & Organization Management, 21*(2), 236-250. https://doi.org/10.1177/1059601196212007
5. Gollwitzer, P. M., & Brandstätter, V. (1997). Implementation intentions and effective goal pursuit. *Journal of Personality and Social Psychology, 73*(1), 186-199. https://doi.org/10.1037/0022-3514.73.1.186
6. Webb, T. L., & Sheeran, P. (2008). Mechanisms of implementation intention effects: The role of goal intentions, self-efficacy, and accessibility of plan components. *British Journal of Social Psychology, 47*(3), 373-395. https://doi.org/10.1348/014466607X267010
7. Bieleke, M., Legrand, E., Mignon, A., & Gollwitzer, P. M. (2018). More than planned: Implementation intention effects in nonplanned situations. *Acta Psychologica, 184*, 64-74. https://doi.org/10.1016/j.actpsy.2017.06.003
8. Ordóñez, L. D., Schweitzer, M. E., Galinsky, A. D., & Bazerman, M. H. (2009). Goals gone wild: The systematic side effects of overprescribing goal setting. *Academy of Management Perspectives, 23*(1), 6-16. https://doi.org/10.5465/AMP.2009.37007999
9. Amodei, D., et al. (2016). Concrete problems in AI safety. arXiv:1606.06565. https://arxiv.org/abs/1606.06565
10. Orseau, L., & Armstrong, S. (2016). Safely interruptible agents. *Proceedings of UAI 2016*. https://auai.org/~w-auai/uai2016/proceedings/papers/68.pdf
11. Hadfield-Menell, D., Russell, S. J., Abbeel, P., & Dragan, A. (2016). The off-switch game. arXiv:1611.08219. https://arxiv.org/abs/1611.08219
12. Manheim, D., & Garrabrant, S. (2019). Categorizing variants of Goodhart's law. arXiv:1803.04585. https://arxiv.org/abs/1803.04585
13. Locke, E. A., & Latham, G. P. (2009). Has goal setting gone wild, or have its attackers abandoned good scholarship? *Academy of Management Perspectives, 23*(1), 17-23. https://doi.org/10.5465/AMP.2009.37008000
14. Bélanger-Gravel, A., Godin, G., & Amireault, S. (2013). A meta-analytic review of the effect of implementation intentions on physical activity. *Health Psychology Review, 7*(1), 23-54. https://doi.org/10.1080/17437199.2011.560095
15. Nahrgang, J. D., et al. (2013). Goal setting in teams: The impact of learning and performance goals on process and performance. *Organizational Behavior and Human Decision Processes, 122*(1), 12-21. https://doi.org/10.1016/j.obhdp.2013.03.008
16. Neth, S. (2025). Off-switching is not guaranteed by objective uncertainty. *Philosophical Studies*. https://doi.org/10.1007/s11098-025-02296-x
