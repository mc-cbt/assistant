# Velocity

## Team

- **Tanner Davies** — Team Lead, Senior Software Engineer
- **Jake Knowlton** — Software Developer
- **Mitchell Cannon** ("Mitch") — Product Manager (PM)

## Subfolders

- [[Teams/Velocity/Standup/Standup|Standup]]

## Responsibilities

- Maintaining the **legacy Air Portal** product.
- Building the **Red App** — an application that runs inside the **Sabre** GDS (Global Distribution System).

## Notes

- (2026-06-29, see [[Daily/2026-06-29]]) Met with [[Chad Maughan]] and [[Mitchell Cannon|Mitch]] re: customer **Jackson & Coker**:
  - **Passive segment copy/edit** built — works with **Hotel** and **Car** ([[Jake Knowlton|Jake]] / [[Tanner Davies|Tanner]]); Tanner is working on **Air** segments.
  - Use case: long-term car rentals for *locum tenens* doctors/nurses (rentals spanning several months).
  - **Ops wants to delay deployment** pending agent training (to prevent abuse).
  - Idea: pass **feature flags from PostHog → Red App** via an endpoint in Andavo, to gate Red App features Ops isn't ready to release. Chad wants this built in the near future.
  - **Top priority now: complete active segment editing** — should start ~6/30. Follow up in standup.
  - Chad to experiment pointing **Sabre EDS events → a local NATS.io** to gauge event volume and decide how to use those events.
