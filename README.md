Open Agents (Markdown) Storage
=====================================

**Open-source store of useful AI-agents.**

> THIS PROJECT IS ON EARLY DEVELOPING STAGE AND SUPPORTS ONLY OPENCODE-AI SEMANTICS

How it works
- Markdown files under `agents/` describe an agent using a YAML front matter block.

Usage quickstart
- Choose an agent: Pick Markdown file from `agents/`.
- Place its config to one of these places ([reference to opencode-ai docs](https://opencode.ai/docs/agents/#markdown)):
  - For Global Installation: ~/.config/opencode/agent/
  - Per-project: .opencode/agent/

CLI (TUI) usage
- From repo: `uv run python -m cli`
- As a tool in any project (recommended):
  - One-off: `uvx --from /path/to/openagents-ai openagents-ai`
  - Installed venv scripts: in repo run `uv sync`, then from another project run `/path/to/openagents-ai/.venv/bin/openagents-ai`
- Controls: Up/Down/PgUp/PgDn navigate, Tab switch Agents/Commands, type to filter, Space select, `a` toggle all, Enter install, Ctrl+L clear, q/Esc quit.
- Behavior: Uses the packaged registry when outside this repo; creates relative symlinks in the current project `.opencode/agent` or `.opencode/command` to the selected items. If you have an `agents/` or `commands/` directory in the current project, those are shown instead.

### Roadmap
- MORE and MORE AI agents
- Lightweight cli tool to automatically pick and install agents. (Inspired by [MCPHub](https://github.com/ravitemer/mcp-hub))
- Support for other AI clients (e.g cursor, claude-code)

## CONTRIBUTING

Project layout
- `agents/` - Markdown agent definitions (one per agent).
- `scripts/` - CLI tooling to link Markdown agents into configs. (WORK IN PROGRESS)
- `SPEC.md` - Task specification for this repo.

