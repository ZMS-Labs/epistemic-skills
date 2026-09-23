> **Applies to:** epistemic-skills v7.1.0.

# Why the project is shaped this way

The central design problem is balancing adequate scrutiny with useful completion. Too little structure permits unsupported conclusions and lost context. Too much structure turns straightforward work into repeated interviews, reports, and approval requests.

### Choices and their costs

| Choice | Problem it addresses | Tradeoff and boundary |
|---|---|---|
| **One canonical implementation** | Copies of a method drift across hosts | Adapters must preserve the source method and disclose host-specific limits |
| **Thin delivery adapters** | Hosts expose different discovery, hook, and goal surfaces | Packaging compatibility is easier to establish than actual loaded behavior |
| **One usage guide, direct access to methods** | Users need orientation without an all-purpose controller | `epistemic` teaches usage; task ownership stays with the agent doing the work |
| **Visible, proportionate method use** | Silent use is hard to inspect; repeated banners are noise | A brief contribution statement is expected, including a valid no-change result |
| **Optional external packages** | Useful integrations should not make the suite unusable elsewhere | Triage prefers the debugging skill from [Superpowers](https://github.com/obra/superpowers), a separate open-source skills library, when it applies, and has its own fallback |
| **A shared lens library** | Focused examination and panel review need consistent methods | Method names are lookup coordinates; roles do not manufacture independent expertise |
| **Separate evidence levels** | A green source check can be mistaken for a working installation | Reports must identify whether they checked structure, delivery, behavior, or benefit |
| **Reuse existing durable records** | Multiple ledgers create conflicting sources of truth | A reused artifact must actually contain the provenance and revisit condition needed |
| **Explicit heavier contracts** | Some work requires stronger continuity or acceptance controls | Mission custody and UAT retain their own requirements; they are not defaults for every edit |

### Why the boundaries matter

A debugging method should return a cause, then let an already-authorized repair continue. A research method should produce evidence without quietly approving a design. A health report should preserve an inaccessible subject as unknown. A recorded decision should help future work without acting as permission.

Those separations make claims easier to challenge. They also provide stopping points: once the scoped question is answered, another pass needs a new reason.

### How this can be evaluated

Tests can check schemas, routing, refusal conditions, generated artifacts, and known failure controls. Host observations can establish what was discovered or loaded. Task trials can assess application and outcome. Comparative trials need valid paired cases before they support a benefit claim.

The v7 comparison produced zero valid pairs, so nothing measured yet shows that v7 helps agents finish tasks more often. The table above gives the reason for each choice, and [Testing and Evaluations](Testing-and-Evaluations.md) has the evidence so far.

For the source architecture and maintenance map, use [the maintainer guide](https://github.com/ZMS-Labs/epistemic-skills/blob/main/docs/MAINTAINING.md). Canonical behavior remains defined by the [v7.1.0 skill tree](https://github.com/ZMS-Labs/epistemic-skills/blob/v7.1.0/plugins/epistemic-skills/skills).
