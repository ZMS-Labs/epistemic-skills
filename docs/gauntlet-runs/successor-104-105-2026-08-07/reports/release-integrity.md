# Lens: release-integrity / public-content

**Verdict from this lens:** GO for merge after review; item 6b remains NOT MET for immutable `v5.0.0`

## Findings

### F1 — current-tree scrubs complete

User-specific path, private repo coordinate, and private checkout identity are
generalized. Estate dispositions recorded. Pattern gate green with RED seeds.
**#105 current-tree bar met on branch.**

### F2 — mutable Release body still overclaims until amended

Immutable tag annotation still says item 6 MET. Correction of record exists in
`RELEASE-5.0.0.md` / errata / public-content review. Mutable GitHub Release body
must link those artifacts and state item 6b **NOT MET**. Prepared text:
`docs/release/RELEASE-BODY-AMEND-v5.0.0.md`. **Owner action after merge.**

### F3 — history rewrite not authorized

Identifiers/topology, not credentials. **Correct non-action.**

### F4 — repository description still advertises a router

GitHub repo `description` still says "with a router that ties them together."
Required replacement recorded in the Release-body amend doc. API update may
require owner credentials. **Open until applied.**
