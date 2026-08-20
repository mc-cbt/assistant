---
date: 2026-08-20
type: meeting
attendees: [Emily Drees, Elliot Frenzel, Matt Condie, Mike Harris, Josh Phelan]
source: Teams transcript
---

# Verbal Approval for University Events and Groups Meeting 2026-08-20

> [!note] Source
> Generated from the Teams transcript (Graph transcript API). The API returns
> `speakerAttribution: false`, so **speaker names are inferred from context** — treat
> attributions as best-effort, not verbatim labels. Recording ran **16:36–17:07 UTC
> (10:36–11:07 AM MDT)** against a 10:30–11:00 AM MDT invite, so the **first ~6 minutes
> are missing**. Organizer [[Mitchell Cannon|Mitch Cannon]] did **not** attend — the
> meeting was explicitly framed as capturing requirements for him to review afterward.
> Speakers: [[Emily Drees]], [[Elliot Frenzel]], [[Matt Condie]], [[Mike Harris]]. **Josh Phelan** was invited but did not
> appear to speak on the recorded portion.

## Summary

Requirements-gathering session for a **"verbal approval"** capability for **university
events and group travel**: an *optional, additional* approval layer that lets an advisor
send an unticketed reservation to an arbitrary email address (typically an **event
arranger**, not a school-designated approver) for approve/deny before ticketing. The core
constraint is that it must be **completely independent of the school's existing approval
process** — a past problem was that **Compleat**/**Air Portal** saw the approval and
skipped the school's own approval layer. [[Matt Condie|Matt]] pushed the conversation from
proposed solution back to needs, and diagrammed the flow live (see
[[Projects/University Approval Workflow/Approval Flow|Approval Flow]]). No timeline committed — **ICs** remain the
higher priority.

## Discussion

### The problem

- These are **event/group requests**: large numbers of travelers who are **not employed by
  the university**, mostly **non-profiled guests** (occasionally profiled).
- Advisors agree in advance with the **arranger** on what is permissible to book, but some
  arrangers still want to **personally sign off on every reservation before ticketing** —
  "my name is on this."
- Today the only path is the arranger **calling in or emailing on every single
  reservation**.
- Prior art: **Travelport / TP+** _(transcript reads "Travel Port" and "TP plus")_ had a
  **separate smart button** that emailed for approval, wrote the verbal approval into the
  **PNR**, and notified the advisor — but the advisor still had to **manually queue it to
  Compleat**.

### Independence from school approval — the hard constraint

- Three existing school patterns: **no approval needed** (instant ticketing), **all
  bookings routed to a specific approver**, and **conditional approval** by circumstance.
  The team considers those well covered already.
- Whatever "verbal approval" does must **not touch** any of them. The past failure mode:
  approval was captured, then **Compleat/Air Portal read it as "already approved"** and
  skipped the school's layer.
- The two concepts must stay **entirely separate**, with neither impacting the other.

### Requirements as landed

- **Point an unticketed reservation at any email address** — free-form and changeable, not
  tied to a configured approver record.
- Approver receives the **itinerary detail a normal invoice would show** (passenger,
  flights, prices) **minus ticket numbers**, before ticketing.
- Approver can **approve or deny**, and the result comes back to trigger the advisor that
  it's OK to issue.
- **Optional free-text message from advisor → approver** (e.g. "I know this is against
  policy, here's why"). The *capability* is a hard requirement; **filling it in is
  optional**.
- **Denial reason** should be capturable and routed back to the advisor — today deniers
  just email in.
- **Timestamped documentation** of the approval/denial — hard requirement. Landed on
  **trip history** as required; **PNR** left as an open question (see Decisions).
- **Completely optional / standalone** — must not hang off an "always" rule, because the
  scenarios vary too much.

### Explicitly *not* required

- **No PDF requirement** and no "log into another system" requirement — an email with two
  hyperlinks scraping the trip data was called acceptable. "Dealer's choice, whichever
  looks best and is easiest."
- **No client-facing reporting** — these are one-offs, not a formal school process. The
  only need is *"the accurate capture of the approval or denial and the reporting of it
  back to us."*
- **No notification back to the arranger after ticketing** — existing systems already send
  the arranger the final itinerary.

### Wish list (wants, not needs)

- On approve, **auto-queue straight to Compleat** for ticketing with no advisor step. Both
  Elliot and Matt want this; Elliot explicitly said he can live without it.
- Fully automated round trip — advisor clicks once, approval comes back into the
  **PNR/Sabre** on its own.

### Scoping and delivery shape

- **Separate workflow, not part of Finalize Trip.** Emily's reasoning: bolted onto
  Finalize Trip, advisors will forget to opt out, the verbal approval gets skipped, and it
  tickets through the school flow. Advisors would run the verbal-approval workflow first,
  then **Finalize Trip** once approval is in hand.
- Practical consequence: auto-queue to Compleat only works if the required **units** are
  already filled out — which Elliot says advisors do before sending for approval anyway.
- **Client setting** to gate the smart button: Elliot's position is every university could
  need it, but Emily noted **only universities and group advisors need it — not
  corporate**. Consensus that a client setting makes sense here.
- Matt flagged this as a **good candidate for the workflow capabilities** he's building
  out with [[Teams/Velocity/Velocity|Velocity]] and [[Teams/Blitz/Blitz|Blitz]] — the
  reason Mitch pulled him onto the call.

### Timeline

- No commitment given. Matt: **"ICs are number one on the priority right now"**; this sits
  below that but high after. Elliot's own guess of **"a couple of months"** was not
  contradicted.
- Elliot noted the **ops side is in transition** and he's handing his role off in roughly
  **three weeks** — part of why he asked.

## Decisions

- (2026-08-20) **Verbal approval will be a standalone, optional workflow**, not folded
  into **Finalize Trip** — agreed by Emily, Elliot, and Mike.
- (2026-08-20) It must be **fully independent of the school's approval process** and must
  not cause **Compleat/Air Portal** to skip that process.
- (2026-08-20) **Documentation in trip history is required**; whether it also writes to the
  **PNR** is an **open question** to clarify (Matt marked the diagram accordingly).
- (2026-08-20) **No PDF and no reporting requirements** — delivery format is the
  implementer's choice, provided the approval/denial is accurately captured and reported
  back.
- (2026-08-20) A **client setting** to enable the button is the likely approach, scoped to
  **university and group** clients rather than corporate.

## Open questions

- Write approval to the **PNR** as well as trip history, or trip history only?
- Delivery mechanism for the approve/deny action (email links vs. a hosted page) — drives
  how the denial-reason box works.
- Whether the client setting is per-university or a blanket group/university flag.

## Action items

- [ ] [[Matt Condie]] — huddle with [[Mike Harris|Mike]] and [[Mitchell Cannon|Mitch]]
      after the call to flesh out the requirements further.
- [ ] [[Mitchell Cannon|Mitch Cannon]] — review the recording and follow up (a further
      meeting was expected).
- [ ] [[Mike Harris]] — design the flow, aiming for fewest clicks / most seamless
      experience.
- [ ] [[Matt Condie]] / [[Mike Harris]] — decide **PNR vs. trip history** documentation and
      close out the open questions before ticketing the work.

## Links

- [[Projects/University Approval Workflow/University Approval Workflow|University Approval Workflow]]
  — the project this meeting kicked off
- [[Projects/University Approval Workflow/Approval Flow|Approval Flow]] — the flow Matt diagrammed live in this
  meeting
- [[Projects/Offline Approvals/Offline Approvals|Offline Approvals]] — separate approval
  work; also touches PNR approval remarks
- [[Products & Systems]] — **Sabre**, **Red App**, **Air Portal**, **Andavo**
- [[Teams/Velocity/Velocity|Velocity]], [[Teams/Blitz/Blitz|Blitz]] — workflow
  capabilities this would build on
- [[Daily/2026-08-20]]
