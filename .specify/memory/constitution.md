<!--
SYNC IMPACT REPORT

- Version change: template → 1.0.0
- Modified principles: N/A (template placeholders replaced)
- Added sections: None (filled existing template sections)
- Removed sections: None
- Templates requiring updates:
  - ✅ .specify/templates/plan-template.md (no changes required; remains compatible)
  - ✅ .specify/templates/spec-template.md (no changes required)
  - ✅ .specify/templates/tasks-template.md (no changes required)
- Deferred / TODOs: None
-->

# Chimera Autonomous Influencer Network Constitution

**Project Type**: Multi-agent system for autonomous AI influencers  
**Business Goal**: Create digital entities that autonomously research trends, generate multimedia content, and manage social & economic engagement  
**Core Architecture**: Hierarchical Swarm (Planner–Worker–Judge) using the FastRender pattern  
**Key Technologies**: Model Context Protocol (MCP) for all external APIs, OpenClaw for agent-to-agent communication, Coinbase AgentKit for agentic commerce

## Core Principles

### I. Safety & Human-in-the-Loop (HITL) (NON-NEGOTIABLE)

Chimera MUST prioritize safety over autonomy.

- All content and actions MUST be evaluated by a Judge before execution/publishing.
- HITL escalation MUST be enforced using tiered thresholds based on Judge confidence:
  - High confidence: auto-approve is allowed only for non-sensitive actions
  - Medium confidence: asynchronous human review is required
  - Low confidence: the agent MUST retry/refine and/or route to human review
- Sensitive topics (politics, health, finance, hate/harassment, minors, self-harm, etc.)
  MUST require human review regardless of confidence.
- Financial actions MUST be treated as high-risk and MUST follow explicit budget and
  approval policy (see Section 2).

### II. Transparency & AI Disclosure (NON-NEGOTIABLE)

The system MUST be transparent about its AI nature when directly asked.

- When a user directly asks whether an entity is AI/automated, the system MUST answer
  truthfully and clearly.
- The system MUST preserve audit trails so humans can understand what was generated,
  what was approved, and why.

### III. MCP-Only External Integrations

All external API calls MUST go through MCP servers.

- Direct network calls to third-party APIs from agent code are forbidden unless routed
  through MCP.
- MCP integrations MUST be treated as contracts: inputs/outputs must be validated and
  failures handled safely (no “best effort” publishing/spending).

### IV. Multi-Agent Architecture Discipline (FastRender Pattern)

Chimera MUST follow the Hierarchical Swarm pattern (Planner–Worker–Judge) and use
OpenClaw for agent-to-agent communication.

- Planners own decomposition, prioritization, and assignment.
- Workers execute specialized tasks and MUST be treated as isolated/fault-contained.
- Judges gate quality and safety, producing confidence and rationale where possible.
- The orchestrator MUST make escalation decisions deterministic and policy-driven.

### V. Strict Spec-Driven Development (SDD)

No implementation code is written until its specification is complete, validated,
and version-controlled.

- Every feature MUST have: `spec.md` (requirements), `plan.md` (design), then `tasks.md`
  (execution), before implementation begins.
- Changes that affect behavior/safety/cost MUST update the spec/plan first (or in the
  same change) so intent remains traceable.

## Critical Constraints & Non-Functional Requirements

- **Scalability**: The architecture MUST support a fleet of 1,000+ concurrent agents.
- **Secrets**: No hardcoded secrets. Secrets MUST NOT be committed to the repository.
  Secrets MUST be managed via secure configuration and be revocable/rotatable.
- **External I/O**: All external API calls MUST go through MCP servers (Principle III).
- **Agentic commerce**: All financial actions MUST use non-custodial wallets via
  Coinbase AgentKit and MUST enforce strict budget governors.
- **Auditability**: Publishing and financial actions MUST be auditable (who/what/why/when).

## Development Workflow, Review, and Quality Gates

- **Review required**: Any change affecting safety policy, HITL thresholds, external
  integrations, or financial actions MUST be reviewed before merge.
- **Testing**: Critical safety, policy, and budget logic MUST be covered by tests.
- **Documentation**: Architecture changes MUST be reflected in the relevant docs/specs.

## Governance
<!-- Example: Constitution supersedes all other practices; Amendments require documentation, approval, migration plan -->

This constitution is the highest-level set of engineering and safety rules for Chimera.
If another document conflicts with it, this document wins.

Amendments:
- Any amendment MUST update the version and `Last Amended` date.
- Versioning follows semantic versioning:
  - MAJOR: backward-incompatible governance changes (removals/redefinitions)
  - MINOR: new principle/section or material expansion
  - PATCH: clarification or non-semantic edits
- Changes MUST be reviewed like code changes, with rationale recorded in the PR and/or
  referenced spec/plan docs.

Compliance:
- Plans SHOULD include a “Constitution Check” gate for applicable principles.
- Reviews MUST explicitly check: HITL compliance, MCP-only external I/O, secret handling,
  and Coinbase AgentKit budget governor enforcement (where applicable).

**Version**: 1.0.0 | **Ratified**: 2026-02-06 | **Last Amended**: 2026-02-06
<!-- Example: Version: 2.1.1 | Ratified: 2025-06-13 | Last Amended: 2025-07-16 -->
