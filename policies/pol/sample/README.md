# Forcepoint NGFW Sample Policies

This directory contains sample Capirca policies for Forcepoint NGFW deployment.

## Sample Policies

### 1. Basic Web Access (`web-access.pol`)
Simple policy allowing HTTP/HTTPS access from internal network to DMZ web servers.

### 2. Three-Tier Application (`three-tier.pol`)
Security policy for three-tier web application with web, application, and database tiers.

### 3. Guest Network Isolation (`guest-isolation.pol`)
Policy to isolate guest network from internal corporate resources.

### 4. PCI DSS Compliance (`pci-dss.pol`)
Compliance-focused policy for payment card industry security standards.

### 5. Malware Response (`malware-response.pol`)
Incident response policy for malware outbreak containment.

## Usage

Generate Forcepoint configurations:

```bash
# Generate all policies
python capirca/aclgen.py --definitions def/ --output_dir output/ policies/pol/sample/*.pol

# Generate specific policy
python capirca/aclgen.py --definitions def/ --output_dir output/ policies/pol/sample/web-access.pol
```

Deploy using REST API:

```bash
# Deploy web access policy
curl -X POST "https://smc.example.com:8082/api/v6/policy" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $API_TOKEN" \
  -d @output/web-access.forcepoint.json
```

## Network Definitions

See `def/networks.def` for network object definitions used by sample policies.

## Service Definitions

See `def/services.def` for service object definitions used by sample policies.