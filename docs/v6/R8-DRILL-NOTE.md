# R8 ready-mark drill (throwaway)

This branch exists only to execute the gauntlet R8 acceptance drill: open
as a DRAFT PR (gating jobs must report skipped), then mark ready with no
new push (each gating workflow must dispatch at the identical head SHA).
The PR is closed unmerged and the branch deleted after the transcript is
retained on the rc2 branch. The three files touched exist solely to hit
every gating workflow's path filter.
