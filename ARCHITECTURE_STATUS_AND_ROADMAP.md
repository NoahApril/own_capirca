# Capirca Architecture Status & Roadmap

**Last Updated:** November 2024  
**Branch:** `capirca-arch-review-mds-phase2-vs-datamodel-api-plan`

## 1. Complete Architecture Vision

This document provides a comprehensive overview of the current implementation status and future roadmap for the Capirca migration and GUI project.

---

## 2. Architecture Layers Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                     Layer 5: Frontend GUI                        │
│  React/Vue • Policy Editor • Approval Workflow • Deployment UI  │
│                        ❌ NOT STARTED                            │
└────────────────────────────┬────────────────────────────────────┘
                             │
┌────────────────────────────┴────────────────────────────────────┐
│                     Layer 4: API Gateway                         │
│  FastAPI • REST Endpoints • Authentication • Request Validation  │
│                      ✅ IMPLEMENTED (Phase 2)                    │
└────────────────────────────┬────────────────────────────────────┘
                             │
┌────────────────────────────┴────────────────────────────────────┐
│                  Layer 3: Business Logic                         │
│  Validation Engine • Deployment Engine • Policy Management      │
│   ⚠️ PARTIALLY IMPLEMENTED (Phase 2 done, Phase 3 pending)      │
└────────────────────────────┬────────────────────────────────────┘
                             │
┌────────────────────────────┴────────────────────────────────────┐
│                    Layer 2: Data Layer                           │
│  Database (PostgreSQL) • ORM (SQLAlchemy) • Migrations (Alembic) │
│                      ✅ IMPLEMENTED (Phase 2)                    │
└────────────────────────────┬────────────────────────────────────┘
                             │
┌────────────────────────────┴────────────────────────────────────┐
│                 Layer 1: Migration Engine                        │
│  Confluence Parser • Object Extractor • Capirca Generator        │
│                      ✅ IMPLEMENTED (Phase 1)                   │
└─────────────────────────────────────────────────────────────────┘
                             │
