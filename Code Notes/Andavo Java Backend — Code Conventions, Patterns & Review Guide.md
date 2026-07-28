
1. Module architecture & layer separation

The apps/java Gradle multi-project build has four module types with a strict directional dependency rule:

*-api      → deployable Spring Boot service (one per K8s pod)
*-services → shared business logic, consumed by multiple APIs
*-model    → POJOs/DTOs, almost no external deps (NO Spring, NO jOOQ)
roam-*     → cross-cutting infra used by all APIs (roam-web, roam-data,
             roam-event, roam-gds, roam-legacy, roam-common, roam-test)

Allowed direction:  api → services → model     (no cross-feature imports)

This is not just documented — it is enforced by ArchUnit. Every module has a ModuleArchitectureTest (e.g. trips-api/src/test/java/com/andavo/trips/ModuleArchitectureTest.java) using noClasses().that().resideInAPackage("com.andavo.trips..").should().dependOnClassesThat().resideInAnyPackage(...). The forbidden-package list encodes the rules: trips may not depend on general.controller, docs, jobs, hooks, or roam.test (in main code). A violation fails the build, so a cross-feature or wrong-direction import won't merge.

Review implications:
- *-model modules must stay free of Spring and jOOQ annotations. If you see @Service, @Component, or jOOQ records in a *-model module, flag it.
- No cross-feature imports (e.g. trips importing booking.model). The ArchUnit test catches most, but new packages may not be in the list yet.
- Keep Spring Boot apps thin; push reusable logic down into *-services/*-model.
- Module docs live in src/main/docs/; each module's root README.md is just an index.

2. Layer-by-layer conventions (verified in code)

Controllers (*-api, ...controller package)

- @RestController + class-level @RequestMapping("/v1/...") for version consistency.
- Constructor injection only (final fields); no field injection.
- Thin: validate/parse → delegate to service → return DTO. Use ResponseEntity only when status/headers need customizing; otherwise return the DTO directly.
- Method security via @PreAuthorize using constants from roam-web/.../security/SecurityConstants.java (e.g. HAS_ROLE_INTERNAL__OR__ADVISOR_FOR_CLIENT). These SpEL checks rely on -parameters compilation; controllers using them extend BaseControllerWithCompiledParameterNamesCheck.
- @Valid before @RequestBody to trigger validation at the boundary.
- @RateLimited on public/risky POST/PUT routes.
- Input guard clauses with Assert.isTrue(...) at method entry.
- Derive user context from Spring Security (AuthenticationContext), never parse JWTs manually.
- Reference: trips-api/.../view/controller/TripController.java.

Services (*-services, ...service package)

- @Service, constructor injection, public classes.
- @Transactional(readOnly = true) on read paths; plain @Transactional on writes; Isolation.SERIALIZABLE only where genuinely needed. Never span transactions across remote/async calls.
- Business logic + authorization defense-in-depth lives here (re-validate when business rules demand it).
- @Cacheable/@CacheEvict using named Caffeine beans from CacheConfig (e.g. CACHE_DEFAULT_60M_1000_SIZE) — never hand-roll caches.
- DTO mapping happens at/below this layer; parallelism via CompletableFuture where useful.

Repositories (*-services, ...repository package)

- @Repository + injected jOOQ DSLContext. No raw SQL strings — only generated tables/records.
- Nested collections via DSL.multiset(...) subqueries (avoid N+1); subresource filters become IN subqueries.
- List/filter endpoints define Map<String, Field<?>> availableFilters keyed by API filter names, fed into ListRequestHelper. Exactly two queries per list request (count + paged). Shared query helper reused by JSON and CSV paths.
- jOOQ stays out of controllers entirely.

Models / DTOs (*-model)

- Lombok @Data/@Getter/@Setter for mutable DTOs; records used for small immutable value types.
- @Schema on class and visible fields (OpenAPI). Internal IDs (iid) hidden with @JsonIgnore.
- Jakarta Bean Validation annotations (@NotNull, @NotEmpty, @Size, @Pattern, etc.) with descriptive message values; @Valid to cascade into nested objects.
- Custom validator placement rule: generic/reusable validators (target String, Integer) go in general-model under ...model.validator[.annotation]; feature-DTO-specific validators stay co-located in that feature's *-model to avoid pulling feature DTOs upstream.

Mappers

- Manual RecordMapper<Record, T> implementations — NOT MapStruct. Composite sub-mappers (a TripMapper instantiates SegmentMapper, TripAttributeMapper, etc.) and recursively maps multiset Result<Record> children. Reference: trips-services/.../view/repository/mapper/TripMapper.java.
- Image URL chokepoint: any image URL from a GDS/3rd party (Sabre, RouteHappy, hotel logos, etc.) must pass through com.andavo.roam.common.ImageUrls#toSecure(String) at the mapping site — Sabre emits http:// and iOS ATS/Android NSC silently block cleartext.

Naming / packaging / visibility

- Feature + layer packaging: com.andavo.<feature>.<area>.{controller,service,repository,repository.mapper}.
- Suffixes: *Controller, *Service, *Repository, *Mapper, *Request, *Response.
- Always use imports, never inline fully-qualified class names.
- Prefer package-private where possible (though most stereotype classes are public by necessity).

3. Cross-cutting infrastructure (don't reinvent)

- Roam starter: every *Application uses @EnableRoamWeb which wires encryption, caching, Micrometer→Datadog, request logging, Auth0, OAuth metadata, method security, rate limiting, and WebMvcConfig. Extend RoamWeb rather than duplicating these configs.
- Error handling: throw standard exceptions (BadRequestException, UnauthorizedException, ForbiddenException, NotFoundException, ConflictException, TooManyRequestsException — all unchecked, in roam-common). WebErrorControllerAdvice (@RestControllerAdvice) standardizes the JSON body (code/version/timestamp/message). Don't catch-and-swallow; let the advice translate. Don't leak internals on 5xx.
- Feature flags: Togglz Features.java enum (@EnabledByDefault, @Label), checked via FeatureManager.isActive(...), runtime-toggleable at /actuator/features. Never use @Value("${...features...}") booleans for toggles.
- Health indicators: custom statuses ordered DOWN(0) > OUT_OF_SERVICE(1) > UP(2) > PAUSED(3) > DEGRADED(4). Never report DOWN for external dependency failures (it kills the K8s pod) — use DEGRADED/PAUSED. New indicators must be added to both the integrations group include list and the default group exclude list in every service that loads them.
- Encrypted properties: two-layer Jasypt. Never use @Value for externally-encrypted properties — create a properties bean in GeneralConfig using @Qualifier("passwordEncryptorExternal").
- Logging: SLF4J only, never System.out; structured/parameterized logs; log at boundaries; no PII.
- Async/events: prefer roam-event domain events for decoupling over synchronous chaining; never cross transaction boundaries with @Async.
- Booking handlers: trips-services createBooking uses a sealed BookingFragment + BookingServiceHandler<O, F> registry auto-wired via List<BookingServiceHandler<?,?>>. New service types = one new handler + one sealed permits entry; don't touch the orchestrator's constructor or inline case dispatch.

4. OpenAPI documentation requirements

This is heavily enforced by convention (checklist in docs-api/README.md):
- Every DTO and visible field needs @Schema(description=...) (one line). Internal IDs @JsonIgnore-d.
- Every @Operation needs a unique kebab-case operationId prefixed by verb (list-, retrieve-, create-, update-, partially-update-) and a short summary with no trailing punctuation.
- Every controller needs class-level @Tags(@Tag(name=..., description=...)) matching the resource name.
- Public endpoints need a full @Operation description with Inputs / Response / call_endpoints JSON example sections, @Parameter annotations, and @ApiResponse for every status code (200/201/204/400/403/404/409/415).
- @Hidden endpoints get no OpenAPI annotations. Internal params like lens are @Parameter(hidden=true).
- Enum query params must be registered in EnumConverterBinder. Use glossary tags (<<glossary:Aircraft>>) instead of inline definitions.

5. Testing conventions & coverage requirements

What's documented & enforced

- Unit tests: JUnit 5 + AssertJ + Mockito. Class [ClassName]Test, methods given..._when..._then...() (in practice also testX_When_Then). Avoid roam-test for unit tests. Test service + repository logic; DB-dependent repo tests move to integration.
- Integration tests: extend AbstractIntegrationTest; declare resources via @IntegrationTest(classes=..., redis=true, referenceData=...) — enable only what's needed. @Nested + @DisplayName on every test/group. Use TestDataService (idempotent fluent builders) in @BeforeAll. RestTestClient.bindToServer() is the preferred full-stack approach (bindToController/bindToContext for narrower scope).
- External deps: mock via @TestConfiguration + @ConditionalOnProperty (@Primary bean), or interface-implementing fakes with JSON fixtures, or @MockBean/@MockitoBean. No Thread.sleep — use Awaitility or sync test APIs (launchJobSync).
- Testcontainers: shared Postgres/Redis/Temporal singletons in roam-test; no withReuse(true) for shared containers; new shared resources must register with suite-scoped cleanup.
- Characterization tests exist for high-risk areas (e.g. TripCreateServiceCharacterizationTest) to lock behavior.

Coverage — important caveat for reviews

- There is NO JaCoCo / coverage-threshold enforcement anywhere in the Gradle or CI config. Coverage is encouraged by convention, not gated by a number. The real gate is: tests must compile and pass, and ArchUnit ModuleArchitectureTest must pass.
- CI (.github/workflows/backend-required.yml → backend-java-test.yml) runs only affected services via path filters, per-module matrix (booking/trips/general/jobs/hooks/docs), 5-min per-test timeout, general excludes the faces tag. Any failure blocks merge; there's no minimum-coverage check to satisfy.
- ~400 test files; general-services (~108) and trips-services (~75) are the densest. ~10% are integration tests by count.

Review implication: since coverage isn't machine-enforced, reviewers are the coverage gate. For new service/repo logic, expect accompanying unit tests; for new endpoints, expect a bindToServer integration test exercising auth + the happy path + key error paths. The handbook's bug-fix workflow also requires a failing test first, then the fix — so bug-fix PRs should include a regression test.

6. Code-review checklist (what to actively look for)

Architecture & layering
- [ ] No cross-feature or wrong-direction imports; *-model free of Spring/jOOQ. (ArchUnit should catch, but verify new packages are covered.)
- [ ] Reusable logic pushed into *-services/*-model, not duplicated in APIs.

Controllers
- [ ] /v1/... routing, constructor injection, thin (no business logic), @Valid before @RequestBody.
- [ ] @PreAuthorize using SecurityConstants; no manual JWT parsing; @RateLimited on new public POST/PUT.

Services / repos
- [ ] @Transactional(readOnly=true) on reads; no transactions across remote/async calls.
- [ ] No raw SQL; multiset not N+1; list endpoints use availableFilters + ListRequestHelper and exactly two queries; clientId filter enforces ROLE_INTERNAL.
- [ ] Lens enforcement propagated to repo (travelers see own data, admins their client, internal everything).

DTOs / mapping
- [ ] No jOOQ records/entities leaked through controllers; manual RecordMapper mapping.
- [ ] Image URLs run through ImageUrls.toSecure(...).
- [ ] @Schema/@JsonIgnore correct; validation annotations present with messages; custom validators placed per the coupling rule.

Cross-cutting
- [ ] Feature toggles via Togglz, not @Value. Health indicators never DOWN for external deps + registered in both group lists. Externally-encrypted props not via @Value. SLF4J, no PII, no System.out.
- [ ] New AUTHORITY_*_ADMIN includes a Flyway backfill migration for existing ROLE_ADMIN users; migrations are new (never edit old ones) with incremented version numbers.

OpenAPI
- [ ] Unique kebab-case verb-prefixed operationId, @Tags, full @Operation description with call_endpoints example, @ApiResponse for all statuses; @Hidden endpoints carry no OpenAPI annotations.

Tests
- [ ] New logic has unit tests (JUnit5/AssertJ/Mockito); new endpoints have bindToServer integration tests covering auth + errors. Bug fixes include a regression test. No Thread.sleep; uses TestDataService, @DisplayName, @Nested. No withReuse(true).
- [ ] Remember coverage is not auto-enforced — you are the gate.

---
A few things worth confirming as you start reviewing: the ArchUnit forbidden-package lists are maintained by hand per module, so a brand-new package added in a PR could slip a bad dependency past the test until the list is updated — worth a glance on PRs that introduce new top-level packages. Want me to save this as a reference doc in the repo (e.g. under agents/rules/ or docs/), or distill it into a shorter PR-review checklist you can paste into reviews?