# Project Chimera – Master Specification

Project Chimera is an autonomous multi-agent influencer network designed to research trends, generate content, and manage engagement and commerce at scale.

## Core Principles

- Spec-driven development is the source of truth
- All external interactions MUST go through MCP servers
- Safety and governance are enforced via deterministic policy routing
- Human-in-the-loop is mandatory for financial and sensitive actions
- All actions must be auditable

## Architecture Direction

- Hierarchical Swarm agent pattern (Planner–Worker–Judge)
- Parallel task execution with fault isolation
- Confidence-based approval routing

## Non-Negotiable Constraints

- No direct API calls outside MCP
- No secret handling inside agents
- Budget governors for all financial operations
- Immutable audit trail for all actions
