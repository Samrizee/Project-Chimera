# Tooling Strategy — Project Chimera

## Purpose

This document defines the MCP servers used to support safe, traceable, and governed development of Project Chimera.

Developer MCP tools exist to:

- Prevent unsafe file edits
- Enforce Git hygiene
- Maintain traceability of agent actions
- Improve reproducibility

---

## 1. filesystem-mcp

### Purpose

Controlled file reading and writing by AI agents.

### Capabilities

- Read files from repo
- Create and modify documents
- Enforce path boundaries
- Log all file mutations

### Usage in Chimera

- Editing specs
- Writing tests
- Updating documentation
- Creating configuration files

### Governance

- No access to secrets
- No system-level files
- All edits auditable

---

## 2. git-mcp

### Purpose

Governed version control interactions.

### Capabilities

- Stage files
- Commit with structured messages
- View diffs
- Revert changes safely

### Usage in Chimera

- Incremental spec updates
- Test additions
- Controlled implementation changes

### Governance

- Prevent force pushes
- Enforce commit message templates
- Log agent actions

---

## 3. docker-mcp (optional but recommended)

### Purpose

Controlled container execution.

### Capabilities

- Build Docker images
- Run containers
- Execute test suites in isolation

### Usage in Chimera

- Run make test
- Validate CI behavior locally
- Reproduce environments

---

## 4. schema-validator-mcp (recommended)

### Purpose

Validate JSON against defined schemas.

### Capabilities

- Validate Task and Result contracts
- Return structured validation errors

### Usage in Chimera

- Pre-commit checks
- Test assertions
- Agent output verification

---

## Tooling Principles

- MCP-only interactions
- Full audit logging
- Least-privilege access
- Deterministic behavior

---

## Success Criteria

Development agents must be able to:

- Modify repo safely
- Validate spec alignment
- Run governed tests
- Maintain clean Git history