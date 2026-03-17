---
name: senior-architect
description: "Comprehensive software architecture expertise. Use when making high-level design decisions, choosing architectural styles, defining system boundaries, or evaluating trade-offs."
---

# Senior Architect

Guide for making high-level architecture decisions across the software development lifecycle.

## Capabilities

- Architectural style selection (monolith, microservices, event-driven, serverless)
- System boundary definition and dependency management
- Technology stack evaluation and trade-off analysis
- Non-functional requirements (scalability, reliability, security, performance)
- Domain decomposition and service boundaries
- Data architecture (SQL, NoSQL, event sourcing, CQRS)
- Integration patterns (sync, async, pub/sub, API gateway)
- Migration planning (strangler fig, parallel run, blue-green)

## Process

### Phase 1 — Understand Context

1. Identify stakeholders and their quality priorities (latency, uptime, cost)
2. Map functional domains and their interactions
3. Inventory existing systems, APIs, and data stores
4. Document constraints: team size, budget, compliance, timeline

### Phase 2 — Choose Architectural Style

| Style | Best When | Trade-off |
|-------|-----------|-----------|
| Monolith | Small team, fast iteration, single deployment | Hard to scale individual components |
| Modular Monolith | Medium team, clear domain boundaries | Needs discipline to maintain module isolation |
| Microservices | Large team, independent deployability needed | Operational complexity, distributed debugging |
| Event-Driven | Async workflows, decoupled producers/consumers | Eventual consistency, harder to reason about |
| Serverless | Unpredictable load, pay-per-use economics | Cold starts, vendor lock-in, observability gaps |

### Phase 3 — Define Boundaries

1. **Aggregate data that changes together** — group by consistency boundary
2. **Separate data that scales differently** — read-heavy vs write-heavy
3. **Align with team ownership** — Conway's Law as ally, not enemy
4. **Minimize cross-boundary transactions** — choreography over orchestration where possible

### Phase 4 — Evaluate Trade-offs

Use the following decision framework for each major choice:

```
Decision: [What are you choosing?]
Context:  [Why is this decision needed now?]
Options:
  A: [Option] — Pros: [...] Cons: [...]
  B: [Option] — Pros: [...] Cons: [...]
Chosen:   [Winner and rationale]
Risks:    [What could go wrong?]
Revisit:  [When to reconsider this decision]
```

Record every significant decision as an ADR (see `architecture-decision-records` skill).

### Phase 5 — Validate

- **Threat model** the architecture for security gaps
- **Failure mode analysis** — what happens when each component fails?
- **Load estimation** — can the design handle 10× expected traffic?
- **Cost projection** — infrastructure costs at launch, 6 months, 1 year
- **Developer experience** — can a new engineer ship a feature in the first week?

## Anti-Patterns

| Anti-Pattern | Symptom | Fix |
|---|---|---|
| Distributed monolith | Microservices but every deploy requires coordinated releases | Enforce independent deployability or merge back |
| Resume-driven architecture | Choosing tech for novelty, not fit | Evaluate against requirements, not hype |
| Big design up front | Months of planning before any code | Time-box architecture spikes to 1-2 weeks |
| Shared database coupling | Multiple services writing to the same tables | Give each service its own data store |
| Premature optimization | Caching, sharding before measuring | Measure first, optimize the bottleneck |

## Tech Stack Reference

| Layer | Options |
|-------|---------|
| Languages | TypeScript, Python, Go, Rust, Java, Kotlin |
| Frontend | React, Next.js, React Native, Flutter |
| Backend | FastAPI, Express, NestJS, Spring Boot |
| Database | PostgreSQL, MongoDB, DynamoDB, Redis |
| Infra | Docker, Kubernetes, Terraform, GitHub Actions |
| Cloud | AWS, GCP, Azure |
| Observability | Prometheus, Grafana, OpenTelemetry, Sentry |

## Related Skills

- `architecture-patterns` for Clean Architecture, DDD, Hexagonal patterns
- `architecture-decision-records` for documenting decisions
- `ddd-strategic-design` for domain decomposition
- `database-design` for schema and storage choices
