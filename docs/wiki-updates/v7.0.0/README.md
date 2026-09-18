# Handbook source and v7.0.0 publication

`pages/` is the **complete 47-page v7.0.0 handbook snapshot**, prepared for
publication. It is not a delta against the old v5 handbook. The GitHub Wiki is a
separate repository; editing this directory does not publish it.

As verified on 2026-09-18, the live wiki contains the corrected v6 snapshot at
`4bfd64e4c26e9bee039cf3e56d8362d73986050f`. Its snapshot and live-link checks
passed in [run 35387408694](https://github.com/ZMS-Labs/epistemic-skills/actions/runs/35387408694).
The v7 snapshot has not yet been published. Its status changes only after a
separate wiki push and live verification.

## Validate the prepared snapshot

```bash
python docs/wiki-updates/v7.0.0/check_wiki.py --self-test
python docs/wiki-updates/v7.0.0/apply_v7_updates.py --self-test
python docs/wiki-updates/v7.0.0/check_wiki.py docs/wiki-updates/v7.0.0/pages --links
```

The snapshot's banners describe the proposed v7 package while current source
links retain the published v6 install reference. `RELEASING.md` RG-4 explicitly
distinguishes those values. Before tagging, the snapshot check is candidate
integrity evidence; a new-version check against the still-v6 live wiki is not
proof of v7 publication.

## Publish after the release tag exists

1. Verify that `v7.0.0` exists and each intended tagged source path resolves.
2. Rotate current installation and navigation links alongside `INSTALL_REF_PIN`,
   README recipes, and the Kimi marketplace source. Leave historical citations
   on the versions they describe.
3. Copy the reviewed complete `pages/` snapshot to a clean wiki checkout. Inspect
   the diff and run the same checker with `--links` against that checkout.
4. Commit and push the wiki, then run the hosted live-wiki check. Record the wiki
   commit, source commit, and successful check in the publication receipt.

`apply_v7_updates.py` is a limited migration helper. It updates counts and
banners and copies the Manifest page; it does not replace the complete snapshot
or blindly rotate tagged URLs. Its `--apply` mode checks that the target tag
exists. The self-test covers these boundaries. Do not treat running the helper
as evidence that all pages have been published.

## Completion evidence

The published wiki must show fifteen skills and fourteen disciplines, include
`Skill-Manifest`, describe retired seats historically, and provide reachable v7
installation/navigation links. A passing live check and the recorded wiki commit
establish that this snapshot landed. The earlier v6 publication and its checks
remain separate historical evidence.
