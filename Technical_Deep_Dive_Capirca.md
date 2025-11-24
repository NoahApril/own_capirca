# Technical Deep Dive: Capirca Architecture

## Core Components Analysis

### 1. Policy Parser (policy.py)

**Key Classes:**
- `ParsePolicy`: Main parser class using PLY (Python Lex-Yacc)
- `Term`: Individual firewall rule representation
- `Header`: Policy metadata and target definitions

**Supported Keywords:**
```python
# Required Keywords
ACTIONS = {'accept', 'count', 'deny', 'reject', 'next', 'reject-with-tcp-rst'}
PROTOS_WITH_PORTS = {'tcp', 'udp', 'udplite', 'sctp'}

# Optional Keywords (platform-specific)
OPTIONAL_KEYWORDS = {
    'logging', 'policer', 'qos', 'packet-length', 
    'fragment-offset', 'counter', 'routing-instance'
}
```

### 2. Naming System (naming.py)

**Network Object Handling:**
```python
# Example from NETWORK.net
INTERNAL = RFC1918
RFC1918 = 10.0.0.0/8
          172.16.0.0/12  
          192.168.0.0/16
```

**Service Object Handling:**
```python
# Example from SERVICES.svc
WEB_SERVICES = HTTP HTTPS
HTTP = 80/tcp
HTTPS = 443/tcp
```

### 3. Generator Framework (aclgenerator.py)

**Base Generator Class:**
```python
class ACLGenerator:
    def __init__(self, pol, defs):
        self.policy = pol
        self.definitions = defs
    
    def _BuildTokens(self):
        # Platform-specific token building
    
    def _BuildWarning(self):
        # Platform-specific warnings
```

**Supported Generators:**
- `cisco.py` (48KB) - Cisco IOS/ASA
- `juniper.py` (41KB) - Juniper JunOS
- `paloaltofw.py` (42KB) - Palo Alto PAN-OS
- `iptables.py` (33KB) - Linux iptables
- `gce.py` (24KB) - Google Cloud Engine

## Migration Data Mapping

### Confluence Table Structure → Capirca Policy

**Typische Confluence Tabelle:**
| Regel | Source | Destination | Port | Protocol | Action | Beschreibung |
|-------|--------|-------------|------|----------|--------|-------------|
| Web-Access | 10.0.0.0/8 | 192.168.1.10 | 80,443 | TCP | Allow | Webserver Zugriff |

**Transformiert zu Capirca:**
```pol
header {
  comment:: "Web Access Rules"
  target:: cisco web-access-filter
  target:: juniper web-access-filter
}

term allow-web-access {
  source-address:: INTERNAL_NETS
  destination-address:: WEBSERVERS
  destination-port:: WEB_SERVICES
  protocol:: tcp
  action:: accept
  comment:: "Webserver Zugriff"
}
```

### Network Object Migration

**Confluence Network Groups:**
```
DMZ_NETS: 10.10.0.0/16, 10.11.0.0/16
INTERNAL_NETS: 192.168.0.0/16, 10.0.0.0/8
```

**Capirca .net File:**
```
DMZ_NETS = 10.10.0.0/16    # DMZ Network 1
           10.11.0.0/16    # DMZ Network 2

INTERNAL_NETS = 192.168.0.0/16  # Internal Network
                10.0.0.0/8       # RFC1918 Private
```

### Service Object Migration

**Confluence Service Definitions:**
```
WEB_PORTS: 80/tcp, 443/tcp
DB_PORTS: 3306/tcp, 5432/tcp, 1433/tcp
```

**Capirca .svc File:**
```
WEB_SERVICES = HTTP HTTPS
HTTP = 80/tcp
HTTPS = 443/tcp

DB_SERVICES = MYSQL POSTGRESQL MSSQL
MYSQL = 3306/tcp
POSTGRESQL = 5432/tcp
MSSQL = 1433/tcp
```

## GUI Architecture Design

### Database Schema

```sql
-- Policies Table
CREATE TABLE policies (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    content TEXT NOT NULL,
    version INTEGER DEFAULT 1,
    status VARCHAR(50) DEFAULT 'draft',
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    created_by INTEGER REFERENCES users(id)
);

-- Network Objects Table  
CREATE TABLE network_objects (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE,
    addresses TEXT[] NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Service Objects Table
CREATE TABLE service_objects (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE,
    ports TEXT[] NOT NULL,
    protocols TEXT[] NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Deployments Table
CREATE TABLE deployments (
    id SERIAL PRIMARY KEY,
    policy_id INTEGER REFERENCES policies(id),
    platform VARCHAR(100) NOT NULL,
    target VARCHAR(255) NOT NULL,
    status VARCHAR(50) DEFAULT 'pending',
    deployed_at TIMESTAMP,
    deployed_by INTEGER REFERENCES users(id),
    output_content TEXT
);
```

