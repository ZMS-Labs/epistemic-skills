# Runtime role binding

Gauntlet role definitions are canonical in the plugin's `agents/` directory.
Every runtime must bind those exact definitions before dispatch; merely giving a
generic worker a similar-sounding task is not equivalent.

## Binding modes

| Mode | Use when | Required record |
|---|---|---|
| `native-agent` | The runtime discovers the packaged custom role and exposes it as a sub-agent type. | Resolved bare or namespaced agent name. |
| `materialized-role` | The runtime has isolated sub-agents but cannot register packaged custom roles. | `gauntlet-role-binding@1` JSON from `scripts/materialize_role.py`, including role, persona, dossier, and prompt hashes. |

Binding mode and orchestration mode are separate. A runtime may use
`materialized-role` with a concurrent fan-out and still satisfy the standard
independence barrier. Use `orchestration: manual-degraded` only when the runtime
cannot run isolated calls concurrently.

## Runtime matrix

| Runtime | Native package path | Required behavior |
|---|---|---|
| Claude Code | Plugin-root `agents/*.md` | Resolve the plugin agent by bare or namespaced name; fall back to materialization if runtime discovery fails. |
| Cursor | `.cursor-plugin/plugin.json` declares `"agents": "./agents/"` | Resolve the plugin subagent; fall back to materialization if unavailable. |
| Gemini CLI | Extension-root `agents/*.md` (preview runtime feature) | Resolve the extension sub-agent after restarting the session; fall back to materialization if unavailable. |
| Codex | Codex plugins do not register plugin-defined collaboration agent types; Codex does discover user-agent TOML files | Run `scripts/render_codex_agents.py --out ~/.codex/agents`, then start a new task and resolve the native role. Until restart or if registration is unavailable, use materialization. |
| Antigravity | Native plugin/import discovery processes the root `agents/*.md` tree | Resolve the imported plugin agent; fall back to materialization if runtime discovery fails. |
| Other harnesses | Harness-specific | Probe native bare/namespaced resolution first; otherwise use materialization. |

## Materialize a role

```text
python scripts/materialize_role.py \
  --role gauntlet-adversary \
  --persona prompts/script-kiddie.md \
  --dossier dossier.md \
  --out prompts/script-kiddie.binding.json
```

Dispatch only the `prompt` field from the resulting record. Keep the complete
JSON beside the report so arbitration can verify the exact role, persona,
dossier, and prompt hashes. The materializer treats dossier text as data and
adds an explicit injection boundary.

If neither native binding nor materialization can be completed, stop the panel.
Do not label an improvised generic prompt as a gauntlet role.

## Register the native roles in Codex

Codex's plugin manifest does not currently carry custom collaboration-agent
definitions. Render the five canonical Markdown roles into Codex's user registry:

```text
python scripts/render_codex_agents.py --out ~/.codex/agents
```

Start a new Codex task after rendering; the available agent-type list is fixed
when a task starts. Re-run the renderer after plugin upgrades. The renderer only
writes the five `gauntlet-*.toml` files and leaves unrelated user agents intact.
