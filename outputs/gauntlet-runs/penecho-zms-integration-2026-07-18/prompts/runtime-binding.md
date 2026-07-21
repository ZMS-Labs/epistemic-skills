# Runtime binding record

- Generator: native `gauntlet-generator`
- Evaluators: native `gauntlet-adversary`, `gauntlet-constructive`, and `gauntlet-metatextual` roles parameterized by the deterministic roster personas in `selection.json`
- Arbitrator: native `gauntlet-arbitrator`, dispatched after mechanical verification
- Orchestration: manual-degraded; evaluator isolation preserved across two capacity-limited batches
- Cross-family separation: unavailable
- Dossier boundary: evaluators read only `dossier.md` and `sources.md`; they did not read other reports
