# Virtual card fails to load ~10 min after deploymentId update

**Status:** Investigating
**Reported by:** [[Maddie Petty]] (Senior Software Engineer, Engineering)
**Reported:** 2026-06-25 ([Teams message](https://teams.microsoft.com/l/message/19:4cb08f6dedce4ca79fcae281d031d11a@thread.v2/1782405694900?context=%7B%22contextType%22%3A%22chat%22%7D))
**Area:** Traveler virtual card sheet (Conferma virtual cards, hotel segments)

## Symptom

In dev1, when Maddie updates the `deploymentId` on a `trip_segment` in the database to a new value, the virtual card loads correctly **right after** the change. But if she tries to load the virtual card again ~10 minutes later, it **fails to load**.

## Reproduction (per Maddie)

1. In the DB, filter `trip_segment` to segment `CZRwFDvqroTDapNPFuH6X`.
2. In the `properties` column, scroll (cmd+arrow) to the end to find the `deploymentId`.
3. Update `deploymentId` to a new value → virtual card works.
4. Wait ~10 minutes, reload the virtual card → it doesn't work.

## Environment / data

- **Env:** dev1 (`dev1-az-usw3-traveler.andavo.io`)
- **Trip:** `CYtiGWUPmmaSJ5Q1hFbPo`
- **Segment:** `CZRwFDvqroTDapNPFuH6X`
- **Trip/segment URL:** https://dev1-az-usw3-traveler.andavo.io/trip/CYtiGWUPmmaSJ5Q1hFbPo/segment/CZRwFDvqroTDapNPFuH6X?activeSegment=1
- **deploymentIds tried:** 216327626, 214797343, 214960767, 216214432

## Relevant code / PRs

- Endpoint: `GET /v1/trips/{tripId}/segments/{segmentId}/virtual-card` (trips-api Java service) returns Conferma virtual-card data.
- `TripVirtualCardController` → `resolveCardDetails()`; `VirtualCardService.getVirtualCardDetails` fetches details from Conferma's `/card` endpoint.
- PR [#5349](https://github.com/andavo-dev/andavo/pull/5349) — feat(trips-api): resolve Conferma `/card` details for bare deployments (ConnexPay/Comdata issuers ship no inline `cardDetails`).
- PR [#5350](https://github.com/andavo-dev/andavo/pull/5350) — traveler virtual card sheet (web + mobile).

## Hypotheses (unverified)

- The "works now, fails ~10 min later" pattern points to something **time-based**: a Conferma deployment TTL/expiry, a cached card token/session that goes stale, or a short-lived auth token used to call Conferma's `/card` endpoint.
- Worth checking whether the failure is on fetching `cardDetails` from Conferma vs. rendering with bare deployment data.

## Next steps

- [ ] Reproduce against one of the listed deploymentIds and capture the failing response/logs.
- [ ] Confirm where the failure occurs (Conferma `/card` call vs. controller vs. frontend).
- [ ] Check for any TTL/caching on deployment or card-detail lookups.
