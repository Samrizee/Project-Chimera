# Technical Specification — Project Chimera

## 1. System Architecture

### 1.1 Architectural Pattern

Project Chimera SHALL implement a Hierarchical Swarm architecture consisting of:

- Planner (Strategist)
- Worker Pool (Executors)
- judgment Pool (Validators)
- Orchestrator (Dispatcher & Policy Router)

The architecture MUST support:

- Parallel task execution
- Fault isolation between agents
- Deterministic routing based on policy rules
- Full auditability of task lineage and decisions

---

### 1.2 MCP Enforcement Layer

All external system interactions MUST pass through MCP servers.

Direct API calls from agents are strictly prohibited.

MCP server categories include:

- Social platform integrations
- Trend and data providers
- Media generation and storage
- Financial services (Coinbase AgentKit)

All MCP activity MUST be logged and auditable.

---

### 1.3 Data Flow

Planner → Orchestrator → Worker → judgment → Orchestrator → Action or HITL

The Orchestrator is the sole authority for:

- Dispatching tasks
- Triggering MCP actions
- Enforcing policies and budgets
- Writing audit logs

---

## 2. Agent Roles

### 2.1 Planner

Responsibilities:

- Decompose campaign goals into discrete Tasks
- Assign required skill per Task
- Set risk classification and review flags
- Validate constraints before enqueueing

Restrictions:

- SHALL NOT perform external calls
- SHALL NOT bypass governance rules

---

### 2.2 Worker

Responsibilities:

- Execute assigned Tasks in isolation
- Invoke Skills exclusively through MCP servers
- Produce structured Result objects
- Attach evidence and source references

Failure Handling:

- MCP outage → return retryable error
- Policy violation → return blocked status
- Timeout → partial results with retry flag

---

### 2.3 judgment

Responsibilities:

- Evaluate Result quality, safety, and compliance
- Generate confidence score (0.0–1.0)
- Route decisions deterministically
- Enforce HITL rules

Decision outputs:

- approve
- reject
- retry
- escalate_to_human

---

## 3. Skills Framework

All Skills MUST:

- Enforce strict input/output contracts
- Reject unexpected fields
- Return structured error codes
- Perform external I/O only via MCP

---

### 3.1 skill_trend_research

Purpose: Identify trending topics across platforms.

Input:

- platforms: string[]
- timeframe:
  - start_iso: string
  - end_iso: string

Output:

- trends: Trend[]

Trend fields:

- trend_id: string  
- topic: string  
- platform: string  
- volume: number  
- sentiment: number [-1.0, 1.0]  
- evidence:
  - sample_urls: string[]
  - notes?: string

Error codes:

MCP_UNAVAILABLE, INVALID_INPUT, TIMEFRAME_TOO_LARGE, RATE_LIMITED, UNKNOWN

---

### 3.2 skill_content_generate

Purpose: Generate multimedia content aligned to a trend.

Input:

- trend: Trend
- content_type: string

Output:

Content:

- content_id: string
- text: string
- media_urls?: string[]
- metadata:
  - platform_intent: string
  - hashtags?: string[]
  - disclosures?: string[]
- confidence_score: number [0.0–1.0]
- safety_tags: string[]

Error codes:

POLICY_BLOCKED, MCP_UNAVAILABLE, INVALID_INPUT, MODEL_FAILURE, UNKNOWN

---

### 3.3 skill_wallet_operation

Purpose: Perform governed wallet actions via Coinbase AgentKit.

Input:

- action_type: string
- amount:
  - value: number
  - currency: string
- recipient: string

Output:

Receipt:

- transaction_id: string
- status: submitted | confirmed | rejected
- timestamp_iso: string
- amount
- recipient
- audit_ref

Error codes:

BUDGET_EXCEEDED, POLICY_BLOCKED, MCP_UNAVAILABLE, INVALID_INPUT, INSUFFICIENT_FUNDS, UNKNOWN

---

## 4. Core Data Contracts

### 4.1 Task Schema

All Planner-generated Tasks MUST conform to the following JSON Schema:

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "Task",
  "type": "object",
  "additionalProperties": false,
  "required": [
    "task_id",
    "tenant_id",
    "campaign_id",
    "created_at_iso",
    "priority",
    "skill",
    "objective",
    "constraints",
    "risk_level",
    "max_attempts",
    "correlation_id"
  ],
  "properties": {
    "task_id": { "type": "string" },
    "tenant_id": { "type": "string" },
    "campaign_id": { "type": "string" },
    "created_at_iso": { "type": "string", "format": "date-time" },
    "priority": { "type": "integer", "minimum": 1, "maximum": 5 },
    "skill": {
      "type": "string",
      "enum": [
        "skill_trend_research",
        "skill_content_generate",
        "skill_wallet_operation"
      ]
    },
    "objective": { "type": "string" },
    "constraints": {
      "type": "object",
      "required": ["platforms", "time_budget_ms", "mcp_only", "no_secrets"],
      "properties": {
        "platforms": { "type": "array", "items": { "type": "string" } },
        "time_budget_ms": { "type": "integer" },
        "mcp_only": { "type": "boolean", "const": true },
        "no_secrets": { "type": "boolean", "const": true }
      }
    },
    "risk_level": {
      "type": "string",
      "enum": ["low", "medium", "high", "financial", "sensitive"]
    },
    "max_attempts": { "type": "integer" },
    "correlation_id": { "type": "string" }
  }
}
