
What's explicitly documented

From agents/rules/backend-java.md, each layer has a stated responsibility:

┌──────────────────────────────┬──────────────────────────────────────────────────────────────────────────────────────────────────────────┬──────────────────────────────────────────────────────────────┐
│            Layer             │                                        Documented responsibility                                         │                    What must NOT be there                    │
├──────────────────────────────┼──────────────────────────────────────────────────────────────────────────────────────────────────────────┼──────────────────────────────────────────────────────────────┤
│ Controller (*-api,           │ "Keep controllers thin: validate/parse input, delegate to services, map results to DTOs." Versioning     │ No jOOQ usage ("do not use jOOQ from controllers"), no       │
│ ...controller)               │ (/v1), @PreAuthorize, @RateLimited, @Valid, OpenAPI annotations.                                         │ business logic, no manual JWT parsing.                       │
├──────────────────────────────┼──────────────────────────────────────────────────────────────────────────────────────────────────────────┼──────────────────────────────────────────────────────────────┤
│ Service (*-services,         │ Unit-of-work boundary (@Transactional), business logic, authorization defense-in-depth, caching,         │ "Never span transactions across remote calls or async        │
│ ...service)                  │ orchestration.                                                                                           │ boundaries."                                                 │
├──────────────────────────────┼──────────────────────────────────────────────────────────────────────────────────────────────────────────┼──────────────────────────────────────────────────────────────┤
│ Repository (*-services,      │ "Place SQL in repository classes." jOOQ DSLContext, type-safe queries, paging/sorting helpers. "Keep     │ No raw SQL strings; no jOOQ leaking upward.                  │
│ ...repository)               │ repositories thin and composable."                                                                       │                                                              │
├──────────────────────────────┼──────────────────────────────────────────────────────────────────────────────────────────────────────────┼──────────────────────────────────────────────────────────────┤
│ Model (*-model)              │ POJOs/DTOs, validation annotations, @Schema.                                                             │ "Keep *-model modules free of Spring/jOOQ annotations."      │
└──────────────────────────────┴──────────────────────────────────────────────────────────────────────────────────────────────────────────┴──────────────────────────────────────────────────────────────┘

So the responsibilities themselves are written down clearly.

What's enforced by machine (not just prose)

- Module direction (api → services → model, no cross-feature imports) is enforced by the ArchUnit ModuleArchitectureTest in every module — a violation fails the build.
- *-model purity is partly enforced the same way (the model module can't depend on Spring/jOOQ infra packages).

Where the lines are sharp in practice

These are consistent across the codebase even though they're convention rather than a written rule:
- jOOQ never escapes the repository. Controllers and services deal in DTOs/domain objects; only repositories touch DSLContext and generated records.
- Mapping (jOOQ record → DTO) lives at the repository layer via manual RecordMapper classes in a repository.mapper sub-package — not in services or controllers.
- @Transactional lives on services, not controllers or repositories.
- @PreAuthorize lives on controllers; services do additional business-rule authorization (lens enforcement, ROLE_INTERNAL checks) but the declarative method-security annotations are at the controller boundary.

The genuinely fuzzy boundaries (watch these in review)

The documentation is clear on responsibilities but does not sharply adjudicate a few recurring gray areas, and the code reflects that:

1. Controller vs. service validation. Docs say validate at the controller edge and "validate invariants in services as guard clauses." In practice controllers do Assert.isTrue(...) input checks and services re-validate. There's no rule on what belongs where, so you'll see overlap. In review, the test is: structural/shape validation at the controller (@Valid, format asserts); business-rule validation in the service.
2. Where DTO mapping happens. The list-endpoint rule and the mapper convention both put record→DTO mapping at the repository (via RecordMapper), but some services also do mapping/assembly (e.g. OffersService composing async results). So "mapping" isn't owned by a single layer — repositories map rows, services assemble/compose. Flag a controller that does any mapping beyond trivial wrapping.
3. Service vs. repository business logic. "Keep repositories thin and composable" is the only guidance. Filter-condition building (build<Entity>Condition, availableFilters) and lens conditions intentionally live in the repository, which is more than a dumb data-access layer. The line is: query construction and lens/auth SQL conditions in the repo; orchestration, cross-entity rules, and transactions in the service.

Bottom line for reviews

The layering is real and largely enforced — you can confidently flag jOOQ in a controller, business logic in a controller, Spring in a *-model, or a cross-feature import. The two things ArchUnit won't catch, and where reviewer judgment matters most, are:
- business logic creeping into controllers or repositories (no automated guard), and
- duplicated/misplaced validation between controller and service.