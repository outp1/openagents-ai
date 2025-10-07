# OpenAgents Constitution
&lt;!-- Sync Impact Report --&gt;
&lt;!-- Version change: 2.0.0 → 2.1.0 --&gt;
&lt;!-- Modified principles: None --&gt;
&lt;!-- Added sections: V. Specification Management (NON-NEGOTIABLE) --&gt;
&lt;!-- Removed sections: None --&gt;
&lt;!-- Templates requiring updates: .specify/templates/plan-template.md ✅ updated --&gt;
&lt;!-- Follow-up TODOs: Create specs/ directory for feature specifications --&gt;

## Core Principles

### I. Modular Agent Design
Every agent is defined as a standalone Markdown file with YAML front matter. Agents must be self-contained, independently installable, and documented with clear purpose. No dependencies on non-standard tools unless explicitly stated.

### II. CLI Interface
All functionality is exposed via a text-based CLI interface. Use stdin/stdout for input/output, with support for JSON and human-readable formats. Errors must be directed to stderr.

### III. Test-Driven Development (NON-NEGOTIABLE)
TDD is mandatory: Write tests first, ensure they fail, then implement to make them pass. Follow Red-Green-Refactor cycle for all features, including CLI commands and agent integrations.

### IV. Observability and Simplicity
Implement structured logging for all operations. Use semantic versioning for releases. Adhere to YAGNI: Start simple, avoid over-engineering, and justify any added complexity.

### V. Specification Management (NON-NEGOTIABLE)
The root SPEC.md MUST describe the general project purpose and include links to all feature specifications in the specs/ directory. Every feature MUST have a dedicated spec file in specs/ linking back to the root SPEC.md. Updates to SPEC.md are required for all project changes, ensuring traceability and alignment.

## Technology Constraints

- Primary language: Python 3.11+
- Package management: uv
- Configuration: Markdown files with YAML front matter
- No external dependencies beyond standard library and uv-managed packages
- Cross-platform compatibility: Linux, macOS, Windows

## Development Workflow

- Features developed via SPEC.md-guided process: spec → plan → tasks → implement → validate
- All changes via pull requests with reviews
- Automated tests must pass before merge
- Documentation updated in same PR

## Governance

This constitution supersedes all other practices. Amendments require: Documentation of change, PR approval by at least two maintainers, and a migration plan if breaking. All PRs must be checked for compliance. Use README.md and SPEC.md for runtime guidance.

**Version**: 2.1.0 | **Ratified**: TODO(initial adoption) | **Last Amended**: 2025-10-02