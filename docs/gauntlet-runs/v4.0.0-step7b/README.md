# Step-7b cross-family consult — v4.0.0 (issue #40)

Packet `consult-packet.txt` (request GX-CONSULT-09073be6f7c94fd0) is the
cross-family adjudication owed by #40, built post-tag over the released
v4.0.0 decision. Operator hand-carry: paste the packet into a non-Anthropic
frontier model chat, send once, transcribe the reply, then:

    python plugins/epistemic-skills/skills/gauntlet/scripts/consult_packet.py \
      record --run GX-CONSULT-09073be6f7c94fd0 --response resp.json

A DISSENT escalates to the operator; it does not auto-reopen the tag.
