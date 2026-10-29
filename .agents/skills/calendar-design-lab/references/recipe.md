# Design recipe: initial working contract

This is a small recording convention, not an implemented universal renderer or a fixed template schema. Evolve it from working designs.

For local case/revision/artifact records and the standard-library initializer/checker, use [case-record.md](case-record.md). A recipe points to an actual retained revision; it may remain a draft. Keep actual replay evidence separate from a declared intent to support another week or year.

Keep enough information to reopen and rerender the selected design:

| Part | Retain |
| --- | --- |
| Identity | Recipe ID, revision, draft/approved status, source experiment |
| Brief | Period/view, language, week start, physical or screen dimensions, desired content |
| Time expression | How days/weeks/months are organized and the relationships the design should preserve |
| Implementation | Editable layout source, entry point, revision, renderer/runtime and relevant dependencies |
| Visual decisions | Font roles, color/material decisions, reusable composition parameters; allow original layouts |
| Assets | Chosen asset files or durable references, versions/checksums, provenance and permitted uses |
| Changes | User feedback, resulting edits, decisions explicitly retained |
| Evidence | Output snapshot, technical review and user review recorded separately |

Save chosen image assets as well as generation metadata where relevant. A prompt or seed alone is insufficient evidence that the selected result can be reproduced.

Distinguish three operations:

- Replay: rerender the saved design with the saved resources.
- Reparameterize: change supported inputs such as year or content while preserving the selected design's relationships.
- Explore: ask AI for a new design decision, creating a new revision or recipe.

Do not claim replay or reparameterization works until actually run and inspected. A change from year to week view may need a new composition rather than a scaled copy.

## Reference and sharing boundaries

Record public links and original analysis for research references where appropriate. Keep private uploads local. Reference access does not by itself establish redistribution rights.

For shared fonts, images, and templates, record the source, license/version, attribution and relevant permitted uses, including embedding, export or redistribution when applicable. Keep research-only assets out of shared recipes. If rights are unresolved, mark them unresolved and exclude those assets from distribution; do not declare that AI generation automatically clears rights.

Sharing in this product means reusing an original or appropriately licensed recipe. It does not grant permission to copy arbitrary third-party calendar products.
