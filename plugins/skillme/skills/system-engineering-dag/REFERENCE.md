# System Engineering DAG — On-Demand Reference

This file is **reference material**, not the runtime router. Load only the sections that correspond
to `AFFECTED` or `UNKNOWN` impact surfaces. The canonical machine rules live in
`system_engineering_dag.json`; `system_engineering_dag_kernel.py` validates/compiles them.

## A. Domain / information / data

### Domain
- entities, value objects, aggregates, invariants
- bounded contexts and ownership boundaries
- business rules, commands, events
- state machines, legal transitions, terminal states
- temporal semantics and lifecycle

### Information architecture
- content inventory/model
- hierarchy, sitemap, navigation
- taxonomy, controlled vocabulary, synonyms
- filters/facets/search paths
- multilingual labels and localization semantics

### Data architecture
Classify data where applicable:
- master, reference, transactional, operational, event
- content, observational, claim, evidence, provenance
- temporal, geospatial, analytical, telemetry
- derived, AI-derived, vector, KG

For each critical dataset define:
- owner/steward/producer/consumer
- source of truth
- classification/sensitivity
- lineage and transformations
- freshness and quality SLOs
- retention/deletion
- archive and backup obligations

Data-quality dimensions:
- completeness, validity, uniqueness, consistency
- accuracy, freshness, timeliness
- referential integrity, semantic validity

## B. Knowledge / ontology / KG

Do **not** activate a KG by default.

Activate only when needed for:
- heterogeneous semantics
- multi-source entity resolution
- graph reasoning
- provenance graph or explainable relationship traversal

If activated:
- vocabulary → taxonomy/concept scheme → ontology
- classes/subclasses/properties/domain/range/cardinality
- canonical IDs, aliases, multilingual names, external IDs
- entity resolution, merge/split policy
- assertions, evidence, provenance, confidence
- valid-from/valid-to semantics
- graph constraints and validation
- ontology/index/version migration

## C. Database and transactions

Design in layers:
1. conceptual model
2. logical model
3. physical schema
4. workload model

Physical concerns:
- types, PK/FK, unique/check constraints
- indexes and index selectivity
- partitioning only when justified
- views/materialized views
- connection pooling
- replication/failover
- archive/cold storage

Transaction concerns:
- atomic boundaries
- isolation level
- locking and deadlock behavior
- optimistic/pessimistic concurrency
- idempotency
- write ordering
- consistency expectations

Workload evidence:
- read/write ratio
- hot rows/tables/keys
- query distribution
- concurrency
- storage/growth forecast
- p95/p99 latency requirements

### Database migration
Prefer:
`expand → mixed-version compatibility → migrate → validate → switch → contract`

Test:
- old app + compatible new schema
- new app + compatible transitional schema
- lock duration
- disk amplification
- partial failure/restart
- data validation
- roll-forward and restore

Never assume down-migration is safe after new-version writes.

## D. Storage

Possible stores:
- relational/document
- object/blob
- graph/vector
- search index
- warehouse/lake/archive

Each store needs:
- source-of-truth role
- derived vs authoritative status
- consistency/freshness
- retention/deletion
- backup/rebuild strategy
- version and migration strategy

Avoid polyglot persistence without a measured need.

## E. Cache

### Reasons to cache
- latency
- database pressure
- external API protection
- cost

Strategies:
- cache-aside
- read-through
- write-through
- write-behind
- refresh-ahead

Design:
- key namespace/version/locale/query/security context
- TTL and freshness
- invalidation mechanism
- event-driven invalidation if justified
- warming
- negative caching where safe

Failure modes:
- cache down
- stale data
- stampede
- penetration
- hot key
- eviction storm
- cold start

Mitigations:
- bypass/source fallback
- request coalescing
- jitter
- rate limiting
- stale-while-revalidate where safe

### Cache security
- cache hit never bypasses authorization
- permission/tenant context in key when required
- never leak tenant-private response into shared cache
- no secrets/credentials in cache
- define private stale-data behavior

## F. API / events / external integrations

API:
- explicit contract/schema
- validation and error taxonomy
- authn/authz
- pagination/filter/sort
- versioning/deprecation
- timeout/retry
- rate limits
- idempotency
- backward compatibility

