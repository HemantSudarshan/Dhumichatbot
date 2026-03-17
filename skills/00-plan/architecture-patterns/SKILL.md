---
name: architecture-patterns
description: "Clean Architecture, DDD, Hexagonal, and layered patterns. Use when structuring large codebases with clear dependency rules and separation of concerns."
---

# Architecture Patterns

Master proven backend architecture patterns including Clean Architecture, Hexagonal Architecture, and Domain-Driven Design to build maintainable, testable, and scalable systems.

## Instructions

1. Clarify domain boundaries, constraints, and scalability targets.
2. Select an architecture pattern that fits the domain complexity.
3. Define module boundaries, interfaces, and dependency rules.
4. Provide migration steps and validation checks.
5. For workflows that must survive failures (payments, order fulfillment, multi-step processes), use durable execution at the infrastructure layer â€” frameworks like DBOS persist workflow state, providing crash recovery without adding architectural complexity.

Refer to `references/implementation-playbook.md` for detailed patterns, checklists, and templates.

## Related Skills

Works well with: `event-sourcing-architect`, `saga-orchestration`, `workflow-automation`, `dbos-*`

## Resources

- `references/implementation-playbook.md` for detailed patterns, checklists, and templates.
