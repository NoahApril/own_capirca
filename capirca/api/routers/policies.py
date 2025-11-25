# coding: utf-8
"""API router for policy management."""

from __future__ import annotations

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from capirca.db import models
from capirca.db.base import get_db
from capirca.api.models.schemas import (
    Policy,
    PolicyCreate,
    PolicyUpdate,
    ValidationResult,
)
from capirca.api.services.validator import PolicyValidator
from capirca.lib import naming

router = APIRouter(prefix="/policies", tags=["policies"])


@router.get("", response_model=List[Policy])
def list_policies(
    skip: int = 0,
    limit: int = 100,
    status: Optional[str] = None,
    db: Session = Depends(get_db),
):
    """List all policies with optional filtering."""
    query = db.query(models.Policy)
    if status:
        query = query.filter(models.Policy.status == status)
    policies = query.offset(skip).limit(limit).all()
    return policies


@router.post("", response_model=Policy, status_code=status.HTTP_201_CREATED)
def create_policy(
    policy: PolicyCreate,
    db: Session = Depends(get_db),
):
    """Create a new policy."""
    db_policy = models.Policy(
        name=policy.name,
        description=policy.description,
        content=policy.content,
        status=policy.status,
        created_by=policy.created_by,
    )
    db.add(db_policy)
    db.commit()
    db.refresh(db_policy)
    return db_policy


@router.get("/{policy_id}", response_model=Policy)
def get_policy(policy_id: int, db: Session = Depends(get_db)):
    """Get a specific policy by ID."""
    policy = db.query(models.Policy).filter(models.Policy.id == policy_id).first()
    if policy is None:
        raise HTTPException(status_code=404, detail="Policy not found")
    return policy


@router.put("/{policy_id}", response_model=Policy)
def update_policy(
    policy_id: int,
    policy_update: PolicyUpdate,
    db: Session = Depends(get_db),
):
    """Update an existing policy."""
    policy = db.query(models.Policy).filter(models.Policy.id == policy_id).first()
    if policy is None:
        raise HTTPException(status_code=404, detail="Policy not found")
    
    if policy_update.name is not None:
        policy.name = policy_update.name
    if policy_update.description is not None:
        policy.description = policy_update.description
    if policy_update.content is not None:
        policy.content = policy_update.content
        policy.version += 1
    if policy_update.status is not None:
        policy.status = policy_update.status
    
    db.commit()
    db.refresh(policy)
    return policy


@router.delete("/{policy_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_policy(policy_id: int, db: Session = Depends(get_db)):
    """Delete a policy."""
    policy = db.query(models.Policy).filter(models.Policy.id == policy_id).first()
    if policy is None:
        raise HTTPException(status_code=404, detail="Policy not found")
    
    db.delete(policy)
    db.commit()
    return None


@router.post("/{policy_id}/validate", response_model=ValidationResult)
def validate_policy(
    policy_id: int,
    db: Session = Depends(get_db),
):
    """Validate a policy for syntax, references, and security issues."""
    policy = db.query(models.Policy).filter(models.Policy.id == policy_id).first()
    if policy is None:
        raise HTTPException(status_code=404, detail="Policy not found")
    
    try:
        definitions = naming.Naming('./def')
    except Exception:
        definitions = None
    
    validator = PolicyValidator(definitions=definitions)
    result = validator.validate_policy(policy.content)
    
    db.query(models.ValidationResult).filter(
        models.ValidationResult.policy_id == policy_id
    ).delete()
    
    for error in result.errors:
        db_validation = models.ValidationResult(
            policy_id=policy_id,
            validation_type=error.validation_type,
            severity=error.severity,
            message=error.message,
            line_number=error.line_number,
        )
        db.add(db_validation)
    
    db.commit()
    
    return result