┌────────────────────────────┴────────────────────────────────────┐
│                  Layer 0: Capirca Core                           │
│  Policy Parser (PLY) • Naming System • ACL Generators (25+)      │
│                      ✅ EXISTING CODEBASE                        │
└─────────────────────────────────────────────────────────────────┘
```

---

## 3. Status Matrix

| Component | Status | Files | Tests | Docs | Priority |
|-----------|--------|-------|-------|------|----------|
| **Capirca Core** | ✅ Complete | `capirca/lib/*` | ✅ Extensive | ✅ Yes | Stable |
| **Migration Engine** | ✅ Complete | `capirca/utils/migration.py` | ✅ 23 tests | ✅ PHASE1 | Stable |
| **Validation Engine** | ✅ Complete | `capirca/api/services/validator.py` | ✅ Yes | ✅ PHASE2 | Stable |
| **Data Model** | ✅ Complete | `capirca/db/models.py` | ✅ Yes | ✅ PHASE2 | Stable |
| **API Layer** | ✅ Complete | `capirca/api/` | ✅ Yes | ✅ PHASE2 | Stable |
| **Deployment Engine** | ❌ Not Started | - | - | ⚠️ Planned | **NEXT** |
| **GUI** | ❌ Not Started | - | - | ⚠️ Concept | LOW |

---

## 4. Detailed Component Breakdown

### ✅ Phase 1: Data Migration Engine (COMPLETE)

**Implemented:**
- Confluence HTML table parser (English & German headers)
- Network object extraction with deduplication
- Service object extraction with protocol handling
- Capirca policy file generation
- Definition file generation (.net and .svc)
- Comprehensive test suite (23 tests)
- Working example script

**Files:**
```
capirca/utils/migration.py          (700+ lines)
tests/utils/migration_test.py       (400+ lines)
examples/migration_example.py       (150+ lines)
PHASE1_IMPLEMENTATION.md            (Documentation)
```

**Capabilities:**
- Parse Confluence tables → Structured rules
- Extract reusable objects automatically
- Generate valid Capirca policies
- Support multiple targets (cisco, juniper, iptables, etc.)

**Next Integration:** Connect to API for persistence

---

### ✅ Phase 2: Validation Engine & API Foundation (COMPLETE)

**From Technical_Deep_Dive_Capirca.md:**

```python
class PolicyValidator:
    def validate_syntax(self, policy_content: str) -> List[ValidationError]:
        """Validate Capirca policy syntax using PLY parser"""
        
    def validate_references(self, policy_content: str, definitions: Definitions) -> List[ValidationError]:
        """Validate object references exist in definitions"""
        
    def validate_security(self, policy_content: str) -> List[SecurityWarning]:
        """Check for security anti-patterns"""
```

**Three Validation Layers:**

1. **Syntax Validation**
   - Use existing `policy.ParsePolicy` from Capirca core
   - Check for parsing errors
   - Validate keyword usage
   - Report line numbers and error details

2. **Reference Validation**
   - Load network objects from DB/definitions
   - Load service objects from DB/definitions
   - Check all references in policy terms
   - Report missing or undefined tokens

3. **Security Validation**
   - Detect `any → any allow` rules
   - Check for overly permissive rules
   - Verify required actions (default deny)
   - Identify shadowed rules
   - Check expiration dates

**Implementation:**
- ✅ Embedded in API as service module (`capirca/api/services/validator.py`)
- ✅ Exposed via `/api/policies/{id}/validate`
- ✅ Supports real-time validation
- ✅ Returns structured validation results (errors, warnings, info)

**Database Models:**
- ✅ `Policy` - stores policy content, version, status
- ✅ `NetworkObject` - reusable network definitions
- ✅ `ServiceObject` - reusable service definitions
- ✅ `Deployment` - deployment tracking
- ✅ `ValidationResult` - validation results storage

**API Endpoints:**
- ✅ `/api/policies` - CRUD operations
- ✅ `/api/network-objects` - CRUD operations
- ✅ `/api/service-objects` - CRUD operations
- ✅ `/api/deployments` - deployment management
- ✅ `/api/policies/{id}/validate` - policy validation

**Files:**
```
capirca/db/
├── __init__.py
├── base.py              # SQLAlchemy setup
├── models.py            # ORM models
└── init_db.py           # Database initialization

capirca/api/
├── __init__.py
├── main.py              # FastAPI app
├── config.py            # Settings
├── models/
│   ├── __init__.py
│   └── schemas.py       # Pydantic models
├── routers/
│   ├── __init__.py
│   ├── policies.py
│   ├── network_objects.py
│   ├── service_objects.py
│   └── deployments.py
└── services/
    ├── __init__.py
    └── validator.py     # PolicyValidator

tests/api/
├── __init__.py
├── test_phase2_api.py
└── test_validator.py

examples/phase2_example.py
PHASE2_IMPLEMENTATION.md
```

---

### ⚠️ Phase 3: Deployment Engine (PLANNED)

**From Technical_Deep_Dive_Capirca.md:**

```python
class DeploymentEngine:
    def generate_configs(self, policy_id: int) -> Dict[str, str]:
        """Generate platform-specific configurations"""
        
    def deploy_to_platform(self, platform: str, config: str, target: str) -> DeploymentResult:
        """Deploy configuration to target platform"""
        
    def rollback_deployment(self, deployment_id: int) -> RollbackResult:
        """Rollback failed deployment"""
```

**Capabilities:**
- Generate configs for multiple platforms (cisco, juniper, palo alto, etc.)
- Store generated configs in database
- Track deployment status (pending, running, success, failure)
- Provide rollback mechanism
- Audit trail for all deployments

**Integration Points:**
- Use existing Capirca generators from `capirca/lib/`
- Async processing (Celery or FastAPI Background Tasks)
- Store deployment metadata in `deployments` table

---

### ❌ Data Model & Database (NOT STARTED - HIGH PRIORITY)

**Proposed Schema (from Technical_Deep_Dive_Capirca.md):**

```sql
-- Policies Table
CREATE TABLE policies (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    content TEXT NOT NULL,           -- .pol file content
    version INTEGER DEFAULT 1,
    status VARCHAR(50) DEFAULT 'draft',  -- draft, approved, deployed
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    created_by INTEGER REFERENCES users(id)
);

-- Network Objects Table  
CREATE TABLE network_objects (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE,  -- e.g. INTERNAL_NETS
    addresses TEXT[] NOT NULL,           -- ['10.0.0.0/8', '192.168.0.0/16']
    description TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Service Objects Table
CREATE TABLE service_objects (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE,  -- e.g. WEB_SERVICES
    ports TEXT[] NOT NULL,               -- ['80/tcp', '443/tcp']
    protocols TEXT[] NOT NULL,           -- ['tcp']
    description TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Deployments Table
CREATE TABLE deployments (
    id SERIAL PRIMARY KEY,
    policy_id INTEGER REFERENCES policies(id),
    platform VARCHAR(100) NOT NULL,      -- cisco, juniper, etc.
    target VARCHAR(255) NOT NULL,        -- filter name or target
    status VARCHAR(50) DEFAULT 'pending', -- pending, running, success, failure
    deployed_at TIMESTAMP,
    deployed_by INTEGER REFERENCES users(id),
    output_content TEXT,                  -- generated config
    error_message TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Users Table (optional, for ownership)
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) NOT NULL UNIQUE,
    email VARCHAR(255),
    role VARCHAR(50) DEFAULT 'user',      -- admin, user, viewer
    created_at TIMESTAMP DEFAULT NOW()
);

-- Validation Results Table (optional)
CREATE TABLE validation_results (
    id SERIAL PRIMARY KEY,
    policy_id INTEGER REFERENCES policies(id),
    validation_type VARCHAR(50),          -- syntax, reference, security
    severity VARCHAR(20),                 -- error, warning, info
    message TEXT,
    line_number INTEGER,
    created_at TIMESTAMP DEFAULT NOW()
);
```

**Technology Stack:**
- **Database:** PostgreSQL (or SQLite for dev)
- **ORM:** SQLAlchemy 2.0+
- **Migrations:** Alembic
- **Models:** Pydantic for API validation

**Implementation Steps:**
1. Create `capirca/db/` package
2. Define SQLAlchemy models
3. Create Alembic migrations
4. Add database configuration
5. Connection pooling and session management

---

### ❌ API Layer (NOT STARTED - HIGH PRIORITY)

**Proposed Endpoints (from Technical_Deep_Dive_Capirca.md):**

```python
# Policy Management
GET    /api/policies              # List all policies with filters
POST   /api/policies              # Create new policy
GET    /api/policies/{id}         # Get policy details
PUT    /api/policies/{id}         # Update policy
DELETE /api/policies/{id}         # Delete policy
POST   /api/policies/{id}/validate # Validate policy

# Network Objects
GET    /api/network-objects       # List network objects
POST   /api/network-objects       # Create network object
GET    /api/network-objects/{id}  # Get network object
PUT    /api/network-objects/{id}  # Update network object
DELETE /api/network-objects/{id}  # Delete network object

# Service Objects
GET    /api/service-objects       # List service objects
POST   /api/service-objects       # Create service object
GET    /api/service-objects/{id}  # Get service object
PUT    /api/service-objects/{id}  # Update service object
DELETE /api/service-objects/{id}  # Delete service object

# Deployments
POST   /api/policies/{id}/deploy  # Deploy policy to platform
GET    /api/deployments           # List deployments
GET    /api/deployments/{id}      # Get deployment status
POST   /api/deployments/{id}/rollback # Rollback deployment

# Migration
POST   /api/migration/confluence  # Migrate Confluence HTML to policy
POST   /api/migration/import      # Import existing .pol files
```

**Technology Stack:**
- **Framework:** FastAPI
- **Validation:** Pydantic models
- **Authentication:** JWT or API keys
- **Background Jobs:** Celery or FastAPI Background Tasks
- **Caching:** Redis (optional)

**Pydantic Models Example:**
```python
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class PolicyBase(BaseModel):
    name: str
    description: Optional[str] = None
    content: str

class PolicyCreate(PolicyBase):
    pass

class PolicyUpdate(PolicyBase):
    status: Optional[str] = None

class Policy(PolicyBase):
    id: int
    version: int
    status: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class ValidationError(BaseModel):
    severity: str  # error, warning, info
    message: str
    line_number: Optional[int] = None
    
class ValidationResult(BaseModel):
    is_valid: bool
    errors: List[ValidationError]
```

**Implementation Structure:**
```
capirca/api/
├── __init__.py
├── main.py              # FastAPI app factory
├── config.py            # Settings (pydantic-settings)
├── dependencies.py      # Auth, DB session
├── routers/
│   ├── policies.py      # Policy CRUD + validation
│   ├── network_objects.py
│   ├── service_objects.py
│   ├── deployments.py
│   └── migration.py     # Confluence migration endpoint
└── services/
    ├── validator.py     # PolicyValidator
    ├── generator.py     # Use existing Capirca generators
    └── deployer.py      # DeploymentEngine
```

---

### ❌ GUI (NOT STARTED - LOW PRIORITY)

**Planned for Phase 4-5 (after API is stable)**

**Technology Stack (from Migration Analysis):**
- React with TypeScript
- Material-UI or Ant Design
- Monaco Editor for code editing
- React Query for state management

**Core Features:**
1. **Policy Management**
   - Visual policy editor
   - Syntax highlighting
   - Real-time validation
   - Template-based creation

2. **Object Browser**
   - Network object management
   - Service object management
   - Drag & drop support

3. **Deployment UI**
   - Multi-platform selection
   - Approval workflow
   - Status monitoring
   - Rollback interface

4. **Audit & History**
   - Change tracking
   - Diff viewer
   - User activity log

**Not Started Yet:** Wait for stable API

---

## 5. Recommended Implementation Order

### ✅ Phase 1: COMPLETED
- [x] Confluence parser
- [x] Object extraction
- [x] Policy generation
- [x] Tests and documentation

### ✅ **Phase 2A: Data Model & API Foundation (COMPLETED)**

**Sprint 1:**
- [x] Set up database (SQLite + SQLAlchemy)
- [x] Define all database models
- [x] Set up FastAPI app structure
- [x] Implement basic CRUD for policies

**Sprint 2:**
- [x] Implement CRUD for network_objects and service_objects
- [x] Create Pydantic models for validation
- [x] Set up API testing framework

**Sprint 3:**
- [x] Validation endpoint integration
- [x] Test end-to-end workflows
- [x] Documentation for API usage

### ✅ Phase 2B: Validation Engine (COMPLETED)

**Sprint 4:**
- [x] Implement `PolicyValidator` service
- [x] Add syntax validation (using Capirca parser)
- [x] Add reference validation
- [x] Expose validation endpoint

**Sprint 5:**
- [x] Add security rule validation
- [x] Store validation results in database
- [x] Add validation to policy workflow
- [x] Tests and examples

### 🎯 Phase 3: Deployment Engine (NEXT PRIORITY)

**Sprint 6-7 (Week 6-7):**
- [ ] Implement `DeploymentEngine` service
- [ ] Generate configs for multiple platforms
- [ ] Store deployment metadata
- [ ] Add deployment status tracking

**Sprint 8 (Week 8):**
- [ ] Add rollback functionality
- [ ] Background job processing (Celery)
- [ ] Deployment audit trail
- [ ] Documentation

### 🎯 Phase 4: GUI (Future)
- [ ] React app setup
- [ ] Authentication integration
- [ ] Policy editor component
- [ ] Object management UI
- [ ] Deployment UI
- [ ] User testing and refinement

---

## 6. Technology Stack Summary

| Layer | Technology | Status | Notes |
|-------|-----------|--------|-------|
| **Frontend** | React + TypeScript | ❌ Not started | Phase 4 |
| **API** | FastAPI | ❌ Not started | **Phase 2A (next)** |
| **Business Logic** | Python 3.6+ | ⚠️ Partial | Migration done, validation needed |
| **ORM** | SQLAlchemy 2.0 | ❌ Not started | **Phase 2A (next)** |
| **Database** | PostgreSQL | ❌ Not started | **Phase 2A (next)** |
| **Migrations** | Alembic | ❌ Not started | **Phase 2A (next)** |
| **Background Jobs** | Celery | ❌ Not started | Phase 3 |
| **Caching** | Redis | ❌ Not started | Optional |
| **Testing** | pytest | ✅ Existing | Continue |
| **Capirca Core** | PLY, absl, PyYAML | ✅ Existing | Don't modify |

---

## 7. Decision: What to Start Next?

### Option A: Continue with Phase 2 Validation Engine (Pure Logic)
**Pros:**
- Direct continuation of Phase 1
- Faster validation feedback
- Can work standalone

**Cons:**
- No persistence (results lost)
- No multi-user support
- CLI-only usage
- Will need refactoring when API is added

### Option B: Start with Data Model & API (Foundation) ⭐ **RECOMMENDED**
**Pros:**
- Creates foundation for all future work
- Enables multi-user scenarios
- Validation can be embedded as service
- Unblocks GUI development
- Better architecture (no rework needed)

**Cons:**
- Requires more upfront setup
- Takes longer before visible features

### **Recommendation: Option B - Data Model & API First**

**Rationale:**
1. Phase 1 is complete and stable
2. Validation logic is meaningless without persistence
3. API enables both CLI and GUI consumers
4. Follows standard web application architecture
5. Aligns with Technical Deep Dive and Migration Analysis documents
6. Avoids technical debt and rework

---

## 8. Immediate Action Items

### ✅ Week 1: Foundation Setup (COMPLETED)
1. **Database Setup**
   - [x] Create `capirca/db/` package
   - [x] Define SQLAlchemy models
   - [x] Database initialization

2. **API Skeleton**
   - [x] Create `capirca/api/` package
   - [x] Set up FastAPI app
   - [x] Configure settings (environment variables)
   - [x] Add database session management
   - [x] Create router structure

3. **Documentation**
   - [x] Create planning documents
   - [x] Create PHASE2_IMPLEMENTATION.md
   - [x] Update ARCHITECTURE_STATUS_AND_ROADMAP.md

### ✅ Week 2: Core CRUD Implementation (COMPLETED)
1. **Policy Management**
   - [x] Implement policy CRUD endpoints
   - [x] Add Pydantic models
   - [x] Write API tests
   
2. **Object Management**
   - [x] Network objects CRUD
   - [x] Service objects CRUD
   - [x] Tests

3. **Deployment Management**
   - [x] Deployment record CRUD
   - [x] Deployment endpoints
   - [x] End-to-end test

### ✅ Week 3: Validation Engine (COMPLETED)
1. **Validator Service**
   - [x] Implement PolicyValidator
   - [x] Syntax validation
   - [x] Reference validation
   - [x] Security checks

2. **API Integration**
   - [x] Validation endpoint
   - [x] Store results in DB
   - [x] Return structured errors

---

## 9. Success Metrics

### Phase 2A (Data Model & API) Success Criteria:
- [x] All database tables created
- [x] CRUD operations working for all entities
- [x] API endpoints tested
- [x] Phase 1 migration tool can persist via API (integration ready)
- [x] Documentation complete

### Phase 2B (Validation Engine) Success Criteria:
- [x] Syntax validation catches all parser errors
- [x] Reference validation detects undefined objects
- [x] Security checks find common anti-patterns
- [x] Validation results accessible via API
- [x] Tests and examples provided

**Phase 2 Status: ✅ COMPLETE**

---

## 10. References

- **Technical_Deep_Dive_Capirca.md** - Architecture details, validation & deployment design
- **PHASE1_IMPLEMENTATION.md** - Migration engine implementation
- **PHASE2_IMPLEMENTATION.md** - Validation engine and API foundation (NEW)
- **Capirca_Migration_Analysis_Report.md** - GUI vision, sprint plan, ROI
- **FORCEPOINT_SUMMARY.md** - Example of phased delivery approach

---

## 11. Conclusion

**Current State:**
- Phase 1 (Migration Engine) is complete ✅
- **Phase 2 (Validation Engine & API Foundation) is complete ✅**
- Phase 3 (Deployment Engine) is planned but not implemented ⚠️
- Phase 4 (GUI) is planned but not implemented ❌

**Completed in Phase 2:**
- ✅ SQLAlchemy ORM models and database schema
- ✅ FastAPI REST API with full CRUD operations
- ✅ PolicyValidator service with 3-layer validation
- ✅ Integration points for Phase 1 migration tools
- ✅ Comprehensive test suite
- ✅ Complete documentation

**Recommended Next Step:**
- **Start Phase 3: Deployment Engine** 🎯
- Implement actual deployment execution using Capirca generators
- Add background job processing for long-running deployments
- Implement rollback functionality
- Create audit trail for deployments

**Remaining Timeline:**
- Phase 3: 3 weeks (deployment engine)
- Phase 4: 8+ weeks (GUI)

**Total to working GUI:** ~11+ weeks from now

---

**Next Action:** Begin Phase 3 implementation - Deployment Engine with multi-platform support
