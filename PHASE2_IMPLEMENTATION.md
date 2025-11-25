# Phase 2 Implementation: Validation Engine & API Foundation

## Overview

Phase 2 extends the Capirca migration architecture with:
- **Data Model & Database Layer**: SQLAlchemy ORM models and database schema
- **API Layer**: FastAPI REST endpoints for policy, object, and deployment management
- **Validation Engine**: Multi-layer policy validation (syntax, references, security)

This phase provides the foundation for Phase 3 (Deployment Engine) and Phase 4 (GUI).

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    FastAPI REST API                          │
│  /api/policies • /api/network-objects • /api/deployments    │
└───────────────────────────┬─────────────────────────────────┘
                            │
┌───────────────────────────┴─────────────────────────────────┐
│                   Business Services                          │
│  PolicyValidator • DeploymentEngine (stub)                   │
└───────────────────────────┬─────────────────────────────────┘
                            │
┌───────────────────────────┴─────────────────────────────────┐
│                SQLAlchemy ORM + Database                     │
│  Policy • NetworkObject • ServiceObject • Deployment         │
└─────────────────────────────────────────────────────────────┘
```

---

## Components

### 1. Database Models (`capirca/db/models.py`)

SQLAlchemy ORM models for:
- **Policy**: Stores .pol file content, version, status (draft/approved/deployed)
- **NetworkObject**: Reusable network address definitions
- **ServiceObject**: Reusable port/protocol definitions
- **Deployment**: Tracks deployments to platforms
- **ValidationResult**: Stores validation errors/warnings
- **User**: Optional user management for ownership/audit

### 2. API Layer (`capirca/api/`)

FastAPI application with routers:

#### Policies (`/api/policies`)
- `GET /api/policies` - List policies with filtering
- `POST /api/policies` - Create new policy
- `GET /api/policies/{id}` - Get policy details
- `PUT /api/policies/{id}` - Update policy
- `DELETE /api/policies/{id}` - Delete policy
- `POST /api/policies/{id}/validate` - Validate policy

#### Network Objects (`/api/network-objects`)
- `GET /api/network-objects` - List network objects
- `POST /api/network-objects` - Create network object
- `GET /api/network-objects/{id}` - Get details
- `PUT /api/network-objects/{id}` - Update
- `DELETE /api/network-objects/{id}` - Delete

#### Service Objects (`/api/service-objects`)
- Similar CRUD operations for service objects

#### Deployments (`/api/deployments`)
- `GET /api/deployments` - List deployments
- `POST /api/deployments` - Create deployment record
- `GET /api/deployments/{id}` - Get deployment status
- `POST /api/deployments/{id}/rollback` - Rollback (stub for Phase 3)

### 3. Validation Engine (`capirca/api/services/validator.py`)

The `PolicyValidator` service implements three validation layers:

#### Syntax Validation
- Uses Capirca's PLY parser (`policy.ParsePolicy`)
- Detects syntax errors in policy files
- Reports line numbers and error details

```python
validator = PolicyValidator(definitions=naming_obj)
errors = validator.validate_syntax(policy_content)
```

#### Reference Validation
- Checks if all referenced network/service tokens exist
- Validates against loaded definitions
- Catches `UndefinedAddressError` from Capirca parser

#### Security Validation
- Detects security anti-patterns:
  - Any → any accept rules (overly permissive)
  - Missing action directives
  - Policies without explicit deny rules
- Extensible for custom security rules

---

## Usage Examples

### 1. Initialize Database

```python
from capirca.db.init_db import init_db
init_db()
```

### 2. Create a Policy via API

```python
import requests

policy = {
    "name": "web-firewall",
    "description": "Allow web traffic",
    "content": """
header {
  target:: juniper web-filter
}
term allow-http {
  destination-port:: HTTP HTTPS
  protocol:: tcp
  action:: accept
}
"""
}

response = requests.post("http://localhost:8000/api/policies", json=policy)
policy_id = response.json()["id"]
```

### 3. Validate a Policy

```python
response = requests.post(f"http://localhost:8000/api/policies/{policy_id}/validate")
result = response.json()

if result["is_valid"]:
    print("✅ Policy is valid")
else:
    for error in result["errors"]:
        print(f"{error['severity']}: {error['message']}")
```

### 4. Create Network Objects

```python
network_obj = {
    "name": "INTERNAL_NETS",
    "addresses": ["10.0.0.0/8", "192.168.0.0/16"],
    "description": "RFC 1918 networks"
}

response = requests.post("http://localhost:8000/api/network-objects", json=network_obj)
```

### 5. Create Deployment Record

```python
deployment = {
    "policy_id": policy_id,
    "platform": "juniper",
    "target": "web-filter",
    "status": "pending"
}

response = requests.post("http://localhost:8000/api/deployments", json=deployment)
```

---

## Running the API Server

### Development Mode

```bash
# Install dependencies
pip install -r requirements.txt

# Initialize database
python -m capirca.db.init_db

# Start API server
python -m uvicorn capirca.api.main:app --reload
```

The API will be available at:
- **API**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs
- **OpenAPI JSON**: http://localhost:8000/openapi.json

### Production Mode

```bash
# Run with Gunicorn + Uvicorn workers
gunicorn capirca.api.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

---

## Configuration

Set environment variables to configure the API:

```bash
export CAPIRCA_DATABASE_URL="postgresql://user:pass@localhost/capirca"
export CAPIRCA_NAMING_DEFINITIONS_DIRECTORY="./def"
```

Or use a `.env` file:

