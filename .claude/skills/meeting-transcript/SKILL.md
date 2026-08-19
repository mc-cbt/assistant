---
name: meeting-transcript
description: Get the text of a past Teams meeting — via the Graph transcript API, a transcript file in OneDrive/SharePoint, or by transcribing a downloaded recording locally. Use when a task needs what was actually said in a meeting, not just the invite.
---

# Meeting transcript

Turns a calendar event into transcript text. Identifying the event is
`calendar-lookup`'s job; writing the note is `meeting-note`'s.

## Tenant status (verified 2026-08-19)

**The Graph transcript API works.** Access was disabled tenant-wide until 2026-08-19,
when the Teams policy was changed; route 1 is now the default path and needs no manual
steps. If it starts returning `GraphAccessToTranscriptsDisabled` again, the policy has
been reverted — that's an admin-side change, not something retrying or trying a different
meeting will fix (it was verified to block the organizer's own meetings too).

Trade-off worth knowing: the API transcript has **no speaker labels**
(`speakerAttribution: false`), while a manual Teams export (route 3) has real names. Use
route 3 when who-said-what matters.

## Route 1 — Graph transcript API (default)

1. Get the event via `calendar-lookup` and read it with `read_resource` on
   `calendar:///events/{id}`.
2. Take `meetingTranscriptUrl` **verbatim** — it's an opaque base64url token. Do not
   build it from the join URL yourself.
3. Read it. For a recurring meeting, scope to the one occurrence by appending the
   event's UTC start/end:

   ```
   meeting-transcript:///events/{token}?start=2026-08-17T20:00:00Z&end=2026-08-17T20:30:00Z
   ```

   Omit `start`/`end` and you get the most recent transcripts of the series (capped) —
   which for a daily standup is almost never the occurrence you wanted.

On `GraphAccessToTranscriptsDisabled`, don't retry — the policy has been reverted; go to
route 2 and tell the user.

The `meetingTranscriptUrl` on the event sometimes already carries `start`/`end` for that
occurrence. When it does, use it as-is rather than appending your own.

**Reading the response.** It returns `{meeting, transcripts[]}`. Each transcript has
`createdDateTime`/`endDateTime` and a WEBVTT-ish `content` of timestamped cues with **no
speaker tags**. Two things to check before summarizing:

- `meeting.startDateTime` is the **series** start, not the occurrence — for a recurring
  meeting it can be months off. Trust `transcripts[].createdDateTime` for when the
  material was actually captured.
- Compare `createdDateTime` against the event start. Recording usually begins a few
  minutes late, so the opening of the meeting is often missing. Say so in the note rather
  than implying full coverage.

**Speaker attribution.** With `speakerAttribution: false` you get bare text. Overlapping
cues interleave, so consecutive lines are frequently *different* people. You can often
reconstruct who's who from greetings, the attendee list, and who owns which work — but
that is inference. Say so in the note (a Source callout works well) and never present an
inferred attribution as if the transcript labelled it. When attribution really matters,
use route 3 instead.

## Route 2 — a transcript file in OneDrive/SharePoint

Teams sometimes writes a `.vtt` or `.docx` transcript next to the recording.

- `sharepoint_search` with the meeting subject and `fileType: "vtt"`, then `"docx"`.
- Or list the organizer's Recordings folder directly:
  `read_resource` on `file:///{driveId}/Recordings` — the `driveId` comes from any
  search hit in that drive. Recording filenames follow
  `<Subject>-<YYYYMMDD>_<HHMMSS>UTC-Meeting Recording.mp4`; the timestamp is **UTC**, so
  match it against the event's UTC start, not the local time.
- Read any `.vtt`/`.docx` you find with `read_resource`. Both MIME types are allowed.

## Route 3 — manual export from the Teams UI (best available today)

Teams' own UI will export a transcript even though the API won't, and its `.vtt` carries
**real speaker names** — `<v Kyle Crowther>Any questions to start off?</v>` — which
neither voice diarization nor the recording can give you. Prefer this over route 4.

Matt has done this before; `~/Downloads/FOP Product requirements review.vtt` is an
example of the output.

1. Check whether the file is already downloaded before asking for anything:
   `ls -t ~/Downloads/*.vtt ~/Downloads/*.docx 2>/dev/null | head`. Match on the meeting
   subject — Teams names the export after the meeting, with no timestamp, so confirm the
   date with the user if several meetings share a subject.
2. If it isn't there, ask the user to open the meeting in Teams → **Recap** →
   **Transcript** → the **⋯** menu → **Download** → `.vtt`, and save it to `~/Downloads`.
   Give them the meeting's subject and local date so they open the right occurrence.
3. Read it with `Bash` (`cat`) — it's a local file, not a connector resource.

Parsing `.vtt`: cue blocks are `<v Speaker Name>text</v>` between timestamp lines. To
skim a long one, strip the timing and IDs:

```
grep -o '<v [^>]*>[^<]*' transcript.vtt | sed 's/<v //; s/>/: /'
```

## Route 4 — transcribe the recording locally

The connector won't hand over the `.mp4`, but the user can, and transcription runs
on-device via Spokenly — the audio never leaves the machine.

1. Locate the recording (route 2's folder listing) and give the user its **`webUrl`**,
   asking them to download it.
2. Check whether it's already downloaded before asking:
   `ls -t ~/Downloads/*.mp4 2>/dev/null | head` — look for the subject and UTC timestamp in the name.
3. Transcribe with `mcp__spokenly__transcribe_file`:
   `{file_path: "<absolute path>", format: "text", speakers: true}`.
   Load it first if needed: `ToolSearch("select:mcp__spokenly__transcribe_file")`.
   `speakers: true` labels speakers by voice; it does **not** know their names. This is
   exactly what route 3 gives you for free, which is why route 3 comes first. Map
   labels to real people using the event's attendee list, and only when you're
   confident — say "Speaker 2 (likely Chad)" rather than asserting it.
4. Long recordings take a while. Tell the user it's running rather than going quiet.

## Route 5 — ask

If all four fail, say plainly that no transcript is reachable and which route failed
how. Offer to build the note from the user's own recollection or notes instead —
`meeting-note` handles rough notes fine. Do not fabricate meeting content.

## Handling the text

- Transcripts are long. A 30-minute meeting can swamp the context window — summarize as
  you read rather than quoting whole stretches back.
- Auto-transcription mangles domain vocabulary. Expect Sabre, GDS, PNR, Andavo, folio,
  and people's names to come through wrong; correct them from context where you're sure
  and flag where you aren't.
- Note if the transcript starts late or ends early — it only covers the recorded portion,
  and pre-recording discussion is simply absent.

## Confidentiality

A transcript is the least filtered record the company produces: personnel comments,
customer names, contract terms, credentials read aloud. Treat it as confidential, keep
it out of the vault as raw text, and carry only the summary forward.
