# Evidence Matcher Prompt Spec

For each requirement:

1. quote/identify the requirement source reference;
2. identify candidate evidence IDs;
3. explain why each candidate does or does not support the requirement;
4. classify status: `READY`, `MISSING`, `INCOMPLETE`, `AMBIGUOUS`, `HUMAN_REVIEW`;
5. output a next-action recommendation if unresolved.

A semantic similarity match is not sufficient proof of satisfaction for a critical requirement. The final critical state is subject to deterministic business rules and human review when configured.
