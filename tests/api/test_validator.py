"""Tests for the PolicyValidator service."""

from __future__ import annotations

import pytest

from capirca.api.services.validator import PolicyValidator


def test_valid_syntax():
    validator = PolicyValidator(definitions=None)
    
    policy_content = """
header {
  target:: juniper test-filter
}

term allow-dns {
  protocol:: udp
  destination-port:: DNS
  action:: accept
}
""".strip()
    
    errors = validator.validate_syntax(policy_content)
    for err in errors:
        if err.severity == "error":
            assert False, f"Unexpected syntax error: {err.message}"


def test_invalid_syntax():
    validator = PolicyValidator(definitions=None)
    
    policy_content = """
header {
  target:: juniper test-filter
}

term broken {
  this is not valid
}
""".strip()
    
    errors = validator.validate_syntax(policy_content)
    assert any(e.severity == "error" for e in errors), "Expected syntax error"


def test_security_validation_any_to_any():
    validator = PolicyValidator(definitions=None)
    
    policy_content = """
header {
  target:: juniper test-filter
}

term allow-all {
  source-address:: any
  destination-address:: any
  action:: accept
}
""".strip()
    
    errors = validator.validate_security(policy_content)
    warnings = [e for e in errors if e.severity == "warning"]
    assert len(warnings) > 0, "Expected warning for any->any accept rule"


def test_security_validation_missing_action():
    validator = PolicyValidator(definitions=None)
    
    policy_content = """
header {
  target:: juniper test-filter
}

term missing-action {
  source-address:: 10.0.0.0/8
  destination-address:: 192.168.0.0/16
}
""".strip()
    
    errors = validator.validate_security(policy_content)
    errors_only = [e for e in errors if e.severity == "error"]
    assert len(errors_only) > 0, "Expected error for missing action"


def test_full_validation():
    validator = PolicyValidator(definitions=None)
    
    policy_content = """
header {
  target:: juniper test-filter
}

term allow-ssh {
  source-address:: 10.0.0.0/8
  destination-address:: 192.168.1.0/24
  destination-port:: SSH
  protocol:: tcp
  action:: accept
}

term deny-all {
  action:: deny
}
""".strip()
    
    result = validator.validate_policy(policy_content)
    assert result.is_valid or not any(e.severity == "error" for e in result.errors)
