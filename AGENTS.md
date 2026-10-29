# Project instructions

## Product and current scope

The eventual product is a public website for creating, revising, exporting, and remixing personal annual, monthly, weekly, and daily calendars. The current milestone is validating the underlying design capability through real examples.

- Keep facts, user-confirmed preferences, model hypotheses, proposals, and completed work distinct.
- Treat an unspecified taste as unknown. Do not infer a palette, illustration subject, or lifestyle from a profession or unrelated chat history.
- A rejected design is not evidence that every individual feature in it was disliked. Record the actual feedback before generalizing.
- Do not describe an initial skill or a technically valid output as a validated design capability.
- Use concise Chinese explanations and Mermaid diagrams when a process or dependency benefits from them.

## Design workflow

Read `.agents/skills/calendar-design-lab/SKILL.md` when designing or revising a calendar. Follow explicit user preferences over suggested workflow defaults.

Keep the calendar calculation, visual rendering, design judgement, and user approval separate. Use deterministic code for date facts. Allow different compositions and visual languages rather than hardcoding one house style.

Record user-approved decisions and unresolved questions in the active experiment. Preserve a selected design's editable source, material assets and versions before claiming reproducibility. A prompt or random seed alone is not the saved design.

## Repository boundaries

- Work inside this repository. Do not modify unrelated project mirrors or reference sources.
- This is a public repository: do not commit private conversation history, personal reference uploads, credentials, local font files, or unrelated outputs.
- Use public reference links and brief original analysis where appropriate. Do not copy third-party calendar art into shared templates without the necessary rights.
- Keep `.env`, `reference-inputs/`, `output/`, and `tmp/` local. Review staged files before pushing.
- Do not add a blanket open-source license or import third-party assets without checking the relevant scope and recording the decision.

## Validation

Run `python3 -m unittest discover -s tests -v` after changes to the date tool. Add meaningful date-boundary tests when behavior changes.

Technical verification and subjective approval must be reported separately. Test or skill-structure validation does not certify visual quality or clear a third-party asset's rights.
