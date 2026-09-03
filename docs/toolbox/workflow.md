# docs/toolbox/workflow.md
# My Vibe-Coding Workflow

## Before coding
1. Open:
   - `docs/spec.md`
   - `docs/architecture.md`
   - `docs/memory.md`
   - `docs/toolbox/workflow.md`
2. In Copilot Chat:
   - Attach SPEC + ARCHITECTURE.
   - Ask: "Summarize current state and open questions."
3. Update `docs/progress.md`:
   - What's done
   - What I'm focusing on now
   - Any locked decisions

## Implementation loop (per feature)

1. Clarify:
   - Write a short note in `progress.md`: Please Reference `docs\template\progress.md`
2. Implement:
   - "Implement X `.github\copilot-instructions.md`."
3. Review:
   - Does it match `spec.md`?
   - Any security issues (keys, input validation)?
4. Test:
   - Run relevant tests.
   - If missing, ask: "Add tests for X in `backend/tests/`."
5. Commit:
   - Small commits with clear messages.
6. Update:
   - `progress.md` (done/next)
   - `memory.md` (new pitfalls/patterns)(reference `docs\toolbox\workflow.md`)

## Debugging checklist

When something breaks:

- [ ] Read error carefully; paste into Copilot with context files.
- [ ] Check:
  - Env vars (`LLM_API_KEY`, URLs)
  - Imports and paths
  - Tool registry includes the new tool
  - Skill allows the tool
- [ ] Add a minimal test that reproduces the issue.
- [ ] Find the root cause and list out the files involved
- [ ] Fix, then ensure test passes.

## Security checklist

- [ ] No API keys in frontend or logs.
- [ ] All LLM output treated as untrusted.
- [ ] Tool execution bounded (timeouts, path restrictions).
- [ ] Localhost-only CORS.

## When I'm stuck

- Re-read `spec.md` and `architecture.md`.
- Ask Copilot:
  - "What are the minimal changes to make X work?"
  - "Propose 3 options with trade-offs."
- Step away briefly; come back and re-scope to something smaller.