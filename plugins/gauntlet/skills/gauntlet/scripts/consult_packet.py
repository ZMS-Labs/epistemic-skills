#!/usr/bin/env python3
"""consult_packet.py — Step 7b external cross-family adjudication helper.

Bakes the `consult-chatgpt-pro` discipline into the gauntlet as a two-command flow.
DEFAULT MODE IS MANUAL HANDOFF: `build` emits a copy-paste-ready, secret-screened
consult packet for the operator to send to GPT-5.6 Pro in a signed-in browser; `record`
ingests the Pro reply and appends a durable external-adjudication line. No browser
automation here — the operator (or an agent's own browser control) does the send; this
tool prepares the packet safely and captures the result auditably.

stdlib only. Exit 0 on success; non-zero + a blocking message on a secret-screen hit.

Subcommands
-----------
build   --input run.json [--out packet.txt] [--stub stub.json] [--nonce STR]
        run.json shape:
          {
            "subject": "one-line subject label",
            "dossier_text": "the frozen verified dossier (or use dossier_path)",
            "dossier_path": "optional path read if dossier_text absent",
            "verdict": "GO | CONDITIONAL | NO-GO",
            "verdict_gate": "e.g. P1 clear; one P2 open -> CONDITIONAL",
            "decisive_tensions": ["ledger tension 1 (UPHELD/OVERRULED/SPLIT ...)", ...],
            "conditions": ["if CONDITIONAL: the conditions"],   # optional
            "depth": "max",                                       # advisory
            "one_way_door": true                                  # advisory
          }
        Prints the packet + a request_id derived from content (deterministic).

record  --run RUN_ID --response resp.json [--ledger runs/adjudications.jsonl]
        resp.json shape (transcribe the Pro reply into this):
          {
            "request_id": "<from the packet>",
            "external_model": "GPT-5.6 Pro",
            "reading": "CONCURRENCE | DISSENT",
            "strongest_reason_verdict_wrong": "text (required on DISSENT)",
            "confidence": "low | medium | high",
            "notes": "optional"
          }
        Appends one adjudication record. A DISSENT is flagged ESCALATE-TO-SOVEREIGN;
        it never rewrites the gauntlet verdict.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_LEDGER = ROOT / "runs" / "adjudications.jsonl"

# Secret-screen: block obvious credential material from leaving the trust boundary.
# Conservative — false positives are cheaper than a leaked secret.
SECRET_PATTERNS = [
    (re.compile(r"\bsk-[A-Za-z0-9]{16,}\b"), "openai-style key"),
    (re.compile(r"\bghp_[A-Za-z0-9]{20,}\b"), "github token"),
    (re.compile(r"\bAKIA[0-9A-Z]{16}\b"), "aws access key id"),
    (re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{10,}\b"), "slack token"),
    (re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"), "private key block"),
    (re.compile(r"(?i)\b(password|passwd|secret[_-]?key|api[_-]?key|bearer)\b\s*[:=]\s*\S+"),
     "inline credential assignment"),
]

READINGS = {"CONCURRENCE", "DISSENT"}


def secret_screen(text):
    """Return [(label, char_offset)] for each match. NEVER returns any bytes of the
    matched secret — only its type and position, so callers can report without echoing
    sensitive material (confidentiality screen)."""
    hits = []
    for rx, label in SECRET_PATTERNS:
        for m in rx.finditer(text):
            hits.append((label, m.start()))
    return hits


def request_id(subject, verdict, tensions, nonce=""):
    h = hashlib.sha256()
    h.update((subject + "\x00" + verdict + "\x00" + "\x00".join(tensions) + "\x00" + nonce).encode("utf-8"))
    return "GX-CONSULT-" + h.hexdigest()[:16]


def build_packet(run, nonce=""):
    subject = run["subject"].strip()
    verdict = run["verdict"].strip()
    tensions = [t.strip() for t in run.get("decisive_tensions", []) if t.strip()]
    dossier = run.get("dossier_text")
    if dossier is None and run.get("dossier_path"):
        dossier = Path(run["dossier_path"]).read_text(encoding="utf-8")
    dossier = (dossier or "").strip()
    conditions = run.get("conditions", [])
    gate = run.get("verdict_gate", "").strip()

    rid = request_id(subject, verdict, tensions, nonce)
    tension_block = "\n".join(f"  - {t}" for t in tensions) or "  - (none recorded)"
    cond_block = "\n".join(f"  - {c}" for c in conditions)
    cond_section = f"\nConditions attached to the verdict:\n{cond_block}\n" if conditions else ""

    packet = f"""[GAUNTLET-CONSULT request_id={rid}]

ROLE
Act as an independent expert adversary from a different reasoning tradition than the
review you are checking. Your job is to ATTACK the verdict below — find the single
strongest reason it is WRONG — not to restate or endorse it.

TASK
A frozen adversarial review ("gauntlet") reached a computed verdict on the subject
below. Decide whether you CONCUR with the verdict or DISSENT, and give the strongest
concrete reason the verdict could be wrong (a missed failure mode, an over/under-weighted
tension, or a category the panel did not consider).

