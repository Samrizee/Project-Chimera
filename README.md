# 🧬 Project Chimera — Spec Kit & Specify CLI

**Autonomous AI development tooling, templates, and agent integrations for Spec‑Driven Development (SDD).**

[![CI/CD](https://img.shields.io/badge/CI/CD-Active-green)](.github/workflows) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE) [![Python 3.11+](https://img.shields.io/badge/Python-3.11+-blue)](pyproject.toml) [![Docker Ready](https://img.shields.io/badge/Docker-Ready-blue)](Dockerfile)

Project Chimera provides the `specify` CLI, templates, scripts, and documentation to bootstrap and manage specification-first projects and AI-assisted workflows. The repo includes reference implementations, agent integration guidance, and helper scripts for packaging and CI.

## Vision

Build a reusable platform and patterns for autonomous, spec-driven agent development focusing on safe research, content generation, engagement, and telemetry.

## Key Features

- Project and agent templates for multiple AI agents
- The `specify` CLI (in `src/specify_cli/`) to initialize and manage projects
- Scripts to update agent context, create release packages, and run environment checks
- Documentation and conventions in `AGENTS.md` for adding and packaging agents

## Repository Layout (selected)

- `src/specify_cli/` — core Python package and CLI code
- `templates/` — starter templates and command examples
- `scripts/` — Bash & PowerShell helpers (`update-agent-context`, `check-prerequisites`, etc.)
- `docs/` — user and developer documentation
- `AGENTS.md` — detailed agent integration guide and conventions
- `tests/` — unit/integration tests
- `configs/`, `media/`, `memory/` — example runtime artifacts

## Quickstart (Linux)

1. Create and activate a virtualenv:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install dependencies and (optionally) editable install:

```bash
pip install -r requirements.txt
pip install -e .
```

3. Run tests:

```bash
pytest -q
```

4. Useful Makefile commands:

```bash
make setup       # install deps and prepare environment
make test        # run tests
make lint        # run linters
make docker-build# build Docker image
```

## Architecture & Workflows

- Agent Pattern: Planner → Worker → judgment (orchestrator + HITL escalation)
- Development flow: spec → plan → tasks → implementation → tests → review
- Use `templates/` and `specs/` for SDD artifacts. Example copies are available in the repo templates.

Typical steps to add a feature:

```bash
cp templates/spec-template.md specs/new-feature.md
cp templates/plan-template.md plans/new-feature-plan.md
cp templates/tasks-template.md tasks/new-feature-tasks.md
# implement code and tests
pytest -q
```

## Adding or Updating Agents

Follow `AGENTS.md`. Key rules:

- Use the actual CLI executable name as keys in `AGENT_CONFIG` (`src/specify_cli/__init__.py`).
- Update both Bash and PowerShell helper scripts when adding agents.
- When changing `src/specify_cli/__init__.py`, bump `pyproject.toml` version and add a `CHANGELOG.md` entry.

## Security, Safety & Governance

- Route external integrations through MCP servers for auditing, telemetry, and rate-limiting.
- Human‑in‑the‑Loop (HITL) checks required for sensitive content and financial actions.
- Follow the repository safety rules listed in docs and policy files.

## Contributing

1. Open an issue describing the change.
2. Create a branch, add focused changes and tests.
3. Run `pytest` and `make lint` locally.
4. Submit a PR; describe any agent or packaging changes.

If your change touches `src/specify_cli/__init__.py`, update `pyproject.toml` version and add `CHANGELOG.md` entry per repo conventions.

## Resources

- Agent guide: `AGENTS.md`
- CLI implementation: `src/specify_cli/`
- Scripts: `scripts/bash/` and `scripts/powershell/`

## License

This project is licensed under the terms in `LICENSE`.

---

Need badges, examples, or diagrams added? Tell me which sections to expand (CLI examples, spec templates, CI badges), and I will update the README accordingly.
# Project Chimera — Spec Kit & Specify CLI

Project Chimera provides a Spec-Driven Development (SDD) toolkit and reference implementation called "Specify". It includes templates, scripts, and agent integrations to bootstrap and manage specification-first projects and AI-assisted development workflows.

## Key Features

- Opinionated project templates and command files for multiple AI agents.
- A Python-based `specify` CLI to initialize and manage projects.
- Agent integration guidance and pre-built command/workflow templates.
- Helper scripts for packaging releases, updating agent context, and CI/CD guidance.

## Repository Layout (selected)

- `src/specify_cli/` — core Python package and CLI implementation.
- `templates/` — project and agent templates used by the CLI.
- `scripts/` — helper scripts (bash & PowerShell) for setup and context updates.
- `docs/` — user and developer documentation (quickstart, installation, upgrade notes).
- `AGENTS.md` — detailed guide for adding and supporting AI agents.
- `tests/` — test suite covering utilities and components.
- `configs/` — configuration examples and defaults.
- `media/` and `templates/` — assets and content templates used by examples.

For a deeper dive on agent conventions and how to add new agents, see `AGENTS.md`.

## Quickstart (Linux)

1. Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
# Optional: install the package in editable mode for development
pip install -e .
```

3. Run tests:

```bash
pytest -q
```

4. Common development commands (via `Makefile`):

```bash
make setup       # install deps and prepare environment
make test        # run tests
make lint        # run linters
make docker-build# build Docker image
```

## Typical Workflows

- Initialize a new project from templates using the `specify` CLI (see `src/specify_cli`).
- Update IDE/agent context files with `scripts/bash/update-agent-context.sh` or `scripts/powershell/update-agent-context.ps1`.
- Create release packages using the scripts under `.github/workflows/scripts/`.

## Adding or Updating Agents

Follow the guidance in `AGENTS.md`. Highlights:

- Use the actual CLI executable name as the agent key in `AGENT_CONFIG` inside `src/specify_cli/__init__.py`.
- Update both Bash and PowerShell helper scripts when adding new agents.
- Bump package version in `pyproject.toml` and add a `CHANGELOG.md` entry for changes to `__init__.py`.

## Contributing

1. Open an issue describing the proposed change.
2. Create a focused branch and include tests for new behavior.
3. Run `pytest` and `make lint` locally before submitting a PR.

If your change touches `src/specify_cli/__init__.py`, update the package version in `pyproject.toml` and add a `CHANGELOG.md` entry per the project conventions.

## Security & Governance

- Follow the repository's safety and governance guidance for human-in-the-loop checks and financial actions.
- External integrations should go through MCP servers for auditing and telemetry.

## License

This project is licensed under the terms described in the `LICENSE` file.

---

If you want this README expanded with badges, diagrams, or example outputs (CLI usage examples, sample `spec` files, or CI badges), tell me which sections to expand and I will add them.
# 🧬 Project Chimera: Autonomous AI Influencer Factory

**Autonomous digital entities that research, create, and engage without human intervention.**

[![CI/CD](https://img.shields.io/badge/CI/CD-Active-green)](.github/workflows)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Spec-Driven](https://img.shields.io/badge/Development-Spec--Driven-blue)](.specify/)
[![Python 3.11+](https://img.shields.io/badge/Python-3.11+-blue)](pyproject.toml)
[![Docker Ready](https://img.shields.io/badge/Docker-Ready-blue)](Dockerfile)

## 🎯 Vision

Build a **factory** that produces **Autonomous AI Influencers** capable of:
- 🔍 **Trend Research**: Monitoring social platforms for emerging topics
- 🎨 **Content Generation**: Creating multimedia content (video, text, images)
- 🤝 **Engagement Management**: Autonomous interaction and community building
- 📊 **Performance Optimization**: Learning and adapting based on engagement metrics

## 📁 Repository Structure

├── .specify/ # Specification framework & templates
├── specs/ # Executable specifications (SDD)
├── src/ # Source code implementation
├── tests/ # Test suite (TDD-first)
├── skills/ # Runtime agent capabilities
├── docs/ # Documentation & research
├── memory/ # Agent memory & context
├── templates/ # Content generation templates
├── media/ # Media assets
├── scripts/ # Development scripts
├── .github/ # CI/CD workflows
├── .cursor/ # IDE agent context rules
├── configs/ # Configuration files
├── logs/ # Application logs
│
├── AGENTS.md # Agent definitions & roles
├── CLAUDE.md # Claude IDE context rules
├── agent.mdc # Agent configuration
├── pyproject.toml # Python dependencies
├── Makefile # Development commands
├── Dockerfile # Container configuration
├── README.md # This file
└── .coderabbit.yaml # AI code review policy


## 🚀 Quick Start

### Prerequisites
- Python 3.11+ with [uv](https://github.com/astral-sh/uv)
- Docker & Docker Compose
- Git with commit signing
- MCP Sense telemetry (for development)

### Installation

```bash
# Clone repository
git clone https://github.com/your-org/project-chimera.git
cd project-chimera

# Set up environment
make setup

# Verify installation
make test


## Development Commands

# Install dependencies
make setup

# Run tests
make test

# Run in development mode
make dev

# Lint code
make lint

# Build Docker image
make docker-build

# Run in Docker
make docker-run

## 🏗️ Architecture
Agent Pattern: Hierarchical Swarm (Planner-Worker-judgment)
Planner: Decomposes goals, assigns tasks, manages priorities

Worker: Executes specialized skills (research, content creation, engagement)

judgment: Evaluates quality, safety, and compliance before publishing

Orchestrator: Manages agent coordination and human-in-the-loop escalation

Core Technologies
Model Context Protocol (MCP): All external API integrations

OpenClaw: Agent-to-agent communication protocol

Coinbase AgentKit: Agentic money & wallet management

FastRender Pattern: Optimized content generation pipeline

# 📋 Development Principles
1. Spec-Driven Development (SDD)
No implementation without specification. Every feature follows:

specs/ → plan.md → tasks.md → implementation → tests

2. MCP-Only External Integrations
All external APIs must route through MCP servers for:

Security auditing

Rate limiting

Error handling

Telemetry collection

3. Human-in-the-Loop (HITL) Safety
Content approval based on confidence thresholds

Sensitive topics always require human review

Financial actions require explicit budget governance

4. Agentic Skills Architecture
Skills are isolated, reusable capability packages:

skill_trend_research: Platform trend analysis

skill_content_generation: Multi-format content creation

skill_engagement_manager: Community interaction


🛠️ Development Workflow


# 1. Create specification
cp .specify/templates/spec-template.md specs/new-feature.md

# 2. Design implementation plan
cp .specify/templates/plan-template.md plans/new-feature-plan.md

# 3. Create tasks
cp .specify/templates/tasks-template.md tasks/new-feature-tasks.md

# 4. Implement with failing tests
pytest tests/ -xvs -k "new_feature"

# 5. Submit for review
git push origin feature/new-feature



For AI Agents
AI agents interact through:

.cursor/rules - IDE behavior guidelines

CLAUDE.md - Project context and constraints

AGENTS.md - Role definitions and capabilities



🔒 Safety & Governance
Non-Negotiable Principles
Safety First: Content approval thresholds based on risk categories

AI Transparency: Clear disclosure when directly asked about AI nature

Financial Governance: Strict budget controls for agentic money

Audit Trails: Complete traceability of all agent decisions

Review Requirements
✅ Safety policy changes → Human review required

✅ Financial integrations → Human review required

✅ HITL threshold changes → Human review required

✅ MCP server additions → Team review required


📊 Monitoring & Telemetry
MCP Sense Integration

// .cursor/mcp.json
{
  "mcpServers": {
    "tenx-sense": {
      "command": "npx",
      "args": ["-y", "@tenx/mcp-sense", "--api-key", "YOUR_KEY"]
    }
  }
}





