# Project Chimera — AI Agent Operating Rules

## 1. Project Context (Non-Negotiable)

This is Project Chimera, an autonomous multi-agent influencer system built using spec-driven development.

The system uses a Hierarchical Swarm architecture with:

- Planner agents
- Worker agents
- judgment agents
- An Orchestrator enforcing governance

All external interactions MUST route through MCP servers.

Safety, auditability, and deterministic policy routing are core system requirements.

---

## 2. Prime Directive (Absolute Rule)

🚨 NEVER generate, modify, or refactor code without first consulting the specifications in the `specs/` directory.

All implementation MUST:

- Align with functional requirements in `specs/functional.md`
- Conform to contracts in `specs/technical.md`
- Respect OpenClaw rules in `specs/openclaw_integration.md`

If any behavior is unclear or underspecified:

→ STOP and request clarification  
→ DO NOT invent APIs, schemas, or logic  

---

## 3. Mandatory Planning & Traceability

Before writing any code, you MUST:

1. Summarize the relevant spec sections
2. Describe your implementation plan step by step
3. Identify which contracts and schemas are being enforced
4. Confirm governance and safety implications

Only after this explanation may code be produced.

---

## 4. Spec Fidelity Over Speed

Correctness and spec alignment are more important than speed.

The agent must:

- Prefer strict schema validation
- Enforce deterministic behavior
- Avoid implicit assumptions
- Reject vague or loosely typed structures

---

## 5. MCP Enforcement

The agent MUST:

- Never call external APIs directly
- Always assume MCP servers are the only integration layer
- Stub or mock MCP calls in tests where necessary

Any direct HTTP/API calls outside MCP are violations.

---

## 6. Test-First Mandate

All new features MUST:

- Have failing tests written first
- Directly map to spec contracts
- Validate schemas strictly

No implementation should exist without test coverage tied to specs.

---

## 7. Safety & Governance Awareness

The agent MUST always:

- Respect HITL routing thresholds
- Enforce budget governors
- Treat financial and sensitive actions as high-risk
- Log actions with correlation IDs

Never bypass governance logic for convenience.

---

## 8. Communication Style

When responding or coding:

- Be explicit
- Reference spec sections
- Avoid assumptions
- Highlight risks and edge cases

---

## 9. Forbidden Behaviors

The agent MUST NOT:

❌ Generate code that conflicts with specs  
❌ Invent undocumented APIs  
❌ Skip planning steps  
❌ Bypass MCP  
❌ Ignore governance rules  
❌ Produce “quick hacks”  

---

## 10. Success Criteria

The agent is successful only when:

✅ Code strictly follows specs  
✅ Tests validate contract behavior  
✅ Governance is enforced  
✅ No hallucinated logic exists  

---

## 11. Final Reminder

Project Chimera prioritizes:

SPEC → PLAN → TEST → IMPLEMENT  

Never reverse this order.
