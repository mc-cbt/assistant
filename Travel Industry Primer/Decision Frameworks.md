# Decision Frameworks

How the pieces talk to each other (Part 4) and the frameworks that give customers a sharper read on their own situation (Part 5). The frameworks are not gospel — every company is different — but they reflect patterns that have held up across hundreds of programs.

---

## Part 4 · How the pieces talk to each other

### The four data flows that matter most

Almost every integration conversation, every customer pain point, every "why is our reporting wrong" question traces back to one of these.

| Flow | From | To | Why it matters |
|------|------|----|----|
| **Profile sync** | Profile system | [[Glossary#OBT|OBT]], [[Glossary#TMC|TMC]], expense | If profiles drift, you get duplicate bookings, wrong loyalty numbers, missing TSA pre-check, mismatched expense data. |
| **Itinerary feed** | TMC mid-office | Expense, duty of care, reporting | If itineraries do not flow, expense reports require manual receipt entry, duty of care misses travelers, and reporting is incomplete. |
| **Card data feed** | Card issuer | Expense, reporting | If card data does not flow, expense reconciliation is manual and slow. Fraud risk goes up. Spend visibility is incomplete. |
| **Booking data feed** | TMC mid-office, OBT | Reporting, sustainability, supplier negotiation | If booking data is fragmented across systems, reporting requires stitching, supplier negotiations are weaker, sustainability calculations are approximate. |

### Where data typically breaks

- **Out-of-channel bookings.** Travelers book on consumer sites, supplier-direct sites, or personal accounts. Those bookings are invisible to the TMC, the duty-of-care provider, and reporting. **Industry-typical leakage is 10–25% of trips.**
- **Multi-TMC programs.** Companies with regional TMCs (e.g., Christopherson in the US, a different TMC in EMEA) need a consolidation layer like DataFlex Net or Grasp to roll up reporting.
- **Profile drift.** Loyalty numbers, payment methods, and document numbers stored in three places, kept in sync by no one.
- **Expense and travel disconnected.** Expense reports do not match booking data because the systems were never integrated. Travelers re-enter everything manually.
- **Card data feed gaps.** Card transactions hit one system, expense lines hit another, and finance has no clean way to reconcile.

### The integration question that wins deals

> When diagnosing a customer, ask: *"If a traveler books a flight, books a hotel through the booking tool, charges everything to their corporate card, files an expense report, and finishes the trip — how many systems did that data have to live in, and which ones do not talk to each other?"*

The answer is your starting opportunity map. (See [[Anatomy of a Corporate Trip]] for the spine the data travels along.)

---

## Part 5 · Decision frameworks

### Framework 1 · Does the company need a TMC at all?

Comes up most with smaller customers weighing managed vs. unmanaged. The answer is rarely about cost alone.

| Signal | Probably no TMC needed | TMC strongly indicated |
|--------|------------------------|------------------------|
| Annual travel spend | Under $50K | Over $1M |
| Trip volume | Under 50 trips/year | Over 200 trips/year |
| International travel | Domestic only | Significant international or multi-leg |
| Industry | Tech, services, low compliance | Regulated (life sciences, financial services, government, defense) |
| Risk profile | Low-risk destinations only | Executives, journalists, high-risk regions |
| Group bookings | Rare | Conferences, offsites, customer events |
| Reporting needs | Simple expense reports suffice | Procurement, finance, sustainability all need data |

See [[Why Companies Hire a TMC]] for the thresholds and triggers behind this.

### Framework 2 · OBT vs. agent vs. hybrid

Almost no real-world program is purely one or the other. The question is the mix.

| Profile | OBT-only | Agent-only | Hybrid (most programs) |
|---------|----------|-----------|------------------------|
| Best for | Simple domestic travel, junior travelers, cost-sensitive programs | Complex international, executives, high-touch industries (entertainment, sports, government) | Mixed — OBT for routine bookings, agent for complex |
| Trade-off | Travelers handle complexity themselves; high failure cost on edge cases | Agent fees on every booking; high cost at volume | Requires good policy on when to escalate to agent |
| Typical online adoption rate | 95%+ | 0% (by definition) | 60–85% |

### Framework 3 · Bundled vs. best-of-breed

Once a company decides to have a managed program, the next question is whether to buy the whole stack from one vendor or assemble best-of-breed per layer.

| Approach | What it looks like | Trade-off |
|----------|--------------------|-----------|
| **Bundled (single TMC stack)** | TMC + their OBT + their reporting + their card integration + their expense partner. Sometimes one logo for everything (Navan). | Easier integration, single throat to choke, simpler procurement. Limited best-in-class per layer. |
| **Hybrid** | TMC of your choice + agnostic OBT (Concur Travel, Cytric, Deem) + best expense system + chosen card + independent reporting. | Strong per layer, common pattern at enterprise. Integration burden falls on the customer or the TMC. |
| **Pure best-of-breed** | TMC, OBT, expense, cards, duty of care, reporting, sustainability — all independent vendors selected on their own merits. | Best capability per layer. Heaviest integration cost. Requires a strong internal travel manager or consultant. |

### Framework 4 · Program maturity model

A useful diagnostic when you walk into a customer cold. Most companies are at stage 1 or 2 and want to get to stage 3. (See also [[Travel Program Maturity]].)

| Stage | Description | Common signals |
|-------|-------------|----------------|
| **Stage 0 · Unmanaged** | No TMC, no policy, everyone books on consumer sites, expenses on personal cards. | Travel cost is unknown. Finance reconciles by department, not by traveler. No duty of care. Common in companies under 100 employees. |
| **Stage 1 · Basic** | TMC contract, OBT in place, but no real policy enforcement and no card mandate. | Online adoption 30–50%. Travel data lives in the TMC; expense data lives elsewhere. Reporting is ad-hoc. |
| **Stage 2 · Managed** | Written policy, mandated corporate card, TMC + OBT + expense, monthly reporting. | Online adoption 60–80%. Compliance metrics tracked. A real travel manager owns the program. |
| **Stage 3 · Strategic** | Preferred suppliers negotiated annually, sustainability tracked, duty of care integrated, savings calculated and reported. | Online adoption 80%+. Procurement involved. Annual hotel RFPs run. Carbon reporting at least quarterly. |
| **Stage 4 · Integrated** | TMC + expense + cards + risk + meetings all integrated. End-to-end visibility. AI-assisted optimization. Sustainability built into booking flows. | Single dashboard for spend, savings, compliance, carbon. Expense reports auto-populate from itineraries. Small enterprise teams managing large programs. |

## Related

- [[Why Companies Hire a TMC]]
- [[Anatomy of a Corporate Trip]]
- [[Ecosystem Layers]]
- [[Where Christopherson & Andavo Plug In]]
- [[Glossary]]

---
*Source: New Hire Orientation Packet (Jeff Madsen) — Part 2: The Corporate Travel Ecosystem (Field Guide). See [[Travel Industry Primer/Travel Industry Primer|Travel Industry Primer]].*
