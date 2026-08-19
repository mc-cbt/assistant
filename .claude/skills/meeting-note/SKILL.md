---
name: meeting-note
description: Turn raw meeting material (a transcript, recording captions, or rough notes) into a structured meeting note filed in the right place — Teams/<Team>/Standup/ for team standups, Meetings/ for one-off meetings — following the vault's naming, wiki-link, and hub conventions. Use when the user asks to summarize a meeting, write up meeting notes, or file a transcript into the vault.
---

# Meeting note

Writes one note per meeting to `Meetings/<Topic> Meeting YYYY-MM-DD.md`.

This skill is about **turning material into a filed note**. Getting the material is a
separate job — see `meeting-transcript` for pulling a Teams transcript, or just paste
notes in directly.

## Inputs you need

Before writing, you should have:

- **Date** of the meeting (ISO, zero-padded). Ask if you can't determine it.
- **Topic / title** — from the calendar subject if available. Strip recurrence noise
  ("Weekly", "Sync - Copy") only when it makes the filename clearer.
- **Attendees** — real names where possible. Transcript speaker labels are often
  display names; map them to `People/` notes when a note exists.
- **Body material** — transcript text, captions, or notes.

## Where the note goes

**Check for an existing home before defaulting to `Meetings/`.** A recurring team meeting
usually already has a folder, and notes must go there to stay with their series:

- `Teams/<Team>/Standup/YYYY-MM-DD.md` — team standups (e.g.
  `Teams/Blitz/Standup/2026-08-18.md`). Bare date filename, no "Meeting" in the name.
- `Teams/<Team>/…` — other recurring team meetings (retros, planning) if a folder exists.
- `Meetings/<Topic> Meeting YYYY-MM-DD.md` — one-off and cross-team meetings. This is the
  default only when nothing more specific exists.

Look before you write: `ls Teams/<Team>/` and check the team's hub note. When an existing
folder has prior notes, **match their structure and heading names** rather than imposing
the template below — those notes set the house style for that series.

## Filename and location

For `Meetings/`: `<Topic> Meeting YYYY-MM-DD.md`, e.g. `Meetings/FOP in Sabre Meeting 2026-07-08.md`.

- Zero-padded ISO date, always.
- If the file already exists, **do not overwrite it.** Show the user what's there and
  ask whether to merge the new material in or write a second note with a disambiguating
  suffix.
- Sanitize the topic for the filesystem: no `/`, `:`, or leading/trailing spaces.

## Structure

```markdown
---
date: 2026-07-08
type: meeting
attendees: [Matt Condie, Chad Maughan]
source: Teams transcript
---

# <Topic> Meeting 2026-07-08

## Summary

Two to four sentences. What the meeting was for and where it landed.

## Discussion

### <Topic heading>

- Terse bullets. Group by subject, not chronology — a transcript's order is rarely the
  clearest order.

## Decisions

- (2026-07-08) What was decided, and by whom if it matters.

## Action items

- [ ] Owner — what they agreed to do (due date if one was stated)

## Links

- [[Projects/FOP/FOP|FOP]]
- [[Daily/2026-07-08]]
```

Omit a section entirely if the meeting produced nothing for it. An empty **Decisions**
heading is worse than no heading — and never invent decisions or action items that the
material doesn't support.

## Writing rules

- **Wiki-link people, projects, and teams** on first mention. The vault uses two forms:
  bare `[[Trey Bailey]]` for people, and `path|display` for folder hubs
  (`[[Projects/FOP/FOP|FOP]]`, `[[Teams/Velocity/Velocity|Velocity]]`). When writing into
  a folder that already has notes, copy whatever form those notes use. Check the folder
  before linking — link only notes that exist, and mention any person or project that
  came up without a note so the user can decide whether to create one.
- **Bold the key terms** — system names, identifiers, decisions. Existing meeting notes
  lean on bold heavily to make bullets skimmable; match that density.
- **Attribute sparingly.** Name someone when who said it matters (a commitment, a
  decision, a dissent). Otherwise summarize the conclusion.
- **Terse bullets**, not prose. These are working notes.
- **Don't quote the transcript at length.** A short verbatim quote is fine when the
  exact wording is the point; otherwise summarize.
- **Flag uncertainty inline.** Auto-transcripts mangle names, acronyms, and system names
  — real examples seen here: "Conferma" → "Conference"/"confirm NFT", "Finicity" →
  "ethnicity", "Jake Knowlton" → "Jake Norton", "folios" → "portfolios". Give your best
  reading and mark it, so a later reader can tell what was said from what you inferred:

  ```
  **Finicity vs. Plaid** _(name unclear in transcript — "ethnicity versus Plaid"; Finicity
  is the likely reading)_
  ```

- **Record the source and its limits.** When the note came from a transcript, open with a
  callout naming the source, who was present, and any caveat that changes how much to
  trust it — unlabelled speakers, or a recording that started late.

## Linking it from the hub

Link the note from **its own folder's hub**, not always `Meetings/Meetings.md` — a note
in `Teams/Blitz/Standup/` is indexed by `Teams/Blitz/Standup/Standup.md`. Append under
`## Notes`, newest last, matching the form already used in that hub:

```
- [[Meetings/FOP in Sabre Meeting 2026-07-08|FOP in Sabre Meeting 2026-07-08]]
```

If `Meetings/Meetings.md` doesn't exist yet, create it with a short Purpose section and
a `## Notes` list, and add `- [[Meetings/Meetings|Meetings]]` to `Home.md` under
`## Subdirectories` in alphabetical order.

## Feeding status back

When the meeting produced a real status change for a project, team, or person, offer to
add a date-stamped line to that note, linking back:

```
- (2026-07-08, see [[Meetings/FOP in Sabre Meeting 2026-07-08]]) Agreed to ship FOP config behind a flag.
```

Ask before writing to a `People/` note. Don't do this silently for every bullet — only
what's worth finding again later.

## Confidentiality

Transcripts capture far more than the user would write down: customer names, contract
terms, personnel discussion, credentials read aloud. Keep secrets and PII out of the
note — reference the system of record instead. If something sensitive is clearly central
to the meeting, tell the user what you left out rather than filing it.
