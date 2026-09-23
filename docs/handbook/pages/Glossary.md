> **Applies to:** epistemic-skills v7.0.0.

# A small glossary

These terms name practical distinctions used throughout the handbook.

| Term | Plain meaning | Example |
|---|---|---|
| **Epistemic** | About knowledge: its basis, limits, and revision | Asking what supports a completion claim |
| **Canonical source** | The authoritative implementation from which copies or adapters derive | A method's versioned `SKILL.md` |
| **Host / harness** | The application or runtime providing the agent's tools and instruction loading | A CLI, IDE, or desktop agent application |
| **Consumer** | The thing that actually uses a changed artifact | The process that loads a configuration |
| **Oracle** | The observation or rule used to judge a claim | Reloading and observing a persisted setting |
| **Negative control** | A deliberately unsuitable or failing case that should not pass | A seeded missing field rejected by a validator |
| **Load-bearing claim** | A fact whose truth changes the next decision or action | Which revision is currently deployed |
| **Provenance** | Recoverable information about where evidence came from | Source revision, observation time, and receipt |
| **Re-anchor** | Check a prior claim against its durable source and relevant current state | Refresh branch and deployment identity before resuming |
| **Lens** | A procedure organized around a useful question and evidence mechanism | Checking rollback feasibility |
| **Dossier** | The shared, versioned subject and evidence used in a review | A frozen migration proposal and verified assumptions |
| **Adjudication** | Weighing findings and resolving their material tensions | Explaining why a benefit does or does not outweigh an evidenced risk |
| **Revision condition** | What observation or changed criterion would reopen a conclusion | A rollback test failing after a schema change |
| **Receipt** | A recorded action or observation with identity and supporting evidence | A release record tied to a commit and published artifacts |
| **Proof bundle** | The evidence required to establish the intended outcome and its integrity | Behavior, anti-spoof checks, and target identity |
| **Frontier** | The next permitted step whose prerequisites are satisfied | A migration step after required decisions are settled |
| **Custody** | A durable record of authority, scope, effects, and acceptance | An opted-in Manifest mission |

A receipt's existence does not make every claim inside it true. A lens name does not create professional credentials. A copied instruction does not prove the host loaded or applied it.

[Core Concepts](Core-Concepts.md) explains the reasoning behind these distinctions.
