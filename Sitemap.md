# Product Sitemap

## MVP information architecture

```text
/
|-- /dashboard
|   |-- readiness summary
|   |-- blocked jobs
|   `-- recent activity
|
|-- /jobs
|   `-- /jobs/:jobId
|       |-- overview
|       |-- requirements
|       |-- evidence
|       |-- blockers
|       |-- actions
|       `-- audit trail
|
|-- /completion-packs
|   `-- /completion-packs/:packId
|
|-- /knowledge
|   |-- requirement templates
|   `-- source documents
|
`-- /settings
    |-- integrations
    |-- roles & approvals
    `-- readiness rules
```

## Hackathon prototype screens

1. **Dashboard** - blocked vs review vs billing-ready jobs.
2. **Job Detail** - job status, readiness, critical blockers.
3. **Evidence Analysis** - requirement -> evidence -> reasoning.
4. **Action Approval** - proposed follow-up, owner, approval control.
5. **Completion Pack** - generated evidence summary and download/export actions.

See `design/mockups/` for conceptual layouts. Real implementation screenshots belong in `screenshots/`.
