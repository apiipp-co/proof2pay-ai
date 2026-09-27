# Security Policy

## Do not commit
- API keys or service-role credentials;
- real customer signatures or identity documents;
- unredacted private job photos;
- production database exports;
- model/provider secrets.

## Report a security issue
For a hackathon repository, report privately to the project owner rather than opening a public issue containing sensitive details.

## MVP security posture
- `.env` excluded from git;
- least-privilege credentials;
- synthetic browser demo data and a small published NYC Parks work-order snapshot with no private customer artifacts;
- human approval gates;
- job/evidence authorization boundary planned for production.