```env
CAPIRCA_DATABASE_URL=sqlite+pysqlite:///capirca_phase2.db
CAPIRCA_NAMING_DEFINITIONS_DIRECTORY=./def
```

---

## Testing

Run Phase 2 tests:

```bash
# Install test dependencies
pip install pytest pytest-cov

# Run all Phase 2 tests
pytest tests/api/ -v

# Run with coverage
pytest tests/api/ --cov=capirca.api --cov=capirca.db --cov-report=html
```

### Test Coverage

- API endpoints (policies, objects, deployments)
- Database CRUD operations
- Validation engine (syntax, references, security)
- Error handling and edge cases

---

## Integration with Phase 1 (Migration Engine)

Phase 2 can be integrated with the Phase 1 migration tool to persist migrated policies:

```python
from capirca.utils.migration import ConfluenceParser, ObjectExtractor, CapircaGenerator
from capirca.db import models
from capirca.db.base import session_scope

# Phase 1: Parse and generate
parser = ConfluenceParser()
rules = parser.parse_table(html_content)

extractor = ObjectExtractor()
network_objects = extractor.extract_network_objects(rules)
service_objects = extractor.extract_service_objects(rules)

generator = CapircaGenerator(network_objects, service_objects)
policy_content = generator.generate_policy(rules, policy_name="migrated-policy")

# Phase 2: Persist to database
with session_scope() as db:
    # Store policy
    policy = models.Policy(
        name="migrated-policy",
        description="Migrated from Confluence",
        content=policy_content,
        status="draft"
    )
    db.add(policy)
    
    # Store network objects
    for name, addresses in network_objects.items():
        net_obj = models.NetworkObject(name=name, addresses=addresses)
        db.add(net_obj)
    
    # Store service objects
    for name, service_def in service_objects.items():
        svc_obj = models.ServiceObject(
            name=name,
            ports=service_def.ports,
            protocols=service_def.protocols
        )
        db.add(svc_obj)
```

---

## API Documentation

### Pydantic Models

All API requests/responses use Pydantic models for validation:

- `PolicyCreate` / `PolicyUpdate` / `Policy`
- `NetworkObjectCreate` / `NetworkObjectUpdate` / `NetworkObject`
- `ServiceObjectCreate` / `ServiceObjectUpdate` / `ServiceObject`
- `DeploymentCreate` / `Deployment`
- `ValidationError` / `ValidationResult`

### Error Responses

Standard HTTP status codes:
- `200 OK` - Success
- `201 Created` - Resource created
- `204 No Content` - Deleted successfully
- `400 Bad Request` - Invalid input
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server error

---

## Database Schema

### Policies Table
```sql
CREATE TABLE policies (
    id INTEGER PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    content TEXT NOT NULL,
    version INTEGER DEFAULT 1,
    status VARCHAR(50) DEFAULT 'draft',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by INTEGER
);
```

### Network Objects Table
```sql
CREATE TABLE network_objects (
    id INTEGER PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL,
    addresses JSON NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Service Objects Table
```sql
CREATE TABLE service_objects (
    id INTEGER PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL,
    ports JSON NOT NULL,
    protocols JSON NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Deployments Table
```sql
CREATE TABLE deployments (
    id INTEGER PRIMARY KEY,
    policy_id INTEGER NOT NULL,
    platform VARCHAR(100) NOT NULL,
    target VARCHAR(255) NOT NULL,
    status VARCHAR(50) DEFAULT 'pending',
    deployed_at TIMESTAMP,
    deployed_by INTEGER,
    output_content TEXT,
    error_message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (policy_id) REFERENCES policies(id)
);
```

---

## Next Steps (Phase 3)

Phase 3 will implement the **Deployment Engine**:
- Actual deployment execution using Capirca generators
- Background job processing (Celery or FastAPI background tasks)
- Rollback functionality
- Deployment audit trail
- Multi-platform support (Juniper, Cisco, Palo Alto, etc.)

---

## Files Created

### Database Layer
- `capirca/db/__init__.py` - Package init
- `capirca/db/base.py` - SQLAlchemy configuration
- `capirca/db/models.py` - ORM models
- `capirca/db/init_db.py` - Database initialization script

### API Layer
- `capirca/api/__init__.py` - Package init
- `capirca/api/main.py` - FastAPI application
- `capirca/api/config.py` - Configuration settings
- `capirca/api/models/__init__.py` - Pydantic models package
- `capirca/api/models/schemas.py` - Pydantic schemas
- `capirca/api/routers/__init__.py` - Routers package
- `capirca/api/routers/policies.py` - Policy endpoints
- `capirca/api/routers/network_objects.py` - Network object endpoints
- `capirca/api/routers/service_objects.py` - Service object endpoints
- `capirca/api/routers/deployments.py` - Deployment endpoints

### Services Layer
- `capirca/api/services/__init__.py` - Services package
- `capirca/api/services/validator.py` - PolicyValidator service

### Tests
- `tests/api/__init__.py` - Test package
- `tests/api/test_phase2_api.py` - API endpoint tests
- `tests/api/test_validator.py` - Validator tests

### Examples
- `examples/phase2_example.py` - Complete usage example

### Documentation
- `PHASE2_IMPLEMENTATION.md` - This file

---

## Summary

Phase 2 successfully implements:
- ✅ Database schema with SQLAlchemy ORM
- ✅ FastAPI REST API with full CRUD operations
- ✅ Multi-layer policy validation engine
- ✅ Integration points for Phase 1 migration tools
- ✅ Comprehensive test suite
- ✅ Example scripts and documentation

**Status**: Phase 2 Complete ✅  
**Next**: Phase 3 - Deployment Engine
