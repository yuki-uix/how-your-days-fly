---
name: calendar-design-lab
description: "Design and revise annual, monthly, weekly, or daily calendars from real preferences, using exact date data and preserving an editable design for reuse. Use for calendar design experiments and design recipes, not ordinary scheduling or calendar-event management."
---

# Calendar Design Lab

Help a person create a calendar they would actually use, then preserve the design so another person can reuse or adapt it. This skill is an initial workflow under evaluation; it does not establish that design quality has been validated.

## Establish the brief

Read the active experiment if supplied. Separate explicit requirements, user-confirmed visual preferences, evidence from references, model hypotheses, and unresolved choices. A profession, personality guess, or unrelated history is not enough evidence for a palette or composition.

Use examples and comparisons when a preference is difficult to verbalize. Ask for the missing information that materially changes the design while continuing independent work. If references are unavailable and the user requests a design, make a few comparable, inexpensive visual studies such as wireframes or small typography/layout samples. Label the assumptions; do not call them personalized conclusions or leave the user with only style names and a questionnaire.

Record calendar scale, use, time organization, output size, language, week start, and desired content as they become known. Annual, monthly, weekly, and daily calendars share design resources but require scale-appropriate composition.

## Explore and implement

For a new calendar concept or a substantial visual revision, read [references/design-language.md](references/design-language.md). State a compact design card covering reading task, temporal semantics, spatial organization, typography roles, composition/whitespace, series invariants, and validation. Keep unconfirmed choices provisional; a well-reasoned design is still a hypothesis until the user evaluates it.

When summarizing calendar modes or comparing time structures, read [references/patterns.md](references/patterns.md). Treat this as an extensible design vocabulary. Separate time structure, hierarchy, content role, and medium; do not turn exploratory studies into user preferences or a closed set of product templates.

For public learning materials or the rationale behind this vocabulary, read [references/learning-guide.md](references/learning-guide.md). Preserve each source's terminology and distinguish viewing extent, temporal granularity, temporal mapping, and spatial layout. Turn relevant concepts into controlled studies before treating them as validated design rules.

For a new mapping, date grouping, normalization, or cross-period change, read [references/temporal-semantics.md](references/temporal-semantics.md). For hierarchy, numeral choice, whitespace, or a multi-page series, read [references/typographic-composition.md](references/typographic-composition.md). Read only what the current decision needs. Do not collapse calendar days into equal elapsed seconds or infer a numeral feature from a font's broad category.

Analyze references in terms of number forms, hierarchy, grouping, density, whitespace, materials, image relationships, and how time is experienced. Distinguish studying an approach from permission to redistribute the reference's concrete artwork.

Propose substantially different directions where useful. Give each a spatial or temporal idea and connect visual choices to the brief. Avoid producing near-identical color variants as evidence of exploration. Do not prescribe one universal aesthetic or require all calendars to use illustration.

Separate whole-direction studies from controlled comparisons: a whole direction may change several visual decisions, while a comparison testing a particular rule should identify its changed variable and retain the rest. Preserve source evidence, transfer hypotheses, technical findings and subjective feedback as separate records.

Use `scripts/calendar_data.py` for deterministic Gregorian date data, or a verified alternative when requirements extend beyond its scope. Run `--help` for options. Keep date facts separate from generated imagery. The tool does not provide lunar dates, holidays, solar terms, typography, or visual layout.

Choose tools suited to the selected design: editable vector/code layouts for typography and date structures; image generation or licensed imagery when the concept needs bitmap art. Preserve the selected assets. Do not rely on generating the entire calendar as an image to establish correct dates.

## Review and revise

Read [references/review.md](references/review.md) when checking a draft or interpreting feedback. Inspect the actual render at its intended use size. Technical checks and the user's design judgement are separate results.

Ask what should stay as well as what should change when needed. Turn feedback into localized edits to the design source or parameters; preserve approved decisions. Do not infer that a rejection means every feature was disliked.

## Preserve and hand off

Read [references/recipe.md](references/recipe.md) when saving, replaying, sharing, or adapting a design. Keep the chosen design source, parameters, asset references, versions, and render together. Record user approval only when it actually occurred.

Report what was produced, what was checked, what the user has accepted, and what remains unknown. A valid skill file, successful date test, attractive mockup, or working export is not proof of the entire design capability.
