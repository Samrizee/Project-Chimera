# Software Requirements Specification (SRS)
## Project Chimera: Autonomous Influencer Network

**Project Type**: Multi-agent system for autonomous AI influencers  
**Business Goal**: Create digital entities that autonomously research trends, generate multimedia content, and manage social & economic engagement  
**Core Architecture**: Hierarchical Swarm (FastRender) using Planner–Worker–Judge roles  
**External Integration Standard**: All external API calls MUST go through MCP servers  
**Commerce Standard**: All financial actions MUST use non-custodial wallets via Coinbase AgentKit with strict budget governors  
**Scalability Target**: Support 1,000+ concurrent agents (across campaigns/tenants)

---

## 1. System Architecture Overview

### 1.1 Architectural Pattern: Hierarchical Swarm (FastRender)

The system SHALL use a Hierarchical Swarm architecture with distinct agent roles:

- **Planner (Strategist)**: Converts high-level goals into a structured queue of Tasks.
- **Worker (Executor)**: Performs isolated, specialized work to produce Results.
- **Judge (Validator)**: Evaluates Results for quality, safety, policy compliance, and confidence; routes outcomes.

The architecture MUST support:

- **Parallel execution**: Multiple Workers can execute Tasks concurrently.
- **Fault isolation**: A Worker failure MUST NOT crash the swarm; Tasks MUST be retried or reassigned.
- **Deterministic routing**: Judge decisions MUST be driven by policy rules and confidence thresholds.
- **Auditability**: The system MUST record task lineage and approvals for publishing and spending actions.

### 1.2 Data Flow

1. **Planner → Orchestrator**: Planner submits `Task` objects to the orchestrator queue.
2. **Orchestrator → Worker**: Orchestrator assigns Tasks to Workers based on capability/skill requirements.
3. **Worker → Judge**: Worker returns `Result` objects for evaluation.
4. **Judge → Orchestrator**: Judge returns an `evaluation` (approve/reject/escalate) and confidence, plus required next actions.
5. **Orchestrator → Action**: If approved, orchestrator triggers MCP-based publishing/commerce; otherwise routes to retry/HITL queue.

### 1.3 Swarm + MCP Integration Diagram (Mermaid.js)

```mermaid
flowchart TD
  %% Roles
  P[Planner Agent<br/>(Strategist)]
  O[Orchestrator<br/>(Dispatcher + Policy Router)]
  W1[Worker Pool<br/>(Executors)]
  J[Judge Pool<br/>(Validator)]
  H[Human Review Queue<br/>(HITL)]
  D[Dashboard<br/>(Ops + Review)]

  %% Integration layer
  MCP[MCP Integration Layer]
  MCP1[MCP Server: Social Platforms]
  MCP2[MCP Server: Trend/News/Data]
  MCP3[MCP Server: Coinbase AgentKit]
  MCP4[MCP Server: Storage/Media]

  %% Data stores (conceptual)
  Q[(Task Queue)]
  A[(Audit Log)]

  P -->|Create Tasks| O
  O -->|Enqueue Task| Q
  Q -->|Dispatch| W1
  W1 -->|Result| J
  J -->|Approve / Reject / Escalate| O
  O -->|Escalate| H
  H -->|Decision| O
  O -->|Ops visibility| D
  D -->|Review actions| H

  %% External calls must go through MCP
  O -->|External actions via MCP ONLY| MCP
  W1 -->|External reads via MCP ONLY| MCP
  MCP --> MCP1
  MCP --> MCP2
  MCP --> MCP3
  MCP --> MCP4

  %% Audit
  O --> A
  J --> A
  H --> A
  W1 --> A
```

---

## 2. Agent Roles & Responsibilities

### 2.1 Planner (Strategist)

- **Inputs**
  - Campaign goal(s) (e.g., “increase follower engagement by 15% in 30 days”)
  - Platform constraints (per platform policies)
  - Budget constraints (per tenant/campaign)
  - Historical performance summaries (optional)
- **Core Logic**
  - MUST decompose goals into discrete, testable `Task`s with clear success criteria.
  - MUST assign each Task a `skill` requirement (e.g., `skill_trend_research`).
  - MUST set `risk_level` and `requires_human_review` flags for sensitive domains.
  - MUST NOT directly call external APIs (MCP-only constraint applies system-wide).
- **Outputs**
  - One or more `Task` objects pushed to the orchestrator queue.
- **Failure Modes (and required behavior)**
  - **Invalid task definition**: MUST fail fast with an error reason; MUST NOT enqueue incomplete Tasks.
  - **Policy conflict (e.g., forbidden topic)**: MUST mark Task as `blocked` and route to HITL with rationale.
  - **Budget conflict**: MUST reduce scope or request HITL approval; MUST NOT bypass budget governors.

