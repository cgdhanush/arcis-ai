# ARCIS

Autonomous Regulatory Compliance Intelligence System for Indian Banking and Financial Institutions.

ARCIS automates the compliance lifecycle for RBI, SEBI, and government circulars using a multi-agent backend and a live management dashboard.

## MVP Scope

This implementation provides an MVP scaffold with:

- Ingestion pipeline for new notifications.
- Conflict detection placeholder logic.
- MAP generation from regulation content.
- Risk scoring and assignment to departments.
- Evidence validation with confidence output.
- Hash-chained audit trail verification.
- JWT + RBAC protected APIs.
- React dashboard with KPI visibility.

## Tech Stack

- Backend: Python, FastAPI, LangChain, SQLAlchemy, PostgreSQL.
- LLM: OpenAI GPT-4o-ready agent layer.
- Frontend: React, Vite, TailwindCSS, Axios, Recharts.
- Local infra: Docker Compose.

## Repository Layout

- backend: API, services, agent workflow skeleton, models.
- frontend: dashboard UI and API client.
- docs: architecture notes.
- docker-compose.yml: local full-stack runtime.

## Roles

- compliance_officer
- department_owner
- management_viewer

## Quick Start

1. Create local env file:

```bash
cp .env.example .env
```

2. Start full stack:

```bash
docker compose up --build
```

3. Open dashboard:

- http://localhost:5173

4. Seed sample demonstration data (optional but recommended after startup):

```bash
token=$(curl -s -X POST http://localhost:8000/api/v1/auth/token \
  -H "Content-Type: application/json" \
  -d '{"username":"demo.user","role":"compliance_officer"}' | python -c 'import sys, json; print(json.load(sys.stdin)["access_token"])')

curl -s -X POST http://localhost:8000/api/v1/sample-data/seed \
  -H "Authorization: Bearer $token" \
  -H "Content-Type: application/json" \
  -d '{}'
```

5. Get token in UI using one of the supported roles.

If you want to run backend directly during development:

```bash
cd backend
uvicorn main:app --reload
```

If you want to run frontend directly during development:

```bash
cd frontend
npm install
npm run dev
```

## Backend API

Base URL: http://localhost:8000/api/v1

Public:

- GET /health
- POST /auth/token

Protected examples:

- POST /upload-regulation
- POST /detect-conflicts
- POST /generate-maps
- GET /maps
- POST /assign-maps
- POST /upload-evidence
- POST /validate-evidence
- GET /dashboard
- GET /audit-log

## Demo Flow

1. Issue token:

```bash
curl -s -X POST http://localhost:8000/api/v1/auth/token \
	-H "Content-Type: application/json" \
	-d '{"username":"ops.user","role":"compliance_officer"}'
```

2. Ingest notification:

```bash
curl -s -X POST http://localhost:8000/api/v1/notifications/ingest \
	-H "Content-Type: application/json" \
	-H "Authorization: Bearer <TOKEN>" \
	-d '{
		"source":"RBI",
		"external_id":"RBI-ITG-2024-001",
		"title":"Master Direction on IT Governance 2024",
		"content":"Banks must conduct VAPT and update cyber controls within 60 days."
	}'
```

3. Review generated data:

```bash
curl -s -H "Authorization: Bearer <TOKEN>" http://localhost:8000/api/v1/maps
curl -s -H "Authorization: Bearer <TOKEN>" http://localhost:8000/api/v1/risks
curl -s -H "Authorization: Bearer <TOKEN>" http://localhost:8000/api/v1/audit/verify
```

## Notes

- Agent logic in this MVP is deterministic placeholder logic intended for rapid validation.
- Replace placeholder functions in backend/src/agents/orchestrator.py with real LangChain agent chains and model providers.
- Add migrations, tests, and websocket streaming in the next implementation phase.
