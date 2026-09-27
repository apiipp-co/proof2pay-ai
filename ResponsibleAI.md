# Responsible AI & Safety Specification

## Principle

PROOF2PAY assists with **evidence reconciliation and workflow orchestration**. It must not manufacture proof or become the sole authority for legal acceptance, billing authorization, or payment.

## Risk taxonomy

### Hallucinated completion
Risk: AI interprets a technician statement as proof.  
Control: claims and evidence are separate objects; a claim alone cannot satisfy a critical evidence requirement unless policy explicitly allows it.

### Incorrect requirement interpretation
Risk: retrieved SOW/policy clause is wrong or irrelevant.  
Control: source reference is mandatory; ambiguity routes to human review.

### Fabricated or altered evidence
Risk: system generates/relabels content as proof.  
Control: generated documents are marked as drafts; original evidence hashes/metadata are preserved where feasible.

### Automation overreach
Risk: agent sends customer communication or triggers billing without authorization.  
Control: explicit approval gate for consequential external actions.

### Privacy
Risk: evidence contains customer names, phone numbers, addresses, signatures, or site photos.  
Control: data minimization, masking/redaction for demo, role-scoped access, retention policy.

### Bias and inconsistent treatment
Risk: similar evidence is assessed differently.  
Control: deterministic critical rules, standardized templates, audit logs, evaluation test set.

## Transparency requirements

Every blocker should expose:
- requirement title;
- source reference;
- evidence considered;
- status;
- explanation;
- uncertainty/limitations;
- recommended action;
- whether human review is mandatory.

## Human-in-the-loop gates

Human confirmation is required before:
- final billing-ready confirmation in the MVP;
- customer-facing requests;
- completion/handover documents intended for external use;
- downstream accounting/invoicing actions.

## Evaluation checklist

- No unsupported statement presented as verified evidence.
- All critical decisions source-linked.
- Ambiguous test cases correctly escalate.
- Prompt injection in uploaded documents does not override system/business rules.
- PII does not appear in logs beyond what is required.
- Generated completion pack clearly separates source facts from generated narrative.
