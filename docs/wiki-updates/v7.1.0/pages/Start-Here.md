> **Applies to:** epistemic-skills v7.1.0.

# Start with a real task

You do not need to memorize the catalog or run the suite in order. Install the suite, then pick a real task whose result you can check yourself and ask for the outcome you want.

### 1. Install it and load the usage guide

Follow the [install steps in the README](https://github.com/ZMS-Labs/epistemic-skills/blob/v7.1.0/README.md#installation-and-compatibility). [Installation and Harness Compatibility](Installation-and-Harness-Compatibility.md) shows what has been checked for each tool.

Then ask your agent to load `epistemic`, the suite's usage guide. If your agent can't find the skill on its own, ask it to read the installed `SKILL.md` file for `epistemic` directly. Each tool calls skills a little differently, so there is no single slash command that works everywhere. Once the guide is loaded, the agent doesn't need to keep announcing it.

### 2. Say what you want and what the agent may do

Here is an example request:

> The design rests on a premise that "the research says" short retries beat long timeouts. Run one literature check on that premise before we commit: cite what you actually find, and flag where the evidence is thin. Briefly name any methods you actually use.

That request already gives the agent permission to run the check. It shouldn't stop once it has restated the premise more convincingly, or ask for that permission a second time. It should come back to you only if it needs to make a significant decision or do something the request didn't cover.

### 3. Expect a contribution you can recognize

A useful reply from the agent is concrete. [Resolve](Skill-Resolve.md) is the suite's method for settling a question with evidence, and the agent's reply might read like this:

> I used Resolve's literature investigation for that one check. The premise traces to two papers: one supports it with stated caveats, the other contradicts it for workloads like ours. The design decision now names that split instead of "the research says."

The reply should describe what the agent actually loaded, did and saw. Naming a method is not evidence that it was used. When a quick direct check is enough, the agent doesn't need any of the methods.

### 4. Check the result at the right level

| Claim | Useful evidence |
|---|---|
| “The source changed” | The intended diff |
| “The agent's app can find the skill” | The app itself showing that it found the skill |
| “The change is live” | The running program behaving the new way |
| “The user outcome works” | The relevant interaction and result |

If the evidence covers only part of the job, ask what was left unchecked. If the agent couldn't reach something, it should say so and claim less.

Next: the [Skill Catalog](Skill-Catalog.md), three worked examples in [Workflow Recipes](Workflow-Recipes.md), or [How the Pieces Fit](How-the-Pieces-Fit.md).
