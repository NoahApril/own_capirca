#!/usr/bin/env python3
"""
Example script demonstrating Capirca Phase 2 API usage.

This script shows how to:
1. Initialize the database
2. Create policies, network objects, and service objects
3. Validate policies
4. Create deployment records
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from capirca.db import models
from capirca.db.base import Base, engine, session_scope
from capirca.api.services.validator import PolicyValidator
from capirca.lib import naming


def init_database():
    """Initialize the database."""
    print("Initializing database...")
    Base.metadata.create_all(bind=engine)
    print("Database initialized!")


def create_sample_data():
    """Create sample policies, objects, and validate."""
    with session_scope() as db:
        print("\n1. Creating network objects...")
        network_obj = models.NetworkObject(
            name="INTERNAL_NETS",
            addresses=["10.0.0.0/8", "192.168.0.0/16", "172.16.0.0/12"],
            description="RFC 1918 private networks"
        )
        db.add(network_obj)
        print(f"   Created network object: {network_obj.name}")

        print("\n2. Creating service objects...")
        service_obj = models.ServiceObject(
            name="WEB_SERVICES",
            ports=["80", "443"],
            protocols=["tcp"],
            description="HTTP and HTTPS"
        )
        db.add(service_obj)
        print(f"   Created service object: {service_obj.name}")

        print("\n3. Creating policy...")
        policy_content = """header {
  comment:: "Example firewall policy"
  target:: juniper example-filter
  target:: cisco example-acl
}

term allow-web-from-internal {
  comment:: "Allow web traffic from internal networks"
  source-address:: INTERNAL_NETS
  destination-port:: HTTP HTTPS
  protocol:: tcp
  action:: accept
}

term allow-dns {
  comment:: "Allow DNS queries"
  destination-port:: DNS
  protocol:: udp tcp
  action:: accept
}

term deny-all {
  comment:: "Default deny"
  action:: deny
}
"""
        policy = models.Policy(
            name="example-policy",
            description="Example multi-target policy",
            content=policy_content,
            status="draft"
        )
        db.add(policy)
        db.flush()
        print(f"   Created policy: {policy.name} (ID: {policy.id})")

        print("\n4. Validating policy...")
        try:
            defs = naming.Naming('./def')
        except Exception:
            print("   Warning: Could not load definitions, skipping reference validation")
            defs = None

        validator = PolicyValidator(definitions=defs)
        result = validator.validate_policy(policy.content)

        print(f"   Validation result: {'VALID' if result.is_valid else 'INVALID'}")
        if result.errors:
            print(f"   Found {len(result.errors)} issue(s):")
            for error in result.errors:
                severity_icon = "❌" if error.severity == "error" else "⚠️" if error.severity == "warning" else "ℹ️"
                line_info = f" (line {error.line_number})" if error.line_number else ""
                print(f"     {severity_icon} [{error.validation_type}] {error.message}{line_info}")
        else:
            print("   ✅ No issues found")

        for error in result.errors:
            validation_result = models.ValidationResult(
                policy_id=policy.id,
                validation_type=error.validation_type,
                severity=error.severity,
                message=error.message,
                line_number=error.line_number
            )
            db.add(validation_result)

        print("\n5. Creating deployment record...")
        deployment = models.Deployment(
            policy_id=policy.id,
            platform="juniper",
            target="example-filter",
            status="pending"
        )
        db.add(deployment)
        db.flush()
        print(f"   Created deployment record (ID: {deployment.id})")

    print("\n✅ Phase 2 example completed successfully!")


def main():
    """Run the example."""
    print("=" * 60)
    print("Capirca Phase 2 Example")
    print("=" * 60)

    init_database()
    create_sample_data()

    print("\nTo run the API server:")
    print("  $ pip install -r requirements.txt")
    print("  $ python -m uvicorn capirca.api.main:app --reload")
    print("\nAPI will be available at: http://localhost:8000")
    print("API docs at: http://localhost:8000/docs")


if __name__ == "__main__":
    main()
