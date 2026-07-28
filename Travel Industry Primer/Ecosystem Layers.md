# Ecosystem Layers

The players, layer by layer. Every entry follows the same pattern: a short definition for someone with no industry context, the job the layer does in the trip, the major vendors and what camp they live in, how the layer connects to a [[Glossary#TMC|TMC]], and questions to ask a customer. The **fifteen layers** cover the complete ecosystem, in the order they appear in a trip.

1. Identity and profile management
2. Online booking tools ([[Glossary#OBT|OBTs]])
3. The TMC itself — the hub
4. Global distribution systems and [[Glossary#NDC|NDC]]
5. Hotel sourcing and rate loading
6. Ground transport
7. Corporate cards and payment rails
8. Expense management
9. Reporting and analytics
10. Risk and duty of care
11. Sustainability and carbon
12. Visa and immigration services
13. Travel insurance
14. Quality control and fare optimization
15. Meetings and events ([[Glossary#SMM|SMM]])

---

## Layer 1 · Identity and profile management

**What it is.** The system that stores who the traveler is and what they prefer — name as it appears on their passport, frequent flyer numbers, Known Traveler Number, Global Entry, seat preferences, meal restrictions, payment methods, emergency contacts, sometimes passport and visa documents.

**The job.** Without a profile, every booking starts from zero. With a profile, the OBT and the agent both pull the same data automatically. It also enables single sign-on, so the traveler has no separate password for the booking tool.

**Major vendors:**

| Vendor | Position |
|--------|----------|
| SAP Concur Profile | Bundled with Concur Travel and Expense. Default profile system for most large enterprises that run on Concur. |
| DataFlex Net/Grasp | Independent profile and data hub. Used by TMCs that want a profile system not tied to a specific OBT. |
| TripSource | BCD Travel's traveler-facing profile and itinerary platform. |
| TMC-native profiles | Most TMCs maintain their own profile databases as system of record, syncing into OBTs as needed. |
| Okta, Microsoft Entra ID, Google Workspace SSO | Identity providers that let a traveler use their work login to access the OBT and other tools. Not travel-specific, but always involved. |
| Umbrella | Built a TMC-facing tool called **Faces** for traveler profile storage. Faces has pre-built connections with OBTs and GDSs for profile syncing. |

**Connection to the TMC.** Profiles flow both ways. The TMC pushes loyalty redemptions, document numbers, and preferences back into the profile; the OBT pulls preferences during shopping. When a profile lives in two systems and they drift, you get duplicate bookings, wrong loyalty numbers, and missing TSA pre-check. **Profile sync is one of the most common quiet failure modes in a travel program.**

**What to ask a customer:**
- Where does the profile data live today, and is it the same in your booking tool, your expense tool, and your TMC?
- Who owns updating Known Traveler Numbers and Global Entry IDs when they renew?
- Are travelers single sign-on into the booking tool, or do they have a separate password?

---

## Layer 2 · Online booking tools (OBTs)

**What it is.** The self-serve interface where travelers book their own flights, hotels, and cars without calling an agent. The corporate equivalent of Expedia, except it shows the company's negotiated rates, enforces policy, and routes for approvals.

**The job.** OBTs handle high-volume, low-complexity bookings — domestic round trips, single-hotel stays, simple car rentals. Roughly **70–80% of transactions** in a healthy program flow through the OBT. The remaining **20–30%** (international multi-leg trips, executive itineraries, group bookings, last-minute changes) go to an agent. Push everything into the OBT and you frustrate travelers; route everything to agents and you pay high transaction fees.

**Major OBTs:**

| OBT | Owner | Position |
|-----|-------|----------|
| SAP Concur Travel | SAP Concur | Market leader by enterprise share. Tightly integrated with Concur Expense. Undergoing a multi-year platform modernization ("Concur Travel evolution") that is the source of significant industry chatter. |
| Cytric Travel | Amadeus | Enterprise OBT with strong European footprint. Owned by Amadeus (one of the three big GDSs). Now branded as part of "Cytric Easy" with Microsoft Teams integration. |
| Spotnana | Spotnana | Newer, modern, API-first travel platform. Sold both as an OBT and as a full TMC backbone. Powers some other brands behind the scenes. |
| Deem | Travelport | Modern OBT used by mid-market and enterprise. Often paired with traditional TMCs wanting a cleaner UX than Concur. |
| Navan (booking) | Navan | Built into the Navan all-in-one platform. Cannot be used standalone; you must use Navan as the TMC. |
| Egencia | Amex GBT | Egencia is now part of Amex GBT. Their OBT remains a major mid-market option. |
| Andavo Online | [[Christopherson Business Travel|Christopherson]] | Christopherson's own OBT and platform layer. Modern UX, multi-source content, integrated with the agent and reporting layers. |

### TMC-agnostic vs. TMC-native OBTs

- **TMC-agnostic:** Concur Travel, Cytric, and Deem can sit on top of multiple TMCs. The same Concur Travel installation could be served by Christopherson, BCD, or AmexGBT depending on which TMC contract the company holds. This is most of the enterprise market.
- **TMC-native:** Navan, Egencia (Amex GBT), and Andavo Online are tightly bundled with their parent TMC and not designed to be operated by a different TMC. **Choosing the OBT is essentially choosing the TMC.**

**Connection to the TMC.** When a traveler clicks Book on the OBT, the OBT sends the booking to the TMC, the TMC issues the ticket through a GDS or directly with an airline, the confirmation flows back to the OBT, and data flows to the reporting layer. The TMC also handles all post-booking servicing (schedule changes, refunds, exchanges) even on bookings that started in the OBT.

**What to ask a customer:**
- What percent of your bookings are made online today? Below 50% online adoption signals a clunky OBT or a workforce that needs handholding — both create cost.
- Is your OBT bundled with your TMC or independent? This determines whether changing TMCs requires also changing the OBT.
- How is policy configured? Most policy violations come from policies that are too rigid, not too lax — overly strict OBT settings push travelers to book outside the tool.

---

## Layer 3 · The TMC itself — the hub

**What it is.** The travel management company. The contracted vendor that holds the relationship with the airlines, hotels, and supplier networks; provides agents; runs the mid-office and ticketing infrastructure; produces reporting; and owns the program-management relationship with the customer.

**The job.** Everything in this guide flows through or around the TMC. The OBT calls into it. The expense tool pulls from it. The duty-of-care provider feeds off its itinerary stream. The reporting layer aggregates its data. The card program reconciles against it. *A TMC that is not the hub of the program is not really a TMC — it is a booking agency with extra steps.*

**The three camps** (commit to memory; see [[Market & Competitors]] for detail):

| Camp | Who lives there | Strengths & weaknesses |
|------|-----------------|------------------------|
| Service-heavy legacy | AmexGBT, BCD, FCM, CWT (now part of GBT) | **Strengths:** global scale, board-level relationships, deep enterprise programs. **Weaknesses:** inflexible tech, hidden fees, slow UX adoption. |
| Tech-first / self-serve | Navan, Perk, Egencia (next-gen) | **Strengths:** modern UX, integrated expense, low/zero fees. **Weaknesses:** weak after-hours service, limited reporting depth, no global SLA, total cost rises at scale. |
| Tech-forward TMC | [[Christopherson Business Travel|Christopherson]] / Andavo, Direct-ATPI | **Strengths:** platform sophistication of a tech company plus the human support of a traditional TMC. **Weaknesses:** smaller global footprint than legacy giants, less brand recognition. |

**How TMCs make money** (see [[TMC Economics]]):
- **Transaction fees.** Per booking, often differentiated by online vs. agent-touched. The traditional model. Every TMC has them; the question is how much is hidden in markups.
- **Management or technology fees.** Monthly or per-traveler subscription for platform access, account management, reporting. Increasingly the dominant model in modern programs.
- **Supplier commissions and overrides.** Hotel commissions especially — paid by the hotel chain to the TMC for booking volume. Some TMCs rebate these to the customer; others keep them.

**What to ask a customer:**
- Who is your current TMC, and what model are you on — transaction fees, management fees, or both?
- What are your top three frustrations with them? (Listen for service quality, reporting depth, technology, account management.)
- When does the contract expire? Most TMC contracts run two to three years with auto-renewal. The window to switch is six to nine months before expiration.

---

## Layer 4 · Global distribution systems and NDC

**What it is.** The plumbing that connects airlines and hotels to travel agencies and OBTs. When you searched Expedia and saw fares from twelve airlines, you were looking at a GDS feed. Most corporate travel content flows through GDSs, with a growing share moving to NDC (New Distribution Capability) and direct connects.

**The three GDSs:**

| GDS | Headquarters | Notes |
|-----|--------------|-------|
| Sabre | Southlake, TX | Largest in North America. Most U.S. airlines and TMCs ride on Sabre. Owns SynXis (hotel CRS) and various agency platforms. |
| Amadeus | Madrid, Spain | Largest in Europe and globally by some measures. Owns Cytric (OBT) and significant hotel and rail content. |
| Travelport | London / Atlanta | Operates Galileo, Apollo, and Worldspan (legacy brands consolidated). Smaller share than Sabre or Amadeus, but still major. |

**NDC and direct connects.** NDC is an IATA standard that lets airlines push richer content — branded fares with detailed attributes, ancillaries like seat upgrades and bags, dynamically priced offers — directly to agencies, instead of forcing everything through the GDS data model. Most major airlines now offer NDC content; adoption is uneven across TMCs and OBTs. Companies routing bookings through agencies that cannot consume NDC see lower fare options and miss airline-direct discounts.

**Direct connects** are a direct API integration with an airline, bypassing both GDS and NDC framing. Examples: Southwest (historically not on the GDS at all; requires a direct connect for corporate booking), Lufthansa Group, and major low-cost carriers.

**Why this matters.** Content depth is a real differentiator. A TMC plugged into all three GDSs, NDC channels for major carriers, plus direct connects will surface lower fares and more options than one tied to a single GDS. **Christopherson is GDS-agnostic; some competitors are not.**

**What to ask a customer:**
- Are you seeing NDC content in your current OBT? A surprising number of programs are not, and they are leaving money on the table.
- How does Southwest get booked? If "travelers book it themselves," that volume is invisible to their program.

---

## Layer 5 · Hotel sourcing and rate loading

**What it is.** The activities and platforms that get negotiated hotel rates loaded into the channels travelers actually use. Hotel content is the messiest part of corporate travel. Flights are essentially commodified (a few hundred airlines globally); there are roughly **a million hotels**, each with its own rate structure, every chain with its own loyalty program, every market with its own seasonality.

**The annual RFP cycle.** Some large companies run an annual hotel sourcing process, typically **September through November**, asking preferred chains in their top travel cities for negotiated rates. The rates then get loaded into the GDS, the OBT, and the agent screens; the cycle repeats every year. Smaller companies skip the formal RFP and rely on TMC-negotiated rates (rates the TMC has secured for its book of business).

**Major sourcing platforms and programs:**

| Platform / Program | Owner | Position |
|--------------------|-------|----------|
| HRS | HRS Group | Major independent hotel sourcing and procurement platform. RFP automation, rate auditing, payment integration. |
| Lanyon (now Cvent) | Cvent | Hotel RFP and meetings sourcing platform, widely used by enterprise procurement. |
| BCD Stay | BCD Travel | BCD's hotel content marketplace; gives BCD customers access to ~49,700 properties. |
| Premier Select | AmexGBT | AmexGBT's hotel content and savings program for their book of business. |
| Hotel Engine | Engine (independent) | Marketplace-style platform popular with mid-market and SMB. Negotiated rates without per-company RFPs. |
| Booking.com for Business | Booking Holdings | Aggregator content, not corporate-negotiated. Sometimes plugged into OBTs as a content fallback. |
| Oversee | Oversee | Hotel rate auditing — finds lower rates after booking and rebooks automatically. Most TMCs deploy it behind the scenes. |

**Connection to the TMC.** Hotels enter the program through several pipes — the GDS feed, direct connects to chains, marketplace content from BCD/HRS/AmexGBT, and Booking.com aggregators. A good TMC presents all of these in one shopping experience and applies the company's negotiated rates first. **Hotel attachment rate** (percentage of trips where the hotel is booked through the program) is a useful health metric — weak hotel content sees bookings drift to consumer sites.

**What to ask a customer:**
- Do you run an annual hotel RFP, or rely on TMC-negotiated rates?
- What is your hotel attachment rate? Below 60% is a problem. Above 80% is healthy.
- Do you use a rate auditing tool like Oversee?

---

## Layer 6 · Ground transport

**What it is.** Rental cars, rideshare, and black car services. Smaller spend than air or hotel for most companies, but a high-touch traveler experience layer.

**Major players:**

| Category | Vendors |
|----------|---------|
| Rental car | Avis Budget Group (Avis, Budget, Payless), Enterprise Holdings (Enterprise, National, Alamo), Hertz (Hertz, Dollar, Thrifty), Sixt |
| Rideshare | Uber for Business, Lyft Business |
| Black car / chauffeur | Blacklane, Carey, Groundspan (aggregator) |
| Rail (EU and corridors like NYC-DC) | Amtrak Business, Trainline, Eurostar, SNCF Connect, Deutsche Bahn |

**Connection to the TMC.** Rental cars usually flow through the GDS like air and hotels. Rideshare typically integrates via direct app linkage — Uber for Business plugs into Concur Expense to push receipts automatically and can be tied to company policy. Black car services book through dedicated platforms, sometimes via the agent.

**What to ask a customer:**
- Do you have a preferred rental car program with negotiated rates?
- Is Uber for Business connected to your expense system, or are travelers expensing their own rides?

---

## Layer 7 · Corporate cards and payment rails

**What it is.** How the trip gets paid for. The choice of card model dictates how reconciliation works, how clean the data is, how fast cash-back rewards arrive, and how much fraud risk lives in the system.

**The four card models:**

| Model | How it works | Trade-offs |
|-------|--------------|------------|
| Individual card | Each traveler uses a card in their name; they pay it, the company reimburses via expense. | Clean for the company, friction for the traveler (out-of-pocket while waiting for reimbursement). |
| Corporate liability card | Each traveler gets a card; the company pays the issuer directly each cycle, not the traveler. | Less traveler friction. More fraud risk. Standard at large enterprises. |
| Lodge / central pay | One card or account on file at the TMC. All bookings charge to it. Travelers do not see the card. | Cleanest data feed. Strongest reconciliation. Standard for air and hotel in mature programs. |
| Virtual card per booking | A unique, single-use card number generated for each booking, often via a dedicated platform. | Maximum fraud control and matching precision. Adds vendor complexity and supplier acceptance issues. |

**Major issuers and platforms:**

| Category | Players |
|----------|---------|
| Card issuers (corporate) | American Express (Corporate, Business Platinum, BTA), Citi Commercial Cards, JPMorgan Chase Commercial Card, Bank of America, Capital One Spark, U.S. Bank |
| Networks | American Express, Visa, Mastercard |
| Virtual card platforms | Conferma Pay (Sabre), AirPlus International, eNett (Booking Holdings), WEX, Mesh Payments |
| Cards-first platforms (card + expense bundled) | Ramp, Brex, Mercury, Mesh — increasingly common in startups and mid-market |

**Connection to the TMC.** Three things matter: (1) the TMC needs the card on file to charge bookings; (2) the card data feed needs to flow into the expense system so transactions match itineraries; (3) if the company uses lodge or virtual cards, the TMC operates them — Conferma in particular is widely integrated with TMC mid-office systems. **Clean card data feeds (merchant codes, transaction IDs, matched bookings) eliminate hours of expense work per traveler per month** — one of the most undersold value points in corporate travel.

**What to ask a customer:**
- What card model do you use today, and is air booked on a different card from hotel?
- Does your card data feed flow into your expense system automatically, or are travelers re-entering it?
- Have you looked at virtual cards for hotel? A common quick win, especially for chargeback issues with hotels.

---

## Layer 8 · Expense management

**What it is.** The system where travelers submit expense reports after a trip and where finance approves and reimburses. Often confused with travel: travel is about booking and managing the trip; expense is about reconciling and paying for it after the fact.

**Major platforms:**

| Platform | Owner | Position |
|----------|-------|----------|
| SAP Concur Expense | SAP Concur | The market giant. Bundled with Concur Travel by default. Most large enterprise programs run on Concur Expense whether or not they use Concur Travel. |
| Navan Expense | Navan | Bundled with Navan Travel. Cannot be used standalone. Strong UX, modern card integration. |
| Expensify | Expensify | Strong in SMB and mid-market. Lightweight, mobile-first, popular with engineering-led companies. |
| Ramp | Ramp | Cards-first platform with expense and bill pay built in. Aggressive mid-market growth over the last three years. |
| Brex | Brex | Similar to Ramp — corporate cards plus expense plus reimbursements. Common in venture-backed companies. |
| Emburse | Emburse (parent) | Holds Certify, Chrome River, Captio, Tallie, SpringAhead. Mid-market and enterprise. Often the fallback for companies wanting an alternative to Concur. |
| Workday Expenses | Workday | For companies that already run Workday HR and Finance. Tight ERP integration. |
| Coupa Expense | Coupa | Part of Coupa's broader procurement and BSM suite. Common where Coupa is the procurement platform of record. |

**Connection to the TMC.** Three integration points: (1) the TMC pushes itinerary data so receipts and bookings line up automatically; (2) the card feed (corporate or virtual) flows into the expense system; (3) after approval, expense data sometimes flows back to the TMC's reporting layer for a complete spend view. When these three flows work, expense reports get pre-populated and travelers spend minutes not hours. When they do not, you have a complaint.

**What to ask a customer:**
- What expense system are you on? (Narrows the integration conversation immediately.)
- How long does it take a traveler to file an expense report? Above 30 minutes per report signals data is not flowing.
- Are travel data and expense data reconciled, or are they two separate reports for finance?

---

## Layer 9 · Reporting and analytics

**What it is.** The dashboards, reports, and data feeds that tell the company what is actually happening: spend by category/supplier/department, policy compliance rates, savings vs. published fares, carbon footprint, online adoption. The boring-but-essential layer that turns travel from a cost center into a managed program.

**Where reporting comes from:**

| Source | What it gives you |
|--------|-------------------|
| TMC-native reporting | Every TMC has its own. Strong for booking data: spend, suppliers, savings, online adoption, fare type mix. |
| Grasp Technologies | Independent reporting and data hub. Used for multi-TMC consolidation, regional rollups, benchmarking. |
| Prime Analytics | Reporting and consulting platform focused on benchmarking and savings tracking. |
| Customer-side BI | Tableau, Power BI, Looker. The TMC or CIS feeds raw data; the customer's analytics team builds custom views. |

**What good reporting actually answers:**
- How much are we spending on travel, by category, department, region, traveler?
- How much are we saving, vs. published fares and vs. last year?
- What is our policy compliance rate, and where is it breaking?
- Who are our top suppliers by volume, and are we hitting preferred-supplier targets?
- What is our carbon footprint per trip, per department, in total?
- Where are our travelers right now? (Live duty-of-care view.)
- Where do we leak — bookings outside the program, expense reports with no matching itinerary, etc.?

**What to ask a customer:**
- When you walk into the boardroom and need to report on travel spend, where does that data come from? (Often: "my analyst pulls it from three places and stitches it together.")
- Do you have a single dashboard for spend, savings, compliance, and carbon, or are these separate?

---

## Layer 10 · Risk and duty of care

**What it is.** The legal and ethical obligation a company has to keep traveling employees safe — in some jurisdictions a literal legal duty ("duty of care"). The supporting infrastructure: real-time traveler tracking, pre-trip risk briefings, in-trip alerting, medical and security assistance, evacuation services.

**Major providers:**

| Provider | Position |
|----------|----------|
| International SOS | The largest player. Medical and security assistance, 24/7 multilingual support, evacuation, clinics in 90+ countries. Default for global enterprises. |
| Crisis24 (formerly GardaWorld) | Strong global intelligence and security operations. Owns Drum Cussac and other intel firms. |
| Global Rescue | Evacuation-focused. Smaller scale than ISOS but well-known for field rescue. |
| World Travel Protection (WTP) | Owned by Zurich Cover-More. Mid-market and enterprise duty-of-care services. |
| Healix | Medical and security assistance. Common in UK and EU programs. |
| Anvil (now part of WorldAware) | Intelligence and risk management; consolidations have moved this space around in recent years. |

**Connection to the TMC.** The TMC sends a real-time itinerary feed to the duty-of-care provider — every booking, change, cancellation. The provider matches travelers to risk data. If something happens, the security team queries the platform and sees who is in the affected area. **This integration is not optional in a mature program; it is one of the biggest reasons companies hire a TMC at all.**

**What to ask a customer:**
- Who is your duty-of-care provider, and how does data flow from your TMC?
- What happens if a traveler books outside your program (e.g., personal Expedia account for a work trip)? Almost always: that traveler is invisible to the duty-of-care system. Big risk.

---

## Layer 11 · Sustainability and carbon

**What it is.** The infrastructure for measuring, reporting, and sometimes offsetting the carbon footprint of business travel. A relatively new layer — most programs added it after 2020. Increasingly required for ESG and CSRD reporting, particularly for European companies and U.S. companies with European subsidiaries.

**Major platforms:**

| Platform | Position |
|----------|----------|
| Thrust Carbon | Independent emissions calculation and reporting platform. Integrates with TMCs, OBTs, expense systems. |
| Squake | European-headquartered emissions calculation and offsetting platform. Strong in EU programs. |
| CHOOOSE | Norwegian platform; sustainable aviation fuel (SAF) procurement and emissions reporting. |
| Atmosfair | German non-profit. Carbon offset and SAF programs, often used for compliance reporting. |
| TMC-native | Most TMCs now offer emissions data in reporting; quality varies by methodology. |

**How it works.** Booking data — flight legs, distances, cabin class, hotel nights, car miles — flows into the calculation engine. The engine applies a methodology (DEFRA, GHG Protocol, sometimes airline-specific data) to compute kilograms of CO2 equivalent per trip. Aggregated reports support corporate ESG goals; per-trip data sometimes appears in the OBT to nudge travelers toward lower-emission choices.

**What to ask a customer:**
- Do you report on travel emissions today, and to whom? Investor relations? Internal sustainability team? CSRD? (The audience changes the requirements.)
- Are emissions visible to travelers at the point of booking?

---

## Layer 12 · Visa and immigration services

**What it is.** Specialized vendors that help travelers obtain visas, manage passport renewals, and handle immigration documentation. Almost always handled outside the TMC, but referred by it.

**Major providers:**

| Provider | Position |
|----------|----------|
| CIBT (CIBTvisas) | The largest player in the U.S. corporate visa space. Often the default referral from TMCs. |
| VFS Global | Operates visa application centers worldwide on behalf of governments. The infrastructure layer underneath many corporate visa programs. |
| VisaCentral | U.S.-headquartered visa service. Direct competitor to CIBT. |
| Newland Chase | Immigration and visa consulting; focus on long-term assignment and immigration alongside business visas. |

**Connection to the TMC.** The TMC flags trips that need a visa during the booking flow and refers the traveler to the visa vendor. Some TMCs have integrations that pre-populate the visa application with traveler details. The visa vendor handles the actual passport handling, government interaction, and document return.

---

## Layer 13 · Travel insurance

**What it is.** Insurance coverage for trip cancellation, interruption, baggage loss, medical emergencies, and evacuation. Sometimes bundled with corporate cards (Amex Platinum, Chase Sapphire), sometimes purchased per trip, sometimes carried as an annual program.

**Major providers:**

| Provider | Position |
|----------|----------|
| Allianz Global Assistance | The largest. Bundled with many travel platforms and cards. |
| Travel Guard (AIG) | Major U.S. corporate travel insurance underwriter. |
| Generali Global Assistance | Strong in Europe, growing in U.S. corporate. |
| Card-bundled coverage | Amex Platinum, Chase Sapphire Reserve, and many corporate card products include trip protection. Often overlooked — and sometimes redundant with separately purchased coverage. |

---

## Layer 14 · Quality control and fare optimization

**What it is.** Tools that watch the program for opportunities to save money after the booking is made. Auto-rebook a flight if the fare drops. Audit a hotel rate against a lower one. Catch duplicate bookings. Flag policy exceptions. The plumbing that turns a static booking into a continuously optimized one.

**Major tools:**

| Tool | Function |
|------|----------|
| Yapta (now part of Coupa) | Automatically rebooks air and hotel when fares drop. The category-defining tool. Often run silently by the TMC. |
| Oversee | Hotel rate auditing — finds lower rates after booking. Most TMCs deploy it. |
| FareIQ, FairlyOdds | Smaller players in fare savings. |
| Mid-office quality control (TMC-internal) | Every serious TMC runs scripts in their mid-office to flag issues — duplicate bookings, fare disparities, missing loyalty numbers, policy exceptions. |

**What to ask a customer:**
- Are you running fare and hotel rate auditing? Many small and mid-market programs are not, and they should be.

---

## Layer 15 · Meetings and events (SMM)

**What it is.** Strategic Meetings Management — the discipline of treating internal meetings, conferences, customer events, and incentive trips as a managed category, the same way transient travel is managed. Group air, group hotel blocks, registration, attendee management, on-site logistics. A separate-but-adjacent ecosystem.

**Major platforms and providers:**

| Category | Players |
|----------|---------|
| Event management platforms | Cvent (the dominant platform), Bizzabo, Splash, Hopin, RainFocus |
| Hotel and venue sourcing | Cvent Sourcing (formerly Lanyon), HRS Meetings, Groupize |
| TMC meetings teams | AmexGBT M&E, BCD M&E, FCM Meetings, Christopherson Meetings & Events |
| Group air specialists | Most major TMCs have dedicated group air desks for groups of ten or more travelers |

**Connection to the TMC.** Most large TMCs have a dedicated meetings and events division, separate from the transient travel team. Some companies use their TMC for both; others use a specialized event firm and route only the air through the TMC. The lines blur, and integrations between event platforms and travel programs are a frequent customer ask.

## Related

- [[Why Companies Hire a TMC]]
- [[Anatomy of a Corporate Trip]]
- [[Decision Frameworks]]
- [[Where Christopherson & Andavo Plug In]]
- [[Vendor Cheat Sheet]]
- [[Glossary]]

---
*Source: New Hire Orientation Packet (Jeff Madsen) — Part 2: The Corporate Travel Ecosystem (Field Guide). See [[Travel Industry Primer/Travel Industry Primer|Travel Industry Primer]].*