Events/queues/streams:
- producer/consumer ownership
- event schema/version
- ordering expectations
- at-least/at-most/effectively-once assumptions
- retry/backoff
- DLQ
- replay
- duplicate/out-of-order handling
- retention

External dependencies:
- SLA/SLO assumptions
- timeout budget
- circuit breaker/fallback
- degradation mode
- data contract
- reconciliation for irreversible side effects

## G. Search / retrieval / AI

Search capabilities are opt-in:
- keyword/full-text
- prefix/autocomplete
- synonym/fuzzy
- faceted
- geo
- semantic/hybrid

If search index is used:
- index schema/analyzers/tokenizers
- ranking/boosting
- freshness
- zero-downtime reindex
- alias switch/previous-index rollback

AI/retrieval:
`query → intent/router → SQL/search/KG/vector → rerank → evidence → generation`

Version:
- model
- system prompt/prompt
- tools
- embedding/chunking
- retrieval policy
- reranker
- ontology/index
- eval dataset

AI-derived data is not ground truth without provenance and verification.

AI tests:
- golden set/regression
- retrieval accuracy
- groundedness/citation correctness
- prompt injection/tool misuse
- privacy/data exfiltration
- latency/cost/fallback

## H. Security / privacy / IAM

### Security assurance
Choose assurance based on risk/criticality rather than applying identical controls everywhere.

Core:
- asset inventory
- trust boundaries
- threat/abuse model
- authentication
- authorization
- service/machine identity
- secrets/key management
- encryption
- session expiry/revocation
- audit
- privacy
- supply-chain security

Authorization tests must include negative cases:
- user A cannot read/write user B
- tenant A cannot reach tenant B
- expired/revoked credentials denied
- privilege escalation denied

Privacy:
- data minimization
- purpose limitation
- data flow
- retention/deletion
- export/access
- PII redaction in telemetry
- backup-retention implications

Supply chain:
- dependency/lockfile review
- SCA
- secret scanning
- container/IaC scanning
- SBOM
- provenance/attestation
- signing where assurance requires it
- dependency EOL/upgrade ownership

## I. Multi-tenancy

If multi-tenancy exists:
- tenant identity/context propagation
- DB isolation strategy
- query predicates/policies
- tenant-aware cache keys
- object-store path isolation
- search/vector/KG isolation
- quotas and noisy-neighbor controls
- tenant-scoped audit
- tenant migration/deletion/export
- tenant-scoped restore or documented limitation

## J. Network / infrastructure / configuration

Network path as applicable:
`DNS → CDN/WAF → LB/ingress → app → private services → data`

Define:
- public/private boundaries
- segmentation
- ingress/egress
- firewall/security groups
- service-to-service policy
- DDoS controls

Infrastructure:
- IaC
- compute/containers/serverless
- storage/data services
- queue/search/cache
- secrets/observability
- region/AZ strategy justified by SLO/RPO/RTO

Environments:
- local/dev/test/integration/preview/QA/staging/preprod/prod/DR
- purpose, data policy, access, secrets, external integrations
- parity requirements proportional to risk

Configuration:
- versioned
- validated
- audited
- rollbackable
- feature flags have owner/default/expiry/cleanup
- high-risk feature has kill switch where feasible

## K. UX / frontend / design

UX must map to domain state and permissions:
- journeys/flows/tasks
- state transitions
- loading/empty/error/offline/stale/partial
- permission denied
- maintenance/degraded mode

Frontend:
- routing
- rendering strategy
- server/client/form state
- server cache
- error boundaries
- bundle/asset policy
- accessibility and i18n

Design system:
- tokens
- typography/color/spacing/grid
- components/patterns
- focus/keyboard
- responsive rules
- motion/content rules

Wireframe/prototype are downstream of domain/IA/flow constraints, not substitutes for them.

## L. Test obligation catalog

Select tests from impact/failure modes; do not run everything by default.

Static:
- lint/format/type
- static analysis
- architecture fitness
- dependency/license/secret/IaC scans

Code:
- unit
- property-based
- fuzz
- component

Integration:
- DB/cache/queue/search/KG/external APIs
- contract
- API

Data:
- constraints
- transaction/isolation/deadlock
- migration
- data quality
- lineage/provenance
- KG/ontology validation

UI:
- component
- visual regression
- E2E
- cross-browser/device
- accessibility
- i18n

Performance:
- benchmark
- load
- stress
- spike
- soak
- volume
- scalability
- concurrency

