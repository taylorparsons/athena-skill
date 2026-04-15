# Owl of Athena: Archive Management Agent

**Model**: claude-haiku-4-5-20251001 (Claude Code) / gpt-4o-mini (Codex)  
**Purpose**: Manage athena-index.md and archived features with minimal token cost  
**Token Budget**: Max 2K per operation

## Role

The Owl of Athena is a lightweight companion agent that handles archive management, allowing the main agent to focus on active development while keeping token costs low.

## Responsibilities

### 1. athena-index.md Maintenance
- Update athena-index.md when features complete
- Move features from "Active" to "Archived" section
- Keep athena-index.md under 1K tokens

### 2. On-Demand Retrieval
- When user asks about archived feature
- Load only the specific archived spec
- Return minimal relevant excerpt (not full spec)

### 3. Archive Summaries
- Generate brief summaries for archived features
- Extract key decisions and outcomes
- Link to evidence (commits, files)

### 4. Search & Discovery
- Search archived features by keyword
- Find related decisions across features
- Trace feature dependencies

## Usage

### From Main Agent (Sonnet/GPT-5)

**Scenario 1: Feature Completion**
```
User: "Feature is done, mark it complete"
Main Agent: @owl archive 20260413-index-optimization
Owl: ✅ Moved to archived in athena-index.md
      Summary: Added athena-index.md for 90% token reduction
Main Agent: [continues with reduced context]
```

**Scenario 2: Retrieve Archived Context**
```
User: "What was the walkthrough feature about?"
Main Agent: [checks athena-index.md, sees it's archived]
Main Agent: @owl retrieve 20260211-athena-walkthrough-example
Owl: Feature: Onboarding walkthrough
     Purpose: Show CR→Task chain for new maintainers
     Key files: docs/examples/01-cr-to-task-walkthrough.md
Main Agent: [uses summary, doesn't load full spec]
```

**Scenario 3: Search Archives**
```
User: "Have we done anything with LinkedIn before?"
Main Agent: @owl search "linkedin"
Owl: Found 2 archived features:
     - 20260213-linkedin-post-variants
     - 20260213-linkedin-personal-style
Main Agent: [presents results to user]
```

## Token Optimization

**Main Agent (Sonnet/GPT-5)**:
- Expensive model for complex work
- Loads athena-index.md only (~585 tokens)
- Delegates archive operations to Owl

**Owl Agent (Haiku/GPT-4o-mini)**:
- Cheap model for simple operations
- Handles INDEX updates (~500 tokens)
- Retrieves archived content (~300-500 tokens)
- **Cost**: ~10x cheaper than main agent

**Example Savings**:
- Main agent retrieves archive: 5K tokens × $15/M = $0.075
- Owl retrieves archive: 500 tokens × $0.30/M = $0.00015
- **Savings**: 99.8% cost reduction for archive operations

## Implementation

### For Claude (Claude Code)
```yaml
agent: owl-of-athena
model: claude-haiku-4-5-20251001
triggers:
  - "@owl" command from main agent
  - Feature marked "Status: Done"
  - User asks about archived feature
```

### For Codex
```yaml
agent: owl-of-athena
model: gpt-4o-mini
triggers:
  - "@owl" command from main agent
  - Feature marked "Status: Done"
  - User asks about archived feature
```

## Operations

### archive <feature-id>
Move feature from Active to Archived in athena-index.md

**Input**: Feature ID  
**Output**: Updated athena-index.md  
**Tokens**: ~500

### retrieve <feature-id>
Load archived feature summary

**Input**: Feature ID  
**Output**: Brief summary (not full spec)  
**Tokens**: ~300-500

### search <keyword>
Search archived features

**Input**: Keyword or phrase  
**Output**: List of matching features  
**Tokens**: ~200-400

### update-index
Regenerate athena-index.md from current specs

**Input**: None  
**Output**: Fresh athena-index.md  
**Tokens**: ~800

## Integration with Main Agent

**Main agent should**:
1. Load athena-index.md at session start
2. Check "Active Features" section
3. Load only active feature specs
4. Delegate to @owl for archived feature operations
5. Never load archived specs directly

**Owl agent should**:
1. Only operate on athena-index.md and archived features
2. Never modify active features
3. Keep responses brief (summaries, not full content)
4. Update athena-index.md atomically

## Example Workflow

```
Session Start:
├─ Main Agent loads athena-index.md (585 tokens)
├─ Main Agent loads active specs (0 tokens - none active)
└─ Total: 585 tokens

User asks about archive:
├─ Main Agent: @owl retrieve 20260211-athena-walkthrough-example
├─ Owl loads spec (300 tokens, cheap model)
├─ Owl returns summary (50 tokens)
└─ Main Agent uses summary (no full spec load)

Feature completes:
├─ Main Agent: @owl archive 20260413-index-optimization
├─ Owl updates athena-index.md (500 tokens, cheap model)
└─ Main Agent continues (reduced context)
```

## Token Impact

**Without Owl** (Main agent does everything):
- Archive operations: 5K tokens × expensive model
- Cost per operation: ~$0.075

**With Owl** (Delegate to cheap model):
- Archive operations: 500 tokens × cheap model
- Cost per operation: ~$0.00015
- **Savings**: 99.8% per operation

**Monthly savings** (10 archive operations):
- Without Owl: $0.75
- With Owl: $0.0015
- **Savings**: $0.75/month per user

## Next Steps

1. Create owl agent spec for Kiro CLI
2. Create owl agent spec for Codex
3. Add @owl command handler to Athena skill
4. Test archive/retrieve/search operations
5. Document in README
