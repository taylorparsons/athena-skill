# athena-index.md Test Results

**Test Date**: 2026-04-14 (re-measured)
**Branch**: feature/index-based-archival
**Tokenizer**: cl100k_base (tiktoken) — approximate for Claude; actual Claude token counts may vary slightly

## Measured Token Counts

| File | Tokens | Size |
|---|---|---|
| `docs/decisions.md` | 7,250 | 30,504 bytes |
| `docs/PRD.md` | 7,002 | 19,813 bytes |
| All 19 `spec.md` files | 9,015 | — |
| All 19 `tasks.md` files | 3,302 | — |
| `docs/progress.txt` | 4,412 | 16,090 bytes |
| `docs/requests.md` | 3,807 | 14,054 bytes |
| `docs/athena-index.md` | 1,601 | 6,531 bytes |
| `docs/TRACEABILITY.md` | 180 | 604 bytes |

## Session Startup Totals

**Without athena-index.md** (load all specs):
- Common files: 22,651 tokens
- + 19 spec.md files: 9,015 tokens
- **Total: 31,666 tokens**

**With athena-index.md** (load INDEX, skip archived specs):
- Common files: 22,651 tokens
- + athena-index.md: 1,601 tokens
- **Total: 24,252 tokens**

**Savings: 7,414 tokens (23% reduction)**

### What Drives the Savings

The spec replacement accounts for all of it: swapping 9,015 tokens of spec files for 1,601 tokens of athena-index.md saves 7,414 tokens. Every additional closed feature adds ~470 tokens to the spec load that Owl skips.

The larger token consumers — `decisions.md` (7,250), `PRD.md` (7,002), `progress.txt` (4,412) — are loaded in both scenarios. These grow unboundedly without pruning. `prune-done` targets `progress.txt` at session end.

## Validation Tests

✅ athena-index.md contains 19 features
✅ docs/specs/ contains 19 directories
✅ All features accounted for
✅ All spec paths valid
✅ Sample spec file accessible

## Real-World Usage

### Scenario 1: No Active Features (Current State)
- Load: athena-index.md (1,601 tokens) — skip all 19 archived specs
- **Startup: 24,252 tokens**

### Scenario 2: 1 Active Feature
- Load: athena-index.md + 1 active spec (~475 tokens avg)
- Skip: 18 archived specs
- **Startup: ~24,727 tokens**

### Scenario 3: User Asks About Archived Feature
- Agent checks athena-index.md → dispatches to Owl
- Owl loads specific archived spec on-demand (~475 tokens avg, cheap model)
- Main agent receives summary only

## Recommendations

✅ **Merge to main**: athena-index.md approach is production-ready  
✅ **Update Athena skill**: Add athena-index.md loading to ATHENA loop  
✅ **Document usage**: Add athena-index.md guidance to README  

## Next Steps

1. Update Athena SKILL.md to load athena-index.md first
2. Add script to auto-update athena-index.md when features complete
3. Test in real Athena session
4. Merge to main
