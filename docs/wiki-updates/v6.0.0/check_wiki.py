#!/usr/bin/env python3
"""Oracle for the public epistemic-skills wiki.

The wiki is a separate repository with no CI of its own, and until this file it
had no checker at all. That is the root cause of every wiki defect this project
has recorded: `apply_v6_updates.py` could rewrite pages, but nothing could tell
you whether the result was *correct*, so drift was found by humans reading pages
months later -- or not found.

The concrete damage a checker would have caught: `Design-History-and-Audits.md`
carries a link reading "designs, audits, and evidence in v3.0.0" whose URL points
at `tree/v5.0.0/docs`. A previous blanket version bump moved the URL and left the
text behind. Rule LINK-VERSION-AGREEMENT below exists for exactly that, and it is
why this file refuses to be replaced by a wider regex in the applier.

Expectations are DERIVED, never written down here:
  * live skill names come from `plugins/epistemic-skills/skills/`
  * retired names are imported from `.github/scripts/check_no_phantom_skills.py`
  * the current version comes from the package manifest

so this checker cannot disagree with the package it checks.

Every rule carries a NON-VACUITY control: a rule that inspects nothing passes
silently and certifies the drift it exists to catch.

Usage:
  python check_wiki.py <wiki-clone>            # structural rules, offline
  python check_wiki.py <wiki-clone> --links    # also HTTP-resolve every URL
  python check_wiki.py --self-test             # planted RED controls
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import re
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
SKILLS_DIR = REPO / "plugins" / "epistemic-skills" / "skills"

WORDS = {12: "twelve", 13: "thirteen", 14: "fourteen", 15: "fifteen", 16: "sixteen"}


def live_skills() -> set[str]:
    return {d.name for d in SKILLS_DIR.iterdir() if d.is_dir() and (d / "SKILL.md").is_file()}


def retired_skills() -> dict[str, str]:
    """Imported from the shipped checker so the two lists cannot drift apart."""
    src = REPO / ".github" / "scripts" / "check_no_phantom_skills.py"
    spec = importlib.util.spec_from_file_location("_phantom", src)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return dict(mod.RETIRED)


def current_version() -> str:
    data = json.loads((REPO / "plugins" / "epistemic-skills" / ".claude-plugin"
                       / "plugin.json").read_text(encoding="utf-8"))
    return data["version"]


def page_slug(skill: str) -> str:
    special = {"evidence-locked-uat": "Skill-Evidence-Locked-UAT"}
    if skill in special:
        return special[skill]
    return "Skill-" + "-".join(w.capitalize() for w in skill.split("-"))


# --- rules ------------------------------------------------------------------

APPLIES_TO = re.compile(r"\*\*Applies to:\*\*\s+epistemic-skills\s+v(\d+\.\d+\.\d+)")
MD_LINK = re.compile(r"\[([^\]]+)\]\((https?://[^)]+)\)")
VER_IN_TEXT = re.compile(r"\bv(\d+\.\d+\.\d+)\b")
URL_VER = re.compile(r"/(?:tree|blob|releases/tag)/v(\d+\.\d+\.\d+)")
COUNT_NEAR = re.compile(
    r"\b(twelve|thirteen|fourteen|fifteen|sixteen)\b\s+(skills|disciplines)", re.I)


def check(wiki: Path, version: str, live: set[str], retired: dict[str, str],
          check_links: bool) -> list[str]:
    fail: list[str] = []
    pages = sorted(wiki.glob("*.md"))
    if not pages:
        return [f"VACUOUS: no *.md pages under {wiki}"]

    n_skills = len(live)
    n_disc = n_skills - 1
    ok_words = {WORDS[n_skills], WORDS[n_disc]}

    # RULE 1 -- every live skill has a page; no orphan Skill-* page.
    slugs = {p.stem for p in pages}
    for s in sorted(live):
        if page_slug(s) not in slugs:
            fail.append(f"SKILL-PAGE-MISSING: live skill {s!r} has no {page_slug(s)}.md")
    known = {page_slug(s) for s in live} | {page_slug(s) for s in retired}
    for p in sorted(slugs):
        if p.startswith("Skill-") and p != "Skill-Catalog" and p not in known:
            fail.append(f"SKILL-PAGE-ORPHAN: {p}.md names no live or retired skill")

    # RULE 2 -- version banner is current on every page that carries one.
    banners = 0
    for p in pages:
        for m in APPLIES_TO.finditer(p.read_text(encoding="utf-8")):
            banners += 1
            if m.group(1) != version:
                fail.append(f"STALE-BANNER: {p.name} applies-to v{m.group(1)}, expected v{version}")
    if banners == 0:
        fail.append("VACUOUS: no 'Applies to:' banner found on any page")

    # RULE 3 -- spelled counts match the derived inventory, UNLESS the line names
    # the past version it describes.
    #
    # A wiki legitimately carries history: "v5.0.0 shipped fourteen skills" is
    # true and must stay true. Forcing every count to the current inventory would
    # rewrite that sentence into a lie -- the mirror image of the drift this rule
    # exists to catch. So the exemption is not "looks historical", which is
    # unfalsifiable, but "states its own version on the same line", which is
    # checkable and forces the writer to say which release they mean.
    counts = 0
    exempt = 0
    for p in pages:
        for ln in p.read_text(encoding="utf-8").splitlines():
            for m in COUNT_NEAR.finditer(ln):
                counts += 1
                word, noun = m.group(1).lower(), m.group(2).lower()
                want = WORDS[n_skills] if noun == "skills" else WORDS[n_disc]
                if word == want:
                    continue
                past = [v for v in VER_IN_TEXT.findall(ln) if v != version]
                if past:
                    exempt += 1
                    continue
                fail.append(f"STALE-COUNT: {p.name} says {word!r} {noun}, expected {want!r} "
                            f"({n_skills} skills = 1 entry point + {n_disc} disciplines). "
                            f"If this describes a past release, name that version on the same line.")
    if counts == 0:
        fail.append("VACUOUS: no spelled skill/discipline count found anywhere")

    # RULE 4 -- LINK-VERSION-AGREEMENT. If link text names a version and the URL
    # names a version, they must be the same version. This is the rule a blanket
    # bump violates, and the reason this checker exists.
    checked_links = 0
    for p in pages:
        for m in MD_LINK.finditer(p.read_text(encoding="utf-8")):
            text, url = m.group(1), m.group(2)
            uv, tv = URL_VER.search(url), VER_IN_TEXT.search(text)
            if not uv:
                continue
            checked_links += 1
            if tv and tv.group(1) != uv.group(1):
                fail.append(f"LINK-VERSION-MISMATCH: {p.name} link text says v{tv.group(1)} "
                            f"but URL points at v{uv.group(1)} -- {text[:58]!r}")
    if checked_links == 0:
        fail.append("VACUOUS: no versioned GitHub URL found to check")

    # RULE 5 -- retired seats are not described in the present tense.
    # The verb must not be negated. "`helix` is not a live skill" is the CORRECT
    # way to describe a retired seat, and an earlier form of this rule flagged it
    # -- 9 false positives against 1 true one. A rule that fires on the correct
    # phrasing trains writers to avoid the correct phrasing.
    #
    # The rule reads the VISIBLE text -- a Markdown link's label, not its raw
    # `[text](target)` spelling -- and ignores capitalisation. The raw-text,
    # case-sensitive form could not see "[Helix](Helix-Central-Passage) is the
    # central passage", the exact sentence the published Contributing page
    # carried, so the gate false-greened on the one real defect it had caught
    # in prose review. Precision is kept by the same constraints as before:
    # word boundaries, a verb immediately after the name, and the negation
    # lookahead.
    #
    # Two exemptions, both checkable and both in the spirit of STALE-COUNT's
    # "states its own version on the same line": a line that names a date or a
    # past version is history recording itself (the design-history table), and
    # a page that opens with the "**Historical page.**" banner has already
    # told the reader the seat is not live -- the retired seat's own retained
    # page is exactly that case.
    RETIRED_PRESENT = re.compile(
        r"\b(" + "|".join(re.escape(k) for k in retired) + r")\b`?\s+"
        r"(?:is|selects|owns|routes|hands)\b(?!\s+(?:not|no longer|never))",
        re.IGNORECASE)
    ANY_LINK = re.compile(r"\[([^\]]+)\]\([^)]*\)")
    DATED_LINE = re.compile(r"\b\d{4}-\d{2}-\d{2}\b")
    for p in pages:
        text = p.read_text(encoding="utf-8")
        if "**Historical page.**" in text:
            continue
        for ln in ANY_LINK.sub(r"\1", text).splitlines():
            if DATED_LINE.search(ln):
                continue
            if any(v != version for v in VER_IN_TEXT.findall(ln)):
                continue
            for m in RETIRED_PRESENT.finditer(ln):
                fail.append(f"RETIRED-PRESENT-TENSE: {p.name} -- {m.group(0)!r}")

    # RULE 6 -- optional live link resolution.
    if check_links:
        import urllib.request, urllib.error
        seen: dict[str, int] = {}
        for p in pages:
            for m in MD_LINK.finditer(p.read_text(encoding="utf-8")):
                url = m.group(2)
                if "github.com/ZMS-Labs/epistemic-skills" not in url:
                    continue
                if url in seen:
                    code = seen[url]
                else:
                    try:
                        req = urllib.request.Request(url, method="HEAD")
                        with urllib.request.urlopen(req, timeout=25) as r:
                            code = r.status
                    except urllib.error.HTTPError as e:
                        code = e.code
                    except Exception:
                        code = -1
                    seen[url] = code
                if code < 0:
                    # A request that could not COMPLETE (timeout, DNS failure,
                    # connection reset) was mapped to -1 and then passed the
                    # `code >= 400` test, while the summary line below counted
                    # it among "resolved" URLs. The scheduled live job stayed
                    # green over links nobody checked. "A rule that cannot go
                    # red is not a rule" -- this one could not go red for the
                    # most common failure of a network probe.
                    fail.append(
                        f"UNREACHABLE: {p.name} -> request did not complete "
                        f"{url}")
                elif code >= 400:
                    fail.append(f"DEAD-LINK: {p.name} -> HTTP {code} {url}")
        if not seen:
            fail.append("VACUOUS: --links resolved no URLs")
        else:
            # Count RESOLVED and UNREACHABLE separately. The old line counted
            # every attempted URL as "resolved", including the ones whose
            # request never completed -- the summary asserting coverage the
            # probe did not have.
            unreachable = sum(1 for c in seen.values() if c < 0)
            print(f"  resolved {len(seen) - unreachable} distinct repository "
                  f"URLs ({unreachable} UNREACHABLE)")

    print(f"  {len(pages)} pages | {banners} banners | {counts} counts | "
          f"{checked_links} versioned links | {exempt} historical counts | expecting v{version}, "
          f"{n_skills} skills / {n_disc} disciplines")
    return fail


def self_test() -> int:
    """Planted RED controls: every rule must fail on a seeded defect, and the
    clean fixture must pass. A rule that cannot go red is not a rule."""
    live, retired, version = live_skills(), retired_skills(), current_version()
    n = len(live)
    good_pages = {
        "Home.md": (f"> **Applies to:** epistemic-skills v{version}\n\n"
                    f"Ships {WORDS[n]} skills and {WORDS[n-1]} disciplines.\n"
                    f"[the v{version} tree](https://github.com/ZMS-Labs/epistemic-skills/tree/v{version}/x)\n"),
    }
    for s in live:
        good_pages[f"{page_slug(s)}.md"] = f"> **Applies to:** epistemic-skills v{version}\n\n# {s}\n"

    cases = [
        ("clean fixture passes", {}, None),
        ("stale banner", {"Home.md": good_pages["Home.md"].replace(
            f"epistemic-skills v{version}", "epistemic-skills v1.0.0", 1)}, "STALE-BANNER"),
        ("stale count", {"Home.md": good_pages["Home.md"].replace(
            f"{WORDS[n]} skills", f"{WORDS[n-2]} skills", 1)}, "STALE-COUNT"),
        ("link text/URL version mismatch", {"Home.md": good_pages["Home.md"].replace(
            f"[the v{version} tree]", "[the v3.0.0 tree]", 1)}, "LINK-VERSION-MISMATCH"),
        ("missing live skill page", {page_slug(sorted(live)[0]) + ".md": None}, "SKILL-PAGE-MISSING"),
        ("orphan skill page", {"Skill-Nonexistent-Thing.md":
                               f"> **Applies to:** epistemic-skills v{version}\n"}, "SKILL-PAGE-ORPHAN"),
        ("historical count naming its version is allowed", {"Home.md": good_pages["Home.md"]
          + f"\nv5.0.0 shipped {WORDS[n-1]} skills.\n"}, None),
        ("historical count NOT naming its version is caught", {"Home.md": good_pages["Home.md"]
          + f"\nIt shipped {WORDS[n-1]} skills.\n"}, "STALE-COUNT"),
        ("retired seat in present tense", {"Home.md": good_pages["Home.md"]
                                           + "\n`helix` is the central passage.\n"}, "RETIRED-PRESENT-TENSE"),
        # The published Contributing page carried exactly this shape --
        # "[Helix](Helix-Central-Passage) is the central passage ..." -- and the
        # raw-text, case-sensitive rule could not see it: the gate false-greened
        # on the one real defect it existed to catch.
        ("retired seat behind a Markdown link and capitalisation",
         {"Home.md": good_pages["Home.md"]
          + "\n[Helix](Helix-Central-Passage) is the central passage.\n"}, "RETIRED-PRESENT-TENSE"),
        ("retired seat correctly negated is NOT flagged", {"Home.md": good_pages["Home.md"]
                                           + "\n`helix` is not a live skill; removed in v5.0.0.\n"}, None),
        ("negation survives Markdown and capitalisation too", {"Home.md": good_pages["Home.md"]
          + "\nHistorical [Helix](Helix-Central-Passage) is not a live seat.\n"}, None),
        ("a dated line is history, not present tense", {"Home.md": good_pages["Home.md"]
          + "\n| 2026-07-20 | helix design | Helix is the central passage, not the router. |\n"}, None),
        # The retired seat's own retained page opens with a banner that already
        # tells the reader the seat is not live; its body legitimately describes
        # the historical design in the present tense.
        ("a banner-marked historical page may use present tense",
         {"Skill-Helix.md": "> **Historical page.** `helix` is not a live skill.\n\n"
                            "# Helix\n\nHelix is the sole guide to the central passage.\n"},
         None),
        ("empty wiki is vacuous, not clean", {"__WIPE__": None}, "VACUOUS"),
    ]
    failures = 0
    for name, mutation, expect in cases:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            wipe = "__WIPE__" in mutation
            if not wipe:
                for fn, body in good_pages.items():
                    (root / fn).write_text(body, encoding="utf-8")
                for fn, body in mutation.items():
                    if body is None:
                        (root / fn).unlink(missing_ok=True)
                    else:
                        (root / fn).write_text(body, encoding="utf-8")
            out = check(root, version, live, retired, check_links=False)
            hit = any(expect in f for f in out) if expect else not out
            if hit:
                print(f"[PASS] {name}")
            else:
                failures += 1
                print(f"[FAIL] {name}: expected {expect!r}, got {out[:3]}")

    # THE LINK RULE HAD NO PLANTED CONTROL AT ALL: every case above runs with
    # check_links=False, so the one rule that reaches the network was the one
    # rule never proven able to go red. Both directions are planted here, with
    # `urlopen` replaced -- no network in the self-test.
    import urllib.error
    import urllib.request

    class _Resp:
        status = 200

        def __enter__(self):
            return self

        def __exit__(self, *exc):
            return False

    link_cases = [
        ("live link resolves", lambda *a, **k: _Resp(), None),
        # A request that could not COMPLETE used to be mapped to -1 and then
        # pass the `code >= 400` test, while the summary line counted it among
        # "resolved" URLs -- the scheduled live job green over an unchecked
        # link.
        ("unreachable link is a failure",
         lambda *a, **k: (_ for _ in ()).throw(OSError("name resolution")),
         "UNREACHABLE"),
        ("404 link is still a failure",
         lambda *a, **k: (_ for _ in ()).throw(
             urllib.error.HTTPError("u", 404, "gone", None, None)),
         "DEAD-LINK"),
    ]
    real_urlopen = urllib.request.urlopen
    for name, fake, expect in link_cases:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for fn, body in good_pages.items():
                (root / fn).write_text(body, encoding="utf-8")
            urllib.request.urlopen = fake
            try:
                out = check(root, version, live, retired, check_links=True)
            finally:
                urllib.request.urlopen = real_urlopen
        hit = any(expect in f for f in out) if expect else not out
        if hit:
            print(f"[PASS] {name}")
        else:
            failures += 1
            print(f"[FAIL] {name}: expected {expect!r}, got {out[:3]}")

    print(f"check_wiki self-test: {'PASS' if not failures else 'FAIL'}")
    return 1 if failures else 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("wiki", nargs="?")
    ap.add_argument("--links", action="store_true", help="HTTP-resolve every repository URL")
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()
    if args.self_test:
        return self_test()
    if not args.wiki:
        ap.error("a wiki clone path is required unless --self-test")
    root = Path(args.wiki)
    if not root.is_dir():
        ap.error(f"not a directory: {root}")
    fail = check(root, current_version(), live_skills(), retired_skills(), args.links)
    for f in fail:
        print(f"  {f}")
    print(f"wiki gate: {'PASS' if not fail else f'FAIL ({len(fail)} defects)'}")
    return 1 if fail else 0


if __name__ == "__main__":
    sys.exit(main())
