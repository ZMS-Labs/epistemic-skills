> **Applies to:** epistemic-skills v7.0.0.

# Start with a real task

You do not need to memorize the catalog or run the suite in order. Choose a task whose result you can inspect, install through the host's documented mechanism, and begin with the actual outcome you want.

### 1. Establish the available instructions

Follow [installation and host coverage](Installation-and-Harness-Compatibility.md). Ask the agent to load `epistemic` through its available skill interface, or explicitly read the installed canonical `SKILL.md` when native discovery is unavailable. Invocation syntax varies by host; a universal slash command is not assumed.

The entry establishes usage guidance. Once it is loaded, repeatedly announcing it adds no value.

### 2. State the outcome and authority

An illustrative request:

> Fix the preference that disappears after reload. Preserve existing settings, investigate the cause, and verify that the saved value survives reopening the page. Briefly name any methods you actually use.

The task gives repair authority within its scope. The agent should not stop after diagnosis or request that same authority again. It should ask only if a consequential unresolved choice or action exceeds the grant.

### 3. Expect a contribution you can recognize

A useful acknowledgment is concrete:

> I used Triage with Systematic Debugging to distinguish the failed write from a stale read. The repair now passes the reload check.

That sentence must describe actual instruction loading, application, and observation. An announcement is not itself evidence. No substantive method needs to fire when a routine direct check is enough.

### 4. Check the result at the right level

| Claim | Useful evidence |
|---|---|
| “The source changed” | The intended diff |
| “The host discovers it” | An observed discovery response |
| “The change is active” | Behavior at the consuming runtime |
| “The user outcome works” | The relevant interaction and result |

Ask for the uncovered scope when evidence is partial. Missing access should narrow the claim, not become a successful check.

Continue with [the catalog](Skill-Catalog.md), [three worked examples](Workflow-Recipes.md), or [the conceptual map](How-the-Pieces-Fit.md).
