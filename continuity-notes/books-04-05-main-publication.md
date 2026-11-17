# Books 4–5 — completed-books-only publication audit

## Authorization and boundary

The user requested **Book4 and Book5 on `main`**, automatic publication of each subsequently completed book, and then the next three-chapter batch. `PUBLICATION_POLICY.md` records the standing instruction. No partial Book6 publication is authorized.

Before publication, live `main` was `2bef7d9676f3d55fd91e2219068d76f55ca0d09c`, containing Books1–3 and only Book4/Ch61. The working branch `arena/ec1bc639-ananta-novel` was live at `c48e895b7fb7166b41695a7fe89fe162e00d172c`, with completed Books4–5 and incomplete Book6/Ch101–113. All262 saved workspace files were independently compared with that live commit and matched exactly; stale local HEAD/index metadata was advanced on the SAME branch without rewriting a file. No lost prose was redrafted or recommitted.

## Exact publication contents

Completed-book source snapshot: **`77735cdb633cec4f98b4b8ee4f0417032b4f1f3b`** (Ch100 completion,231 tracked paths), plus only the new publication policy and this audit. The snapshot includes the Bible/tests and supporting notes current at Book5 completion. Historical prospective notes may mention Ch101, but there is no Ch101 source or Book6 manuscript in this publication.

| Book | Completion commit | Range | Sources | Words |
|---|---|---|---:|---:|
|4|`89c51ea84e99f483a49cdcbbb7793647d3d86d26`|61–80|20|89,189|
|5|`77735cdb633cec4f98b4b8ee4f0417032b4f1f3b`|81–100|20|86,980|

Both merged files match the exact numeric join of their20 sources with only chapter END markers removed. Every Book4/5 source and merge in the publication equals the existing working manuscript byte-for-byte. Neither subtitle is assigned.

Merged SHA256:

- Book4: `50ce1dd305d7954022fb7bd2162b796a7a7b191fe95bc237a3e12e098808b365`
- Book5: `8ee7ddbd97de3b746a98dd583c801ca0abda36d0ec949222ad819cba2ef728d9`

The frozen42 Book5 source/merge/chapter-note/completion-audit files retain their exact completion-snapshot bytes. Books1–3, Ch61 and all other already-published story sources are unchanged. Existing27/50 length warnings and legacy merge distinctions are not silently repaired.

## Verification and execution

Validate the exact publication tree independently in an exported temporary directory:36 chronology/reveal regressions and all FIVE published books' canon checks. Also verify exact Book4/5 merges,20-source ranges, source-byte preservation and the absence of `book-06/` or any chapter source above100. Only these validated bytes may be committed as the publication snapshot.

Use an alternate Git index on the CURRENT branch for the completed-book snapshot; do not delete, move or overwrite the unfinished workspace files. Open the PR from that same branch and squash-merge its explicit number only after reviewing its complete net file list against `main`. This prevents incomplete Book6 chapters from entering `main`'s tree or commit history.

Immediately restore the continuing branch's original262-file manuscript tree, retain these two publication records, verify all262 original hashes again, push that branch and record the verified `main` ancestry without changing the restored tree. No chapter may be drafted while the working branch is in the temporary publication-snapshot state.

The next authorized drafting batch is **Ch114–116 only**. Book6 remains incomplete; it is not automatically published merely because this batch was requested. Its completion boundary remains Ch120. Preserve all0–113 sources, consequence notes and historical plans during continuation.

## Publication-tree validation result

**PASS:**36/36 chronology/reveal regressions and all FIVE published books' canon checks in the independently exported publication tree. Exact20-source numeric END-stripped Book4/5 merges, source/merge byte equality, Book5's42-file freeze,233-path target inventory and99 net paths versus the prior `main` were verified. There is no `book-06/` or chapter source above100. Only historical27/50 length warnings remain. All262 continuing-workspace files retained their original113-completion hashes throughout preparation.
