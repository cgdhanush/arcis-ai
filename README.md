# ARCIS – Autonomous Regulatory Compliance Intelligence System

> AI-powered Regulatory Compliance Automation Platform for Indian Banking and Financial Institutions

ARCIS is an intelligent compliance automation platform designed to simplify regulatory compliance for banks and financial institutions. It continuously ingests notifications from regulatory authorities such as the **Reserve Bank of India (RBI)**, **Securities and Exchange Board of India (SEBI)**, and other government agencies, automatically analyzes regulatory changes, detects conflicts, generates Management Action Plans (MAPs), assigns responsibilities, validates evidence, and maintains a tamper-proof audit trail.

The project follows a modern full-stack architecture consisting of a **FastAPI backend**, **React + Vite frontend**, and **PostgreSQL** database running inside Docker.

---

# Features

## Regulatory Notification Ingestion

* Upload regulatory circulars and notifications
* Support for RBI, SEBI and government circulars
* Store and process structured notification metadata

---

## AI-assisted Compliance Processing

* Regulation parsing
* MAP (Management Action Plan) generation
* Risk scoring
* Conflict detection
* Department assignment
* Evidence validation
* Confidence scoring

---

## Compliance Dashboard

Interactive dashboard providing:

* Compliance KPIs
* Risk overview
* Pending MAPs
* Evidence status
* Audit trail visibility
* Regulatory notification history

---

## Security

* JWT Authentication
* Role Based Access Control (RBAC)
* Protected REST APIs
* Audit logging
* Hash-chain verification

---

# Technology Stack

## Backend

* Python
* FastAPI
* SQLAlchemy
* PostgreSQL
* LangChain (Agent Framework)
* JWT Authentication

---

## Frontend

* React
* Vite
* TypeScript
* TailwindCSS
* Axios
* Recharts

---

## Infrastructure

* Docker
* Docker Compose
* PostgreSQL

---

# Repository Structure

```text
arcis-ai/
│
├── backend/
│   ├── src/
│   │   ├── agents/                 # AI agent orchestration
│   │   ├── api/                    # API routes
│   │   ├── auth/                   # JWT authentication
│   │   ├── core/                   # Configuration
│   │   ├── database/               # Database setup
│   │   ├── models/                 # SQLAlchemy models
│   │   ├── schemas/                # Pydantic schemas
│   │   ├── services/               # Business logic
│   │   ├── utils/                  # Helper utilities
│   │   └── main.py                 # FastAPI application
│   │
│   ├── tests/                      # Backend tests
│   ├── uploads/                    # Uploaded regulation documents
│   ├── requirements.txt
│   ├── pyproject.toml
│   ├── main.py
│   └── __pycache__/
│
├── frontend/
│   ├── src/
│   │   ├── components/             # Reusable React components
│   │   ├── pages/                  # Dashboard pages
│   │   ├── services/               # Axios API client
│   │   ├── hooks/                  # Custom hooks
│   │   ├── assets/                 # Static assets
│   │   ├── App.tsx
│   │   └── main.tsx
│   │
│   ├── dist/                       # Production build
│   ├── node_modules/
│   ├── package.json
│   ├── package-lock.json
│   ├── vite.config.ts
│   ├── tsconfig.json
│   ├── tailwind.config.js
│   ├── postcss.config.js
│   └── index.html
│
├── docs/                           # Documentation
├── docker-compose.yml              # Full stack deployment
└── README.md
```

---

# System Architecture

```
                    +-------------------------+
                    |    Regulatory Sources   |
                    | RBI • SEBI • Govt Docs  |
                    +-----------+-------------+
                                |
                                |
                                ▼
                    +-------------------------+
                    |      FastAPI Backend    |
                    +-------------------------+
                    | Notification Ingestion  |
                    | AI Agent Orchestrator   |
                    | Conflict Detection      |
                    | MAP Generator           |
                    | Risk Engine             |
                    | Evidence Validation     |
                    | Audit Trail             |
                    +-----------+-------------+
                                |
                    PostgreSQL Database
                                |
                                ▼
                    +-------------------------+
                    |   React Dashboard       |
                    | KPI Dashboard           |
                    | Notifications           |
                    | MAP Management          |
                    | Audit Logs              |
                    +-------------------------+
```

---

# Roles

The system currently supports three user roles.

| Role               | Description                               |
| ------------------ | ----------------------------------------- |
| compliance_officer | Creates and manages compliance activities |
| department_owner   | Handles assigned MAPs and evidence        |
| management_viewer  | Read-only dashboard access                |

---

# Backend Directory

```
backend/
```

Contains:

* FastAPI application
* REST APIs
* AI agent workflow
* Authentication
* Database models
* Business logic
* Validation
* Upload handling

### Important Files

