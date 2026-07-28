# Project Spec — Form of Payment (FOP): Admin/Internal Configuration UI + Storage

**Status:** Ready for implementation
**Source PRD:** Form of Payment (FOP) — 2026-06-25 (Matthew Condie)
**Figma:** `Admin - 2026` → section "Default payment method" (node `16959:73556`)
**Feature flag:** existing PostHog `client-wallet` (`FEATURE_FLAGS.ADMIN.CLIENT_WALLET`)

---

## 1. Context

Andavo can store cards but has **no ability to designate which card is used for a booking**. This project builds the **admin-side configuration experience** from the linked Figma: a redesigned **Corporate Wallet**, a **Settings → Payments** per-segment configuration page, an **attribute-configuration modal**, a bidirectional **add/edit corporate card modal**, an **override modal**, and **in-UI warning banners** for unconfigured/expired cards. It also adds the **backend storage** to persist exactly what that UI configures.

Most of the data layer already exists: `wallet_payment_rule` (generic `(client, type, value) → card`), `PaymentRuleType {ARRANGER, RULE_CLASS, ATTRIBUTE}`, the wallet REST surface (`/v1/wallet/...`, `AUTHORITY_WALLET_ADMIN`), and shared React wallet components. The gap is the **segment dimension**, **backup cards**, **per-segment mode**, and the redesigned UI. This spec extends rather than greenfields.

**Driving client:** State of Louisiana (arranger flow, Oct 2026 go-live). The existing **global arranger flow must not break.**

---

## 2. Scope

### In scope
- Backend storage to persist per-segment FOP config (mode, attribute mappings, backup) — **Air / Hotel / Rail only**.
- Read/write REST endpoints feeding the config UI. (Card-tile segment/attribute tags and missing-value counts are derived **client-side** from existing attribute/rule-class/user data + the config response — no dedicated endpoints.)
- Redesigned Corporate Wallet (card grid + list/table toggle, segment/attribute tags, status, banners) in **both Admin and Internal**.
- Settings → Payments per-segment config page (modes incl. inherit/virtual/attribute/specific-card/traveler).
- Attribute-config modal (assign one card per attribute value, individually).
- Add/edit corporate card modal with **full bidirectional assignment** (segment tags, set-as-default, assign-to-attribute-value).
- Override modal; in-UI missing-value (warning) + expired-card banners.
- Built behind the existing `client-wallet` flag.

### Out of scope (deferred / future specs)
- **Card-selection resolution endpoint** (FR-32) and **traveler checkout** (FR-26–31) — separate follow-up spec. Leave a named seam in the resolver (see §4.6).
- **Backend expiry notification system** (email/push, FR-38) — only in-UI banners here.
- **Bulk-select** assign (FR-20); **advanced "Use this payment method when" If/Operator/Value rule builder**.
- **Car** and **Add-ons** segments (Figma shows them; both excluded).
- Top-level Payments section tabs **Virtual cards / Authorizations / Unused tickets** (corporate wallet only).
- **Virtual-card generation** — "Virtual card" is exposed as a per-segment *mode option* (gated by the `ANDAVO_PAYMENTS` setting), but no generation logic.

### Decisions locked (from clarification)
1. Spec = **config UI + storage only**.
2. Storage = **extend `wallet_payment_rule`** with `segment_type` + `is_backup`; widen unique key.
3. Per-segment **mode encoded inside `wallet_payment_rule`** via a SEGMENT mode-marker row + sentinels (no new table, no new client setting).
4. Build **Admin + Internal together**, sharing components.
5. **Corporate wallet + Settings config only** (no other Payments tabs).
6. Gate behind **existing `client-wallet`** flag.
7. In-UI **expiry & missing-card banners** included; bulk-select / advanced builder / expiry-notifications deferred.
8. Add/edit card modal includes **full bidirectional assignment**.
9. **Inherit = live reference** (resolved at read time).

---

## 3. The encoding contract (core design artifact)

