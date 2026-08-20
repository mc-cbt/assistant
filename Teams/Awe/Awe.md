# Awe

## Team

_(Inferred from the 6/30 standup — confirm.)_

- **Dallas Norton** — Principal Engineer, Team Manager (lead)
- **Jonathan Law** ("JLaw") — Principal Software Engineer
- **Maddie Petty** — Senior Software Engineer
- **Brian Kingery** — _(role TBD; not in Org Chart)_

## Responsibilities

- Owns the **booking project** — the primary effort the product and engineering org is focused on.

## Milestones

- **GBTA conference (August 2026)** — the booking project is targeted at this conference. Key deadline shaping cross-team priorities.

## Notes

- **Standup notes:** [[Teams/Awe/Standup/Standup|Standup]] — date-stamped daily standup files.
- (2026-06-29, see [[Daily/2026-06-29]]) Met with [[Chad Maughan]] and [[Dallas Norton]] re: team management ahead of **GBTA (Aug 2026)**. Chad wants to push to get some significant features done for the conference; the target feature list lives in the **Awe standup channel** in Teams.
- (2026-08-20, see [[Teams/Awe/Standup/2026-08-20]]) **[[Jonathan Law]] is now Awe team lead** — day-to-day leadership and decisions, making official what he was already doing.
- (2026-08-20, see [[Teams/Awe/Standup/2026-08-20]]) **Blocked on Sabre:** we cannot ship on Sabre's **new APIs** without a **contract amendment**, though they're enabled for us in test. A PoC gets first-shop through first-fare-selection on the new flight shop APIs but must fall back to **BFM** for anchoring and context; it returned more result flights, and timing/sold-out behaviour is unmeasured. Parked on a branch.
- (2026-08-20, see [[Teams/Awe/Standup/2026-08-20]]) **Priority order: planner/arranger ("Ranger") above servicing** (exchanges, cancellations, refunds). Multi-traveler and companion-on-someone-else's-trip explicitly not ready.
- (2026-08-20, see [[Teams/Awe/Standup/2026-08-20]]) **Travelers with missing Sabre profile IDs** can sign into Andavo but can't book and can't self-fix. Three upstream causes: user creation still allowed for clients with the externally-managed-profile flag, one enrollment flow not setting the profile ID, and a missing default rule class failing the push to **Faces**. Stopgap is to surface incompleteness at the start of booking; a bulk admin view is punted as too expensive to compute.
- (2026-08-20, see [[Teams/Awe/Standup/2026-08-20]]) **Booking going out to all internal users**; the **beta bookers** feature flag retires — if you have booking create, you can book.