Security:
- SAST/DAST/SCA
- authn/authz negative tests
- container/IaC
- penetration proportional to assurance

Resilience:
- dependency down
- latency/fault injection
- chaos
- failover
- backup restore
- DR/game day

Release:
- smoke
- startup/liveness/readiness
- canary/progressive verification
- production synthetic journeys

## M. Reliability / capacity

Patterns where justified:
- timeout
- retry with exponential backoff/jitter
- circuit breaker
- bulkhead
- backpressure
- rate limit
- load shedding
- idempotency
- saga/outbox
- degraded/read-only modes

Capacity model:
- users/RPS/concurrency
- DB connections
- storage/bandwidth
- queue depth
- cache memory
- search/vector size
- forecast horizons

Autoscale on signals that represent bottleneck/queueing, not CPU by reflex.

## N. Observability / SRE

Signals:
- structured logs
- metrics
- distributed traces
- events
- profiles if justified

Design:
- telemetry schema/semantic naming
- request/correlation/trace IDs
- cardinality budget
- sampling
- PII redaction
- retention/cost budget
- owner per signal/dashboard
- trace propagation

Golden signals:
- latency
- traffic
- errors
- saturation

Product/service:
- business metrics
- SLIs
- SLOs
- error budgets
- actionable alerts

Criticality target should influence architecture:
`criticality → SLI/SLO/RPO/RTO → redundancy/recovery`

## O. Backup / restore / disaster recovery

Define first:
- RPO
- RTO
- data/service priority

Backup scope may include:
- DB
- objects/files
- configuration
- IaC/state
- search/KG/ontology config
- source/docs
- required security metadata

Backup controls:
- encryption
- immutability
- independent access
- off-region/off-site where risk requires
- retention tiers
- deletion protection

Restore:
- full
- PITR
- tenant/object
- configuration/environment

Restore evidence:
- integrity check
- successful restore
- app boot/readiness
- data validation
- **business invariant reconciliation**
- actual RTO/RPO
- key-recovery proof for encrypted backups

External side effects:
- payment/message/email ledger
- idempotency
- reconciliation
- duplicate/replay policy

DR strategies:
- backup/restore
- pilot light
- warm standby
- active/passive
- active/active

Choose from RTO/RPO, not prestige.

Game day record:
- hypothesis
- blast radius
- abort rule
- observer
- expected vs actual
- actual RTO/RPO
- gaps/actions

## P. Release / rollback / roll-forward

Build:
- build once, promote many
- immutable/identified artifact
- provenance/SBOM according to assurance

Manifest as applicable:
- work item/SkillMe run
- branch/commit/artifact
- schema/migration
- config/infra
- feature flags
- dependencies
- search/ontology
- model/prompt/embedding
- test evidence
- recovery decision

Deployment strategy chosen by risk:
- direct
- rolling
- blue/green
- canary
- shadow
- progressive

Rollback classes:
- app
- config
- infra
- feature
- model
- search index
- cache
- DB/data

For each:
- trigger
- target state/version
- compatibility assumptions
- validation
- what if rollback fails

Use roll-forward when reverse change is more dangerous after new writes.

`deploy != release`; release completes after production verification.

## Q. Incident / emergency / governance

Incident:
- severity
- incident commander
- comms/escalation
- containment
- evidence preservation
- runbooks
- kill switches
- recovery
- post-recovery validation
- blameless postmortem
- corrective actions

Emergency change:
- minimum safe bypass only
- retain traceability/owner/minimum test/recovery/evidence
- mandatory post-hoc review

Waiver:
- control
- reason/risk
- compensating control
- approver
- expiry/review date

Freshness:
Critical artifacts should record:
- owner
- evidence
- status
- last verified
- reverify trigger/date

Reverify on:
- major architecture change
- new region/data store/auth model
- critical dependency change
- elapsed freshness window

Governance:
- ADRs
- dependency lifecycle/EOL
- cost architecture
- deprecation
- retention
- decommission
- credential revocation
- audit evidence

## R. Decommission

Plan for:
- stop new traffic
- notify consumers
- export/archive required data
- revoke credentials
- disable integrations
- remove DNS/infrastructure/secrets
- honor retention/deletion
- preserve required audit evidence
- close dependencies

A system that cannot be safely retired is not fully lifecycle-designed.
