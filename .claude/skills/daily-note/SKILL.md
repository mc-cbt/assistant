---
name: daily-note
description: Create or open today's daily note in Daily/, seeded from _template.md, carrying over unfinished items from the previous entry and linking it from the Daily hub. Use when the user asks to start the day, create/open today's note, plan the day, or add something to today's daily note.
---

# Daily note

One entry per workday at `Daily/YYYY-MM-DD.md`. Entries are for **workdays only** — there is
no note for a day nothing happened, and gaps in the sequence are normal and expected.

## Creating today's note

1. **Get the date.** Use the current date from context. If it is missing or you are
   unsure, run `date +%F` rather than guessing. The filename is the zero-padded ISO
   date: `Daily/2026-08-18.md`.

2. **Check whether it already exists.** If `Daily/<today>.md` is present, do *not*
   overwrite it — open it, show the current contents, and continue from there. Adding
   to an existing note is the common case once the day is underway.

3. **Seed from the template.** Copy `Daily/_template.md` verbatim. Do not invent a new
   structure; the four sections (Plan for the day, Priorities, Notes, Wrap-up) are
   stable and other notes rely on them.

4. **Carry over from the previous entry.** Find the most recent existing daily note
   before today (`ls Daily/*.md | sort` — skip `_template.md` and `Daily.md`). Read its
   **Wrap-up → Carry over to tomorrow** list and its unfinished **Priorities**, and seed
   today's Priorities with them. If the previous note's carry-over is empty and its
   priorities all look complete, leave Priorities blank for the user to fill in — do not
   manufacture work.

   If the previous entry is more than a few days old, say so and confirm the carry-over
   is still relevant before pulling it forward. Stale priorities are worse than an empty
   list.

5. **Link it from the hub.** Append a line to `Daily/Daily.md` under `## Notes`, keeping
   the existing chronological order and exact link form:

   ```
   - [[Daily/2026-08-18|2026-08-18]]
   ```

## Writing entries

- Use `[[wiki-links]]` for projects, people, and teams — link the folder hub note, e.g.
  `[[Projects/FOP/FOP|FOP]]`, `[[Teams/Velocity/Velocity|Velocity]]`. Match the
  `path|display` form already used in the existing notes.
- Priorities are a short numbered list (roughly 3–5). If the user rattles off more,
  offer to push the overflow to Notes rather than growing the list.
- Keep bullets terse — these are working notes, not prose.

## Feeding status back into other notes

When something in a daily note is a real status change for a project, person, or team,
also record it on that note with a date stamp and a link back:

```
- (2026-08-18, see [[Daily/2026-08-18]]) Shipped the FOP config UI behind a flag.
```

Do this for progress worth remembering later, not for every bullet. Ask before adding to
someone's People note.

## Confidentiality

Daily notes routinely touch internal projects, customers, and colleagues. Keep secrets,
credentials, and customer PII out of them entirely — reference the system of record
instead.
