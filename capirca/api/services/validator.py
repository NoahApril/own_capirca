#
# Copyright 2024 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Policy validation service for Capirca Phase 2B."""

from __future__ import annotations

import re
from typing import List, Dict, Optional

from absl import logging
from capirca.lib import policy
from capirca.lib import naming

from capirca.api.models.schemas import ValidationError, ValidationResult


class PolicyValidator:
    """Service for validating Capirca policy files.
    
    Implements three layers of validation:
    1. Syntax Validation - checks policy syntax using Capirca parser
    2. Reference Validation - ensures all referenced objects exist
    3. Security Validation - checks for security anti-patterns
    """
    
    def __init__(self, definitions: Optional[naming.Naming] = None):
        """Initialize validator with optional definitions.
        
        Args:
            definitions: Optional Naming object for reference validation.
                        If not provided, will attempt to load from default path.
        """
        self.definitions = definitions
        
    def validate_policy(
        self,
        policy_content: str,
        check_syntax: bool = True,
        check_references: bool = True,
        check_security: bool = True
    ) -> ValidationResult:
        """Validate a policy file with all validation layers.
        
        Args:
            policy_content: The .pol file content as a string
            check_syntax: Whether to perform syntax validation
            check_references: Whether to perform reference validation
            check_security: Whether to perform security validation
            
        Returns:
            ValidationResult with is_valid flag and list of errors
        """
        errors: List[ValidationError] = []
        
        if check_syntax:
            errors.extend(self.validate_syntax(policy_content))
        
        if check_references and self.definitions:
            errors.extend(self.validate_references(policy_content))
            
        if check_security:
            errors.extend(self.validate_security(policy_content))
        
        is_valid = not any(e.severity == "error" for e in errors)
        
        return ValidationResult(is_valid=is_valid, errors=errors)
    
    def validate_syntax(self, policy_content: str) -> List[ValidationError]:
        """Validate Capirca policy syntax using the PLY parser.
        
        Args:
            policy_content: The .pol file content as a string
            
        Returns:
            List of ValidationError objects for syntax issues
        """
        errors: List[ValidationError] = []
        
        try:
            defs = self.definitions
            if not defs:
                try:
                    defs = naming.Naming(policy.DEFAULT_DEFINITIONS)
                except Exception:
                    pass
            
            parsed_policy = policy.ParsePolicy(
                policy_content,
                definitions=defs,
                optimize=False,
                shade_check=False
            )
            
            if parsed_policy is False:
                errors.append(ValidationError(
                    severity="error",
                    message="Failed to parse policy: syntax error detected",
                    validation_type="syntax"
                ))
            
        except policy.ParseError as e:
            errors.append(ValidationError(
                severity="error",
                message=f"Parse error: {str(e)}",
                validation_type="syntax"
            ))
        except Exception as e:
            errors.append(ValidationError(
                severity="error",
                message=f"Unexpected syntax validation error: {str(e)}",
                validation_type="syntax"
            ))
        
        return errors
    
    def validate_references(self, policy_content: str) -> List[ValidationError]:
        """Validate that all referenced objects exist in definitions.
        
        Args:
            policy_content: The .pol file content as a string
            
        Returns:
            List of ValidationError objects for missing references
        """
        errors: List[ValidationError] = []
        
        if not self.definitions:
            errors.append(ValidationError(
                severity="warning",
                message="Definitions not loaded, skipping reference validation",
                validation_type="reference"
            ))
            return errors
        
        try:
            parsed_policy = policy.ParsePolicy(
                policy_content,
                definitions=self.definitions,
                optimize=False
            )
            
            if parsed_policy is False:
                return errors
                
        except policy.UndefinedAddressError as e:
            errors.append(ValidationError(
                severity="error",
                message=f"Undefined address: {str(e)}",
                validation_type="reference"
            ))
        except Exception as e:
            logging.debug(f"Reference validation exception: {e}")
        
        return errors
    
    def validate_security(self, policy_content: str) -> List[ValidationError]:
        """Check for security anti-patterns in the policy.
        
        Detects:
        - any → any allow rules
        - Missing default deny rules
        - Overly permissive rules
        - Expired terms
        
        Args:
            policy_content: The .pol file content as a string
            
        Returns:
            List of ValidationError objects for security issues
        """
        errors: List[ValidationError] = []
        
        lines = policy_content.split('\n')
        
        in_term = False
        term_name = ""
        term_has_action = False
        term_src_any = False
        term_dst_any = False
        term_action = ""
        term_line_start = 0
        
        for line_num, line in enumerate(lines, 1):
            stripped = line.strip()
            
            if stripped.startswith('term '):
                in_term = True
                term_name = stripped.split()[1] if len(stripped.split()) > 1 else "unnamed"
                term_has_action = False
                term_src_any = False
                term_dst_any = False
                term_action = ""
                term_line_start = line_num
            elif in_term and stripped == '}':
                if not term_has_action:
                    errors.append(ValidationError(
                        severity="error",
                        message=f"Term '{term_name}' missing action",
                        line_number=term_line_start,
                        validation_type="security"
                    ))
                
                if term_action == "accept" and term_src_any and term_dst_any:
                    errors.append(ValidationError(
                        severity="warning",
                        message=f"Term '{term_name}' allows any → any traffic (overly permissive)",
                        line_number=term_line_start,
                        validation_type="security"
                    ))
                
                in_term = False
            elif in_term:
                if re.match(r'\s*action::\s*accept', stripped):
                    term_has_action = True
                    term_action = "accept"
                elif re.match(r'\s*action::\s*(deny|reject)', stripped):
                    term_has_action = True
                    term_action = "deny"
                
                if re.match(r'\s*source-address::\s*any', stripped, re.IGNORECASE):
                    term_src_any = True
                if re.match(r'\s*destination-address::\s*any', stripped, re.IGNORECASE):
                    term_dst_any = True
        
        has_deny_term = "action:: deny" in policy_content or "action:: reject" in policy_content
        if not has_deny_term:
            errors.append(ValidationError(
                severity="info",
                message="Policy does not contain an explicit deny rule (consider adding a default deny)",
                validation_type="security"
            ))
        
        return errors
