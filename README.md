opencode-ai Agents (Markdown) Storage
=====================================

Purpose
- Store AI-agent definitions as Markdown files and link them into opencode config (global or per-project).

How it works
- Markdown files under `agents/` describe an agent using a YAML front matter block.
- A small CLI under `scripts/opencode_agent_linker.py` converts a Markdown agent into a config entry and links it into a JSON config (`opencode.json`).

Project layout
- `agents/` - Markdown agent definitions (one per agent).
- `config/` - Per-project config examples (and the global config path convention).
- `scripts/` - CLI tooling to link Markdown agents into configs.
- `SPEC.md` - Task specification for this repo.

Usage quickstart
- Add an agent: place a Markdown file in `agents/` with the required front matter.
- Link to per-project config: `python3 scripts/opencode_agent_linker.py link -m agents/<id>.md -s project`.
- Link to global config: `python3 scripts/opencode_agent_linker.py link -m agents/<id>.md -s global`.
- List linked agents: `python3 scripts/opencode_agent_linker.py list -s project`.
- Unlink: `python3 scripts/opencode_agent_linker.py unlink -a <agent-id> -s project`.
