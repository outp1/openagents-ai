
$ARGUMENTS

## Workflow
1) Intake and scoping
   - Clarify objectives, constraints, and success criteria. If ambiguous, ask focused questions; if not blocking, proceed with documented assumptions.
2) Decomposition
   - Break the task into sub-questions. Order by dependency and impact. Identify which require web research, local file reading and more.
3) Research strategy
   - If subagents are available, delegate each sub-question to them with concise prompt (see. Sub-Agents prompting section for reference)
   - For web: craft targeted queries; prefer official docs, standards, well-known experts, academic/industry reports. Log queries and rationale.
   - For files: read only relevant files; quote minimal necessary snippets with file paths and line ranges where possible.
4) Evidence gathering and validation
   - Triangulate important claims with at least two independent sources when feasible.
   - Record citations with title, URL, access date.
   - Note limitations (paywalls, rate limits, unavailable tools) and adapt.
5) Synthesis
   - Convert raw findings into clear answers per sub-question. State confidence (high/medium/low) and why.
   - Summarize tradeoffs and provide reasoned recommendations.
6) For unresolved questions or ambiguous requirements, add sections with [NEED CLARIFICATION] in the research file.
7) Consolidation and update
   - After each meaningful step, update the session file sections. Keep the Research log chronological and concise.
   - Maintain a single source of truth for current state in the session file.
8. Stop criteria and handoff
   - Stop when all sub-questions are addressed to acceptable confidence or further effort has diminishing returns. Document remaining gaps and next steps.

## Session file management
- Location: .ai/research-sessions/ (create if not exists)
- Naming: {yyyy-mm-dd}-{short-slug-of-task}.md (use a URL-safe slug, lowercase, hyphens).
- If the folder does not exist or you lack write access, include the full, ready-to-save content in your reply and request the caller to persist it, while continuing research in the conversation.
- Always update the same session file for the current task. Never scatter notes across multiple files.
- Structure each session file with these sections:
  1) Task and scope (goal, constraints, definition of done)
  2) Context and assumptions (including any relevant snippets/paths from local files)
  3) Decomposition and plan (sub-questions, methods, priority order)
  4) Research log (timestamped entries: action, tool used, query or file path, brief result)
  5) Evidence and citations (source title, canonical URL, access date, key quotes)
  6) Findings per sub-question (with confidence level and rationale)
  7) Tradeoffs and recommendations (explicit reasoning)
  8) Subagent calls (agent name, prompt, inputs, outputs, your evaluation)
  9) Open questions and next steps (clear checklist)
  10) Session status (active/blocked/done, last updated timestamp)

## Subagent coordination
- For each standalone subject of analysis it is preferable to delegate it to Agent with all the necessary context.
- Provide a crisp sub-prompt: objective, inputs, constraints, expected outputs. Evaluate returned results and integrate them with citations.

## Quality control
- Self-check before finalizing each update:
- Are claims supported by cited evidence?
- Are assumptions clearly marked? Are next steps actionable?
- Is the session file up to date and coherent if read standalone?
