# Form of Payment (FOP) — Product Requirements Document

**Status:** Draft for review
**Last updated:** 2026-06-25
**Author:** Matthew Condie (engineering)
**Product owner:** Kyle Crowther
**Primary source:** "FOP Product requirements review" meeting, 2026-06-19 (Kyle Crowther, Matthew Condie, Jonathan Law), plus related Teams discussion.

> **Confidentiality:** Contains internal product plans and a named client (State of Louisiana). Treat as confidential.
>
> **Draft caveat:** This PRD is reconstructed from a meeting transcript and chat threads. Several items are marked **[TO CONFIRM]** or **[OPEN]** and need validation against the latest Figma and codebase before they are treated as committed scope. Vendor/system names taken from an auto-generated transcript (Conferma, Compleat, Sabre Red App, AEL) should be verified against authoritative internal sources.

---

## 1. Overview

### 1.1 Summary
Form of Payment (FOP) gives a company the ability to **designate which credit card is used during the booking process**, automatically and per scenario, rather than relying on the traveler to supply their own card. Today Andavo stores cards but has **no ability to designate a card for any purpose** — this capability is net-new.

"Complex FOP" refers to the rules-driven variant: selecting the card based on a trip/profile **attribute** (e.g., department, cost center) or a special flow such as **arranger** or **virtual card**.

### 1.2 Problem statement
- There is **no real form-of-payment integration in Andavo today**; prior legacy payment logic lived outside the system and is incomplete.
- Companies want to consolidate expenses (e.g., all flights on one corporate card) so they can **reconcile receipts to cards easily** from the data Andavo/Christopherson returns.
- Some companies need **per-department / per-attribute** card selection rather than a single company card.
- The current **expired-card failure loop is painful**: a booking fails at mid-office (Compleat), opens a support/JIRA ticket, support investigates, the account manager contacts the client, the client updates the card, and the booking is retried — a long manual chain. Ops asked for an automated **backup card** mechanism.

### 1.3 Goals
- Let a travel manager designate company cards for **Air, Rail, and Hotel** segments (Car is excluded).
- Support **attribute-based** card selection (department, cost center, rule class, etc.) and the existing **arranger** flow.
- Surface the correct card(s) at **checkout**, defaulting the company-preferred card while still allowing the traveler's own cards.
- Provide an optional **backup card** to avoid stuck bookings when the designated card is expired.
- Build the configuration experience in **both Admin and Internal** apps.

### 1.4 Non-goals (V1)
- **Split form of payment** (paying across multiple cards) — newly possible in the GDS; explicitly deferred.
- **Add-ons / non-segment payments** — deferred; expected to slot in later without much trouble.
- **Reductive "card not allowed" policies** — **Decided:** V1 is additive only (which cards are allowed). Reductive/exclusion rules revisited post-V1.
- **Andavo-side virtual-card generation** — virtual cards continue to be generated at mid-office (Compleat/Conferma) for now.
- **Sabre Red App integration / "killing Sabre"** — long-term direction, not V1.
- **Per-attribute logic on traveler (personal) cards** — never; the most granular a traveler card gets is per-segment, and that is itself a future item.
- **Multiple attributes per segment** and **multiple cards per attribute value** — V1 is one attribute per segment, one card per value (architect to allow future expansion).

---

## 2. Background & context

### 2.1 Driving client: State of Louisiana
- The entire state is the client and does **not** charge to a single card.
- Each department has **three individuals who hold a credit card ("CBA cards"**; the expansion of "CBA" is currently unknown — **[TO CONFIRM]**). Travelers know their department's cardholder.
- This is the **arranger flow**, which is **already built/hard-coded** and must **not** be broken by this work.
- Rollout decision: roll out **100% of divisions at once** (rather than department-by-department, which would have been a "massive nightmare"). **Target go-live: October 2026.**

### 2.2 Current systems / integration points
- **Sabre (GDS)** stores cards today (the "Sabre wallet"). Long-term goal is to manage payments natively in Andavo and "kill Sabre."
- **Compleat (mid-office)** processes bookings; generates virtual cards via **Conferma**, and swaps a static hotel-guarantee card.
- **Conferma** generates **one-time-use virtual cards** (hotel today; air being added).
- **AEL** — Andavo Expression Language; Andavo's ANTLR-based attribute/expression rules engine (lives in `general-model`, package `com.andavo.model.expression`). Used today for client-attribute rules, approvals, and workflows — **not** for payment rules (see §2.3).

