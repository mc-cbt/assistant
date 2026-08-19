---
name: calendar-lookup
description: Find events on Matt's Outlook/Teams calendar by title, date, attendee, or organizer, and resolve a vague reference ("yesterday's FOP sync") to one specific event with its id, attendees, and transcript URL. Use when a task needs to identify a meeting, check what's scheduled, or look up who attended something.
---

# Calendar lookup

Resolves a human reference to a meeting into a concrete calendar event. Other skills
(`meeting-transcript`, `meeting-note`) take that event as input.

## Tools

`mcp__claude_ai_Microsoft_365__outlook_calendar_search` — metadata only.
`mcp__claude_ai_Microsoft_365__read_resource` with `calendar:///events/{id}` — full detail.

These are claude.ai connector tools. If they aren't loaded, fetch them first:
`ToolSearch("select:mcp__claude_ai_Microsoft_365__outlook_calendar_search,mcp__claude_ai_Microsoft_365__read_resource")`.
If the connector reports it needs authentication, ask the user to run `/mcp` and
authenticate **claude.ai Microsoft 365** — you cannot do it for them.

## Searching

- `query` is **required**. Use `*` to match everything and rely on the date filters —
  this is the right move for "what did I have yesterday".
- Narrow with `afterDateTime` / `beforeDateTime`. They take natural language
  ("yesterday", "last Monday") or ISO dates. Prefer explicit ISO dates you computed
  from `date` over natural language when precision matters.
- `order: "newest"` for "the most recent X". Note that setting `order` forces the
  date-range path, so results are bounded by the date filters (default ±1 year).
- Other filters: `attendee`, `organizer`, `calendarName`, `calendarOwnerEmail` (for a
  delegated calendar). All filters AND together.
- Max 25 per page. If the last item has `nextOffset`, pass it as `offset` for the next
  page.

## Time zones — read this before naming or reporting anything

Events come back as `{dateTime, timeZone}`. **In this tenant the connector returns
`timeZone: "UTC"`**, so a 9:00 AM Mountain standup appears as `15:00`. Before you show a
time to the user or derive a date for a filename:

1. Get the local zone with `date +%Z` / `date +%z`.
2. Convert on macOS (BSD `date`) by parsing as UTC to an epoch, then formatting local:

   ```
   TZ=UTC date -jf '%Y-%m-%dT%H:%M:%S' '2026-08-18T15:30:00' +%s \
     | xargs -I{} date -r {} +'%F %I:%M %p %Z'      # -> 2026-08-18 09:30 AM MDT
   ```

   Don't use `date -jf ... -u +...` — `-u` applies to the *output* too, so it just
   echoes the UTC time back and looks like a successful conversion.

A late-afternoon Mountain meeting is the *next* day in UTC. Getting this wrong puts the
meeting note under the wrong date, so convert — don't eyeball it.

## Disambiguating

Standups and other recurring meetings return one event per occurrence with the same
subject. When more than one event matches:

- If the user gave a date, filter to that **local** date first.
- If exactly one remains, use it and state which one you picked (subject + local date
  and time).
- If several remain, list them — subject, local date/time, organizer — and ask which.
  Don't guess between two occurrences of the same recurring meeting.
- If none match, say so and show what *was* on the calendar in that window rather than
  widening the search silently.

Skip all-day events with `showAs: "free"` (OOO markers, birthdays) unless the user is
clearly asking about those.

## Reading full detail

`outlook_calendar_search` returns a truncated `summary` and email addresses only. Read
the event when you need:

- **`meetingTranscriptUrl`** — the opaque `meeting-transcript:///events/{token}` URI
  that `meeting-transcript` needs. Only on Teams meetings. Pass it **verbatim**; never
  construct or edit the token.
- **`attendees[]` with display names and `responseStatus`** — the search result gives
  addresses only. `responseStatus: "declined"` or `"none"` is a hint someone may not
  have actually attended; the transcript is the real evidence.
- **`body`** — the full invite, including agenda links.
- **`onlineMeeting.joinUrl`**, `recurrence`, `isCancelled`.

## What to hand off

Report the resolved event as: subject, local date and time, organizer, attendee display
names, event id/URI, and whether `meetingTranscriptUrl` is present.

## Confidentiality

Calendars expose the whole company — attendee lists, interview and HR meetings, customer
names. Pull only the events the task needs, and don't dump full attendee lists (some
here run to 200 people) into notes or output unless asked.