### 2.2 Worker (Executor)

- **Inputs**
  - A `Task` object from the orchestrator, including `skill` requirement and constraints
- **Core Logic**
  - MUST execute Tasks in an isolated, side-effect-controlled manner.
  - MUST use MCP servers for all external reads/writes.
  - MUST produce a `Result` object with complete artifacts and evidence (sources, prompts, URLs, receipts).
  - MUST NOT publish content or spend funds directly unless the Task explicitly authorizes it AND the action is performed via orchestrator-controlled MCP calls.
- **Outputs**
  - A `Result` object returned to the Judge.
- **Failure Modes (and required behavior)**
  - **MCP server unavailable**: MUST return `status=error` with retryable flag and diagnostic context.
  - **Timeout**: MUST return partial evidence (if any) and mark as retryable.
  - **Policy violation detected**: MUST stop, return `status=blocked`, and include violation details.

### 2.3 Judge (Validator)

- **Inputs**
  - A `Result` object
  - Applicable policies (brand safety, platform rules, spending limits, disclosure requirements)
  - Optional context: prior rejections, human feedback, campaign constraints
- **Core Logic**
  - MUST evaluate quality, safety, and compliance.
  - MUST compute a `confidence_score` in \([0.0, 1.0]\) and provide reasons.
  - MUST enforce HITL routing rules (Section 5).
  - MUST enforce “AI disclosure when directly asked” policy for interactive outputs.
- **Outputs**
  - An `evaluation` decision: `approve` | `reject` | `escalate_to_human` | `retry`
  - Required next action(s) and policy tags
- **Failure Modes (and required behavior)**
  - **Insufficient evidence**: MUST `retry` or `escalate_to_human` (never auto-approve).
  - **Conflicting policies**: MUST escalate to human with full rationale.
  - **Repeated failure loop**: MUST trigger escalation after a bounded retry count (see Section 5.4).

---

## 3. Skills Framework Definition (Strict I/O Contracts)

All skills MUST:

- Accept **only** the inputs defined by contract (additional fields MUST be rejected or ignored per policy).
- Return outputs that validate against the output contract.
- Return deterministic, structured errors with machine-readable codes.
- Perform all external I/O through MCP servers.

### 3.1 `skill_trend_research` (Module Contract)

```text
module: skill_trend_research
purpose: Identify and summarize trending topics across specified platforms and timeframe.

input:
  platforms: string[]            # REQUIRED. Example: ["x", "instagram", "tiktok"]
  timeframe:
    start_iso: string            # REQUIRED. ISO-8601 date-time
    end_iso: string              # REQUIRED. ISO-8601 date-time

output:
  trends: Trend[]                # REQUIRED. Non-empty if success, else error

Trend:
  trend_id: string               # REQUIRED. Stable identifier
  topic: string                  # REQUIRED. Human-readable topic label
  platform: string               # REQUIRED. One of input platforms
  volume: number                 # REQUIRED. Normalized volume or absolute count (must define unit in metadata)
  sentiment: number              # REQUIRED. Range [-1.0, 1.0]
  evidence:
    sample_urls: string[]        # REQUIRED. Source URLs (via MCP)
    notes: string                # OPTIONAL. Short summary of why it is trending

errors:
  - code: MCP_UNAVAILABLE | INVALID_INPUT | TIMEFRAME_TOO_LARGE | RATE_LIMITED | UNKNOWN
    message: string
    retryable: boolean
```

### 3.2 `skill_content_generate` (Module Contract)

```text
module: skill_content_generate
purpose: Generate multimedia content aligned to a trend and content type, returning confidence.

input:
  trend: Trend                   # REQUIRED. Must conform to skill_trend_research Trend schema
  content_type: string           # REQUIRED. Example: "short_video" | "post" | "thread" | "carousel"

output:
  content: Content               # REQUIRED on success

Content:
  content_id: string             # REQUIRED
  text: string                   # REQUIRED. Primary caption/script/body
  media_urls: string[]           # OPTIONAL. Generated/selected media assets (via MCP storage/media server)
  metadata:
    platform_intent: string      # REQUIRED. Target platform for formatting/compliance
    hashtags: string[]           # OPTIONAL
    disclosures: string[]        # OPTIONAL. e.g., ["AI-assisted"] when required by policy
  confidence_score: number       # REQUIRED. Range [0.0, 1.0]
  safety_tags: string[]          # REQUIRED. e.g., ["sensitive:none"] or ["sensitive:health"]

errors:
  - code: POLICY_BLOCKED | MCP_UNAVAILABLE | INVALID_INPUT | MODEL_FAILURE | UNKNOWN
    message: string
    retryable: boolean
```

