# ARCIS Architecture

ARCIS is implemented as an MVP monorepo with:

- FastAPI backend for ingestion, MAP generation, risk scoring, evidence validation, and audit verification.
- PostgreSQL for transactional storage.
- Hash-chained audit records for tamper evidence.
- React dashboard for real-time compliance visibility.

Core flow:

1. Notification ingestion from RBI, SEBI, or Ministry feed.
2. Conflict detection against policy context.
3. MAP generation with department owner and deadline.
4. Risk scoring and assignment.
5. Evidence validation with confidence output.
6. Immutable audit record append for each critical action.
