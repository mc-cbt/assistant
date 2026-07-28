# Anatomy of a Corporate Trip

The fastest way to understand the ecosystem is to trace one trip through it. Every player in [[Ecosystem Layers]] touches one of the steps below. Once you can see the spine, the rest is just attaching vendors to the right vertebra.

In an integrated program the traveler consciously experiences maybe **three** of these steps. The other nine happen in the background — that invisibility is the point.

## The twelve steps

| # | Step | What happens | Players involved |
|---|------|--------------|------------------|
| 1 | **Trigger and approval** | Someone decides they need to travel. Depending on the company, they either just book (if in policy) or get pre-approval from their manager. | Travel policy, sometimes a pre-trip approval tool |
| 2 | **Profile and preferences** | Loyalty numbers, seat preferences, meal restrictions, payment methods, passport details — pulled from the traveler's profile so they don't re-enter them. | Profile system (Concur Profile, DataFlex Net, TripSource, [[Glossary#TMC|TMC]]-native), [[Glossary#SSO|SSO]] provider |
| 3 | **Search and shop** | The traveler opens the [[Glossary#OBT|OBT]] or calls an agent. The system queries multiple content sources for available flights, hotels, cars at applicable rates. | OBT, [[Glossary#GDS|GDS]], [[Glossary#NDC|NDC]] channels, hotel networks, car rental APIs |
| 4 | **Pre-trip approval** | If required by policy, the booking pauses for a manager or finance approver. Auto-approves if in policy. | OBT pre-trip approval workflow, sometimes a separate tool |
| 5 | **Booking and ticketing** | The system creates a [[Glossary#PNR|PNR]] (passenger name record), issues the ticket, books the hotel, reserves the car. Confirmations go to the traveler. | TMC mid-office, GDS, ticketing platform, supplier APIs |
| 6 | **Payment** | The trip charges to a corporate card, a virtual card, or a central pay account. Each model has different reconciliation implications. | Corporate card issuer, virtual card platform (Conferma, AirPlus), TMC central pay |
| 7 | **Pre-trip prep** | Visa check, risk briefing, itinerary push to the traveler's phone, calendar invites, mobile app load. | Visa vendor, duty-of-care platform, itinerary app |
| 8 | **The trip itself** | The traveler flies, checks in, attends the meeting, returns. If something disrupts (cancelled flight, delay, illness), the TMC and risk providers respond. | TMC 24/7 desk, duty-of-care responder, supplier (airline, hotel) |
| 9 | **Receipts and expense** | Receipts collected (often automatically via card feeds and OCR), itinerary imported into the expense system, expense report submitted. | Expense platform (Concur, Navan, Ramp, etc.), card data feeds, OCR/receipt apps |
| 10 | **Reconciliation** | Expense report data, card transaction data, and booking data get matched. Mismatches flagged. Approvers review. | Expense platform, finance ERP, card issuer |
| 11 | **Reporting** | All trip data — bookings, spend, policy compliance, savings, supplier mix, carbon — rolls up into dashboards for procurement, finance, and travel managers. | TMC reporting, independent reporting (DataFlex, Grasp), BI tools |
| 12 | **Negotiation and program optimization** | Annual hotel [[Glossary#RFP|RFPs]], airline volume reviews, policy updates, supplier rationalization, carbon goals. Feeds data back into next year's program. | TMC consulting team, procurement, hotel sourcing platform |

## The key insight: two adjacent steps not talking

> When a customer asks why their current setup is broken, ninety percent of the time it is because **two adjacent steps in this chain are not talking to each other.** Booking and expense do not match. Card data does not flow into reporting. The duty-of-care feed is missing the international trips because they were booked outside the OBT.

Your job is to find the seams and explain how an integrated program closes them. (This is the CSM lens on the trip spine.)

## Related

- [[Why Companies Hire a TMC]]
- [[Ecosystem Layers]] — each vendor maps to one of these steps.
- [[Decision Frameworks]] — the four data flows and where they break.

---
*Source: New Hire Orientation Packet (Jeff Madsen) — Part 2: The Corporate Travel Ecosystem (Field Guide). See [[Travel Industry Primer/Travel Industry Primer|Travel Industry Primer]].*
