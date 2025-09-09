# Specification for opencode-ai-agents

## Overview
opencode-ai-agents is an open-source store of AI agents defined as Markdown files under the `agents/` directory.

## Project Structure
- `agents/` - Markdown agent definitions (one per agent).
- `scripts/` - CLI tooling to link Markdown agents into configs.
- `SPEC.md` - This specification document.

## README Specifications
- **Purpose**: The README should onboard users and new contributors, providing a concise project overview, usage guidance, and an overview of the repository layout.

- **Scope**: Non-normative guidance intended to standardize README quality and consistency across the repository.

- **Content Requirements**:
  - A top-level title that clearly identifies the project (the example in this repo uses "opencode-ai Agents (Markdown) Storage").
  - A brief project introduction describing the repository's intent and current state.
  - A section explaining how agents are stored (e.g., `agents/` with one file per agent and YAML front matter).
  - A quickstart or usage section describing how to locate and configure agents (globally or per-project).
  - A project layout section describing major directories (`agents/`, `scripts/`, `SPEC.md`).
  - A roadmap or future work section (optional).
  - A contribution or collaboration section with how to contribute to the project.

- **Formatting & Style**:
  - Use Markdown with clear headings and bullet lists.
  - Use backticks for file paths and commands.
  - Maintain consistent, readable formatting across sections.

- **Quality & Validation**:
  - Self-contained document with no reliance on external docs for core onboarding.
  - Consistent terminology and structure across repository READMEs (if present).

- **Maintenance**:
  - Treat README as a living document; align content with repository changes, but update this SPEC if the README's intended spec changes.

## Design Principles
- Simplicity: keep READMEs readable and aligned with file layout.
- Clarity: ensure readers understand where to find agents and how to extend the repo.
- Consistency: standardize terms and structure across READMEs.

## References
- agents/: Directory with agent definitions.
- scripts/: CLI tooling.
- SPEC.md: This specification document.
