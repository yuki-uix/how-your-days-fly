---
name: calendar-design-lab
description: "Explore, design, revise and replay annual, monthly, weekly or daily calendars from a natural-language brief, keeping evidence, exact dates and editable recipes. Use for themed calendar design and design experiments, not ordinary scheduling or event management."
---

# Calendar Design Lab

Help a person create a calendar they would actually use, then preserve the design so another person can reuse or adapt it. This skill is an initial workflow under evaluation; it does not establish that design quality has been validated.

Identify the requested mode first: discuss, create, revise or replay. A hypothetical product question calls for analysis; an actual commission calls for visible work. Use product-design judgment to connect use, theme and content, and UX judgment to resolve the next important uncertainty through a question or example. Do not start a personal calendar project merely because it appears in a capability discussion.

## Establish the brief

Read the active experiment if supplied. For an open brief, read [references/discovery.md](references/discovery.md). Separate explicit requirements, user-confirmed choices, verified facts, system defaults, hypotheses and unknowns. A profession, theme label or unrelated history is not enough evidence for a palette or composition.

Use examples and comparisons when a preference is difficult to verbalize. Ask for the missing information that materially changes the design while continuing independent work. If references are unavailable and the user requests a design, make a few comparable, inexpensive visual studies such as wireframes or small typography/layout samples. Label the assumptions; do not call them personalized conclusions or leave the user with only style names and a questionnaire.

Record calendar scale, use, time organization, output size, language, week start, and desired content as they become known. Annual, monthly, weekly, and daily calendars share design resources but require scale-appropriate composition.

For a substantial multi-turn case, reuse its existing record or follow [references/case-record.md](references/case-record.md). Keep real case files local under ignored `output/cases/` by default. The helper can initialize/check evidence records and fingerprint selected files; it does not understand the brief or render a design. Unknown fields need not block an exploratory draft. Make consequential defaults visible, and resolve necessary delivery facts before calling an output ready for use.

## Explore and implement

Start from the [unified design atlas](../../../docs/design-atlas.md) when a request spans structure, rules, studies and materials. From the repository root, run `python3 scripts/design_catalog.py --scale month --json` (or year/week/day) to retrieve linked choices together. Use each linked original record for its details. Recorded study choices, present-day recommendations, replacement candidates and unimplemented directions are different relations; preserve that distinction when proposing a design.

For a new calendar concept or a substantial visual revision, read [references/design-language.md](references/design-language.md). State a compact design card covering reading task, temporal semantics, spatial organization, typography roles, composition/whitespace, series invariants, and validation. Keep unconfirmed choices provisional; a well-reasoned design is still a hypothesis until the user evaluates it.

Read [references/design-exploration.md](references/design-exploration.md) when turning a theme into creative directions, making a comparison or revising from feedback. Theme roles can combine; a book list or quotation is needed only when the chosen direction uses it. Let the number and fidelity of studies follow the design question and available brief, and show actual artifacts when design work was requested.

When summarizing calendar modes or comparing time structures, read [references/patterns.md](references/patterns.md). Treat this as an extensible design vocabulary. Separate time structure, hierarchy, content role, and medium; do not turn exploratory studies into user preferences or a closed set of product templates.

For public learning materials or the rationale behind this vocabulary, read [references/learning-guide.md](references/learning-guide.md). Preserve each source's terminology and distinguish viewing extent, temporal granularity, temporal mapping, and spatial layout. Turn relevant concepts into controlled studies before treating them as validated design rules.

For a new mapping, date grouping, normalization, or cross-period change, read [references/temporal-semantics.md](references/temporal-semantics.md). For hierarchy, numeral choice, whitespace, or a multi-page series, read [references/typographic-composition.md](references/typographic-composition.md). Read only what the current decision needs. Do not collapse calendar days into equal elapsed seconds or infer a numeral feature from a font's broad category.

When type or layout lacks a defensible choice or receives explicit criticism, use that reference's actual-content specimen and composition-study method before another full design. Compare the relevant font roles, remove or demote unjustified auxiliary information, and inspect whole-page balance as well as actual-size glyphs. Font availability and passing technical checks are not selection rationales.

For date-numeral roles, figure forms, padding, alignment or dedicated numeral materials, use the [numeral topic guide](../../../docs/numeral-font-library.md). Independent role selection may reuse a family; check actual shaped results and language, not feature tags alone.

For English/Latin family selection, native italics, letterspacing or optical-size studies, use the [English topic guide](../../../docs/latin-type-library.md) and query `--tag latin`; categories and weight numbers are descriptors, not quality ratings.

For deeper selection, query the library by `--domain typography` or `--domain layout` and role; use the [type/layout topic guide](../../../docs/type-layout-library.md). Keep requirements, aesthetic positions, project hypotheses and renderer support distinct. Font axes/features do not prove the exporter applies them; sparse grids and expressive density are alternatives with conditions, not universal quality standards.

Analyze references in terms of number forms, hierarchy, grouping, density, whitespace, materials, image relationships, and how time is experienced. Distinguish studying an approach from permission to redistribute the reference's concrete artwork.

Propose substantially different directions where useful. Give each a spatial or temporal idea and connect visual choices to the brief. Avoid producing near-identical color variants as evidence of exploration. Do not prescribe one universal aesthetic or require all calendars to use illustration.

Separate whole-direction studies from controlled comparisons: a whole direction may change several visual decisions, while a comparison testing a particular rule should identify its changed variable and retain the rest. Preserve source evidence, transfer hypotheses, technical findings and subjective feedback as separate records.

Use `scripts/calendar_data.py` for deterministic Gregorian date data, or a verified alternative when requirements extend beyond its scope. Run `--help` for options. Keep date facts separate from generated imagery. The tool does not provide lunar dates, holidays, solar terms, typography, or visual layout.

Choose tools suited to the selected design: editable vector/code layouts for typography and date structures; image generation or licensed imagery when the concept needs bitmap art. Preserve the selected assets. Do not rely on generating the entire calendar as an image to establish correct dates.

When selecting or expanding imagery, motifs, typography, content modules, or a multi-page sequence, read [references/material-library.md](references/material-library.md). Query the retained catalog by year/month/week/day and role; keep research-only examples, licensed files, original components and unimplemented proposals distinct. Match the material to its reading task, record the actual selection/crop/sequence, and check resolution before print.

## Review and revise

Read [references/review.md](references/review.md) when checking a draft or interpreting feedback. Inspect the actual render at its intended use size. Technical checks and the user's design judgement are separate results.

Ask what should stay as well as what should change when needed. Turn feedback into localized edits to the design source or parameters; preserve approved decisions. Do not infer that a rejection means every feature was disliked.

Record keep/change/unknown against the affected revision. Carry forward accepted relationships; a new revision's overall user-review status remains pending until supported. Check the requested language and actual content; the current English proofs and fixed weekly studies do not establish Chinese typesetting or a general calendar generator.

## Preserve and hand off

Read [references/recipe.md](references/recipe.md) when saving, replaying, sharing, or adapting a design. Keep the chosen design source, parameters, asset references, versions, and render together. Record user approval only when it actually occurred.

Report what was produced, what was checked, what the user has accepted, and what remains unknown. A valid skill file, successful date test, attractive mockup, or working export is not proof of the entire design capability.

Keep individual preferences in the case. Promote a recurring relationship into a conditional rule only with scoped evidence and known limits; turn a stable operation into a tool when actual cases justify it. Preserve contradictions as hypotheses. No fixed user or case count automatically validates a rule.