### 2.3 What already exists in the codebase (current state)
A code review of `andavo-dev/andavo` found that more of the data layer is already built than originally assumed. This reshapes V1 scope toward the **segment dimension, UI, checkout, and backup/virtual additions** rather than rules storage.

- **Generic payment-rule store already exists.** PR #3683 added `wallet_payment_rule` — a generic `(client_id, payment_rule_type_id, value) → credit_card_id` table (unique on `client_id, payment_rule_type_id, value`). `PaymentRuleType` already supports **`ATTRIBUTE`, `RULE_CLASS`, and `ARRANGER`**, each validated against the correct source. So **attribute-based and rule-class-based card selection is already persisted today.**
- **Arranger tagging** is a Boolean `is_arranger_card` flag on `wallet_credit_card` plus an `ARRANGER`-type row in `wallet_payment_rule` mapping `arrangerUserId → cardId`. (Note: despite PR #3683's description, **no `CORPORATE_ARRANGER` card-type enum was added** — it's a flag on the existing `CORPORATE` type.)
- **Admin/company-card wallet UI already exists**, merged to `main` but feature-flagged off via PostHog flag **`client-wallet`** (`apps/admin-web/.../Settings/WalletPage`). The backend (`/v1/wallet/...`, gated by `AUTHORITY_WALLET_ADMIN`) is fully live. A richer "Payments + Corporate wallet" UI exists as **draft PR #5050** (by [[Jessica Wright|Jess]]) on mock data. *(The earlier "Sohail built it / commented out" theory was incorrect — no such authorship exists.)*
- **Attribute eligibility is already enforced.** `WalletService.validateAttributeValue` rejects attributes whose value list is empty, so only **list-valued** attributes (`InputType.LIST`) are selectable; free-form attributes (e.g., Employee ID, `InputType.INPUT`) are already excluded. **Rule Class** is a first-class list on the Client aggregate (`Client.getRuleClasses()`), separate from the attributes table — matching FR-17.
- **Segment model exists** (`SegmentType`: FLIGHT→AIR, HOTEL→HOTEL, CAR→CAR, TRAIN→RAIL) and AEL already knows `SegmentType` in approval/workflow scopes — but there is **no segment concept in the payment-rule path yet.** Adding it means a new `PaymentRuleType.SEGMENT` (value = `AIR|RAIL|HOTEL`), no schema change.

---

## 3. Personas & roles

| Persona | Capabilities |
|---|---|
| **Travel Manager / Admin** | Configures company cards; designates cards per segment / attribute / arranger / virtual; sets backup cards. |
| **Traveler** | Books travel; at checkout sees the highlighted company default card plus their own cards; can switch to a personal card; can add a card at checkout (always personal). |
| **Arranger** | A traveler who can designate a card to be used as the arranger card (already built; State of Louisiana CBA cardholders). |
| **Internal staff (Christopherson/Andavo support, Account Managers)** | Need the wallet + settings inside the **Internal** app to support clients. Currently chase down expired-card updates with clients. |
| **Ops / online support** | Handle failed-booking tickets today; requested the backup-card feature. |
| **Advisor (future)** | Sabre Red App flow — would benefit from knowing which traveler card to use per segment. Out of V1. |

> **Decided (out of V1):** Department heads / managers self-selecting their own department's FOP after the company configures it (raised in chat by Josh Cameron) is **out of scope for V1**. Only Admin/Internal configure cards; revisit delegated self-service later.

---

## 4. Functional requirements

> Workstreams (as scoped in the meeting): (1) store card↔segment/attribute associations, (2) build the card-selection endpoint, (3) build the configuration UI (Admin + Internal), (4) build the checkout flow (built last).

### 4.1 Card / wallet management (Admin + Internal)
- **FR-1.** Provide a **company-card wallet** in the Admin app, distinct from the traveler's personal wallet, showing the organization's company cards.
- **FR-2.** Provide the same wallet capability in the **Internal** app so Christopherson/Andavo staff can support clients. *(Internal may combine cards + settings on one page; Admin may keep them as two pages.)*
- **FR-3.** Add a card via standard credit-card fields, with an optional **nickname**.
- **FR-4.** Support a **card (grid) view** and a **list/table view**, toggleable. *(The grid is cheap to build; the toggle is low-cost and likely retained.)*
- **FR-5.** Provide a **"Use this payment method for"** control on the company card's add/edit form, assigning the card to one or more **segment types** (Air, Rail, Hotel — **multi-select**; **Car excluded**).
- **FR-6.** When a card is assigned to a segment, display a **segment icon** on the card tile (e.g., airplane for air, hotel icon for hotel).
- **FR-7.** The segment/attribute assignment controls appear on **company cards only** — never on traveler cards (for now).
- **[TO CONFIRM] FR-8.** Bidirectional configuration: allow assigning segment/attribute from **both** the card screen and the settings screen (Kyle unsure; verify against latest Figma with designer [[Jessica Wright|Jess]]).

### 4.2 Payment-rules / settings screen ("complex FOP" engine)
- **FR-9.** Provide a **Settings page** (separate from the wallet) that shows, **per segment (Air / Rail / Hotel)**, which card should be used.
- **FR-10.** For each segment, offer a configuration dropdown with these options:
  1. **Traveler's card** (default).
  2. **A specific company card.**
  3. **Based on an attribute** (the complex path — see §4.3).
  4. **Virtual card** (only when the Andavo payment / Conferma client setting is enabled — see §4.4).
  5. **Inherit from another segment** (e.g., Rail inherits Air's configuration). The option to inherit a segment must not appear within that same segment's own list.
- **FR-11.** **Default behavior:** if nothing is configured for a segment, the **traveler's card** is used. A blank configuration intentionally means "traveler's card." (Design decided not to force an explicit selection.)
- **FR-12.** **Missing-value banner/notification:** persistently surface unconfigured values (e.g., "there are 3 values you need to set up for Air"). Clicking through reopens the configuration modal. **Decided:** use **warning** styling (most clients fill in all values, so a missing one is notable).
- **FR-13.** **Pin/sort unconfigured values to the top** for visibility. *(The arranger rules screen is believed to already do this; reuse if possible.)*
- **[TO CONFIRM] FR-14.** Migrate the existing "rules" tab to the modal-based pattern; make the existing "base it off of" control **segment-specific**; potentially remove the existing allow/deny toggle in favor of "segment defined ⇒ payment rules; not defined ⇒ traveler's card." Verify current behavior in code.

### 4.3 Attribute-based card selection ("based on an attribute")
- **FR-15.** When a segment is set to "based on an attribute," prompt the user to **choose the attribute**.
- **FR-16.** Eligible attributes = **any list-valued attribute** (fixed value list). **Free-form attributes (e.g., Employee ID) are excluded.** Attributes may be **profile-level or trip-level**.
- **FR-17.** Include these **special first-class values** in the attribute list even though they are not in the attributes table:
  - **Arranger** — routes into the existing (already-built) arranger flow / State of Louisiana CBA logic.
  - **Rule Class** — a first-class, list-valued attribute.
- **FR-18.** **One attribute per segment** for V1 (architect for possible future multiple attributes).
- **FR-19.** After an attribute is chosen, list **every value** of that attribute and let the user assign a card to each. **Decided:** **one card per value** (single-select) for V1 — matches the existing `wallet_payment_rule` unique key `(client, type, value)`. Multi-select-per-value revisited post-V1.
- **[TO CONFIRM] FR-20.** **Bulk select** multiple attribute values and assign one card to all at once (confirm exact behavior with [[Jessica Wright|Jess]]).
- **FR-21.** Different segments may use **different attributes** (e.g., Air by Department, Hotel by Cost Center → two independent configurations). If a segment is not attribute-based, it simply uses its assigned company card or the traveler's card.

### 4.4 Virtual cards (Conferma) — mostly future, called out for architecture
- **FR-22.** When the **Andavo payment / Conferma client setting** is enabled, expose **"Virtual card"** as a per-segment option.
- **FR-23.** A virtual card is treated like a single card (similar to the traveler's card) and is **never attribute-based**.
- **FR-24.** Today, virtual cards are generated at **mid-office (Compleat → Conferma)**; hotel uses a static guarantee card replaced at Compleat. The future state (Andavo generating the one-time card at booking time) is **out of V1 scope**.
- **[OPEN] FR-25.** Checkout display for a virtual card that does not exist until submit — design TBD (possibly a separate project).

### 4.5 Checkout flow (traveler experience) — built last
- **FR-26.** On the review/checkout screen, populate applicable cards from the **new card-selection endpoint** (§4.6).
- **FR-27.** If exactly **one** company-level card applies to the context, **default it**, show **last four**, and **visually highlight** it as the company-preferred card (design work with Gregory). Show the traveler's own cards underneath.
- **FR-28.** If **two or more** company cards apply, **do not default** — present a required selection field. *(Expected ~1% of cases.)*
- **FR-29.** Allow the traveler to **add a card at checkout**, with a checkbox **"save to my travel profile"** vs. use-once. A card added in the booking flow is **always a traveler/personal card**. Company cards can only be added via Admin/Internal.
- **FR-30.** The **arranger checkout is unique**: the card is **not** inserted at time of booking (unlike all other flows). Preserve the existing behavior.
- **[OPEN] FR-31.** **Attribute-collection timing:** if payment depends on a **trip** attribute, the value must be collected **before** card selection (today attributes/UDIDs are collected at "purchase"). Likely solution: a client-setting-driven experience that prompts for the attribute earlier when payment is attribute-based.

### 4.6 Card-selection endpoint (back end)
- **FR-32.** Build an endpoint that **returns the list of applicable cards** given context: the **traveler** (→ their cards), the **client/company**, the **segment** (e.g., air), and relevant **trip/profile attribute values**.
- **FR-33.** Logic is **additive** (which cards are allowed) for V1 — **decided**; reductive "not allowed" rules are out of V1.
- **FR-34.** The endpoint feeds the **checkout flow** first and is intended to later feed the **Sabre Red App** flow (Andavo inserting cards directly). Red App is long-term.

### 4.7 Backup payment — **in V1 (decided)**
- **FR-35.** Allow an optional **backup card** per configuration. If the primary designated card is **expired** at checkout, fall back to the backup so the booking is not stuck.
- **FR-36.** If the backup is also expired, fall through (ultimately to traveler selection).
- **FR-37.** If the designated card **is the traveler's card**, there is **no backup** — prompt the traveler to fix/add a card at checkout.
- **FR-38.** **Expiry notifications** must also cover backup cards.

---

## 5. Business rules summary
- **Blank configuration = traveler's card.** No company card defined ⇒ the traveler's card is on the hook for payment; this must always be surfaced via the missing-values banner.
- **99% case:** one designated card per scenario, defaulted at checkout; traveler can still pick their own card. **~1% case:** multiple company cards apply ⇒ default none, force selection.
- **Segment FOP applicability:** Air, Rail, Hotel require FOP; **Car never does.**
- **Card tagging dimensions:** company vs. traveler card; arranger-tagged (already built); per-segment (multi-select); per-attribute-value (single card per value in V1).
- **Inherit:** a segment can inherit another segment's full mapping to avoid rebuilding.
- **Decline/expiry fallback:** designated expired ⇒ backup ⇒ (if expired) fall through; traveler card ⇒ no backup, prompt at checkout.
- **Traveler cards:** never attribute-based; segment/attribute tile is shown on company cards only.
- **Hotel** is expected to be simpler (often virtual or static guarantee card); attribute-based hotel mapping is allowed but rare.

---

## 6. Non-functional & technical considerations
- **Reuse existing storage (not greenfield):** card↔purpose associations are already persisted in the generic `wallet_payment_rule` table `(client, payment_rule_type_id, value) → card`. **Add `PaymentRuleType.SEGMENT`** (value = `AIR|RAIL|HOTEL`) to extend it to segments — no schema change. **Constraint:** the unique key `(client, type, value)` allows one card per value (consistent with the single-card-per-value decision); a combined "segment AND attribute" key would require composite-value encoding or a schema extension.
- **Payment rules are NOT AEL today** (corrected): they are a flat `PaymentRule {type, attributeId}` client setting plus `wallet_payment_rule` rows, resolved by a plain `switch` on `PaymentRuleType`. There is nothing AEL to "wrap" for backward compatibility. AEL is a separate, capable engine and already models `SegmentType` in approval/workflow scopes, so a future migration of payment rules onto AEL (with a segment-bearing scope) is feasible but **not required for V1**.
- **Attribute model (verified in code):** only list-valued attributes (`InputType.LIST`) are eligible — `WalletService.validateAttributeValue` already rejects empty-value-list attributes, so free-form (e.g., Employee ID) is excluded automatically. "Rule Class" is first-class via `Client.getRuleClasses()`, separate from the attributes table.
- **PCI / encryption (separate workstream):** cards must be decrypted and re-encrypted another way (story owned by JQ; ~1–2 months). Confirmed **separable** from FOP. **Mitigation:** access cards through an **abstraction/function** so the encrypt/decrypt implementation can change underneath without affecting FOP code.
- **Sabre constraints:** long-term goal to pull company cards out of Sabre into Andavo and insert cards via the Sabre Red App. Whether cards can be **synced out of Sabre automatically is unknown** — ask Jake/Tanner.
- **Cardholder-name / Sabre FOP remark constraints** (from related chat): the `CardHolderName` element in the Sabre `UpdatePassengerNameRecordRQ` FOP remark exposes only GivenName/Surname (both optional); when Andavo replaces the FOP for complex-FOP clients, the correct cardname handling needs direction to avoid failing the FOP or side effects. **[TO CONFIRM]** with someone who knows the Sabre financial side effects.

---

## 7. Scope & phasing

**In scope (V1):**
1. **Segment dimension on the existing rules store** — add `PaymentRuleType.SEGMENT` (`AIR|RAIL|HOTEL`); attribute/rule-class/arranger association storage already exists (reuse `wallet_payment_rule`).
2. **Card-selection endpoint** — returns applicable cards given context (traveler, client, segment, attribute values); additive logic; single card per value.
3. **Configuration UI** — finish/unflag the wallet page (behind `client-wallet`, likely building on draft PR #5050) + settings/payment-rules page, in **Admin and Internal**.
4. **Backup card** — optional per-config fallback + backup expiry notifications (FR-35–38).
5. **Checkout flow** — default + highlight the company card, show traveler cards, add-card-at-checkout (built last).

**Out of scope (V1):** split payment; add-ons/non-segment payments; reductive "not allowed" policies; Andavo-side virtual-card generation; Sabre Red App integration; per-attribute logic on traveler cards; multiple attributes per segment; multiple cards per value; department-head self-select.

**Estimate:** No firm estimate. Framing from the meeting: "days for the bare-bones plumbing, then **week-to-infinity** of polish, refinement, and quirks." Delivery cadence: small incremental PRs roughly daily / every other day.

---

## 8. Dependencies
- **Design ([[Jessica Wright|Jess]], Gregory):** latest Figma source of truth; checkout default-card highlight; attribute-collection timing; empty states; confirm bidirectional config and bulk-select. **Draft PR #5050** ([[Jessica Wright|Jess]]) is the likely UI starting point.
- **Existing admin wallet:** confirmed to exist behind PostHog flag **`client-wallet`** (backend live). V1 finishes/unflags it rather than building from scratch.
- **Arranger flow:** must remain intact; State of Louisiana go-live in October 2026.
- **PCI encryption story (JQ):** separate but card-access abstraction must accommodate it.
- **Sabre sync feasibility:** Jake/Tanner.
- **Conferma / virtual-card air expansion:** in progress.

---

## 9. Open questions & decisions

### 9.1 Resolved
| # | Question | Resolution |
|---|---|---|
| 1 | Additive vs. reductive logic | **Additive only for V1**; reductive/exclusion rules deferred. |
| 2 | Reuse arranger card-tag storage vs. build new | **Reuse** `wallet_payment_rule` (generic `(client, type, value) → card`); add `PaymentRuleType.SEGMENT`. Attribute/rule-class/arranger storage already exists. |
| 3 | Does an admin wallet already exist? | **Yes** — merged behind PostHog flag `client-wallet`; backend live. Draft PR #5050 ([[Jessica Wright|Jess]]) is a richer UI. "Sohail" attribution was incorrect. |
| 4 | Missing-value banner styling | **Warning.** |
| 5 | Backup card in V1 or punt | **In V1** (FR-35–38). |
| 9 | Multi-select cards per value | **Single card per value** for V1. |
| 11 | Department-head self-select | **Out of V1.** |
| 14 | Verify AEL spelling / payment-rule storage | **AEL = Andavo Expression Language.** Payment rules are **not** AEL today (flat format) — the "wrap in AEL" plan is dropped. |

### 9.2 Still open — needs design (route to [[Jessica Wright|Jess]]/Kyle follow-up)
6. **Attribute-collection timing** at checkout — when payment depends on a *trip* attribute, the value must be collected before card selection (today UDIDs are collected at purchase). Likely a client-setting-driven earlier prompt.
7. **Virtual-card checkout UX** — how to display a card that doesn't exist until submit; possibly a separate project.
8. **Bidirectional config** (FR-8) and **bulk-select** (FR-20) behavior — confirm against latest Figma.

### 9.3 Still open — needs a subject-matter expert
10. **Sabre card-sync feasibility** — can company cards be synced out of Sabre automatically? Ask Jake/Tanner.
12. **Cardname handling** for Sabre FOP replacement on complex-FOP clients (Sabre `CardHolderName` only exposes GivenName/Surname) — needs someone who knows the Sabre financial side effects (Jeanine).
13. **"CBA card"** meaning — likely the industry term *Central Bill / Corporate Billed Account*, but **unconfirmed**; verify with Kyle.

---

## 10. Action items (from the meeting)
- **Matthew:** investigate payment-rule storage (AEL?) and arranger tag reuse; review AEL attribute/segment handling; reuse the existing traveler card-grid component; start building in small daily/every-other-day PRs; ask Maddie about the hidden/flagged admin wallet; ask Jake & Tanner about Sabre card-sync feasibility.
- **Kyle:** sync with design ([[Jessica Wright|Jess]]/Gregory) on checkout highlight, attribute-collection timing, empty states, bidirectional config, bulk-select, latest Figma; dig into whether the admin wallet already exists; pursue Sabre→Andavo card-sync on the product side; keep the encryption story with JQ; schedule a ~30-min follow-up (Monday/Tuesday) when [[Jessica Wright|Jess]] is back, inviting Jonathan and pulling in Ricky or Maddie.
- **Jonathan:** available for architecture/backup support; confirmed encryption is separable; help reach out re: the hidden wallet.

---

## 11. Glossary
- **FOP** — Form of Payment. "Complex FOP" = attribute/rule-driven payment selection.
- **OBT** — Online Booking Tool (Andavo's booking platform).
- **GDS / Sabre** — Global Distribution System; the card store today ("Sabre wallet").
- **Sabre Red App** — Sabre's agent-side app; future target for Andavo-inserted cards.
- **Compleat** — Mid-office system; processes bookings, generates virtual cards via Conferma, swaps the static hotel-guarantee card.
- **Conferma** — Virtual-card vendor; one-time-use cards (hotel today, air being added).
- **Virtual card** — One-time-use card generated per booking.
- **CBA card** — Per-department cardholder cards used by State of Louisiana; drives the arranger flow. "CBA" is likely *Central Bill / Corporate Billed Account* (industry term) but **unconfirmed** — verify with Kyle.
- **Arranger / arranger flow** — Already-built flow where a designated cardholder's card is used; card not inserted at time of booking; tied to State of Louisiana.
- **AEL** — Andavo Expression Language; ANTLR-based rules engine (`com.andavo.model.expression`). Used for client-attribute/approval/workflow rules — **not** payment rules today.
- **Attribute** — Profile- or trip-level data point; only list-valued (`InputType.LIST`) attributes are eligible for FOP.
- **Rule Class** — A first-class (not in attributes table) list-valued attribute.
- **UDID** — User-defined record attributes on a booking, collected at purchase; used for reconciliation/distribution.
- **Traveler/personal card** vs. **Company card** — personal cards added via booking/profile (never attribute-based); company cards managed in Admin/Internal (only these get segment/attribute/arranger tagging).
- **Backup card** — Optional emergency card used if the designated card is expired.
- **Split payment** — Paying across multiple cards; out of V1 scope.
- **Admin** vs. **Internal** — client/travel-manager-facing config vs. Christopherson/Andavo staff support tooling; both need wallet/settings.