CONTEXT AND EVIDENCE
Subject: {subject}
Computed verdict: {verdict}
Verdict gate: {gate or "(standard P1->NO-GO / P2-open->CONDITIONAL)"}{cond_section}
Decisive tensions from the conflict ledger:
{tension_block}

Frozen dossier (the only facts the review was allowed to use):
{dossier}

CONSTRAINTS
- Judge only on the dossier facts above; do not assume access to anything not provided.
- Attack the verdict; do not merely agree. If you cannot find a real reason it is wrong,
  say so explicitly and CONCUR — do not manufacture a weak objection.
- One-way-door decision: weigh the cost of being wrong in the irreversible direction.
- Confidentiality: treat everything here as scoped; add no external private data.

OUTPUT CONTRACT
- reading: CONCURRENCE or DISSENT (one word).
- strongest_reason_verdict_wrong: the single best concrete reason it could be wrong
  (required if DISSENT; if CONCURRENCE, state the closest thing to a real objection).
- confidence: low / medium / high.
- Do not claim to have inspected anything not provided above.
"""
    return rid, packet


def cmd_build(args):
    run = json.loads(Path(args.input).read_text(encoding="utf-8"))
    rid, packet = build_packet(run, nonce=args.nonce or "")
    hits = secret_screen(packet)
    if hits:
        print("BLOCKED — secret-screen hit; do NOT send. Redact these first "
              "(type + char offset only; the matched bytes are intentionally not shown):",
              file=sys.stderr)
        for label, offset in hits:
            print(f"  - {label} at char {offset}", file=sys.stderr)
        return 3
    if args.out:
        Path(args.out).write_text(packet, encoding="utf-8")
    stub = {
        "request_id": rid, "external_model": "GPT-5.6 Pro", "reading": "CONCURRENCE|DISSENT",
        "strongest_reason_verdict_wrong": "", "confidence": "low|medium|high", "notes": "",
    }
    if args.stub:
        Path(args.stub).write_text(json.dumps(stub, indent=1), encoding="utf-8")
    print(packet)
    print("\n" + "=" * 72, file=sys.stderr)
    print("MANUAL HANDOFF (default): paste the block above into a signed-in ChatGPT "
          "GPT-5.6 Pro chat, send ONCE, then transcribe the reply into a response JSON "
          "and run:  consult_packet.py record --run <run-id> --response resp.json",
          file=sys.stderr)
    print(f"request_id: {rid}", file=sys.stderr)
    return 0


def cmd_record(args):
    resp = json.loads(Path(args.response).read_text(encoding="utf-8"))
    reading = str(resp.get("reading", "")).strip().upper()
    if reading not in READINGS:
        print(f"ERROR: reading must be one of {sorted(READINGS)}, got {reading!r}", file=sys.stderr)
        return 2
    if reading == "DISSENT" and not str(resp.get("strongest_reason_verdict_wrong", "")).strip():
        print("ERROR: a DISSENT must include strongest_reason_verdict_wrong", file=sys.stderr)
        return 2
    record = {
        "run_id": args.run,
        "request_id": resp.get("request_id", ""),
        "external_model": resp.get("external_model", "GPT-5.6 Pro"),
        "reading": reading,
        "strongest_reason_verdict_wrong": resp.get("strongest_reason_verdict_wrong", ""),
        "confidence": resp.get("confidence", ""),
        "notes": resp.get("notes", ""),
        "disposition": "ESCALATE-TO-SOVEREIGN" if reading == "DISSENT" else "CONCURS-VERDICT-STANDS",
    }
    hits = secret_screen(json.dumps(record))
    if hits:
        print("BLOCKED — secret-screen hit in the response; redact before recording.", file=sys.stderr)
        return 3
    ledger = Path(args.ledger) if args.ledger else DEFAULT_LEDGER
    ledger.parent.mkdir(parents=True, exist_ok=True)
    with ledger.open("a", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")
    print(f"recorded {reading} for run {args.run} -> {record['disposition']}")
    if reading == "DISSENT":
        print("ESCALATE-TO-SOVEREIGN: the external adversary dissents. The computed verdict "
              "is unchanged; the operator decides whether to override.")
    return 0


def main():
    ap = argparse.ArgumentParser(description="Gauntlet Step 7b external adjudication helper")
    sub = ap.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("build", help="assemble a secret-screened consult packet (manual handoff default)")
    b.add_argument("--input", required=True)
    b.add_argument("--out")
    b.add_argument("--stub")
    b.add_argument("--nonce", default="")
    b.set_defaults(fn=cmd_build)
    r = sub.add_parser("record", help="record the Pro reply as concurrence/dissent")
    r.add_argument("--run", required=True)
    r.add_argument("--response", required=True)
    r.add_argument("--ledger")
    r.set_defaults(fn=cmd_record)
    args = ap.parse_args()
    return args.fn(args)


if __name__ == "__main__":
    raise SystemExit(main())