All per-segment data lives in `wallet_payment_rule`. Two new columns disambiguate scope:

- `segment_type SMALLINT NULL` — stores the `SegmentType` id (2=FLIGHT/AIR, 4=HOTEL, 5=TRAIN/RAIL). `NULL` = legacy/global.
- `is_backup BOOLEAN NOT NULL DEFAULT false`.

| Concept | type | `value` | `segment_type` | `is_backup` | `credit_card_id` |
|---|---|---|---|---|---|
| Legacy global arranger/rule-class/attribute | 1/2/3 | userId/class/attr | **NULL** | false | card |
| Per-segment MODE marker | **SEGMENT(4)** | sentinel (below) | seg | false | card only for `CARD` mode, else NULL |
| Per-segment per-attribute-value card | ATTRIBUTE(3) | attr value | seg | false | card |
| Per-segment per-rule-class card | RULE_CLASS(2) | rule class | seg | false | card |
| Per-segment per-arranger card | ARRANGER(1) | userId | seg | false | card |
| Per-segment backup card | SEGMENT(4) | `BACKUP` | seg | **true** | card |

**Mode-marker `value` sentinels** (one SEGMENT row per `(client, segment)`):
- *no marker row* → `TRAVELER` (blank = traveler's card, FR-11)
- `CARD` → specific company card (in this row's `credit_card_id`)
- `ATTRIBUTE:<attributeUid>` → per-value cards in ATTRIBUTE rows w/ matching `segment_type`
- `RULE_CLASS` → per-value cards in RULE_CLASS rows w/ `segment_type`
- `ARRANGER` → per-arranger cards in ARRANGER rows w/ `segment_type`
- `INHERIT:<SEGMENT>` → live reference, resolved at read (cycle/self-guarded)
- `VIRTUAL` → virtual mode (writable only when `ANDAVO_PAYMENTS` enabled)
- `BACKUP` → reserved; only with `is_backup=true`; not a mode

Sentinels live only in SEGMENT-typed rows; attribute/class/arranger values live in their own typed rows → no collision. Validate sentinel grammar strictly; reject unknown SEGMENT-row values.

---

## 4. Backend phases (`apps/java`)

> Map segment ids via existing `SegmentType.toServiceType` (FLIGHT→AIR, HOTEL→HOTEL, TRAIN→RAIL). Centralize the "AIR/HOTEL/RAIL only" whitelist in one place and reject CAR/OTHER at the model boundary.

### BE-1 — Schema migration + jOOQ regen
New migration `apps/db/migration/V1xx__wallet_payment_rule_segment.sql` (claim the next free `Vnn`):
- `ADD COLUMN segment_type SMALLINT NULL`; `ADD COLUMN is_backup BOOLEAN NOT NULL DEFAULT false`.
- `ALTER COLUMN credit_card_id DROP NOT NULL` (marker rows for non-CARD modes carry no card).
- Drop old `UNIQUE(client_id, payment_rule_type_id, value)`; add `UNIQUE NULLS NOT DISTINCT (client_id, payment_rule_type_id, value, segment_type, is_backup)`.
  - **⚠ Requires Postgres 15+.** Verify target env. If <15, use dual partial unique indexes (`WHERE segment_type IS NULL` / `IS NOT NULL`) and adjust jOOQ `onConflict` accordingly.
- Add index `(client_id, segment_type, payment_rule_type_id)`.
- Regenerate jOOQ `DbWalletPaymentRule` (confirm codegen task in `apps/java/roam-data/build.gradle`). The repo's write path uses hand-built `DSL.field(...)`, so codegen doesn't block writes, but land it in the same PR to avoid drift.
- **Couple with the legacy-method fix from BE-3 item 3** so existing upserts keep working the instant the constraint changes.

Backfill is implicit (defaults) → legacy rows become `segment_type=NULL, is_backup=false`, preserving global behavior.

### BE-2 — Model & enum changes (`general-model`)
- `payment/PaymentRuleType.java`: add `SEGMENT(4, "SEGMENT")`.
- New `payment/SegmentFopMode.java`: `TRAVELER, CARD, ATTRIBUTE, RULE_CLASS, ARRANGER, INHERIT, VIRTUAL` (the typed UI surface; sentinel string is internal).
- New `payment/PaymentSegment.java` (or constant): `AIR, HOTEL, RAIL` whitelist ↔ `SegmentType` ids.
- `wallet/PaymentRuleValue.java`: add `segmentType`, `backup` fields.
- New DTOs (`model/wallet/`): `SegmentRuleConfig` (response: segment, mode, cardId, attributeId, inheritFromSegment, resolvedMode/resolvedSegment, backupCardId, and the per-value assignments `[{value, creditCardId}]` so the client can diff against available values) and a single composite `SetSegmentRuleConfigRequest` (mode + optional cardId/attributeId/inheritFromSegment + `valueAssignments[]` + backupCardId + `override` bool). No `missingValueCount`, `CardSegmentTags`, or `SegmentAssignmentSummary` DTOs — those are computed client-side.
- Leave `SetPaymentRuleValueRequest` unchanged (legacy).

### BE-3 — Service layer (`general-services/.../wallet/service/WalletService.java`)
Add a **new segment-aware path alongside** the legacy `setPaymentRuleValue` (do not change legacy semantics; segment writes must **not** go through `resolvePaymentRule`).
1. **Sentinel codec** (pure static, unit-tested): `encodeMode` / `decodeMode` with strict grammar validation; reject unknown sentinels (`BadRequestException`).
2. `listSegmentRuleConfigs(clientId)` — read marker + per-value + backup rows for all segments; run inherit resolver; return each segment's mode + per-value assignments + backup. **No missing-value count** (client computes it from existing attribute/rule-class/user data).
3. `setSegmentRuleConfig(clientId, segment, request)` — **single composite write in one `@Transactional`**, reused by both the Settings page and the add/edit card modal:
   - validate segment ∈ {AIR,HOTEL,RAIL};
   - apply mode (card ownership via `isCreditCardOwnedByClient`; attribute via `validateAttributeValue`; rule-class/arranger existence; **INHERIT cycle/self guard** depth ≤3, re-checked at read; **VIRTUAL gated on `ANDAVO_PAYMENTS`**; TRAVELER = delete marker);
   - diff + apply per-value assignments (null card → delete the row; row type derived from the active mode's dimension);
   - apply/clear the backup row;
   - all under the existing `isAllowPaymentRulesEnabled(client)` gate.
4. **Override detection** — if any part of the change set displaces a *different* card already mapped to a segment default or value, return a structured 409 + displaced-card metadata unless `override=true`; on override, clear+write atomically.
5. Audit via existing `AuditMetadataBuilder` + `auditPublisher`, adding `segmentType/isBackup/mode/override`.

### BE-4 — Repository layer (`general-services/.../wallet/repository/WalletRepository.java`)
- New field constants for `segment_type` / `is_backup`.
- New segment-aware methods (do **not** change legacy signatures): `upsertSegmentPaymentRule`, `deleteSegmentPaymentRule`, `findSegmentPaymentRuleCreditCardId`, `findSegmentMarker`, `listSegmentValueRows` (the read returns assignments; the client derives tags + missing counts — no card-tag join or missing-count query needed).
- **Compatibility fixes (required, ship with BE-1):**
  - Legacy `upsertPaymentRuleValue` → set `segment_type=NULL, is_backup=false` and use the **full 5-column conflict target** (3-col target no longer matches a constraint and would fail at runtime).
  - Legacy `deletePaymentRuleValue` / `findPaymentRuleCreditCardId` → add `AND segment_type IS NULL AND is_backup=false`.
  - `getArrangerCreditCardsByClient` → add `AND segment_type IS NULL` so segment-scoped arranger rows don't leak into the legacy `getClientCreditCards` merge.

### BE-5 — Controller / REST (`general-api/.../controller/WalletController.java`)
**Two endpoints**, both `@PreAuthorize` INTERNAL or `AUTHORITY_WALLET_ADMIN`, client-scoped by path, under `/v1/wallet/client/{clientId}/cards/rules`:
- `GET /client/{clientId}/cards/rules` → `List<SegmentRuleConfig>` (all segments, resolved; each includes mode + per-value assignments + backup).
- `PUT /client/{clientId}/cards/rules/{segment}` (`SetSegmentRuleConfigRequest`) → single composite update of a segment's mode + per-value assignments + backup; `204`, or `409` + displaced-card(s) when `override` not acknowledged. **This same endpoint backs the add/edit card modal's bidirectional assignment** — the modal issues independent per-segment PUTs rather than calling a separate card endpoint. **Decided:** these per-segment PUTs are *not* atomic across segments (each write is segment-atomic only); no client-side cross-segment orchestration/rollback for V1.

Deliberately NOT added: no `/segment-tags` endpoint (tags derived client-side), no `/summary` endpoint (missing-value counts computed client-side), no separate card-side `/segment-assignments` endpoint (reuses the PUT above). Attribute lists + their values come from the existing client-attribute / rule-class / user (arranger) endpoints.
Follow existing `@Operation`/`@ApiResponse` doc conventions.

### BE-6 — Resolver seam (no behavior)
Mark a named TODO at `findPaymentRuleCreditCardId` for the future `resolveSegmentFop(clientId, segment, travelerContext)` (marker → inherit follow → value lookup → backup → traveler) used by checkout. Persist-only here.

**Backend PR order:** BE-1+repo compat fixes → BE-2 → BE-3/4 read + GET endpoints → BE-3/4 write + PUT endpoints → polish (409 shape, OpenAPI).

---

## 5. Frontend phases (`libs/client`, `apps/`)

### Shared lib + sharing strategy
Generate one shared feature lib so Admin + Internal share all FOP UI; app pages are thin wrappers passing `entityType`/`clientId`/`lens` (as `WalletPage.tsx` / `ClientWalletPage.tsx` already do):
```
bun nx g @andavo/tools/andavo:react-library wallet-fop \
  --directory=libs/client/web/shared/feature/wallet-fop \
  --importPath=@andavo/web/feature/wallet-fop
```
Promote the internal payment-rules helpers (`useResolvedPaymentRuleValues`, `CardNumberCell`, `util.ts`) into the shared lib for reuse from both apps.

### Reuse / extend (existing)
- **Reuse as-is:** `CreditCardVendorIcon`, nomad `EmptyScreen/Banner/DataTable/Badge`/comboboxes, `DeleteFormOfPaymentModal`, RSA create flow + `formatMaskedCardLastFour`, `handleCardNumberInput`, `handleExpirationInput`, `newCreditCardSchema`/`editCreditCardSchema`, `getBillingCountryOptions`.
- **Extend** `AddEditFormOfPaymentModal.tsx` (`shared/platform/common`): add (flag+client-gated) "Use this payment method for" (segment multi-select), "Set as default for" (per-segment), "Assign to what {attribute} for {segment}" (reuse `PaymentRuleValueCombobox` + new `segmentType` prop); country-contextual State/ZIP vs Province/Postal labels derived during render (default US); extend `findOverrides` + `PaymentRuleOverrideAlert` for segment defaults.
- **Extend** `useResolvedPaymentRuleValues.ts` with optional `segmentType` (keep pin-unconfigured + synth-blank-row logic).
- **Extract** `WalletCardTile.tsx` out of `TravelerProfileWalletPage.tsx` (pure refactor) so traveler grid and the FOP corporate grid share the tile.

### New components (in `@andavo/web/feature/wallet-fop`)
- `CorporateWalletPage` (owns view toggle, default **list** for admin, zero-state, banners, add-card entry) → `CorporateWalletGrid` (reuses extracted tile + segment icons/attribute tags w/ `+N` overflow) + `CorporateWalletTable` (DataTable: nickname, cardholder, number+vendor, Segment, Exp. date, tags, Status).
- `WalletViewToggle`, `WalletStatusBadge` (+ `getCardExpiryStatus` util: Active/Expiring Soon/Expired from `MM/YY`).
- `WalletMissingValuesBanner` (warning; "You have N values you still need to set up for {segment} payment" → opens attribute-config modal), `WalletExpiredCardsBanner` ("We found N expired credit cards" → table filter).
- `PaymentConfigurationPage` → `SegmentPaymentSection` (Air/Hotel/Rail) → `DefaultPaymentMethodSelect` (mode-marker encode/decode; blank=Traveler; inherit excludes self; virtual gated by `AndavoPayments`) + Backup dropdown (disabled until a default is set) + "Edit attribute configuration" link.
- `AttributeConfigModal` ("Default payment for {segment}"): pick attribute → list every value with single-card selector; pinned-unconfigured + missing banner; multi-segment combined edit (`segmentTypes[]`) when a segment inherits another ("Default payment for air & hotel").
- `useSegmentRuleConfig` view-model hook (wraps `useCardRules`; derives per-segment missing-value counts + card tiles' tags client-side from existing attribute/rule-class/user data).

### Data-access additions (`libs/client/shared/shared/data-access/src/lib/wallet/`)
Follow api → query → hook layering:
- `wallet-api.ts`: `getCardRules(clientId)` (per-segment config for all segments, incl. per-value assignments + backup) and `setCardRule(clientId, segment, request)` (single composite update; also used by the card modal).
- `segment-payment-query.ts` + extend `walletMutations` with `setCardRule`.
- `useWallet.ts`: `useCardRules(clientId, lens)`, `useSetCardRule(clientId)` (invalidate card-rules + card-list queries on success). Attribute lists/values come from existing client-attribute / rule-class / user (arranger) hooks; **missing-value counts and card-tile segment/attribute tags are derived client-side** by diffing those against the card-rules response — no dedicated endpoints/hooks.
- Types: extend `PaymentRuleType` with `SEGMENT`; add `FopSegment` (`'AIR'|'HOTEL'|'RAIL'`), `SegmentPaymentMode`, `SegmentPaymentConfig`, `SegmentPaymentRuleValue`; optional `segmentTags` on `CreditCard`.

### App wrappers
- Admin: new `apps/admin-web/src/routing/pages/Settings/PaymentsPage/PaymentsPage.tsx` → `PaymentConfigurationPage` (entityType=CLIENT). Add flag-gated `payments` tab in `SettingsLayout.tsx`; swap `WalletPage` to render `CorporateWalletPage` behind the flag.
- Internal: add `payments` route in `apps/internal-web/src/routing/routes/WalletRoutes.tsx`; render `CorporateWalletPage`/`PaymentConfigurationPage` with `lens=INTERNAL`; add tab in `WalletLayout`.

### State management
**No `useEffect`** (`no-use-effect` skill). Server state via TanStack Query (derive with `select`/inline); view toggle / modal / filters via `useState` + handlers; persist on change via mutation `onSuccess`/`onError`; reset-on-entity via React `key`; country labels + expiry status derived during render. Use `useMountEffect` only if unavoidable.

**Frontend PR order:** FE-0 scaffold (lib, tab/route placeholders, `SEGMENT` type, extract tile) → FE-1 wallet redesign → FE-2 segment-config data-access → FE-3 Settings → Payments page + banners → FE-4 attribute-config modal → FE-5 add/edit bidirectional + override → FE-6 polish/tests. FE phases depend on the corresponding BE phases.

---

## 6. Key edge cases
- Blank (no marker row) = Traveler's card; never send a sentinel for it.
- Inherit option excludes the current segment; resolve effective mode live for display.
- Virtual option only when `ANDAVO_PAYMENTS` truthy; if later disabled while set, keep the stored mode but flag inactive (don't delete).
- Backup dropdown disabled until a default FOP is set.
- Expiry status derived from `MM/YY` (Expired past end-of-month; Expiring Soon within threshold — confirm with design).
- Deleting a CARD-mode card cascades the marker row (reverts segment to Traveler); note affected segments in delete audit.
- Override on save (segment default or value) → `PaymentRuleOverrideAlert` before commit.

## 7. Compatibility safeguards (must hold)
1. Legacy rows untouched (new columns default NULL/false).
2. Legacy write/read methods scoped to `segment_type IS NULL AND is_backup=false`.
3. Legacy upsert conflict target widened to the new constraint (couple with migration).
4. `getArrangerCreditCardsByClient` filtered to `segment_type IS NULL` (protects State of Louisiana global arranger flow).
5. `NULLS NOT DISTINCT` (or partial-index fallback) prevents duplicate legacy rows.
6. Segment writes bypass `resolvePaymentRule` (no interference with the global `PAYMENT_RULE_ATTRIBUTE` setting).

## 8. Open items to verify before coding
- **Postgres version** (≥15 for `NULLS NOT DISTINCT`, else partial-index fallback).
- jOOQ codegen task name in `apps/java/roam-data/build.gradle`; behavior with `NULLS NOT DISTINCT` (fallback: `onConflictOnConstraint`).
- Next free Flyway `Vnn`.
- "Expiring soon" threshold (design).
- Country-contextual address label rules (Kyle has context; default US).

## 9. Verification
- **Backend:** unit-test the sentinel codec round-trip + inherit cycle guard; integration tests (RestTestClient) for each new endpoint incl. override 409 path and virtual gating; **regression-run existing wallet + arranger integration tests** (legacy global arranger must stay green). `./gradlew` in the affected service.
- **Frontend:** `write-frontend-tests` + MSW handlers/builders for the new endpoints. Cover: view toggle + default list view; status badge derivation (fixed dates); banners (counts + actions, hidden at 0); `DefaultPaymentMethodSelect` (blank=Traveler, inherit excludes self, virtual hidden w/o `AndavoPayments`, mode round-trip); backup disabled-until-default; attribute-config (pinned order, persist, multi-segment edit); add/edit (segment multi-select + set-default + assign persist; override path; country labels). Run `bun nx run <project>:lint|typecheck|test` for `wallet-fop`, `shared/platform/common`, `data-access`, both apps.
- **End-to-end manual (behind flag):** enable `client-wallet` for a test client → add a corporate card → set Air = specific card, Hotel = inherit Air, Rail = based-on-Department w/ per-value cards + backup → confirm tiles show tags, banners count unconfigured values, override modal appears on conflict; confirm an unrelated arranger client (global) is unaffected.

## 10. Critical files
**Backend:** `apps/db/migration/V1xx__wallet_payment_rule_segment.sql` (new); `general-model/.../payment/PaymentRuleType.java`, `SegmentFopMode.java` (new), `PaymentSegment.java` (new); `general-services/.../wallet/service/WalletService.java`; `general-services/.../wallet/repository/WalletRepository.java`; `general-api/.../controller/WalletController.java`.
**Frontend:** `libs/client/web/shared/feature/wallet-fop/*` (new lib); `libs/client/web/shared/platform/common/src/AddEditFormOfPaymentModal/AddEditFormOfPaymentModal.tsx`; `libs/client/web/internal/feature/wallet/src/payment-rules/useResolvedPaymentRuleValues.ts`; `libs/client/web/shared/feature/profile/src/Wallet/TravelerProfileWalletPage.tsx`; `libs/client/shared/shared/data-access/src/lib/wallet/{wallet-api,wallet-query,useWallet}.ts`; `apps/admin-web/src/routing/layouts/SettingsLayout/SettingsLayout.tsx`; `apps/internal-web/src/routing/routes/WalletRoutes.tsx`.
