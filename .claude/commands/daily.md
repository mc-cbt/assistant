---
description: Create or open today's daily note; with arguments, append them to today's Notes
argument-hint: "[note to jot down]"
---

Follow the `daily-note` skill.

Arguments given: $ARGUMENTS

- **No arguments** — create or open today's daily note per the skill: seed from the
  template if it doesn't exist, carry over from the previous entry, link it from
  `Daily/Daily.md`, then show me the note so I can fill in the plan.

- **Arguments given** — treat them as something to capture in *today's* note. Create the
  note first if it doesn't exist yet. Decide from the wording where it belongs:
  a priority goes under `## Priorities`, anything else under `## Notes`. Add
  `[[wiki-links]]` for any project, team, or person mentioned, and keep the bullet terse
  — don't pad it into prose. Show me the section you changed, not the whole file.
