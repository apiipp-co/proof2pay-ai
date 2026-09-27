# Design System & UX Principles

## Product personality

Professional, operational, evidence-first, calm under pressure. The interface should feel closer to an operations command center than a consumer chatbot.

## Visual direction

- Light neutral workspace with high information clarity.
- Strong hierarchy: **Job status -> blockers -> evidence -> next action**.
- Use restrained accent colors; never rely on color alone for status.
- Monospace is appropriate for IDs, tool names, hashes, and state codes.
- Readiness should communicate state first, percentage second.

## UX principles

### 1. Explain before asking for action
Every blocker must show *why* it exists and which requirement/evidence caused it.

### 2. Evidence over confidence theater
Do not display an AI confidence number without context. Prefer source-linked reasoning and explicit uncertainty.

### 3. Blockers are actionable
A blocker card contains:
- requirement;
- source;
- current evidence;
- status;
- why it is blocked;
- recommended next action;
- responsible role.

### 4. Human control is visible
Approval controls should be explicit, not hidden in conversational text.

### 5. Do not confuse concept with proof
Concept mockups use a visible `CONCEPT` badge. Submission screenshots must come from the working prototype.

## Core screen hierarchy

### Dashboard
- KPI: reported complete, blocked, review required, billing ready.
- priority queue ordered by critical blocker and age.

### Job detail
- Header: job, customer alias, service type, state.
- Billing readiness status.
- critical blockers.
- requirements/evidence table.
- agent activity and approvals.

### Evidence analysis
Split view:
- left: requirement + source;
- center: candidate evidence;
- right: assessment + explanation + next action.

### Completion pack
- evidence summary;
- generated service report draft;
- handover/BAST draft when relevant;
- audit manifest;
- explicit human confirmation.
