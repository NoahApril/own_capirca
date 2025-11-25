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
│                        ❌ NOT STARTED                            │
└────────────────────────────┬────────────────────────────────────┘
                             │
┌────────────────────────────┴────────────────────────────────────┐
│                  Layer 3: Business Logic                         │
│  Validation Engine • Deployment Engine • Policy Management      │
│              ⚠️ PARTIALLY PLANNED (Phase 2 & 3)                │
└────────────────────────────┬────────────────────────────────────┘
                             │
┌────────────────────────────┴────────────────────────────────────┐
│                    Layer 2: Data Layer                           │
│  Database (PostgreSQL) • ORM (SQLAlchemy) • Migrations (Alembic) │
│                        ❌ NOT STARTED                            │
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
| **Validation Engine** | ❌ Not Started | - | - | ⚠️ Planned | **HIGH** |
| **Data Model** | ❌ Not Started | - | - | ⚠️ Schema only | **HIGH** |
| **API Layer** | ❌ Not Started | - | - | ⚠️ Endpoints only | **HIGH** |
| **Deployment Engine** | ❌ Not Started | - | - | ⚠️ Planned | MEDIUM |
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

### ⚠️ Phase 2: Validation Engine (PLANNED)

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

**Planned Implementation:**
- Embed in API as service module
- Expose via `/api/policies/{id}/validate`
- Support both real-time and batch validation
- Return structured validation results (errors, warnings, info)

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

### 🎯 **Phase 2A: Data Model & API Foundation (CURRENT PRIORITY)**

**Sprint 1 (Week 1):**
- [ ] Set up database (PostgreSQL + SQLAlchemy + Alembic)
- [ ] Define all database models
- [ ] Create initial migrations
- [ ] Set up FastAPI app structure
- [ ] Implement basic CRUD for policies

**Sprint 2 (Week 2):**
- [ ] Implement CRUD for network_objects and service_objects
- [ ] Add authentication/authorization
- [ ] Create Pydantic models for validation
- [ ] Set up API testing framework

**Sprint 3 (Week 3):**
- [ ] Connect Phase 1 migration tool to API
- [ ] Add migration endpoint (`POST /api/migration/confluence`)
- [ ] Test end-to-end: Confluence → API → Database
- [ ] Documentation for API usage

### 🎯 Phase 2B: Validation Engine

**Sprint 4 (Week 4):**
- [ ] Implement `PolicyValidator` service
- [ ] Add syntax validation (using Capirca parser)
- [ ] Add reference validation
- [ ] Expose validation endpoint

**Sprint 5 (Week 5):**
- [ ] Add security rule validation
- [ ] Store validation results in database
- [ ] Add validation to policy create/update workflow
- [ ] CLI tool for validation

### 🎯 Phase 3: Deployment Engine

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

### Week 1: Foundation Setup
1. **Database Setup**
   - [ ] Install PostgreSQL
   - [ ] Create `capirca/db/` package
   - [ ] Define SQLAlchemy models
   - [ ] Set up Alembic
   - [ ] Create initial migrations

2. **API Skeleton**
   - [ ] Create `capirca/api/` package
   - [ ] Set up FastAPI app
   - [ ] Configure settings (environment variables)
   - [ ] Add database session management
   - [ ] Create router structure

3. **Documentation**
   - [x] Create this planning document
   - [ ] Update README with architecture section
   - [ ] Document API design decisions

### Week 2: Core CRUD Implementation
1. **Policy Management**
   - [ ] Implement policy CRUD endpoints
   - [ ] Add Pydantic models
   - [ ] Write API tests
   
2. **Object Management**
   - [ ] Network objects CRUD
   - [ ] Service objects CRUD
   - [ ] Tests

3. **Migration Integration**
   - [ ] Connect Phase 1 tools to API
   - [ ] Add migration endpoint
   - [ ] End-to-end test

### Week 3: Validation Engine
1. **Validator Service**
   - [ ] Implement PolicyValidator
   - [ ] Syntax validation
   - [ ] Reference validation
   - [ ] Security checks

2. **API Integration**
   - [ ] Validation endpoint
   - [ ] Store results in DB
   - [ ] Return structured errors

---

## 9. Success Metrics

### Phase 2A (Data Model & API) Success Criteria:
- [ ] All database tables created with migrations
- [ ] CRUD operations working for all entities
- [ ] API endpoints tested with 80%+ coverage
- [ ] Phase 1 migration tool can persist via API
- [ ] Documentation complete

### Phase 2B (Validation Engine) Success Criteria:
- [ ] Syntax validation catches all parser errors
- [ ] Reference validation detects undefined objects
- [ ] Security checks find common anti-patterns
- [ ] Validation results accessible via API
- [ ] Performance: validate 1000-line policy in <5s

---

## 10. References

- **Technical_Deep_Dive_Capirca.md** - Architecture details, validation & deployment design
- **PHASE1_IMPLEMENTATION.md** - Migration engine implementation
- **Capirca_Migration_Analysis_Report.md** - GUI vision, sprint plan, ROI
- **FORCEPOINT_SUMMARY.md** - Example of phased delivery approach

---

## 11. Conclusion

**Current State:**
- Phase 1 (Migration Engine) is complete ✅
- All other components are planned but not implemented ❌

**Recommended Next Step:**
- **Start Phase 2A: Data Model & API Foundation** 🎯
- Implement database models and FastAPI skeleton
- Embed validation engine as part of API services
- This creates a solid foundation for all future work

**Timeline:**
- Phase 2A: 3 weeks (data model + API)
- Phase 2B: 2 weeks (validation engine)
- Phase 3: 3 weeks (deployment engine)
- Phase 4: 8+ weeks (GUI)

**Total to working GUI:** ~16+ weeks from start of Phase 2A

---

**Next Action:** Confirm technology stack and begin Phase 2A Sprint 1 (Database + API setup)
