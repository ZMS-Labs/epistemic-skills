# mission-custody contract@2 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Close the two schema-shaped integrity gaps in mission-custody@1 — receipts are unchained, and the tail checkpoint is anchored by nothing — without breaking any existing @1 mission.

**Architecture:** A new `checkpoint@2` record whose `receipt_ids` entries carry `{request_id, receipt_sha256}`, so receipt content is covered by the checkpoint hash chain. Plus a user-level anchor file, outside the workspace, gated **inside `MissionStore.write_checkpoint`** against the same bytes that produce `prev_checkpoint_sha256`. Migration is an append-only epoch boundary inside one chain: the @1 prefix stays byte-identical.

**Tech Stack:** Python 3.12 stdlib only. No third-party deps anywhere in `contracts/mission-custody/`. Tests are hand-rolled `check(name, cond)` suites run as plain scripts, not pytest.

## Global Constraints

- **Stdlib only.** No new imports outside the standard library, in code or tests.
- **No partial deployment.** The two halves ship together. Receipt shas admitted on the tail are editable without the anchor, so gap-1-alone restores the full P6 defeat with one extra file touch.
- **Empty declarations stay unbounded.** Every existing mission has `scope.in=[]`; nothing added here may make an existing mission unable to close.
- **@1 chains keep working, unmigrated, forever.** Migration is never automatic.
- **The @1 prefix is byte-identical after migration.** Never rewrite history to @2.
- **Error direction:** a false block names its rule and is dischargeable; a false allow silently retires custody. When in doubt, block.
- **Windows/MSYS2 fleet.** `export MSYS_NO_PATHCONV=1 MSYS2_ARG_CONV_EXCL='*' PYTHONIOENCODING=utf-8` before any CLI invocation. Use explicit `Y:/` scratch paths — `mktemp -d` under Git Bash yields `/tmp/...` that Windows Python cannot resolve.
- **Never `str.casefold()`** for path identity — use the existing `_ascii_case_fold`.
- **Tests: assert the SPECIFIC error kind** in every manifest-tamper test. Under @2 an anchor error can fire before `_verify_manifest`, and a broad `except (CustodyError, StoreError)` will stay GREEN while testing nothing.
- **Run before every push:** `python .github/scripts/check_public_content.py` and the enforcement-language audit. Both are local, two-second commands.

## File Structure

