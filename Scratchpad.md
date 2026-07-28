
• Changes requested. I would not approve this structure yet.

  1. Blocker — expense-document access becomes unrestricted same-client trip access.
     apps/java/trips-services/src/main/java/com/andavo/trips/view/service/TripService.java:216 adds AUTHORITY_EXPENSE_ADMIN to the generic trip-retrieval policy. That policy guards the
     authenticated trip endpoint at apps/java/trips-api/src/main/java/com/andavo/trips/view/controller/TripController.java:422, whose default response includes every TripPart: travelers, notes,
     vendor data, attributes, invoices, and segments. It also grants access to any same-client trip—not only trips attached to charges the expense admin can see—so the “no wider” comment is
     inaccurate.

     The code-judo move is to resolve receipt availability at the expense boundary: enrich each charge with its invoice/folio reference, or expose a charge-scoped receipt endpoint that first
     authorizes the charge. That removes the frontend’s per-trip full-object fetch, avoids expanding generic trip access, and keeps the permission aligned with the actual resource.

  2. Blocker — authorization silently depends on the requested response projection.
     apps/java/trips-services/src/main/java/com/andavo/trips/view/service/TripService.java:199 documents that callers must request TripPart.CLIENT, but the public endpoint accepts arbitrary parts
     at apps/java/trips-api/src/main/java/com/andavo/trips/view/controller/TripController.java:348. An authorized expense admin requesting parts=SEGMENTS or parts=INVOICES is silently denied
     because the projected Trip lacks its client. A comment cannot enforce this invariant.

     Authorization metadata must be loaded independently of response shaping—through a small ownership/client lookup or an authorization projection—so permissions do not change based on requested
     fields.

  3. Major — the policy is duplicated instead of having one canonical owner.
     The same authority/client comparison exists in apps/java/trips-services/src/main/java/com/andavo/trips/view/service/TripService.java:212 and apps/java/trips-api/src/main/java/com/andavo/
     trips/web/config/security/method/TripzExpressionService.java:85, with duplicated test matrices. The SpEL composition also retrieves the trip once for ownership and again for expense-client
     scope. Put the rule in a focused trip-access policy and have both entry points delegate to it—or eliminate the second path through the charge-scoped design above.

  Validation: both changed modules compiled, and the focused tests passed (29/29). git diff --check passed, no changed file crossed 1,000 lines, and the branch has no textual merge conflict with
  current origin/main. The tests still do not exercise the actual controller security boundary or the new isTripOwner null guard.