### API Endpoints

```python
# FastAPI Routes
@app.get("/api/policies")
async def list_policies(status: str = None):
    """List policies with optional status filter"""

@app.post("/api/policies")
async def create_policy(policy: PolicyCreate):
    """Create new policy"""

@app.get("/api/policies/{policy_id}")
async def get_policy(policy_id: int):
    """Get policy details"""

@app.put("/api/policies/{policy_id}")
async def update_policy(policy_id: int, policy: PolicyUpdate):
    """Update existing policy"""

@app.post("/api/policies/{policy_id}/deploy")
async def deploy_policy(policy_id: int, deployment: DeploymentRequest):
    """Deploy policy to target platform"""

@app.get("/api/network-objects")
async def list_network_objects():
    """List all network objects"""

@app.post("/api/network-objects")
async def create_network_object(obj: NetworkObjectCreate):
    """Create new network object"""
```

### Frontend Components

```typescript
// Policy Editor Component
interface PolicyEditorProps {
  policy?: Policy;
  onSave: (policy: Policy) => void;
  onValidate: (policy: Policy) => ValidationResult[];
}

// Network Object Browser
interface NetworkObjectBrowserProps {
  onSelect: (objects: NetworkObject[]) => void;
  multiSelect?: boolean;
}

// Deployment Modal
interface DeploymentModalProps {
  policy: Policy;
  platforms: Platform[];
  onDeploy: (deployment: DeploymentConfig) => void;
}
```

## Implementation Strategy

### Phase 1: Data Migration Engine

```python
class ConfluenceParser:
    def parse_table(self, html_content: str) -> List[FirewallRule]:
        """Parse Confluence HTML table to structured rules"""
        
class CapircaGenerator:
    def generate_policy(self, rules: List[FirewallRule]) -> str:
        """Generate Capirca policy from rules"""
        
class ObjectExtractor:
    def extract_network_objects(self, rules: List[FirewallRule]) -> Dict[str, List[str]]:
        """Extract unique network objects from rules"""
        
    def extract_service_objects(self, rules: List[FirewallRule]) -> Dict[str, ServiceDef]:
        """Extract unique service objects from rules"""
```

### Phase 2: Validation Engine

```python
class PolicyValidator:
    def validate_syntax(self, policy_content: str) -> List[ValidationError]:
        """Validate Capirca policy syntax"""
        
    def validate_references(self, policy_content: str, definitions: Definitions) -> List[ValidationError]:
        """Validate object references exist in definitions"""
        
    def validate_security(self, policy_content: str) -> List[SecurityWarning]:
        """Check for security anti-patterns"""
```

### Phase 3: Deployment Engine

```python
class DeploymentEngine:
    def generate_configs(self, policy_id: int) -> Dict[str, str]:
        """Generate platform-specific configurations"""
        
    def deploy_to_platform(self, platform: str, config: str, target: str) -> DeploymentResult:
        """Deploy configuration to target platform"""
        
    def rollback_deployment(self, deployment_id: int) -> RollbackResult:
        """Rollback failed deployment"""
```

## Performance Considerations

### Caching Strategy
- **Policy Content**: Redis cache for compiled policies
- **Object Definitions**: Memory cache for network/service objects
- **Generated Configs**: File-based cache for platform outputs

### Scalability
- **Async Processing**: Celery for long-running deployments
- **Database Indexing**: Proper indexes for policy searches
- **Pagination**: Large policy sets with cursor-based pagination

### Security
- **RBAC**: Role-based access control for policy operations
- **Audit Trail**: Complete audit logging for all changes
- **Encryption**: Sensitive data encryption at rest

## Testing Strategy

### Unit Tests
- Policy parser validation
- Object reference resolution
- Generator output verification

### Integration Tests
- End-to-end policy deployment
- Multi-platform generation
- Confluence migration accuracy

### Performance Tests
- Large policy compilation
- Concurrent user operations
- Deployment throughput

This technical deep dive provides the foundation for implementing a comprehensive GUI-based firewall policy management system using Capirca as the core engine.