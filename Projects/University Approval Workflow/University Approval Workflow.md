# University Approval Workflow

## Purpose

Build an **optional, standalone approval layer** ("verbal approval") for **university
events and group travel**. An advisor with an unticketed reservation in
[[Products & Systems#Sabre|Sabre]] can send the trip detail to **any email address** —
typically an **event arranger** who is *not* a school-designated approver — and get an
**approve/deny** back before ticketing.

The defining constraint: it must be **entirely independent of the school's existing
approval process**. A past failure had **Compleat**/[[Products & Systems#Air Portal|Air
Portal]] read the verbal approval as "already approved" and skip the school's own approval
layer.

Scope is **events and groups**, where travelers are largely **non-profiled guests not
employed by the university**. Corporate clients don't need it.

## Current state

- (2026-08-20, see [[Meetings/Verbal Approval for University Events and Groups Meeting 2026-08-20]])
  Requirements gathered with [[Emily Drees]], [[Elliot Frenzel]], and [[Mike Harris]]. Flow
  diagrammed live — see [[Projects/University Approval Workflow/Approval Flow|Approval Flow]]. Not yet ticketed.
- (2026-08-20) **No timeline committed.** **ICs** are the top priority; this sits high
  after that. Elliot's unchallenged guess was **a couple of months**.
- (2026-08-20) Ops-side ownership is **changing hands** — Elliot is handing off his role in
  roughly three weeks, so the requirements owner will change.
- (2026-08-20) Good candidate for the **workflow capabilities** being built with
  [[Teams/Velocity/Velocity|Velocity]] and [[Teams/Blitz/Blitz|Blitz]] — the reason Matt
  was pulled onto the requirements call.

## Requirements

Confirmed needs:

- Send an unticketed reservation to an **arbitrary, changeable email address** — not a
  configured approver record.
- Approver sees the **itinerary detail a normal invoice would show** (passenger, flights,
  prices), **minus ticket numbers**, before ticketing.
- Approver can **approve or deny**; the result routes back to trigger the advisor to issue.
- **Optional free-text message** advisor → approver. The capability is required; filling it
  in is not.
- **Denial reason** capturable and routed back to the advisor.
- **Timestamped documentation** of the approval/denial in **trip history** (required).
- **Completely optional** invocation — never driven by an "always" rule.
- Must **not affect** the school's approval flow in any of its three shapes (none / all
  bookings routed / conditional).

Explicitly **not** required:

- **No PDF** in the email, and no "log into another system" step — two hyperlinks in an
  email is acceptable. Delivery format is the implementer's choice.
- **No client-facing reporting** — these are one-offs. The only need is accurate capture of
  the approval/denial and reporting it back internally.
- **No post-ticketing notification** to the arranger — existing systems already send the
  final itinerary.

Wish list (wants, not needs):

- On approve, **auto-queue straight to Compleat** for ticketing with no advisor step.
- Fully automated round trip, with the approval landing back in the **PNR/Sabre** on its
  own.

## Technical notes

- Delivered as a **[[Products & Systems#Red App|Red App]] smart button** on an unticketed
  PNR, per the shape discussed.
- **Separate workflow, not part of Finalize Trip.** Bolted onto Finalize Trip, advisors
  would forget to opt out, the verbal approval would be skipped, and the trip would ticket
  through the school flow. Sequence: run verbal approval → approval received → run
  **Finalize Trip**.
- Auto-queue to Compleat only works when the required **units** are already filled out —
  advisors generally complete those before sending for approval.
- **Client setting** to expose the button, scoped to **university and group** clients rather
  than corporate.
- Prior art: **Travelport / TP+** had a separate smart button that emailed for approval,
  wrote the verbal approval into the **PNR**, and notified the advisor — but left the
  advisor to **manually queue to Compleat**.

## Open questions

- Write the approval to the **PNR** as well as trip history, or trip history only?
- Delivery mechanism for approve/deny (email links vs. a hosted page) — determines how the
  denial-reason box works.
- Is the client setting per-university, or a blanket group/university flag?

## Related

- [[Meetings/Verbal Approval for University Events and Groups Meeting 2026-08-20|Verbal Approval for University Events and Groups Meeting 2026-08-20]]
- [[Projects/University Approval Workflow/Approval Flow|Approval Flow]]
- [[Projects/Offline Approvals/Offline Approvals|Offline Approvals]] — separate approval
  work; also touches PNR approval remarks
- [[Products & Systems]]
