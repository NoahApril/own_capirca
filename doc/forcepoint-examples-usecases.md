# Forcepoint REST API Examples and Use Cases

**Target Audience:** Network Engineers, Security Architects, DevOps Engineers  
**Scope**: Practical examples for common Forcepoint NGFW deployment scenarios

---

## Table of Contents

1. [Basic Examples](#basic-examples)
2. [Network Segmentation](#network-segmentation)
3. [Application Security](#application-security)
4. [Remote Access VPN](#remote-access-vpn)
5. [Multi-Site Deployment](#multi-site-deployment)
6. [Compliance and Auditing](#compliance-and-auditing)
7. [Incident Response](#incident-response)
8. [Cloud Integration](#cloud-integration)
9. [Automation Scripts](#automation-scripts)

---

## Basic Examples

### Example 1: Simple Web Access Policy

**Scenario**: Allow internal users to access web servers in DMZ

**Capirca Policy** (`web-access.pol`):
```pol
header {
  comment:: "Basic Web Access Policy"
  target:: forcepoint web-access inet json
}

term allow-http {
  comment:: "Allow HTTP traffic to web servers"
  source-address:: INTERNAL_USERS
  destination-address:: DMZ_WEBSERVERS
  destination-port:: HTTP
  protocol:: tcp
  action:: accept
  logging:: true
}

term allow-https {
  comment:: "Allow HTTPS traffic to web servers"
  source-address:: INTERNAL_USERS
  destination-address:: DMZ_WEBSERVERS
  destination-port:: HTTPS
  protocol:: tcp
  action:: accept
  logging:: true
}

term deny-web {
  comment:: "Deny other web traffic"
  source-address:: INTERNAL_USERS
  destination-address:: DMZ_WEBSERVERS
  destination-port:: WEB_PORTS
  protocol:: tcp
  action:: deny
  logging:: true
}

term deny-all {
  comment:: "Default deny all"
  action:: deny
  logging:: true
}
```

**Network Definitions** (`def/networks.def`):
```
INTERNAL_USERS = 10.0.0.0/8
DMZ_WEBSERVERS = 192.168.100.0/24
```

**Service Definitions** (`def/services.def`):
```
HTTP = 80/tcp
HTTPS = 443/tcp
WEB_PORTS = 80-443/tcp
```

**Generated JSON**:
```json
{
  "policy": {
    "name": "web-access",
    "comment": "Basic Web Access Policy",
    "rules": [
      {
        "name": "allow-http",
        "comment": "Allow HTTP traffic to web servers",
        "sources": {"src": [{"name": "INTERNAL_USERS", "type": "network"}]},
        "destinations": {"dst": [{"name": "DMZ_WEBSERVERS", "type": "network"}]},
        "services": {"service": [{"name": "HTTP", "type": "tcp_service"}]},
        "action": {"action": "allow"},
        "options": {"log_level": "stored"}
      },
      {
        "name": "allow-https",
        "comment": "Allow HTTPS traffic to web servers",
        "sources": {"src": [{"name": "INTERNAL_USERS", "type": "network"}]},
        "destinations": {"dst": [{"name": "DMZ_WEBSERVERS", "type": "network"}]},
        "services": {"service": [{"name": "HTTPS", "type": "tcp_service"}]},
        "action": {"action": "allow"},
        "options": {"log_level": "stored"}
      }
    ]
  }
}
```

### Example 2: DNS and DHCP Services

**Scenario**: Allow DNS queries and DHCP traffic

**Capirca Policy** (`infrastructure.pol`):
```pol
header {
  comment:: "Infrastructure Services Policy"
  target:: forcepoint infrastructure inet json
}

term allow-dns-queries {
  comment:: "Allow DNS queries from internal network"
  source-address:: INTERNAL_NET
  destination-address:: DNS_SERVERS
  destination-port:: DNS
  protocol:: udp
  action:: accept
  logging:: false
}

term allow-dns-tcp {
  comment:: "Allow DNS over TCP for large responses"
  source-address:: INTERNAL_NET
  destination-address:: DNS_SERVERS
  destination-port:: DNS
  protocol:: tcp
  action:: accept
  logging:: false
}

term allow-dhcp {
  comment:: "Allow DHCP traffic"
  source-address:: ANY
  destination-address:: DHCP_SERVERS
  destination-port:: DHCP_SERVER
  protocol:: udp
  action:: accept
  logging:: false
}

term deny-all {
  comment:: "Deny all other traffic"
  action:: deny
  logging:: true
}
```

**Service Definitions**:
```
DNS = 53/udp
DHCP_SERVER = 67/udp
```

---

## Network Segmentation

### Example 3: Three-Tier Application Security

**Scenario**: Secure three-tier web application with web, application, and database tiers

**Capirca Policy** (`three-tier.pol`):
```pol
header {
  comment:: "Three-Tier Application Security"
  target:: forcepoint three-tier-app inet json
}

# Web Tier Rules
term web-to-app {
  comment:: "Allow web servers to application servers"
  source-address:: WEB_TIER
  destination-address:: APP_TIER
  destination-port:: APP_PORTS
  protocol:: tcp
  action:: accept
  logging:: true
}

# Application Tier Rules
term app-to-db {
  comment:: "Allow application servers to database"
  source-address:: APP_TIER
  destination-address:: DB_TIER
  destination-port:: DB_PORTS
  protocol:: tcp
  action:: accept
  logging:: true
}

term app-to-web {
  comment:: "Allow app servers to web servers"
  source-address:: APP_TIER
  destination-address:: WEB_TIER
  destination-port:: HTTP HTTPS
  protocol:: tcp
  action:: accept
  logging:: true
}

# Database Tier Rules
term db-to-app {
  comment:: "Allow database responses to app servers"
  source-address:: DB_TIER
  destination-address:: APP_TIER
  destination-port:: DB_PORTS
  protocol:: tcp
  action:: accept
  logging:: true
}

# Management Access
term mgmt-access {
  comment:: "Allow management access from ops network"
  source-address:: OPS_NETWORK
  destination-address:: WEB_TIER APP_TIER DB_TIER
  destination-port:: SSH HTTPS
  protocol:: tcp
  action:: accept
  logging:: true
}

# Deny Rules
term deny-cross-tier {
  comment:: "Deny direct cross-tier access"
  source-address:: WEB_TIER
  destination-address:: DB_TIER
  action:: deny
  logging:: true
}

term deny-all {
  comment:: "Default deny all"
  action:: deny
  logging:: true
}
```

**Network Definitions**:
```
WEB_TIER = 10.1.0.0/24
APP_TIER = 10.2.0.0/24
DB_TIER = 10.3.0.0/24
OPS_NETWORK = 192.168.200.0/24

APP_PORTS = 8080-8090/tcp
DB_PORTS = 3306/tcp
SSH = 22/tcp
```

### Example 4: Guest Network Isolation

**Scenario**: Isolate guest network from internal corporate network

**Capirca Policy** (`guest-isolation.pol`):
```pol
header {
  comment:: "Guest Network Isolation Policy"
  target:: forcepoint guest-isolation inet json
}

term guest-dns {
  comment:: "Allow DNS for guest users"
  source-address:: GUEST_NETWORK
  destination-address:: DNS_SERVERS
  destination-port:: DNS
  protocol:: udp
  action:: accept
  logging:: false
}

term guest-dhcp {
  comment:: "Allow DHCP for guest users"
  source-address:: GUEST_NETWORK
  destination-address:: DHCP_SERVERS
  destination-port:: DHCP_CLIENT
  protocol:: udp
  action:: accept
  logging:: false
}

term guest-web {
  comment:: "Allow HTTP/HTTPS to internet"
  source-address:: GUEST_NETWORK
  destination-address:: ANY
  destination-port:: HTTP HTTPS
  protocol:: tcp
  action:: accept
  logging:: true
}

term deny-guest-to-corp {
  comment:: "Deny guest access to corporate network"
  source-address:: GUEST_NETWORK
  destination-address:: CORPORATE_NETWORKS
  action:: deny
  logging:: true
  forcepoint-action:: blacklist
}

term deny-all {
  comment:: "Default deny all"
  action:: deny
  logging:: true
}
```

---

## Application Security

### Example 5: API Gateway Protection

**Scenario**: Protect API gateway with rate limiting and access control

**Capirca Policy** (`api-gateway.pol`):
```pol
header {
  comment:: "API Gateway Security Policy"
  target:: forcepoint api-gateway inet json
}

term allow-api-https {
  comment:: "Allow HTTPS API access from trusted sources"
  source-address:: API_CLIENTS
  destination-address:: API_GATEWAY
  destination-port:: HTTPS
  protocol:: tcp
  action:: accept
  logging:: true
  forcepoint-log-level:: essential
}

term allow-api-mgmt {
  comment:: "Allow API management from ops network"
  source-address:: OPS_NETWORK
  destination-address:: API_GATEWAY
  destination-port:: API_MGMT_PORTS
  protocol:: tcp
  action:: accept
  logging:: true
  forcepoint-log-level:: essential
}

term rate-limit-api {
  comment:: "Rate limit suspicious API clients"
  source-address:: SUSPICIOUS_CLIENTS
  destination-address:: API_GATEWAY
  destination-port:: HTTPS
  protocol:: tcp
  action:: deny
  logging:: true
  forcepoint-action:: blacklist
  forcepoint-log-level:: alert
}

term deny-api-abuse {
  comment:: "Deny known API abusers"
  source-address:: API_ABUSERS
  destination-address:: API_GATEWAY
  action:: deny
  logging:: true
  forcepoint-action:: blacklist
}

term deny-all {
  comment:: "Default deny all"
  action:: deny
  logging:: true
}
```

**Service Definitions**:
```
API_MGMT_PORTS = 8443/tcp
```

### Example 6: Database Access Control

**Scenario**: Granular database access control with audit logging

**Capirca Policy** (`database-access.pol`):
```pol
header {
  comment:: "Database Access Control Policy"
  target:: forcepoint database-access inet json
}

term app-db-primary {
  comment:: "Application access to primary database"
  source-address:: APP_SERVERS
  destination-address:: DB_PRIMARY
  destination-port:: MYSQL_POSTGRES
  protocol:: tcp
  action:: accept
  logging:: true
  forcepoint-log-level:: essential
}

term app-db-replica {
  comment:: "Application read access to replica database"
  source-address:: APP_SERVERS
  destination-address:: DB_REPLICA
  destination-port:: MYSQL_POSTGRES
  protocol:: tcp
  action:: accept
  logging:: true
}

term db-backup {
  comment:: "Database backup access from backup server"
  source-address:: BACKUP_SERVER
  destination-address:: DB_PRIMARY DB_REPLICA
  destination-port:: MYSQL_POSTGRES
  protocol:: tcp
  action:: accept
  logging:: true
  forcepoint-log-level:: essential
}

term db-mgmt {
  comment:: "Database management from DBA network"
  source-address:: DBA_NETWORK
  destination-address:: DB_PRIMARY DB_REPLICA
  destination-port:: DB_MGMT_PORTS
  protocol:: tcp
  action:: accept
  logging:: true
  forcepoint-log-level:: essential
}

term deny-unauthorized-db {
  comment:: "Deny unauthorized database access"
  source-address:: ANY
  destination-address:: DB_PRIMARY DB_REPLICA
  destination-port:: DATABASE_PORTS
  action:: deny
  logging:: true
  forcepoint-action:: blacklist
}

term deny-all {
  comment:: "Default deny all"
  action:: deny
  logging:: true
}
```

**Service Definitions**:
```
MYSQL_POSTGRES = 3306/tcp
DB_MGMT_PORTS = 3306-3307/tcp
DATABASE_PORTS = 3306-3307/tcp
```

---

## Remote Access VPN

### Example 7: VPN Client Access

**Scenario**: Control VPN client access to corporate resources

**Capirca Policy** (`vpn-access.pol`):
```pol
header {
  comment:: "VPN Client Access Policy"
  target:: forcepoint vpn-access inet json
}

term vpn-dns {
  comment:: "Allow DNS queries for VPN clients"
  source-address:: VPN_CLIENTS
  destination-address:: DNS_SERVERS
  destination-port:: DNS
  protocol:: udp
  action:: accept
  logging:: false
}

term vpn-corp-apps {
  comment:: "Allow access to corporate applications"
  source-address:: VPN_CLIENTS
  destination-address:: CORPORATE_APPS
  destination-port:: CORP_APP_PORTS
  protocol:: tcp
  action:: accept
  logging:: true
}

term vpn-file-share {
  comment:: "Allow file server access"
  source-address:: VPN_CLIENTS
  destination-address:: FILE_SERVERS
  destination-port:: SMB FTP
  protocol:: tcp
  action:: accept
  logging:: true
}

term vpn-email {
  comment:: "Allow email access"
  source-address:: VPN_CLIENTS
  destination-address:: MAIL_SERVERS
  destination-port:: SMTP IMAPS
  protocol:: tcp
  action:: accept
  logging:: true
}

term deny-vpn-to-dmz {
  comment:: "Deny VPN access to DMZ"
  source-address:: VPN_CLIENTS
  destination-address:: DMZ_NETWORKS
  action:: deny
  logging:: true
}

term deny-all {
  comment:: "Default deny all"
  action:: deny
  logging:: true
}
```

**Service Definitions**:
```
SMB = 445/tcp
FTP = 21/tcp
SMTP = 25/tcp
IMAPS = 993/tcp
CORP_APP_PORTS = 8080-8090/tcp
```

---

## Multi-Site Deployment

### Example 8: Site-to-Site VPN

**Scenario**: Secure communication between multiple sites

**Capirca Policy** (`site-to-site.pol`):
```pol
header {
  comment:: "Site-to-Site VPN Policy"
  target:: forcepoint site-to-site inet json
}

term site1-to-site2 {
  comment:: "Allow Site 1 to Site 2 communication"
  source-address:: SITE1_NETWORKS
  destination-address:: SITE2_NETWORKS
  destination-port:: SITE2_SERVICES
  protocol:: tcp udp
  action:: accept
  logging:: true
}

term site2-to-site1 {
  comment:: "Allow Site 2 to Site 1 communication"
  source-address:: SITE2_NETWORKS
  destination-address:: SITE1_NETWORKS
  destination-port:: SITE1_SERVICES
  protocol:: tcp udp
  action:: accept
  logging:: true
}

term site1-to-datacenter {
  comment:: "Allow Site 1 to Datacenter"
  source-address:: SITE1_NETWORKS
  destination-address:: DATACENTER_NETWORKS
  destination-port:: DATACENTER_SERVICES
  protocol:: tcp udp
  action:: accept
  logging:: true
}

term site2-to-datacenter {
  comment:: "Allow Site 2 to Datacenter"
  source-address:: SITE2_NETWORKS
  destination-address:: DATACENTER_NETWORKS
  destination-port:: DATACENTER_SERVICES
  protocol:: tcp udp
  action:: accept
  logging:: true
}

term deny-all {
  comment:: "Default deny all"
  action:: deny
  logging:: true
}
```

---

## Compliance and Auditing

### Example 9: PCI DSS Compliance

**Scenario**: PCI DSS compliant firewall rules

**Capirca Policy** (`pci-dss.pol`):
```pol
header {
  comment:: "PCI DSS Compliance Policy"
  target:: forcepoint pci-dss inet json
}

term pci-card-data {
  comment:: "Allow payment processing from authorized terminals"
  source-address:: POS_TERMINALS
  destination-address:: PAYMENT_GATEWAY
  destination-port:: PAYMENT_PORTS
  protocol:: tcp
  action:: accept
  logging:: true
  forcepoint-log-level:: essential
  forcepoint-inspection:: enabled
}

term pci-monitoring {
  comment:: "Allow security monitoring"
  source-address:: SIEM_NETWORK
  destination-address:: CARDHOLDER_ENV
  destination-port:: MONITORING_PORTS
  protocol:: tcp udp
  action:: accept
  logging:: true
  forcepoint-log-level:: essential
}

term deny-outbound-from-cardholder {
  comment:: "Deny outbound from cardholder environment"
  source-address:: CARDHOLDER_ENV
  destination-address:: ANY
  action:: deny
  logging:: true
  forcepoint-log-level:: essential
}

term deny-inbound-to-cardholder {
  comment:: "Deny inbound to cardholder environment"
  source-address:: ANY
  destination-address:: CARDHOLDER_ENV
  action:: deny
  logging:: true
  forcepoint-log-level:: essential
}

term deny-all {
  comment:: "Default deny all"
  action:: deny
  logging:: true
  forcepoint-log-level:: essential
}
```

### Example 10: HIPAA Compliance

**Scenario**: HIPAA compliant healthcare network security

**Capirca Policy** (`hipaa.pol`):
```pol
header {
  comment:: "HIPAA Compliance Policy"
  target:: forcepoint hipaa inet json
}

term emr-access {
  comment:: "Allow EMR access from authorized clinical workstations"
  source-address:: CLINICAL_WORKSTATIONS
  destination-address:: EMR_SERVERS
  destination-port:: EMR_PORTS
  protocol:: tcp
  action:: accept
  logging:: true
  forcepoint-log-level:: essential
  forcepoint-inspection:: enabled
}

term medical-imaging {
  comment:: "Allow medical imaging traffic"
  source-address:: IMAGING_DEVICES
  destination-address:: PACS_SERVERS
  destination-port:: DICOM_PORTS
  protocol:: tcp
  action:: accept
  logging:: true
  forcepoint-log-level:: essential
}

term phi-backup {
  comment:: "Allow encrypted PHI backup"
  source-address:: BACKUP_SERVER
  destination-address:: PHI_STORAGE
  destination-port:: BACKUP_PORTS
  protocol:: tcp
  action:: accept
  logging:: true
  forcepoint-log-level:: essential
}

term audit-logging {
  comment:: "Allow audit logging to SIEM"
  source-address:: PHI_NETWORKS
  destination-address:: SIEM_SERVERS
  destination-port:: SYSLOG
  protocol:: udp
  action:: accept
  logging:: true
  forcepoint-log-level:: essential
}

term deny-unauthorized-phi {
  comment:: "Deny unauthorized PHI access"
  source-address:: UNAUTHORIZED_NETWORKS
  destination-address:: PHI_NETWORKS
  action:: deny
  logging:: true
  forcepoint-action:: blacklist
  forcepoint-log-level:: alert
}

term deny-all {
  comment:: "Default deny all"
  action:: deny
  logging:: true
  forcepoint-log-level:: essential
}
```

---

## Incident Response

### Example 11: Malware Outbreak Response

**Scenario**: Automated response to malware outbreak

**Capirca Policy** (`malware-response.pol`):
```pol
header {
  comment:: "Malware Outbreak Response Policy"
  target:: forcepoint malware-response inet json
}

term block-c2-servers {
  comment:: "Block known C2 servers"
  source-address:: ANY
  destination-address:: MALICIOUS_C2
  action:: deny
  logging:: true
  forcepoint-action:: blacklist
  forcepoint-log-level:: alert
}

term block-malicious-domains {
  comment:: "Block access to malicious domains"
  source-address:: ANY
  destination-address:: MALICIOUS_DOMAINS
  destination-port:: HTTP HTTPS
  protocol:: tcp
  action:: deny
  logging:: true
  forcepoint-action:: blacklist
  forcepoint-log-level:: alert
}

term isolate-infected-hosts {
  comment:: "Isolate infected hosts from network"
  source-address:: INFECTED_HOSTS
  destination-address:: CORPORATE_NETWORKS
  action:: deny
  logging:: true
  forcepoint-action:: blacklist
  forcepoint-log-level:: alert
}

term allow-remediation {
  comment:: "Allow security team access for remediation"
  source-address:: SECURITY_TEAM
  destination-address:: INFECTED_HOSTS
  destination-port:: REMEDIATION_PORTS
  protocol:: tcp
  action:: accept
  logging:: true
  forcepoint-log-level:: essential
}

term deny-all {
  comment:: "Default deny all"
  action:: deny
  logging:: true
}
```

---

## Cloud Integration

### Example 12: AWS Security Gateway

**Scenario**: Secure connectivity to AWS cloud resources

**Capirca Policy** (`aws-gateway.pol`):
```pol
header {
  comment:: "AWS Cloud Security Policy"
  target:: forcepoint aws-gateway inet json
}

term aws-api-access {
  comment:: "Allow AWS API access from management network"
  source-address:: MGMT_NETWORK
  destination-address:: AWS_API_ENDPOINTS
  destination-port:: HTTPS
  protocol:: tcp
  action:: accept
  logging:: true
}

term aws-s3-access {
  comment:: "Allow S3 access from application servers"
  source-address:: APP_SERVERS
  destination-address:: AWS_S3_ENDPOINTS
  destination-port:: HTTPS
  protocol:: tcp
  action:: accept
  logging:: true
}

term aws-rds-access {
  comment:: "Allow RDS database access"
  source-address:: APP_SERVERS
  destination-address:: AWS_RDS_ENDPOINTS
  destination-port:: MYSQL_POSTGRES
  protocol:: tcp
  action:: accept
  logging:: true
  forcepoint-inspection:: enabled
}

term aws-vpn-tunnel {
  comment:: "Allow AWS VPN tunnel traffic"
  source-address:: AWS_VPN_CIDR
  destination-address:: CORPORATE_NETWORKS
  protocol:: tcp udp icmp
  action:: accept
  logging:: false
}

term deny-all {
  comment:: "Default deny all"
  action:: deny
  logging:: true
}
```

---

## Automation Scripts

### Script 1: Automated Policy Deployment

```python
#!/usr/bin/env python3
"""Deploy multiple Forcepoint policies from Capirca output"""

import os
import json
import requests
import argparse
from pathlib import Path

class ForcepointPolicyDeployer:
    def __init__(self, smc_url, api_token):
        self.smc_url = smc_url
        self.api_token = api_token
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {api_token}'
        }
    
    def deploy_policy(self, policy_file):
        """Deploy a single policy"""
        with open(policy_file, 'r') as f:
            policy_config = json.load(f)
        
        policy_name = policy_config['policy']['name']
        
        # Check if policy already exists
        existing_policy = self.get_policy_by_name(policy_name)
        
        if existing_policy:
            # Update existing policy
            policy_id = existing_policy['href'].split('/')[-1]
            return self.update_policy(policy_id, policy_config)
        else:
            # Create new policy
            return self.create_policy(policy_name, policy_config)
    
    def get_policy_by_name(self, name):
        """Get policy by name"""
        url = f"{self.smc_url}/api/v6/policy"
        response = requests.get(url, headers=self.headers)
        
        if response.status_code == 200:
            policies = response.json().get('policy', [])
            for policy in policies:
                if policy['name'] == name:
                    return policy
        return None
    
    def create_policy(self, name, config):
        """Create new policy"""
        url = f"{self.smc_url}/api/v6/policy"
        payload = {
            "name": name,
            "policy": config
        }
        
        response = requests.post(url, headers=self.headers, json=payload)
        
        if response.status_code == 201:
            return response.json()
        else:
            raise Exception(f"Failed to create policy: {response.text}")
    
    def update_policy(self, policy_id, config):
        """Update existing policy"""
        url = f"{self.smc_url}/api/v6/policy/{policy_id}"
        response = requests.put(url, headers=self.headers, json=config)
        
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to update policy: {response.text}")
    
    def deploy_all_policies(self, policy_dir):
        """Deploy all policies in directory"""
        policy_files = Path(policy_dir).glob('*.forcepoint.json')
        results = []
        
        for policy_file in policy_files:
            try:
                print(f"Deploying {policy_file.name}...")
                result = self.deploy_policy(str(policy_file))
                results.append({
                    'file': policy_file.name,
                    'status': 'success',
                    'result': result
                })
                print(f"✓ {policy_file.name} deployed successfully")
            except Exception as e:
                results.append({
                    'file': policy_file.name,
                    'status': 'failed',
                    'error': str(e)
                })
                print(f"✗ {policy_file.name} failed: {e}")
        
        return results

def main():
    parser = argparse.ArgumentParser(description='Deploy Forcepoint policies')
    parser.add_argument('--policy-dir', required=True, help='Directory containing policy files')
    parser.add_argument('--smc-url', default=os.environ.get('FORCEPOINT_SMC_URL'))
    parser.add_argument('--api-token', default=os.environ.get('FORCEPOINT_API_TOKEN'))
    
    args = parser.parse_args()
    
    if not args.smc_url or not args.api_token:
        print("Error: SMC URL and API token required")
        return 1
    
    deployer = ForcepointPolicyDeployer(args.smc_url, args.api_token)
    results = deployer.deploy_all_policies(args.policy_dir)
    
    # Print summary
    success_count = sum(1 for r in results if r['status'] == 'success')
    total_count = len(results)
    
    print(f"\nDeployment Summary: {success_count}/{total_count} policies deployed successfully")
    
    if success_count < total_count:
        print("\nFailed deployments:")
        for result in results:
            if result['status'] == 'failed':
                print(f"  - {result['file']}: {result['error']}")
        return 1
    
    return 0

if __name__ == '__main__':
    exit(main())
```

### Script 2: Policy Validation and Testing

```python
#!/usr/bin/env python3
"""Validate Forcepoint policies before deployment"""

import json
import sys
import argparse
from pathlib import Path

class PolicyValidator:
    def __init__(self):
        self.errors = []
        self.warnings = []
    
    def validate_policy_file(self, policy_file):
        """Validate a single policy file"""
        try:
            with open(policy_file, 'r') as f:
                policy = json.load(f)
        except json.JSONDecodeError as e:
            self.errors.append(f"Invalid JSON in {policy_file}: {e}")
            return False
        
        return self.validate_policy_structure(policy, policy_file)
    
    def validate_policy_structure(self, policy, filename):
        """Validate policy structure"""
        valid = True
        
        # Check root structure
        if 'policy' not in policy:
            self.errors.append(f"{filename}: Missing 'policy' root element")
            valid = False
        
        policy_data = policy.get('policy', {})
        
        # Check required fields
        if 'name' not in policy_data:
            self.errors.append(f"{filename}: Missing policy name")
            valid = False
        
        if 'rules' not in policy_data:
            self.errors.append(f"{filename}: Missing 'rules' section")
            valid = False
        
        # Validate each rule
        rules = policy_data.get('rules', [])
        for i, rule in enumerate(rules):
            if not self.validate_rule(rule, filename, i):
                valid = False
        
        return valid
    
    def validate_rule(self, rule, filename, rule_index):
        """Validate individual rule"""
        valid = True
        
        # Check required fields
        required_fields = ['name', 'action', 'sources', 'destinations']
        for field in required_fields:
            if field not in rule:
                self.errors.append(f"{filename}: Rule {rule_index} ({rule.get('name', 'unnamed')}): Missing '{field}'")
                valid = False
        
        # Validate action
        if 'action' in rule:
            action = rule['action']
            if isinstance(action, dict) and 'action' not in action:
                self.errors.append(f"{filename}: Rule {rule_index}: Invalid action format")
                valid = False
        
        # Validate sources and destinations
        for field in ['sources', 'destinations']:
            if field in rule:
                if not isinstance(rule[field], dict):
                    self.errors.append(f"{filename}: Rule {rule_index}: {field} must be an object")
                    valid = False
        
        # Validate services
        if 'services' in rule:
            if not isinstance(rule['services'], dict):
                self.errors.append(f"{filename}: Rule {rule_index}: services must be an object")
                valid = False
        
        return valid
    
    def validate_policies_in_directory(self, policy_dir):
        """Validate all policies in directory"""
        policy_files = Path(policy_dir).glob('*.forcepoint.json')
        
        if not policy_files:
            self.warnings.append(f"No policy files found in {policy_dir}")
            return True
        
        all_valid = True
        for policy_file in policy_files:
            print(f"Validating {policy_file.name}...")
            if not self.validate_policy_file(str(policy_file)):
                all_valid = False
                print(f"✗ {policy_file.name} validation failed")
            else:
                print(f"✓ {policy_file.name} validation passed")
        
        return all_valid

def main():
    parser = argparse.ArgumentParser(description='Validate Forcepoint policies')
    parser.add_argument('--policy-dir', required=True, help='Directory containing policy files')
    parser.add_argument('--strict', action='store_true', help='Treat warnings as errors')
    
    args = parser.parse_args()
    
    validator = PolicyValidator()
    is_valid = validator.validate_policies_in_directory(args.policy_dir)
    
    # Print results
    if validator.errors:
        print("\nErrors:")
        for error in validator.errors:
            print(f"  - {error}")
    
    if validator.warnings:
        print("\nWarnings:")
        for warning in validator.warnings:
            print(f"  - {warning}")
    
    if args.strict and validator.warnings:
        is_valid = False
    
    if is_valid:
        print("\n✓ All policies are valid")
        return 0
    else:
        print("\n✗ Policy validation failed")
        return 1

if __name__ == '__main__':
    exit(main())
```

---

## Conclusion

This comprehensive collection of examples and use cases demonstrates the versatility of Forcepoint REST API integration with Capirca. From basic access control to complex multi-tier applications and compliance scenarios, these examples provide practical templates for common security challenges.

### Key Takeaways

1. **Modular Design**: Create focused policies for specific security zones or applications
2. **Defense in Depth**: Implement multiple layers of security controls
3. **Compliance Focus**: Use essential logging and inspection for regulated environments
4. **Automation Ready**: Structure policies for automated deployment and validation
5. **Incident Response**: Prepare policies for rapid threat response

### Customization Guidelines

* Adapt network and service definitions to match your environment
* Adjust logging levels based on operational requirements
* Implement additional validation for your specific use cases
* Extend automation scripts to integrate with your existing toolchain

---

**Version**: 1.0  
**Last Updated**: 2024-11-24  
**Compatible with**: Forcepoint NGFW 6.x/7.x, Capirca 1.0+