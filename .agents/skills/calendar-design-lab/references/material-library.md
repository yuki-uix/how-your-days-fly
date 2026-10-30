# Choosing scale-appropriate calendar materials

For a decision spanning structure, design rules, examples and material selection, start with the [unified atlas](../../../../docs/design-atlas.md) and `python3 scripts/design_catalog.py --scale month --json`. This page covers the material-specific part of that shared workflow.

Read the repository's [grouped guide](../../../../docs/material-library.md) and use the [retained catalog](../../../../assets/library/catalog.json) when looking for imagery, type, motifs, functional components, or series content. Do not load all case studies by default: select the scale and reading task first.

```sh
python3 scripts/material_catalog.py --scale month --json
python3 scripts/material_catalog.py --scale week --kind reference --json
python3 scripts/material_catalog.py --scale day --shareable-only --json
python3 scripts/material_catalog.py --domain typography --role font-pairing --json
python3 scripts/material_catalog.py --domain layout --kind design-element --json
```

Run from the repository root. `scales` are suggested viewing/use extents, not mutually exclusive folders or limits on an asset's meaning. A weekly photograph can be a week's main image; it does not imply seven different daily images already exist.

## Select by task, then compose

| Extent | Prioritize | Check before moving to another extent |
| --- | --- | --- |
| Year | Continuity, indexes, accumulated states, borders that survive distant viewing | A month-normalized motif must not silently imply equal day duration; full daily imagery may only work as an index |
| Month | Image/date anchors, captions, twelve-part sequence, 4–6 row variation | An isolated image is not a complete twelve-month series; retain a coherent content and crop rule |
| Week | Seven-day area, time or open notes, optional logs/reflection, cross-month identity | Weekend area is a brief decision; adapting to month requires actual day count, not seven repeated boxes |
| Day | Complete date identity, one content unit, optional short record, adjacent/annual context | A series needs retained ordering and date-to-asset/crop mapping; no fresh random regeneration on replay |

Choose materials across roles, not one exclusive style tag: typography, image, frame, ornament, navigation, date module, writing/tracking, content and carrier. Preserve fixed anchors and choose the variables that may change across a series. The original component palettes are studies, not confirmed user taste or universal seasonal colors.

## Rights and evidence in the index

- `reference`: official cases and original transfer analysis, all research-only; do not copy the linked product art, text, proprietary fonts or engineering files into a recipe.
- `image`: inspect the individual provenance record. Current newly collected museum files are item-verified CC0; the existing AI image has a separate generation record and scope.
- `font`: existing OFL families with original files and license text. Check the actual glyphs needed for the selected language and roles.
- `component`: original retained code and SVG studies. No public project license has been selected; do not invent a public redistribution grant.
- `proposal`: a content/module idea without a completed asset. Do not count it as downloaded or implemented.
- `design-element`: source-informed conditions, choices, tradeoffs and proof links. Use the [type/layout topic guide](../../../../docs/type-layout-library.md); requirements, designer positions and implementation capabilities are different evidence. Original studies are not universal styles or user preferences.

`ready` means a local asset exists. The explicit-license filter admits only recorded CC0/OFL items, with their relevant conditions. It is not a legal-clearance service or a check of print resolution, complete series coverage, or design acceptance.

The web-sized museum files are preview material. Before print, use their recorded pixel dimensions and intended physical size; retrieve and retain a higher-resolution official rendition when necessary. Preserve new bytes and hash in the final recipe. Do not call a damaged lace fragment a seamless texture, a moon painting a verified lunar phase, or a flower picture proof of a local bloom season.

## Save the actual selection

For a design, record selected catalog IDs, original file hashes, type roles, placement and crop coordinates, date mapping and series invariants. Replace placeholders with selected assets before calling a design complete. Keep decorative marks explicitly decorative; real moon phases, solar terms, holidays, daylight, climate or personal states need their own verified data or user input.

Rebuild components and boards with `scripts/build_material_library.py`; run `scripts/design_catalog.py --build` after source-record edits to refresh both the material index and its design relationships. The narrower `material_catalog.py` remains available for asset/license filters. This library improves material discovery; it is not a validated universal design generator.
