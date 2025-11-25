# Phase 2 Planning: Validation Engine, Data Model & API

## 1. Purpose
Phase 1 (Data Migration Engine) is complete and documented in `PHASE1_IMPLEMENTATION.md`. The next milestone is to extend the migration tooling with automated validation, persistence, and service interfaces so we can eventually support a full GUI workflow. This plan analyzes the documented architecture (see Section 2) and recommends how to proceed with **Phase 2 (Validation Engine)** in combination with the **Data Model & API foundation**.

## 2. Documentation Reviewed
- `Technical_Deep_Dive_Capirca.md` – Core Capirca architecture, Phase 2/3 definitions, database schema draft, API/GUI outline.
- `PHASE1_IMPLEMENTATION.md` – Detailed description of the migration engine assets already built.
- `Capirca_Migration_Analysis_Report.md` – Migration roadmap, GUI vision, and sprint plan.
- `ANALYSIS_INDEX.md` & `README.md` – High-level repository index and Capirca basics for cross-checking conventions.
- Forcepoint analysis documents (`FORCEPOINT_SUMMARY.md`, `Forcepoint_Extension_Analysis_Report.md`) – Additional context on generator extensibility and phased delivery patterns.

These references confirm that validation, persistence, and service layers are still aspirational and no conflicting plans exist.

## 3. Current State Snapshot
| Area | Status | Notes |
|------|--------|-------|
| Confluence ingestion & policy generation | ✅ Implemented | `capirca/utils/migration.py`, tests, and example script.
| Validation engine | ❌ Not started | Only conceptual classes (`PolicyValidator`) listed in Technical Deep Dive.
| Data model / persistence | ❌ Not started | Draft schema (policies, network_objects, service_objects, deployments) exists only in documentation.
| API layer (FastAPI) | ❌ Not started | Endpoint sketches exist but no code.
| GUI | ❌ Not started | Depends on API + validation.

## 4. Decision Analysis: Phase 2 vs. Data Model/API First
| Option | Pros | Cons | Dependencies |
|--------|------|------|--------------|
| **Implement Validation Engine first** | Direct continuation of Phase 1 code; faster feedback on migrated policies. | No persistent store or API to surface validation results; would require ad-hoc CLI usage; harder to integrate later. | Needs object definitions in-memory only; limited scalability.
| **Implement Data Model & API first** | Establishes persistence, multi-user access, and reusable service endpoints; validation logic can be embedded as API service routines; unblocks GUI work. | Requires upfront database + service scaffolding before validation features are visible. | Needs DB migrations/ORM config and minimal deployment story.

**Recommendation:** Start with the **Data Model & API foundation** and embed the **Validation Engine** as part of those services. This keeps architecture aligned with the Technical Deep Dive and the Migration Analysis roadmap, avoids rework, and enables both CLI and GUI clients to consume the same validation features.

## 5. Proposed Implementation Plan
1. **Platform Foundation (Week 1)**
   - Finalize DB schema (tables: `policies`, `network_objects`, `service_objects`, `deployments`, plus `users` if needed for ownership).
   - Select persistence layer (SQLAlchemy with Alembic migrations) and configure settings (env vars, `.env`, `database.py`).
   - Define Pydantic models shared between FastAPI and internal services.

2. **API Skeleton (Week 1-2)**
   - Scaffold FastAPI app under `capirca/api/` (or similar) with routers for policies, network objects, service objects, deployments.
   - Implement CRUD endpoints mirroring the Technical Deep Dive spec (list/create/update, deploy action endpoint stub).
   - Integrate authentication placeholder (API key or simple token) to prepare for RBAC later.

3. **Validation Engine Integration (Week 2-3)**
   - Implement `PolicyValidator` service module with the three validation layers:
     - **Syntax Validation:** reuse Capirca parser (`policy.ParsePolicy`) to validate `.pol` content.
     - **Reference Validation:** load definitions via `naming.py` and ensure referenced tokens exist.
     - **Security Checks:** start with a rule set (e.g., action defaults, allow-any-any detection) and keep extensible.
   - Expose validation results via API (e.g., `POST /api/policies/{id}/validate`).
   - Add background tasks (Celery or simple async tasks) if validation becomes long-running.

4. **Persistence & Object Sync (Week 3)**
   - Store migrated objects/policies from Phase 1 pipelines into the database through the new API/service layer.
   - Provide export/import helpers to keep `.pol`, `.net`, `.svc` files synchronized with DB entries (enables existing CLI workflows).

5. **Deployment Hooks (Stretch / Week 4)**
   - Define deployment request model (platform, target, version) and store metadata only.
   - Actual deployment execution (Phase 3) can stub responses but capture desired lifecycle (pending → running → success/failure) so UI work can start later.

6. **Testing & Documentation**
   - Unit tests for validators, routers, and ORM models.
   - Integration test simulating end-to-end flow: migrate → persist → validate → prepare deployment record.
   - Documentation update: new `PHASE2_VALIDATION_AND_API_PLAN.md` (this file) + README section referencing new services.

## 6. Suggested Sprint Breakdown
| Sprint | Focus | Deliverables |
|--------|-------|--------------|
| Sprint 1 | DB + API scaffold | SQLAlchemy models, migrations, FastAPI skeleton, basic CRUD for policies/objects. |
| Sprint 2 | Validation engine | PolicyValidator service, validation endpoints, CLI hooks for migration tool to call API. |
| Sprint 3 | Persistence wiring & deployment stubs | Migration tool persists via API, deployment records, initial background job structure, documentation/tests. |

(Adjust sprint length per team cadence; above assumes 1-week sprints for clarity.)

## 7. Immediate Next Steps
1. Approve this plan and confirm technology choices (FastAPI + SQLAlchemy + Alembic + PostgreSQL).
2. Create new `capirca/api/` package (or equivalent) with application factory and router layout.
3. Implement DB models & migrations aligned with Technical Deep Dive schema.
4. Begin PolicyValidator implementation alongside API endpoints so validation is service-accessible from day one.

Once these steps land, we can iterate on advanced validation rules, start Phase 3 (deployment engine), and finally tackle the GUI with a stable backend.