### 3.3 `skill_wallet_operation` (Module Contract)

```text
module: skill_wallet_operation
purpose: Perform non-custodial wallet actions via Coinbase AgentKit with budget governors.

input:
  action_type: string            # REQUIRED. Example: "transfer" | "approve_spend" | "balance_check"
  amount:
    value: number                # REQUIRED for monetary actions
    currency: string             # REQUIRED. Example: "USD" | "USDC" | "ETH"
  recipient: string              # REQUIRED for transfers. Address or recipient identifier

output:
  receipt:
    transaction_id: string       # REQUIRED
    status: string               # REQUIRED. "submitted" | "confirmed" | "rejected"
    timestamp_iso: string        # REQUIRED
    amount:
      value: number
      currency: string
    recipient: string
    audit_ref: string            # REQUIRED. Correlation ID for audit log entry

errors:
  - code: BUDGET_EXCEEDED | POLICY_BLOCKED | MCP_UNAVAILABLE | INVALID_INPUT | INSUFFICIENT_FUNDS | UNKNOWN
    message: string
    retryable: boolean
```

---

## 4. Data Models & API Contracts

### 4.1 JSON Schema: `Task` (Planner → Worker)

The `Task` object MUST validate against the following JSON Schema (draft 2020-12).

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "chimera.task.schema.json",
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
    "task_id": { "type": "string", "minLength": 1 },
    "tenant_id": { "type": "string", "minLength": 1 },
    "campaign_id": { "type": "string", "minLength": 1 },
    "created_at_iso": { "type": "string", "format": "date-time" },
    "priority": { "type": "integer", "minimum": 1, "maximum": 5 },
    "skill": {
      "type": "string",
      "enum": ["skill_trend_research", "skill_content_generate", "skill_wallet_operation"]
    },
    "objective": { "type": "string", "minLength": 1 },
    "constraints": {
      "type": "object",
      "additionalProperties": false,
      "required": ["platforms", "time_budget_ms", "mcp_only", "no_secrets"],
      "properties": {
        "platforms": { "type": "array", "items": { "type": "string" }, "minItems": 0 },
        "time_budget_ms": { "type": "integer", "minimum": 1000 },
        "mcp_only": { "type": "boolean", "const": true },
        "no_secrets": { "type": "boolean", "const": true },
        "budget": {
          "type": "object",
          "additionalProperties": false,
          "required": ["max_value", "currency"],
          "properties": {
            "max_value": { "type": "number", "minimum": 0 },
            "currency": { "type": "string", "minLength": 1 }
          }
        }
      }
    },
    "risk_level": { "type": "string", "enum": ["low", "medium", "high", "financial", "sensitive"] },
    "requires_human_review": { "type": "boolean" },
    "attempt": { "type": "integer", "minimum": 1 },
    "max_attempts": { "type": "integer", "minimum": 1, "maximum": 5 },
    "dependencies": {
      "type": "array",
      "items": { "type": "string" }
    },
    "correlation_id": { "type": "string", "minLength": 1 }
  }
}
```

### 4.2 JSON Schema: `Result` (Worker → Judge)

The `Result` object MUST validate against the following JSON Schema (draft 2020-12).

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "chimera.result.schema.json",
  "title": "Result",
  "type": "object",
  "additionalProperties": false,
  "required": [
    "result_id",
    "task_id",
    "worker_id",
    "created_at_iso",
    "status",
    "artifacts",
    "evidence",
    "correlation_id"
  ],
  "properties": {
    "result_id": { "type": "string", "minLength": 1 },
    "task_id": { "type": "string", "minLength": 1 },
    "worker_id": { "type": "string", "minLength": 1 },
    "created_at_iso": { "type": "string", "format": "date-time" },
    "status": { "type": "string", "enum": ["success", "error", "blocked", "partial"] },
    "artifacts": {
      "type": "object",
      "additionalProperties": true,
      "description": "Skill-specific output payload (e.g., trends list, content object, wallet receipt)."
    },
    "evidence": {
      "type": "object",
      "additionalProperties": false,
      "required": ["mcp_calls", "sources"],
      "properties": {
        "mcp_calls": {
          "type": "array",
          "items": {
            "type": "object",
            "additionalProperties": false,
            "required": ["server", "operation", "timestamp_iso", "status"],
            "properties": {
              "server": { "type": "string" },
              "operation": { "type": "string" },
              "timestamp_iso": { "type": "string", "format": "date-time" },
              "status": { "type": "string", "enum": ["ok", "error"] },
              "request_ref": { "type": "string" },
              "response_ref": { "type": "string" }
            }
          }
        },
        "sources": { "type": "array", "items": { "type": "string" } },
        "notes": { "type": "string" }
      }
    },
    "error": {
      "type": "object",
      "additionalProperties": false,
      "required": ["code", "message", "retryable"],
      "properties": {
        "code": { "type": "string" },
        "message": { "type": "string" },
        "retryable": { "type": "boolean" }
      }
    },
    "correlation_id": { "type": "string", "minLength": 1 }
  }
}
```

