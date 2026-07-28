# Foreign Currency

Support for **foreign / multi-currency** in Andavo — prompted by the upcoming signing of clients in other countries (raised in the [[Teams/Blitz/Standup/2026-06-30|6/30 Blitz standup]]). Owned by [[Blitz]].

**Jira epic:** [AN-10405](https://cbtravel.atlassian.net/browse/AN-10405)

Two pieces:

1. **Exchange-rate workflow** in Andavo (Temporal-based), modeled on the existing Agresso exchange-rate job.
2. **Per-client display currency** so each client sees values in the currency they expect.

## Background (from 6/30 Blitz standup)

- [[Taylor Daily]] built an **exchange-rate table in Agresso**, fed by a SQL script that **pulls rates from the Fed daily**.
- [[Chad Maughan|Chad]] asked why we don't pull exchange-rate data from the **GDS**. Taylor noted a common manual accounting fix is when an **agent enters the wrong currency into the cost fields**.
- Chad wants to **duplicate the exchange-rate storage workflow in Andavo after the Temporal work is done**.
- We're about to **sign clients in different countries**, so we want to **show values in different currencies, configurable per client**.

## Decisions (2026-06-30)

- **Scope:** covers the **exchange-rate workflow** + **per-client display currency**. **Invoice-data workflows are out of scope** (covered under other epics).
- **Rate source:** **Fed daily**, mirroring the existing Agresso job. (Fed rates are USD-based.)
- **Base/accounting currency:** set per **client / agency** — each client (or hosted agency) carries its own base currency. There is no single global base.
- **Per-client config:** **display currency only** — billing/accounting stay in the client/agency base currency.
- **Conversion:** **point-in-time** — store the original currency and the rate as of the transaction date so conversions are reproducible and audit-friendly.
- **Rate table:** **USD pivot + cross-rate** — store USD↔currency rates per day; derive any pair (e.g. EUR→GBP) by crossing through USD.
- **Currency coverage:** ingest **all Fed-published currencies**; enable specific ones per client/agency as needed.
- **Display rounding:** **per-currency standard minor units** (e.g. 2 for USD/EUR, 0 for JPY), applied at display only.
- **Display surfaces:** **Andavo admin app**, **traveler web**, and **reports**. (Not the Red App.)
- **Wrong-currency entry** (the manual-fix pain Taylor raised): **out of scope for now** — related, handle separately.
- **Timeline:** none set; currently in requirements-gathering.

## Goals

- Ingest and store exchange rates in Andavo on a Temporal workflow (replacing the Agresso SQL job as Andavo's source).
- Support **per-client/agency base currencies** with historically accurate, point-in-time conversion.
- Let each client be configured to **view** values in their preferred display currency.

## Scope

**In scope**

- Daily exchange-rate ingestion + storage workflow in Andavo (Fed source, all published currencies).
- Point-in-time capture of currency + rate on relevant records.
- Per-**client/agency** base currency.
- Per-**client** display-currency setting and the display-side conversion that uses it, on the **admin app, traveler web, and reports**.

**Out of scope**

- Invoice-data workflows (other epics).
- Per-client **billing/invoicing** currency (clients billed in the client/agency base currency).
- Per-region / per-traveler currency overrides.
- **Red App** display.
- **Wrong-currency-entry** validation/UX (related; separate effort).

## Requirements (draft)

### Exchange-rate workflow

- Temporal workflow runs **daily**, fetches **all** rates from the **Fed** feed, and stores them in an Andavo exchange-rate table keyed by currency + date.
- **USD-pivot** storage: persist USD↔currency rates per day; compute any non-USD pair as a **cross-rate via USD** for the relevant date.
- Retains full history (one row per currency per day) so point-in-time lookups work.
- Idempotent / retry-safe via Temporal.

### Conversion model

- Two legs, both at **point-in-time** (transaction-date) rates:
  1. **Original transaction currency → client/agency base currency** — for accounting/storage.
  2. **Client/agency base currency → client display currency** — for display only (identity when display = base).
- Persist the **original currency** and the **rate(s) used** on each relevant record.
- Cross-rates computed through the USD pivot.

### Per-client/agency base currency

- Each client/agency has a configured **base currency**; accounting values are held in that base.

### Per-client display currency

- New client setting: **display currency** (default = the client/agency base currency).
- Affects **display only** on the admin app, traveler web, and reports; underlying/accounting values unchanged.
- Rounded to the **target currency's standard minor units** at display.

## Open questions

- **Granularity:** is the base currency set at the **client** level, the **hosting agency** level, or both (agency default + client override)?
- **Data model:** where the client base-currency and display-currency settings live in the client settings model.
- **Defaults:** does an unset base currency default to **USD**?
- **Reports/Domo:** convert at query time or pre-convert stored values?
- **History backfill:** how far back to load Fed rate history (for converting existing/historical transactions); availability of that history.

## Dependencies

- **Temporal** — workflow engine; the rate workflow depends on Temporal being deployed (see [[James Proctor]]).
- **Agresso** — existing exchange-rate table + SQL job to mirror (Finance; [[Taylor Daily]]).

## Related

- [[Teams/Blitz/Blitz Team Priorities|Blitz Team Priorities]] — multi-currency future priority
- [[Teams/Blitz/Standup/2026-06-30|Blitz Standup — 2026-06-30]]
