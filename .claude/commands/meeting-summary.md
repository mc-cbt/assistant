---
description: Find a past meeting on my calendar, pull its transcript, summarize it, and file the note in Meetings/
argument-hint: "[meeting title and/or date, e.g. \"FOP sync yesterday\"]"
---

Summarize a past meeting and file it in the vault. Chain three skills:
`calendar-lookup` → `meeting-transcript` → `meeting-note`.

Meeting reference: $ARGUMENTS

1. **Resolve the meeting** with `calendar-lookup`. Match `$ARGUMENTS` against subject and
   date; with no arguments, list my recent past meetings and ask which one. Only past
   meetings — if the match is in the future, say so and stop. Convert times to my local
   zone before showing them; the connector returns UTC. If several occurrences match,
   list them and ask rather than guessing. Then read the full event for attendee names
   and `meetingTranscriptUrl`.

2. **Get the transcript** with `meeting-transcript`, working its routes in order. Tell me
   which route worked. If route 3 needs me to download the recording, give me the link
   and wait — don't write a note without material.

3. **Write the note** with `meeting-note`: `Meetings/<Topic> Meeting YYYY-MM-DD.md`,
   dated by the meeting's **local** date. Full structure — summary, discussion,
   decisions, action items, links — with `[[wiki-links]]` to existing People, Projects,
   and Teams notes. Link it from `Meetings/Meetings.md`.

4. **Report back**: the note path, the TL;DR, and the action items. Then ask whether to
   date-stamp any status updates onto the related project or team notes.

Don't invent decisions or action items the transcript doesn't support, and keep secrets
and PII out of the note.