### 4.3 Orchestrator Dashboard API Endpoints

The system SHALL expose an Orchestrator Dashboard API for operators and HITL reviewers.
Endpoints MUST be authenticated and audited. Endpoints are described at the contract level.

- **GET `/api/v1/health`**
  - **MUST** return service health, version, and dependency readiness (including MCP servers).
- **GET `/api/v1/tasks`**
  - **MUST** support filtering by `tenant_id`, `campaign_id`, `status`, `risk_level`, and time range.
- **GET `/api/v1/tasks/{task_id}`**
  - **MUST** return the Task plus linked Results and Judge evaluations (by correlation).
- **POST `/api/v1/tasks/{task_id}/retry`**
  - **MUST** enqueue a retry attempt (bounded by `max_attempts`), preserving lineage.
- **GET `/api/v1/review-queue`**
  - **MUST** return HITL items ordered by priority and SLA deadline.
- **POST `/api/v1/review-queue/{item_id}/decision`**
  - **MUST** accept `approve` | `edit_and_approve` | `reject` with reviewer identity and rationale.
  - **MUST** write an immutable audit log entry.
- **GET `/api/v1/audit/events`**
  - **MUST** support filter by `correlation_id`, entity IDs, event type, and time range.
- **GET `/api/v1/metrics`**
  - **MUST** expose operational metrics (queue depth, approval rates, retries, p95 latencies).

---

## 5. Safety & Governance (HITL)

### 5.1 Confidence-Based Tiers (Exact Thresholds)

Every Judge evaluation MUST produce a `confidence_score` in \([0.0, 1.0]\). The system MUST route actions as follows:

- **Tier 1 (Auto-Approve)**: `confidence_score > 0.90`
  - Allowed only when `risk_level` is `low` or `medium` AND the action is not sensitive/financial.
- **Tier 2 (Async HITL Review)**: `0.70 <= confidence_score <= 0.90`
  - MUST be routed to the Human Review Queue.
  - The agent swarm MAY continue non-dependent work while awaiting review.
- **Tier 3 (Retry / Block)**: `confidence_score < 0.70`
  - MUST trigger `retry` with refinement guidance OR immediate escalation if risk is high.

### 5.2 Mandatory HITL Overrides (Regardless of Confidence)

The following MUST ALWAYS route to HITL, even if `confidence_score > 0.90`:

- `risk_level` is `financial` (any wallet/spend/transfer action)
- `risk_level` is `sensitive` (politics/health/finance advice/harassment/minors/etc.)
- First-time actions on a new platform/account/tenant configuration (until explicitly whitelisted)

### 5.3 Routing Logic (Deterministic)

Routing MUST be computed deterministically from:

- `risk_level`
- `requires_human_review` flag (if set true, always route to HITL)
- `confidence_score`
- policy tags (e.g., `sensitive:health`, `financial:transfer`)

### 5.4 Retry Bounding (Anti-Loop Requirement)

For any Task:

- The system MUST cap attempts to `max_attempts` (default: 3 unless explicitly set).
- If attempts are exhausted, the system MUST escalate to HITL with the complete evidence history.

---

## 6. Deployment & Scalability

### 6.1 Container Strategy (Docker)

- Each major service (Orchestrator, Planner service, Worker service, Judge service, Dashboard API) MUST be containerized.
- Containers MUST be immutable and versioned.
- Secrets MUST be injected at runtime (never baked into images).

### 6.2 Cluster Orchestration (Kubernetes)

The production deployment SHOULD run on Kubernetes and MUST support horizontal scaling:

- Worker and Judge pools MUST support horizontal autoscaling based on queue depth and CPU/memory.
- Orchestrator MUST be deployed with high availability (at least 2 replicas) and leader-safe queue semantics.
- MCP servers MUST be monitored as dependencies; degraded MCP availability MUST be visible in `/api/v1/health`.

### 6.3 CI/CD Pipeline Requirements

The CI/CD pipeline MUST enforce:

- **Build**: deterministic builds producing versioned images.
- **Test**: unit tests for policy/routing logic; integration tests for MCP contracts (mocked or sandboxed).
- **Security**: secret scanning and dependency vulnerability scanning.
- **Policy checks**: fail builds if non-MCP external calls are detected (static checks where possible).
- **Deployment**: staged rollout (dev → staging → prod) with rollback capability.

