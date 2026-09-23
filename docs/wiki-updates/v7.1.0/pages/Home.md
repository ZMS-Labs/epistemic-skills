> **Applies to:** epistemic-skills v7.1.0.

# Reusable methods for AI agents

<picture>
  <source media="(max-width: 600px)" srcset="https://raw.githubusercontent.com/ZMS-Labs/epistemic-skills/main/docs/assets/epistemic-cover-mobile.svg">
  <img src="https://raw.githubusercontent.com/ZMS-Labs/epistemic-skills/main/docs/assets/epistemic-cover.svg" alt="Epistemic Skills cover: “Check the cause before naming it. Confirm the change before calling it done.” A branching diagram leads from a question to an observation and then to a supported next step." width="1280">
</picture>

Epistemic Skills is a set of written methods for AI agents: the AI tools that carry out a multi-step task on their own. The methods help an agent investigate a failure, compare options and check whether a change worked. “Epistemic” means concerned with knowledge: what supports a conclusion, where uncertainty remains, and what would change our mind.

There are seventeen skills: one usage guide and sixteen methods for specific jobs. Use the one that fits the question in front of you, and only as deeply as the task needs. Routine work still gets to be routine.

I'm [Zach Stern](https://github.com/SternOne). AI tools write the code. I decide what each project is for and check what comes back. On this project those tools have included Claude, Codex, Cursor and Kimi. For version 7, I wanted to fix three problems: agents skipping a method that applied, piling process onto routine work, and stopping before the work was finished. A Codex agent built version 7 and reviewed it at my direction, so that review was not independent. [Read the case study](https://zms-labs.github.io/showcase/case-studies/epistemic-skills/) on the ZMS Labs showcase.

### A small made-up example

> Request: “The setting is saved, but it resets after reload. Fix it.”
>
> What helps: Triage, the suite's method for finding what caused a failure, works out whether the save failed or the page is showing an old value. The agent then makes the fix it was asked for, reloads, and sees the new value stick. Its final answer says what it fixed and what it checked.

Triage did one job inside the task, and the agent mentioned it in a sentence before carrying on. Because the request was to fix it, finding the cause did not end the job. [Workflow Recipes](Workflow-Recipes.md) walks through the full version of this example step by step.

### Where to go next

| If you want to… | Go to |
|---|---|
| Try the suite on a real task | [Start Here](Start-Here.md) |
| Find the right method quickly | [Skill Catalog](Skill-Catalog.md) |
| See why similar methods are kept separate | [How the Pieces Fit](How-the-Pieces-Fit.md) |
| Read three worked examples, including where each one stops | [Workflow Recipes](Workflow-Recipes.md) |
| See why it is built this way | [Design Rationale](Design-Rationale.md) |
| See what has been tested and what has not | [Testing and Evaluations](Testing-and-Evaluations.md) |
| Install it or fix a setup problem | [Installation and Harness Compatibility](Installation-and-Harness-Compatibility.md) · [FAQ and Troubleshooting](FAQ-and-Troubleshooting.md) |
| Maintain or change the project | [Maintainer guide](https://github.com/ZMS-Labs/epistemic-skills/blob/main/docs/MAINTAINING.md) |

[v7.1.0 release notes](https://github.com/ZMS-Labs/epistemic-skills/releases/tag/v7.1.0) · [Publication record (JSON file)](https://github.com/ZMS-Labs/epistemic-skills/releases/download/v7.1.0/publication-receipt.json) · [Core Concepts](Core-Concepts.md)
