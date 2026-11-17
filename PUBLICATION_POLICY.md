# Completed-book publication policy

## Standing user instruction

The user explicitly requested completed **Books 4 and 5 on `main`** and instructed: **publish every book to `main` as soon as that book is complete**. This publication authorization is independent of the three-chapter drafting default.

- Publish a book only after all its scheduled chapters, consequence notes, continuity checks and merged manuscript are complete and validated.
- Run the applicable chronology/reveal regressions and canon checks; verify every source once, in numeric order, with chapter END markers stripped from the merge. Preserve frozen earlier books and historical records. Do not silently normalize legacy merges.
- Make the chapter's own commit and immediate working-branch push first. Publish the completed book before drafting the next book, even when a three-chapter batch straddles the boundary.
- **Do not publish an incomplete book.** A request to continue authorizes the next three chapters, not unlimited drafting, pending lore, unapproved names or early publication of the next book.
- Use a reviewed pull request to `main`, from the session's existing working branch. Do not switch/create/rename branches, push directly to `main`, force-push or enable auto-merge. Merge the explicitly numbered PR only after its scope and checks pass.
- If the working branch already contains a later incomplete book, publish a completed-books-only snapshot. Keep every existing workspace file byte-for-byte intact; preserve the later work in history, restore it to the working branch immediately after publication, and audit its full manifest before further drafting. A squash merge keeps the incomplete book out of `main`'s tree and commit history.
- Record `main` as an ancestor of the continuing working branch only after verifying the published snapshot. Do not discard unrelated changes from `main`.
- After publication, verify `main`'s actual source inventory and merge bytes, the working branch's clean/local-tracking-live equality and the preservation of unfinished work.

## Initial completed-book scope

| Book | Chapters | Sources | Words | Metadata |
|---|---|---:|---:|---|
| 4 | 61–80 | 20 | 89,189 | Neutral `book-04`; subtitle unassigned |
| 5 | 81–100 | 20 | 86,980 | Neutral `book-05`; subtitle unassigned |

This publication uses the validated Book5-completion snapshot `77735cdb633cec4f98b4b8ee4f0417032b4f1f3b`, with this policy and its publication audit added. It contains **no `book-06/` manuscript**. The previously written Book6 work remains on the working branch and is not a completed book.

Historical notes saying “no main publication” describe their earlier requests; this later explicit instruction authorizes the completed-book publication without rewriting those notes or any story text.
