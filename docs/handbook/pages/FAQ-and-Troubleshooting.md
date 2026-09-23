> **Applies to:** epistemic-skills v7.0.0.

# Questions and practical fixes

### Do I have to run the skills in order?

No. Load the usage guide when needed, then apply a method when its conditions arise. Direct invocation is supported through the host's actual interface. The [Skill Catalog](Skill-Catalog.md) is organized by the question each method answers.

### Does this require Superpowers?

No external package is a required dependency. [Superpowers](https://github.com/obra/superpowers) is a separate open-source skills library. When its systematic-debugging skill is available and applies, Triage uses it and brings its own standard for naming a cause into that investigation. If it is unavailable, Triage uses its own standalone procedure and says which one it actually used.

### The agent announces a skill but does not seem to use it.

Ask which instructions it loaded, what evidence it examined, and what contribution followed. A name or startup message is not application. The usage guide calls for a concise contribution statement; a valid result may also be “the existing approach was adequate.”

### The installed version looks right, but behavior is old.

Identify the actual loaded copy. Check for duplicate user/project/plugin installations, cached versions, and the host's reload boundary. Preserve local customizations. Source, installed files, observed loading, and applied behavior are separate checks. [Context Audit](Skill-Context-Audit.md) can investigate conflicting layers; [Did It Land](Skill-Did-It-Land.md) can verify delivery.

### Why does a slash command or old skill name fail?

Invocation and aliases vary by host. Use the current canonical name through the available interface or explicitly load the file. Historical names are compatibility mappings unless native alias behavior has been verified. Consult the [v7.0.0 usage and identity guidance](https://github.com/ZMS-Labs/epistemic-skills/blob/v7.0.0/plugins/epistemic-skills/skills/epistemic/SKILL.md#delivery-and-identity).

### Why did the agent stop after producing a report?

A bounded method returns to the task owner. If repair or implementation was already authorized, that work should continue. If you requested assessment only, stopping at findings is correct. An unavailable observation holds the claim or action depending on it, not every independent task.

### Are a different model and a second reviewer always required?

No. Ordinary review honors the user's designated reviewer and reports actual separation. A different model family alone does not establish independence. Some explicitly adopted contracts retain their own requirements: Manifest custody requires a distinct accepting actor; UAT can claim blinding only when its contexts actually were separated.

### Is v7 proven better than v6?

No. The bounded comparison produced zero valid pairs, so it supports no superiority claim. Required release checks passed; those checks establish their particular contracts, not universal task benefit. See [Testing and Evaluations](Testing-and-Evaluations.md).

### Can I use mission custody on a case-insensitive filesystem?

Do not rely on its POSIX filename-distinctness or exclusion guarantees there. The macOS diagnostic reproduces [issue #162](https://github.com/ZMS-Labs/epistemic-skills/issues/162). A passing required Ubuntu job does not erase that limit.
