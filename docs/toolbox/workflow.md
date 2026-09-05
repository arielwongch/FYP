# FYP Vibe-Coding Workflow
# FYP Vibe-Coding Workflow

## Before coding
1. Read:
   - `docs/spec.md`
   - `docs/architecture.md`
   - `docs/memory.md`
   - `docs/toolbox/workflow.md`
2. Ask Copilot to summarize the current state and open questions.
3. Update `docs/progress.md` with completed work, current focus, next steps, and
   locked decisions.

## Implementation loop (per feature)

1. Clarify the smallest useful feature and its acceptance check.
2. Implement one focused slice in the relevant `app/` or `ui/` module.
3. Validate immediately with the narrowest useful test, startup check, or lint
   command.
4. Review against `docs/spec.md`, especially secret handling and input validation.
5. Update `docs/progress.md`, `docs/memory.md`, and `docs/logs.md` when the slice
   creates a durable decision or learning.
6. Make small commits with clear messages when committing is requested.

## Debugging checklist

When something breaks:

- [ ] Read error carefully; paste into Copilot with context files.
- [ ] Check:
   - Env vars (`OPENROUTER_API_KEY`, `OPENROUTER_BASE_URL`, `LLM_PROVIDER`)
   - Imports and local module paths
   - Explicit provider selection (`openrouter` or `mock`)
   - `.data/` persistence and JSON validity
  - Tool registry includes the new tool
- [ ] Add a minimal test that reproduces the issue.
- [ ] Find the root cause and list out the files involved
- [ ] Fix, then ensure test passes.

## Security checklist

- [ ] No API keys in browser responses or logs.
- [ ] All LLM output treated as untrusted and validated.
- [ ] Provider selection never silently falls back.
- [ ] Tool execution is bounded when tools are introduced.
- [ ] Bind to localhost by default.

## When I'm stuck

- Re-read `spec.md` and `architecture.md`.
- Ask Copilot:
  - "What are the minimal changes to make X work?"
  - "Propose 3 options with trade-offs."
- Step away briefly; come back and re-scope to something smaller.