| File             | Purpose                   |
| ---------------- | ------------------------- |
| main.py          | Backend entry point       |
| requirements.txt | Python dependencies       |
| pyproject.toml   | Project configuration     |
| src/main.py      | FastAPI application       |
| uploads/         | Uploaded regulation files |
| tests/           | Backend tests             |

---

# Frontend Directory

```
frontend/
```

Contains the React dashboard.

### Important Files

| File               | Purpose                  |
| ------------------ | ------------------------ |
| package.json       | NPM configuration        |
| vite.config.ts     | Vite configuration       |
| tailwind.config.js | TailwindCSS setup        |
| tsconfig.json      | TypeScript configuration |
| src/               | React application source |
| dist/              | Production build         |

---

# Prerequisites

Install the following before running the project.

* Python 3.11+
* Node.js 18+
* npm
* Docker
* Docker Compose
* PostgreSQL (if not using Docker)

---

# Installation

## Clone Repository

```bash
git clone https://github.com/cgdhanush/arcis-ai.git

cd arcis-ai
```

---

# Running with Docker (Recommended)

Start the complete application.

Run in detached mode.

```bash
docker compose up -d
```

Stop containers.

```bash
docker compose down
```

---

# Backend Development

Navigate to backend.

```bash
cd backend
```

Install dependencies.

```bash
pip install -r requirements.txt
```

Run the API server.

```bash
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

Backend available at

```
http://localhost:8000
```

Swagger UI

```
http://localhost:8000/docs
```

OpenAPI Specification

```
http://localhost:8000/openapi.json
```

---

# Frontend Development

Navigate to frontend.

```bash
cd frontend
```

Install packages.

```bash
npm install
```

Run development server.

```bash
npm run dev
```

Frontend available at

```
http://localhost:5173
```

Build production version.

```bash
npm run build
```

Preview production build.

```bash
npm run preview
```

---

# Environment Variables

Create an environment file.

```bash
cp .env.example .env
```

Typical variables include:

```env
DATABASE_URL=postgresql://user:password@postgres:5432/arcis

JWT_SECRET=your-secret-key

OPENAI_API_KEY=your-api-key

ACCESS_TOKEN_EXPIRE_MINUTES=60
```

---

# API Endpoints

Base URL

```
http://localhost:8000/api/v1
```

## Public

```
GET  /health
POST /auth/token
```

## Protected

```
POST /upload-regulation
POST /notifications/ingest
POST /detect-conflicts
POST /generate-maps
GET  /maps
POST /assign-maps
POST /upload-evidence
POST /validate-evidence
GET  /dashboard
GET  /audit-log
GET  /audit/verify
GET  /risks
```

---

# Demo Flow

## Generate Token

```bash
curl -X POST http://localhost:8000/api/v1/auth/token \
-H "Content-Type: application/json" \
-d '{
"username":"ops.user",
"role":"compliance_officer"
}'
```

---

## Upload Notification

```bash
curl -X POST http://localhost:8000/api/v1/notifications/ingest \
-H "Authorization: Bearer <TOKEN>" \
-H "Content-Type: application/json" \
-d '{
"source":"RBI",
"external_id":"RBI-ITG-2024-001",
"title":"Master Direction on IT Governance 2024",
"content":"Banks must conduct VAPT and update cyber controls within 60 days."
}'
```

---

## View Generated MAPs

```bash
curl -H "Authorization: Bearer <TOKEN>" \
http://localhost:8000/api/v1/maps
```

---

## View Risks

```bash
curl -H "Authorization: Bearer <TOKEN>" \
http://localhost:8000/api/v1/risks
```

---

## Verify Audit Chain

```bash
curl -H "Authorization: Bearer <TOKEN>" \
http://localhost:8000/api/v1/audit/verify
```

---

# Seed Sample Data

Generate a token.

```bash
token=$(curl -s -X POST http://localhost:8000/api/v1/auth/token \
-H "Content-Type: application/json" \
-d '{"username":"demo.user","role":"compliance_officer"}' | python -c 'import sys,json;print(json.load(sys.stdin)["access_token"])')
```

Seed the database.

```bash
curl -X POST http://localhost:8000/api/v1/sample-data/seed \
-H "Authorization: Bearer $token" \
-H "Content-Type: application/json" \
-d '{}'
```

---

# Future Enhancements

* LangChain multi-agent workflow
* LLM-powered compliance reasoning
* Automatic circular ingestion from RBI/SEBI
* OCR support for scanned PDFs
* Email notifications
* WebSocket live updates
* PostgreSQL migrations with Alembic
* Kubernetes deployment
* CI/CD pipelines
* Unit and integration testing
* Production monitoring

---

# Notes

The current version is an MVP intended for demonstrating the overall compliance automation workflow. Several AI components currently use deterministic placeholder implementations and can be replaced with production-ready LangChain agents and LLM providers.

---

# License

This project is intended for educational, research, and demonstration purposes. Add an appropriate open-source or proprietary license before production deployment.
