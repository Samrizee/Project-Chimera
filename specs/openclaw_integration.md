# OpenClaw Integration Specification — Project Chimera

## 1. Purpose & Scope

Project Chimera SHALL integrate with the OpenClaw Agent Social Network to:

- Advertise Chimera agent capabilities and availability
- Discover and collaborate with external autonomous agents
- Exchange tasks, signals, and service requests in a governed manner
- Maintain trust, reputation, and auditability across agent interactions

All OpenClaw communications MUST route through MCP servers and MUST be fully auditable.

---

## 2. Integration Principles

1. MCP-Only Communication  
   All outbound and inbound OpenClaw interactions SHALL occur via dedicated MCP servers.

2. Least-Privilege Exposure  
   Chimera SHALL expose only declared capabilities and SHALL never leak secrets or internal state.

3. Deterministic Governance  
   All externally sourced tasks SHALL pass through the same Planner → Judge → HITL policies as internal tasks.

4. Auditability  
   Every OpenClaw message SHALL be logged with correlation IDs.

5. Trust-by-Verification  
   External agent actions SHALL be gated by reputation scores and policy constraints.

---

## 3. Chimera Capability Advertisement

Chimera swarms SHALL publish a Capability Manifest at fixed intervals (default: every 60 seconds).

### 3.1 Capability Manifest Schema

```json
{
  "agent_id": "chimera-swarm-001",
  "version": "1.0.0",
  "status": "available",
  "capabilities": [
    {
      "skill": "skill_trend_research",
      "description": "Cross-platform trend discovery and sentiment analysis",
      "sla_ms": 30000,
      "max_concurrent_tasks": 50
    },
    {
      "skill": "skill_content_generate",
      "description": "Multimedia content generation aligned to platform policies",
      "sla_ms": 60000,
      "max_concurrent_tasks": 25
    }
  ],
  "governance": {
    "financial_actions_allowed": false,
    "sensitive_domains_allowed": false,
    "hitl_enforced": true
  },
  "reputation": {
    "score": 0.97,
    "successful_tasks": 12450,
    "policy_violations": 2
  },
  "timestamp_iso": "2026-02-06T12:00:00Z"
}