| File | Responsibility | Change |
|---|---|---|
| `verify_mission_custody.py` | record validation, epoch classification | modify |
| `checkpoint2.schema.json` | @2 JSON schema | create |
| `custody_anchor.py` | anchor identity, file I/O, state machine | create |
| `custody_store.py` | chain + epoch monotonicity + anchor gate in `write_checkpoint` | modify |
| `custody_mission.py` | `_receipt_entries` chokepoint, RECEIPT-TAMPERED, migrate, quarantine, verdict note | modify |
| `custody_gate.py` | strictest-of guard evaluation | modify |
| `custody_hook.py` | unchanged (inherits via `run_gate`) | none |
| `custody_cli.py` | `migrate`, `anchor-repair`, `anchor-adopt`, `quarantine`, `verify --mission-id`, `--anchor-root` | modify |
| `test_custody_*.py` | per-area suites | modify |
| `examples/invalid-*.json` | invalid corpus (the validator's case table) | create ×8 |

`custody_anchor.py` is a new file rather than more `custody_store.py`, because the anchor is a distinct concern with its own identity rules and its own failure modes, and `custody_store.py` is already the chain's home.

---

### Task 1: checkpoint@2 record kind and epoch classification

**Files:**
- Modify: `plugins/epistemic-skills/contracts/mission-custody/verify_mission_custody.py`
- Create: `plugins/epistemic-skills/contracts/mission-custody/checkpoint2.schema.json`
- Create: `examples/invalid-checkpoint2-string-entry.json`, `invalid-checkpoint2-missing-sha.json`, `invalid-checkpoint2-bad-sha.json`, `invalid-checkpoint2-duplicate-id.json`, `invalid-checkpoint1-object-entry.json`, `invalid-checkpoint-epoch-too-new.json`, `invalid-checkpoint2-unknown-field.json`, `invalid-checkpoint2-entry-extra-key.json`
- Test: `test_custody_mission.py`

**Interfaces:**
- Consumes: nothing.
- Produces: `CHECKPOINT_EPOCH_MAX = 2`; `EPOCH_TOO_NEW = "EPOCH-TOO-NEW"`; `checkpoint_epoch(kind: str) -> int | None`; `validate_checkpoint2(rec: dict) -> list[str]`; `validate_record` accepts `"checkpoint@2"` and returns `["record: EPOCH-TOO-NEW ..."]` for a higher epoch.

- [ ] **Step 1: Write the failing test**

Add to `test_custody_mission.py`, and register it in `TESTS`:

```python
def test_checkpoint2_validation_table(workspace: Path) -> None:
    """The @2 record shape as a CASE TABLE, not one asserted example."""
    from verify_mission_custody import (
        validate_record, checkpoint_epoch, EPOCH_TOO_NEW)
    check("epoch-of-@1", checkpoint_epoch("checkpoint@1") == 1)
    check("epoch-of-@2", checkpoint_epoch("checkpoint@2") == 2)
    check("epoch-of-@9", checkpoint_epoch("checkpoint@9") == 9)
    check("epoch-of-non-checkpoint", checkpoint_epoch("receipt@1") is None)

    base = json.loads(json.dumps(_valid_checkpoint2_fixture()))
    check("valid-@2-clean", validate_record(base) == [])

    bad = json.loads(json.dumps(base)); bad["receipt_ids"] = ["plain-string"]
    check("@2-rejects-string-entry", validate_record(bad) != [])

    bad = json.loads(json.dumps(base)); bad["receipt_ids"] = [{"request_id": "a"}]
    check("@2-rejects-missing-sha", validate_record(bad) != [])

    bad = json.loads(json.dumps(base))
    bad["receipt_ids"] = [{"request_id": "a", "receipt_sha256": "nothex"}]
    check("@2-rejects-bad-sha", validate_record(bad) != [])

    bad = json.loads(json.dumps(base))
    bad["receipt_ids"] = [{"request_id": "a", "receipt_sha256": "0" * 64},
                          {"request_id": "a", "receipt_sha256": "1" * 64}]
    check("@2-rejects-duplicate-request-id", validate_record(bad) != [])

    bad = json.loads(json.dumps(base))
    bad["receipt_ids"] = [{"request_id": "a", "receipt_sha256": "0" * 64,
                           "extra": 1}]
    check("@2-rejects-entry-extra-key", validate_record(bad) != [])

    future = json.loads(json.dumps(base)); future["record"] = "checkpoint@3"
    errors = validate_record(future)
    check("@3-is-epoch-too-new-not-unknown-kind",
          any(EPOCH_TOO_NEW in e for e in errors))
    check("@3-does-not-read-as-unknown-kind",
          not any("unknown kind" in e for e in errors))
```

Add the fixture helper next to it:

```python
def _valid_checkpoint2_fixture() -> dict:
    """A minimal, valid checkpoint@2. Built from a real @1 open so the manifest
    is genuinely schema-valid rather than hand-approximated."""
    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        ws = Path(tmp)
        m = Mission.open(ws, "fixture", "i", "operator:t", "agent:t",
                         actor="agent:t")
        record = json.loads(json.dumps(m.status()))
    record["record"] = "checkpoint@2"
    record["receipt_ids"] = [{"request_id": "req-1", "receipt_sha256": "0" * 64}]
    return record
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd plugins/epistemic-skills/contracts/mission-custody && python test_custody_mission.py 2>&1 | grep -E "epoch-of|@2-|@3-"`
Expected: FAIL — `ImportError: cannot import name 'checkpoint_epoch'`.

- [ ] **Step 3: Write minimal implementation**

In `verify_mission_custody.py`, extend `RECORD_KINDS` and add the epoch machinery:

```python
RECORD_KINDS = {
    "mission-manifest@1",
    "checkpoint@1",
    "checkpoint@2",
    "receipt@1",
    "acceptance-verdict@1",
}

# The highest checkpoint epoch this build understands. A record from a NEWER
# epoch must be distinguishable from garbage: read as an unknown kind it makes
# the mission look CORRUPT, and discovery SKIPS corrupt siblings -- which lets
# a duplicate `open` succeed and silently disarms an armed mission.
# Present-but-unreadable and unreadable are different states.
CHECKPOINT_EPOCH_MAX = 2
EPOCH_TOO_NEW = "EPOCH-TOO-NEW"
_CHECKPOINT_KIND_RE = re.compile(r"^checkpoint@(\d+)$")

CHECKPOINT2_ENTRY_FIELDS = {"request_id", "receipt_sha256"}


def checkpoint_epoch(kind: object) -> int | None:
    """The epoch number of a checkpoint kind, or None if not a checkpoint."""
    if not isinstance(kind, str):
        return None
    match = _CHECKPOINT_KIND_RE.match(kind)
    return int(match.group(1)) if match else None
```

Add the @2 validator, reusing the @1 body for every shared field:

```python
def validate_checkpoint2(rec: dict) -> list[str]:
    """@2 differs from @1 in exactly one field: receipt_ids entries are
    {request_id, receipt_sha256} objects rather than bare id strings."""
    errors: list[str] = []
    _check_exact_fields(errors, rec, CHECKPOINT_FIELDS, "checkpoint")
    if errors:
        return errors
    entries = rec["receipt_ids"]
    if not isinstance(entries, list):
        errors.append("receipt_ids: list of {request_id, receipt_sha256} required")
    else:
        seen: set[str] = set()
        for i, entry in enumerate(entries):
            where = f"receipt_ids[{i}]"
            if not isinstance(entry, dict) or set(entry) != CHECKPOINT2_ENTRY_FIELDS:
                errors.append(
                    f"{where}: exactly {{request_id, receipt_sha256}} required")
                continue
            if not (isinstance(entry["request_id"], str) and entry["request_id"]):
                errors.append(f"{where}.request_id: non-empty string required")
            elif entry["request_id"] in seen:
                # one id, one current entry: duplicates make "the sha for this
                # id" ambiguous, and an auditor cannot resolve it
                errors.append(f"{where}.request_id: duplicate in this list")
            else:
                seen.add(entry["request_id"])
            if not is_sha256(entry["receipt_sha256"]):
                errors.append(f"{where}.receipt_sha256: 64-hex sha256 required")
    # every other field validates exactly as @1
    shared = dict(rec)
    shared["record"] = "checkpoint@1"
    shared["receipt_ids"] = []
    errors.extend(e for e in validate_checkpoint(shared)
                  if not e.startswith("receipt_ids"))
    return errors
```

Rewrite the dispatcher:

```python
def validate_record(record: Any) -> list[str]:
    if not isinstance(record, dict):
        return ["record: JSON object required"]
    kind = record.get("record")
    epoch = checkpoint_epoch(kind)
    if epoch is not None and epoch > CHECKPOINT_EPOCH_MAX:
        # NOT "unknown kind": a caller must be able to tell "written by a newer
        # build" from "corrupt", because discovery treats those differently.
        return [f"record: {EPOCH_TOO_NEW}: {kind!r} is newer than this build "
                f"understands (max checkpoint@{CHECKPOINT_EPOCH_MAX})"]
    if kind not in RECORD_KINDS:
        return [f"record: unknown kind {kind!r}"]
    if kind == "mission-manifest@1":
        return validate_manifest(record)
    if kind == "checkpoint@1":
        return validate_checkpoint(record)
    if kind == "checkpoint@2":
        return validate_checkpoint2(record)
    if kind == "receipt@1":
        return validate_receipt(record)
    return validate_acceptance_verdict(record)
```

Create `checkpoint2.schema.json` mirroring `checkpoint.schema.json`, with:

```json
"receipt_ids": {
  "type": "array",
  "items": {
    "type": "object",
    "required": ["request_id", "receipt_sha256"],
    "additionalProperties": false,
    "properties": {
      "request_id": {"type": "string", "minLength": 1},
      "receipt_sha256": {"type": "string", "pattern": "^[0-9a-f]{64}$"}
    }
  }
}
```

Create the eight `examples/invalid-*.json` files listed under **Files**, each a copy of a valid @2 checkpoint with exactly one defect from the table above. The example corpus IS the validator's case table; `test_mission_custody.py` already asserts every `invalid-*.json` fails validation.

- [ ] **Step 4: Run tests to verify they pass**

Run: `python test_custody_mission.py 2>&1 | tail -3 && python test_mission_custody.py 2>&1 | tail -3`
Expected: `0 failures` from both.

- [ ] **Step 5: Commit**

```bash
git add plugins/epistemic-skills/contracts/mission-custody/
git commit -s -m "feat(mission-custody): checkpoint@2 record kind and epoch classification"
```

---

### Task 2: `_receipt_entries` chokepoint with latest-attestation-wins

**Files:**
- Modify: `custody_mission.py` (every reader of `["receipt_ids"]`)
- Modify: `custody_cli.py:_brief`-adjacent clean-resume summary
- Test: `test_custody_mission.py`

**Interfaces:**
- Consumes: Task 1's `checkpoint_epoch`.
- Produces: `Mission._receipt_entries(checkpoint) -> list[tuple[str, str | None]]`; `Mission._expected_sha(request_id) -> str | None` (latest chain attestation).

- [ ] **Step 1: Write the failing test**

```python
def test_receipt_entries_chokepoint(workspace: Path) -> None:
    """@1 and @2 chains normalise to the same shape, and no consumer may index
    receipt_ids directly -- a string-vs-dict comparison silently never matches,
    which is the false-clean direction."""
    m = open_mission(workspace, "m-entries", "Entries.")
    m.approve()
    m.record_effect("notes/a.md", "hello", "req-1")
    entries = m._receipt_entries(m.status())
    check("entries-normalises-@1", entries == [("req-1", None)])
    check("entries-sha-none-on-@1", entries[0][1] is None)


def test_no_raw_receipt_ids_indexing() -> None:
    """Grep guard. Four latent defects in the predecessor came from exactly
    this: a consumer comparing a string against dict entries, or hashing a
    dict, or filtering by identity that never matches."""
    source = (ROOT / "custody_mission.py").read_text(encoding="utf-8")
    offenders = []
    for i, line in enumerate(source.splitlines(), 1):
        if '["receipt_ids"]' not in line:
            continue
        if "def _receipt_entries" in line or "ALLOW-RAW-RECEIPT-IDS" in line:
            continue
        offenders.append(f"{i}: {line.strip()}")
    check("no-raw-receipt-ids-indexing", not offenders)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python test_custody_mission.py 2>&1 | grep -E "entries-|no-raw"`
Expected: FAIL — `AttributeError: 'Mission' object has no attribute '_receipt_entries'`, and the grep guard lists every current raw site.

- [ ] **Step 3: Write minimal implementation**

```python
    def _receipt_entries(self, checkpoint: dict) -> list[tuple[str, str | None]]:
        """(request_id, receipt_sha256|None) for one checkpoint, @1 or @2.

        THE single reader of receipt_ids. @1 entries are bare strings and carry
        no sha; @2 entries are objects. Every consumer goes through here,
        because a string-vs-dict comparison never matches and never raises --
        it silently reports nothing, which is the false-clean direction."""
        entries: list[tuple[str, str | None]] = []
        for entry in checkpoint["receipt_ids"]:  # ALLOW-RAW-RECEIPT-IDS
            if isinstance(entry, str):
                entries.append((entry, None))
            else:
                entries.append((entry["request_id"], entry.get("receipt_sha256")))
        return entries

    def _expected_sha(self, request_id: str) -> str | None:
        """The LATEST chain attestation for this id, not the first.

        A pre-migration id appears with sha None in @1 records and with a
        backfilled sha from the migration checkpoint onward. Taking the first
        occurrence would discard the backfill and verify at @1 strength while
        the record claims otherwise -- a silent downgrade."""
        latest: str | None = None
        for cp_path in self.store.checkpoint_paths():
            record = json.loads(cp_path.read_text(encoding="utf-8"))
            for rid, sha in self._receipt_entries(record):
                if rid == request_id and sha is not None:
                    latest = sha
        return latest
```

Then convert every raw site the grep guard reports. The known set, each with its failure mode if missed:

- `_all_receipt_ids_ever` — dict entries in a `set()` raise `TypeError`, bricking `record_effect`.
- `_historical_effect_path` — `request_id in ids` never matches, so a lost receipt's path becomes underivable.
- `resume` — iterates ids; must pass `_expected_sha(rid)` into `_load_receipt`.
- `reconcile` membership test — never matches, so the id is appended twice, producing a duplicate the @2 validator then rejects.
- `acknowledge_receipt_loss` retirement filter — removes nothing, so the retired id stays current and `resume` re-raises RECEIPT-MISSING forever: an undischargeable loop.
- `record_verdict` `receipt_refs` — must extract ids only; `acceptance-verdict@1.receipt_refs` **stays a string list** and `_str_list` rejects dicts. Do NOT "fix" the verdict schema.
- `_write_next` copy-forward and `add_receipt_id` — must carry `(id, sha)` pairs on @2.
- `custody_cli.py` clean-resume summary — `len(set(...))` over dicts raises `TypeError` on the happy path.

- [ ] **Step 4: Run tests to verify they pass**

Run: `for t in test_custody_mission.py test_custody_cli.py test_mission_custody.py test_custody_store.py; do python $t >/dev/null 2>&1 && echo "PASS $t" || echo "FAIL $t"; done`
Expected: all PASS, and the grep guard reports no offenders.

- [ ] **Step 5: Commit**

```bash
git commit -s -am "refactor(mission-custody): route every receipt_ids reader through _receipt_entries"
```

---

### Task 3: RECEIPT-TAMPERED detection

**Files:** Modify `custody_mission.py`; Test: `test_custody_mission.py`

**Interfaces:**
- Consumes: Task 2's `_expected_sha`.
- Produces: `_load_receipt(request_id, expected_sha=None)`; marker string `RECEIPT-TAMPERED:<id>`.

- [ ] **Step 1: Write the failing test**

```python
def test_probe_p6_receipt_tamper_is_caught(workspace: Path) -> None:
    """P6: edit an artifact AND its receipt's after_sha256 to match. Under @1
    resume reports clean -- the drift oracle trusts a receipt whose integrity
    nothing attests. Under @2 the chained sha catches it."""
    m = open_mission(workspace, "m-p6", "P6.")
    m.approve()
    m.record_effect("notes/a.md", "original", "p6-1")
    # Chain the receipt sha WITHOUT depending on Task 7's migrate verb: write
    # one @2 checkpoint directly. Task 3 must be testable on its own, and a
    # forward dependency on a later task would make it not so.
    latest, path = m.store.load_latest()
    sha = sha256_file(m.store.receipt_path("p6-1"))
    upgraded = json.loads(json.dumps(latest))
    upgraded["record"] = "checkpoint@2"
    upgraded["revision"] = latest["revision"] + 1
    upgraded["prev_checkpoint_sha256"] = sha256_file(path)
    upgraded["receipt_ids"] = [{"request_id": "p6-1", "receipt_sha256": sha}]
    m.store.write_checkpoint(upgraded)
    (workspace / "notes" / "a.md").write_text("tampered", encoding="utf-8")
    receipt_path = m.store.receipt_path("p6-1")
    record = json.loads(receipt_path.read_text(encoding="utf-8"))
    record["after_sha256"] = sha256_bytes(b"tampered")
    receipt_path.write_text(json.dumps(record, indent=1, sort_keys=True) + "\n",
                            encoding="utf-8")
    findings = m.resume()
    check("p6-caught-as-tampered",
          any(f == "RECEIPT-TAMPERED:p6-1" for f in findings))
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python test_custody_mission.py 2>&1 | grep p6-`
Expected: FAIL — `resume` returns `[]` (the @1 blind spot, reproduced).

- [ ] **Step 3: Write minimal implementation**

```python
    def _load_receipt(self, request_id: str,
                      expected_sha: str | None = None) -> dict | None:
        path = self.store.receipt_path(request_id)
        try:
            raw = path.read_bytes()
        except FileNotFoundError:
            return None
        if expected_sha is not None and sha256_bytes(raw) != expected_sha:
            # TAMPERED is distinct from unloadable: the file parses and
            # validates, it simply is not the receipt the chain attested.
            raise _ReceiptTampered(request_id)
        try:
            record = json.loads(raw.decode("utf-8"))
        except (ValueError, UnicodeDecodeError):
            return None
        if validate_record(record):
            return None
        return record if record.get("request_id") == request_id else None
```

with a module-private signal class and a `resume` branch that appends
`RECEIPT-TAMPERED:<id>` to findings and to `unresolved_verdicts`, reopening the
mission exactly as RECEIPT-MISSING does. `acknowledge_receipt_loss` accepts the
new marker; with a chained sha, "restored" becomes byte-provable (the file at
the id's path hashing to the chained sha IS the original), which is strictly
stronger than @1's path-match heuristic — keep that heuristic as the fallback
for `None`-sha ids.

- [ ] **Step 4: Run tests to verify they pass**

Run: `python test_custody_mission.py 2>&1 | tail -3`
Expected: `0 failures`.

- [ ] **Step 5: Commit**

```bash
git commit -s -am "feat(mission-custody): RECEIPT-TAMPERED closes probe P6"
```

---

### Task 4: `custody_anchor.py` — identity, file, state machine

**Files:** Create `custody_anchor.py`; Create `test_custody_anchor.py`

**Interfaces:**
- Consumes: nothing.
- Produces: `anchor_root(override: str | None = None) -> Path`; `mission_key(mission_dir: Path) -> str`; `read_anchor(key, root)`; `write_anchor(key, root, record) -> bool`; `AnchorState` (a str enum-like: `"verified" | "lagging" | "absent" | "mismatch"`); `classify(anchor, tail_sha, chain_shas) -> AnchorState`; `AnchorMismatch(StoreError)`.

- [ ] **Step 1: Write the failing test**

The state machine as a case table:

```python
def test_anchor_state_table() -> None:
    from custody_anchor import classify
    chain = ["aa" * 32, "bb" * 32, "cc" * 32]      # r1, r2, r3; tail = cc
    tail = chain[-1]
    cases = [
        ("verified",  {"checkpoint_sha256": tail, "revision": 3}, "verified"),
        ("lagging-1", {"checkpoint_sha256": chain[1], "revision": 2}, "lagging"),
        ("lagging-2", {"checkpoint_sha256": chain[0], "revision": 1}, "lagging"),
        ("ahead",     {"checkpoint_sha256": "dd" * 32, "revision": 9}, "mismatch"),
        ("forked",    {"checkpoint_sha256": "ee" * 32, "revision": 2}, "mismatch"),
        ("absent",    None, "absent"),
    ]
    for name, anchor, want in cases:
        check(f"anchor-state-{name}", classify(anchor, tail, chain) == want)


def test_mission_key_is_stable_across_path_spellings(tmp: Path) -> None:
    """Y: is a mapped UNC share on this fleet and NTFS is case-insensitive, so
    one directory has several honest spellings. A key that varies by spelling
    mints parallel anchors, each TOFU-adopting independently -- quiet erosion."""
    from custody_anchor import mission_key
    a = mission_key(tmp / "missions" / "m")
    b = mission_key(Path(str(tmp).upper()) / "missions" / "m")
    check("mission-key-case-stable", a == b)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python test_custody_anchor.py`
Expected: FAIL — `ModuleNotFoundError: No module named 'custody_anchor'`.

- [ ] **Step 3: Write minimal implementation**

```python
def classify(anchor: dict | None, tail_sha: str,
             chain_shas: list[str]) -> str:
    """verified | lagging | absent | mismatch.

    NO auto-advance. A lagging anchor is the legitimate-crash shape AND the
    forged-append shape, and they are byte-identical: `prev_checkpoint_sha256`
    is computable from the readable tail, so an attacker constructs the lag on
    demand. Advancing onto it was rev 1's unanimous CRITICAL."""
    if anchor is None:
        return "absent"
    pinned = anchor.get("checkpoint_sha256")
    if not isinstance(pinned, str):
        return "mismatch"          # unparseable/shape-invalid NEVER means absent
    if pinned == tail_sha:
        return "verified"
    if pinned in chain_shas:
        return "lagging"           # an ANCESTOR, resolved by hash not revision
    return "mismatch"
```

Ancestry is resolved by hashing candidate files, never by comparing `revision`:
`load_latest` never validates `revision` against the filename, so an appended
file carries an attacker-chosen revision number.

`mission_key` = `sha256` of `realpath` → strip `\\?\` → `_ascii_case_fold`
(never `str.casefold`). `anchor_root` honours an explicit override only, refuses
any root resolving inside the workspace, and records `resolved_root` in the
anchor file. **`Path.home()` follows `USERPROFILE`/`HOME`, so the default root
is NOT env-free** — that is disclosed in SECURITY.md, not denied.

- [ ] **Step 4: Run tests to verify they pass**

Run: `python test_custody_anchor.py`
Expected: `all green`.

- [ ] **Step 5: Commit**

```bash
git add custody_anchor.py test_custody_anchor.py
git commit -s -m "feat(mission-custody): anchor identity and state machine"
```

---

### Task 5: anchor gate inside `write_checkpoint` + read-path epoch monotonicity

**Files:** Modify `custody_store.py`; Test: `test_custody_store.py`

**Interfaces:**
- Consumes: Task 1's `checkpoint_epoch`; Task 4's `classify`, `mission_key`, `read_anchor`, `write_anchor`.
- Produces: `MissionStore.anchor_state() -> str`; `AnchorMismatch` raised from `write_checkpoint` and `load_latest`.

- [ ] **Step 1: Write the failing test**

```python
def test_write_refuses_on_unverified_anchor(tmp: Path) -> None:
    """resume() is a WRITER (it appends on drift) and is the standard
    post-interruption verb. A verb-layer rule required judging which verbs
    write, and missing one laundered a forged append. The gate lives in
    write_checkpoint so no verb can be miscategorised."""


def test_epoch_monotonicity_on_read_path(tmp: Path) -> None:
    """The in-scope attacker writes raw files and never calls write_checkpoint,
    so write-path epoch rules do not bind them. A raw-appended checkpoint@1
    after a @2 tail strips receipt-sha coverage and would otherwise read clean."""


def test_verify_then_write_race_is_closed(tmp: Path) -> None:
    """Anchor verified at (N, sha_N); the tail is swapped before publish. The
    write must refuse rather than chain onto the forged bytes."""
```

Each with a concrete body constructing the state on disk and asserting the
specific exception type — never a broad `except (CustodyError, StoreError)`.

- [ ] **Step 2: Run test to verify it fails**

Run: `python test_custody_store.py 2>&1 | grep -E "anchor|epoch|race"`
Expected: FAIL — writes succeed against an unverified anchor.

- [ ] **Step 3: Write minimal implementation**

In `write_checkpoint`, evaluate the anchor against **the same bytes** used for
`prior_sha`, then publish, then advance-only CAS. **Revision 1 is exempt** —
`Mission.open` has no tail and no anchor, and a literal reading of the state
list would call `load_latest()` on an empty chain and make opening a mission
impossible. An anchor present over an EMPTY chain refuses at open, naming
`anchor-adopt`.

A failed anchor **advance** after a successful publish is stderr-warned and the
verb still succeeds; the alternative bricks a mission whenever the anchor root
blinks. In `load_latest`, reject a lower epoch following a higher one and more
than one 1→2 transition, keyed on **record kind only** — never on a note string,
which is mutable and attacker-writable.

- [ ] **Step 4: Run tests to verify they pass**

Run: `python test_custody_store.py 2>&1 | tail -3`
Expected: `0 failures`.

- [ ] **Step 5: Commit**

```bash
git commit -s -am "feat(mission-custody): anchor gate inside write_checkpoint; read-path epoch monotonicity"
```

---

### Task 6: `anchor-repair`, `anchor-adopt`, `quarantine`

**Files:** Modify `custody_cli.py`, `custody_mission.py`; Test: `test_custody_cli.py`

**Interfaces:**
- Consumes: Task 5's `anchor_state`.
- Produces: CLI verbs `anchor-repair`, `anchor-adopt`, `quarantine`; `Mission.quarantine(revisions) -> int`.

- [ ] **Step 1: Write the failing test**

```python
def test_anchor_repair_refuses_non_interactive() -> None:
    """The in-scope attacker can INVOKE processes, including custody verbs, so
    'a human inspects the delta' must be a MECHANISM, not an intention -- the
    estate's keystone failure is writing a control instead of installing one."""


def test_quarantine_restores_verified_and_records_shas() -> None:
    """Without a repudiation path the honest steward's only choices are adopt
    the forgery or leave the mission permanently unwritable -- pressure to click
    through, which retires the control. quarantine MOVES revisions aside
    (never deletes), the tail returns to the pinned revision, and the shas are
    recorded in a note."""
```

- [ ] **Step 2: Run test to verify it fails** — verbs do not exist; argparse exits 2.

- [ ] **Step 3: Write minimal implementation** — `anchor-repair` proves the pinned checkpoint is an ancestor **by hash**, prints the full per-revision delta (amendments, guard changes, receipt admissions, status transitions, frontier, **plus `written_by` and `written_utc`** — a forged amendment can copy the operator's words verbatim, so a foreign actor string or a timestamp gap is the discriminator a human actually has), then advances. It refuses on non-interactive stdin and offers **no `--yes` flag**.

- [ ] **Step 4: Run tests to verify they pass** — `python test_custody_cli.py`.

- [ ] **Step 5: Commit**

```bash
git commit -s -am "feat(mission-custody): anchor-repair, anchor-adopt, quarantine"
```

---

### Task 7: `migrate` — does not bless

**Files:** Modify `custody_mission.py`, `custody_cli.py`; Test: `test_custody_mission.py`

**Interfaces:**
- Consumes: Tasks 1–5.
- Produces: `Mission.migrate() -> int`; reserved note prefix `"contract migrated: "`.

- [ ] **Step 1: Write the failing test** — the precondition matrix as a case table: refuses on drift; refuses on an unreconciled continuity break; refuses when a receipt's `artifact_path` disagrees with the chain's recorded effect path; refuses without a prior operator-consent amendment; refuses when already @2; succeeds otherwise, backfilling `{id, sha}` for every current receipt and appending exactly one migration note.

- [ ] **Step 2: Run test to verify it fails** — `AttributeError: 'Mission' object has no attribute 'migrate'`.

- [ ] **Step 3: Write minimal implementation** — the drift check uses a **non-mutating** probe: `resume()` writes on drift (`custody_mission.py` appends a reopened checkpoint), so a mutating probe would move the tail mid-precondition. Backfilled shas attest receipts **as of migration time only** and inherit every @1 blind spot including P6 — state that in the note and the README, because a single-receipt path has no continuity neighbour (`zip(ids, ids[1:])` is empty for one id) and no runtime check can see that case.

- [ ] **Step 4: Run tests to verify they pass**

- [ ] **Step 5: Commit**

```bash
git commit -s -am "feat(mission-custody): migrate verb, append-only epoch boundary"
```

---

### Task 8: gate strictest-of + status refusal + discovery EpochTooNew

**Files:** Modify `custody_gate.py`, `custody_mission.py`; Test: `test_custody_gate.py`, `test_custody_hook.py`

**Interfaces:**
- Consumes: Tasks 4–5.
- Produces: `run_gate` evaluating strictest-of(pinned, tail).

- [ ] **Step 1: Write the failing test**

```python
def test_lagging_anchor_cannot_disarm_a_just_armed_guard() -> None:
    """Reachable with NO attacker. A failed anchor advance warn-and-succeeds by
    design, so the chain legitimately sits one revision ahead whenever the root
    blinks. If THAT revision is the amend that armed enforce, pinned-only reads
    the PRE-ARMING record and evaluate() returns allow/inert -- silently,
    because the guard-log only writes on a match."""


def test_forged_completed_tail_cannot_disarm_the_gate() -> None:
    """Activeness is read from the TAIL before the gate ever reads authority,
    and run_gate converts NoActiveMission into inert-allow. A forged
    status:'completed' tail therefore disarms every guard."""
```

- [ ] **Step 2: Run test to verify it fails** — both return exit 0 (allow).

- [ ] **Step 3: Write minimal implementation** — union the guard rules from pinned and tail and enforce if **either** says enforce, so a forged tail can only ever ADD restrictions (a false block, which this module's own doctrine calls the safe direction). A tail claiming `completed`/`cancelled` over an OPEN pinned record is a loud refusal, never `NoActiveMission`. `EpochTooNew` is present-but-unreadable: `open` refuses, and the gate takes the degraded-loud path — allow-with-loud-log unless the discovered mission is enforce-armed, in which case block.

- [ ] **Step 4: Run tests to verify they pass**

- [ ] **Step 5: Commit**

```bash
git commit -s -am "feat(mission-custody): strictest-of guard evaluation; forged-completed tail refused"
```

---

### Task 9: verdict in the chain + `verify --mission-id`

**Files:** Modify `custody_mission.py`, `custody_cli.py`; Test: `test_custody_mission.py`, `test_custody_cli.py`

**Interfaces:**
- Produces: note format `verdict PASS <sha256hex>: <reason>`; `"verdict "` added to `_RESERVED_NOTE_PREFIXES`; CLI `verify --mission-id`.

- [ ] **Step 1: Write the failing test** — an edited verdict file is detected; `note()` refuses a caller string beginning `"verdict "`; a COMPLETED mission is loadable through `verify --mission-id`.

- [ ] **Step 2: Run test to verify it fails** — `acceptor_id`/`assurance_tier` appear nowhere in the chain today, and **no CLI surface can load a completed mission at all** (`Mission.load` excludes completed/cancelled; every verb but `open`/`gate` routes through it; discovery is pathless by contract).

- [ ] **Step 3: Write minimal implementation** — machine fields **first**, behind a reserved prefix. `PASS: ` is not reserved, so ordinary `note()` can forge it, and `reason` is free operator text — a reason *ending* in `; verdict_sha256=<hex>` is byte-indistinguishable from a trailing machine suffix. Also reserve `"cleared: "`.

- [ ] **Step 4: Run tests to verify they pass**

- [ ] **Step 5: Commit**

```bash
git commit -s -am "feat(mission-custody): bind acceptance verdicts into the chain"
```

---

### Task 10: docs, disclosure, and the existing-suite audit

**Files:** Modify `README.md`, `SECURITY.md`, `skills/manifest/SKILL.md`; audit all `test_custody_*.py`

**Interfaces:** none produced.

- [ ] **Step 1: Audit every manifest-tamper test for the specific error kind**

`test_amendments_cannot_be_rewritten` forges by rewriting the tail **in place** and asserts `except (CustodyError, StoreError)`. Under @2, `AnchorMismatch` (a `StoreError`) fires *before* `_verify_manifest`, the broad except swallows it, and **the test stays GREEN while no longer testing the append-only check**. In-place edits erode; appends do not. Every such test must assert the specific kind or arrange the anchor onto the forged tail first.

- [ ] **Step 2: Run the full suite and both local gates**

```bash
for t in test_custody_*.py test_mission_custody.py; do python $t >/dev/null 2>&1 && echo "PASS $t" || echo "FAIL $t"; done
python ../../../../.github/scripts/check_public_content.py
python ../../evals/epistemic-flexibility/audit_enforcement_language.py
```

- [ ] **Step 3: Write the disclosures**

SECURITY.md gains: the env-redirect seam (`Path.home()` follows `USERPROFILE`/`HOME`, so the default anchor root is not env-free — mitigated by recording `resolved_root` and treating a previously-unseen root as loud, **not** denied); backfilled shas are as-of-migration only; the single-receipt P6 residue; the sanctioned-`amend` guard downgrade (`amend --text "anything" --guard-mode audit` is chain-legal because the guard rule is length-only); and that `scope` is tamper-checked but enforced by nothing.

- [ ] **Step 4: Commit**

```bash
git commit -s -am "docs(mission-custody): contract@2 disclosures and tamper-test audit"
```

---

## Rollout (not a task — an operator-gated sequence)

Pre-@2 validators reject `checkpoint@2` → `ChainBroken` → mission skipped → a duplicate `open` becomes possible. So: merge → deploy the plugin cache and **re-verify by hashing the custody files each harness actually loads** (committed ≠ deployed; do not inherit a prior session's claim) → migrate the `livefire` scratch mission as a pilot → run the UAT tamper probes (append-forge, in-place edit, receipt P6, split-path, corrupt anchor, enforce-block) → migrate `media-library-rebuild` **only with a recorded operator-consent amendment** → re-run `resume`/`audit`/`status` → receipt the results into the mission. The archived vanta tracer record stays @1.
