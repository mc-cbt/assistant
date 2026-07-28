# Product Portfolio

The [[Christopherson Business Travel]] / Andavo solution catalog is organized into **16 top-level categories**. Most of what you'll touch in the smaller-accounts world falls into **Booking, Payments, Trip Management, Reporting, Risk Management, and Service Delivery**. The full inventory below is grouped by GA, beta/development, and research.

## Release-stage rules — what you can say externally

Each solution shows its release stage. **The stage controls what you can say externally.**

| Stage | What you can say |
| --- | --- |
| **Live (GA)** | Full sales / marketing OK. |
| **Beta** | Sales conversations OK with appropriate framing. |
| **Alpha / Development** | Roadmap discussion **with support from the product team**. |
| **Research** | Internal awareness only. |

> Always verify with the product team before referencing anything that isn't Live in a client-facing artifact. When in doubt, check with the product owner (usually **Tommy in Product Ops**) before referencing anything pre-GA in a client-facing setting.

## What's live today (the GA portfolio)

| Solution | Stage | What it is |
| --- | --- | --- |
| **Andavo Admin** | LIVE | The administrative platform — travel managers, finance, and execs use this to oversee their travel program. Successor to AirPortal; all AirPortal admin capabilities rebuilt and extended here. |
| **Andavo Traveler** | LIVE | The traveler-facing surface. React Native app, web and mobile. Single chronological itinerary view unifying air, car, hotel, rail. Currently still supports AirPortal credentials for login during the transition. |
| **Traveler Trip Management** | LIVE | Self-service trip management for travelers. Mobile and web. |
| **Administrator Trip Oversight** | LIVE | Trip oversight inside Andavo Admin. Centralized visibility into all active, upcoming, and historical trips. Roadmap status: Admin = Beta, but parent solution is live as MVP. |
| **Concur Travel (booking)** | LIVE | SAP Concur's online booking tool. Supported for clients embedded in the Concur ecosystem. We provide agent services, back-office, and configuration. |
| **Deem Booking** | LIVE | Third-party [[Glossary#OBT]], available for Travelport-connected clients not on Concur. |
| **Advisor Services** | LIVE | 24/7/365 human-assisted booking, changes, cancellations, and disruption support. In-house plus after-hours coverage. |
| **Advisor Tools** | LIVE | Proprietary advisor-facing technology embedded in the [[Glossary#GDS]] booking environment. Surfaces traveler intelligence, preferences, policy, and unused tickets to advisors at point of service. |
| **Travel Supply** | LIVE | GDS-agnostic content layer. Multiple GDS sources, [[Glossary#NDC]] channels, direct supplier connects. |
| **Andavo APIs** | LIVE | REST APIs and managed data delivery. Christopherson manages data delivery — clients aren't charged for API access. |
| **Risk Management** | LIVE | Centralized inside Andavo Admin. Traveler tracking, alerts, communication. Replaces the **SecurityLogic** branded tool (do not use SecurityLogic externally — see [[Deprecated Terms]]). |
| **Hotel Sourcing** | LIVE | Managed hotel sourcing and RFP program. Analyzes spend, identifies properties, executes negotiations. |
| **Preferred Rates** | LIVE | Multi-tier portfolio of pre-negotiated hotel rates available to all Christopherson clients from day one. |
| **Rate Assurance** | LIVE | Automated post-booking price monitoring and rebooking for air and hotel. |
| **Sustainability Reporting** | LIVE | Carbon emissions dashboards (DEFRA-aligned) and benchmarking. Delivered as part of the Christopherson partnership. (Formerly **Prime Analytics** — see [[Deprecated Terms]].) |
| **Transaction Reconciliation** | LIVE | Currently a managed service matching financial transactions back to travel booking data. Being productized as a self-service feature in Andavo Admin, currently powered by **DOMO**. |
| **Group & Incentive Travel** | LIVE | Full-service event, meeting, and incentive program management. |
| **VIP Services** | LIVE | White-glove dedicated advisor team for an organization's most notable or frequent travelers. |
| **Policy Development Consulting** | LIVE | Expert guidance on creating effective, balanced travel policies. |

## What's in beta and development

These products are real and being delivered to specific clients, but they have not hit general availability yet. Sales enablement is permitted in most cases — **public marketing is not.** Always check with the product owner before sharing anything externally.

| Solution | Stage / Target | What it is |
| --- | --- | --- |
| **Andavo Payments** | BETA — Q2 2026 GA | Virtual card payment solution. Single-use virtual cards issued automatically with each booking. Replaces the legacy **VirtualPay Lite** product (sunsetting — CSMs are currently leading the migration campaign). Existing VirtualPay Lite clients are the beta cohort. **Conferma** is the underlying card infrastructure but is becoming invisible — clients will eventually only see Andavo Admin. |
| **Andavo Booking** | IN DEV — GBTA 2026 beta unveil | Native online booking tool with GDS-agnostic search and direct connect content. **No migration path from AirPortal — this is net new.** Clients currently using Deem or Concur Travel are potential migration targets at GA. |
| **Policy Engine** | IN DEV — GBTA 2026 beta unveil | Configurable rules engine for travel policy enforcement. Today, policy enforcement happens at the OBT layer (Concur Travel) and at the advisor desk. A native engine is on the long-term horizon. |
| **Reporting (native)** | IN DEV — Post-GBTA 2026 | Native Andavo reporting platform. Self-service dashboards, analytics, deep-dive reporting. Beta clients are applying pressure — strong evidence of market demand for self-service. UI built in Andavo's pattern library. |
| **Trip Request & Proposal** | ALPHA — Post-GBTA 2026 (continued dev) | Structured workflow for guest and event travel. Admins create trip requests, advisors generate curated proposals, guests select. Currently deployed in a single controlled use case (Domo/Domopalooza). **Roadmap only — do not reference in sales conversations without explicit PM approval/support.** |
| **Reconciliation (self-service in Admin)** | IN DEV — Post-GBTA 2026 | The Andavo Admin version of Transaction Reconciliation. Self-service CSV upload, match-by-ticket-number, configurable export. Will run in parallel with the current managed service for clients who prefer the managed approach. |

## What's in research / not yet in build

| Solution | Stage | Why it matters |
| --- | --- | --- |
| **Expense Management** | RESEARCH | Future full-lifecycle expense — receipt capture, submission, approval, reimbursement. Listed because it's a frequent client ask and a known gap vs. Navan/Concur. **Internal awareness only — do not pitch.** |

## Related

- [[Service Delivery Models]] — which solutions to lead with per model.
- [[Deprecated Terms]] — legacy product names mapped to current ones.
- [[Market & Competitors]], [[Vendor Cheat Sheet]].

---
*Source: New Hire Orientation Packet (Jeff Madsen) — Part 1: Company, Market & Product Orientation. See [[Travel Industry Primer/Travel Industry Primer|Travel Industry Primer]].*
