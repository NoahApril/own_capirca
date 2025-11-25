# coding: utf-8
"""API router for deployment management."""

from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from capirca.db import models
from capirca.db.base import get_db
from capirca.api.models.schemas import (
    Deployment,
    DeploymentCreate,
)

router = APIRouter(prefix="/deployments", tags=["deployments"])


@router.get("", response_model=List[Deployment])
def list_deployments(
    skip: int = 0,
    limit: int = 100,
    policy_id: Optional[int] = None,
    db: Session = Depends(get_db),
):
    """List all deployments with optional filtering."""
    query = db.query(models.Deployment)
    if policy_id:
        query = query.filter(models.Deployment.policy_id == policy_id)
    deployments = query.offset(skip).limit(limit).all()
    return deployments


@router.post("", response_model=Deployment, status_code=status.HTTP_201_CREATED)
def create_deployment(
    deployment: DeploymentCreate,
    db: Session = Depends(get_db),
):
    """Create a new deployment record."""
    policy = db.query(models.Policy).filter(models.Policy.id == deployment.policy_id).first()
    if policy is None:
        raise HTTPException(status_code=404, detail="Policy not found")
    
    db_deployment = models.Deployment(
        policy_id=deployment.policy_id,
        platform=deployment.platform,
        target=deployment.target,
        status=deployment.status or "pending",
        deployed_by=deployment.deployed_by,
        output_content=deployment.output_content,
        error_message=deployment.error_message,
        deployed_at=datetime.utcnow() if deployment.status == "success" else None,
    )
    db.add(db_deployment)
    db.commit()
    db.refresh(db_deployment)
    return db_deployment


@router.get("/{deployment_id}", response_model=Deployment)
def get_deployment(deployment_id: int, db: Session = Depends(get_db)):
    """Get a deployment by ID."""
    deployment = db.query(models.Deployment).filter(models.Deployment.id == deployment_id).first()
    if deployment is None:
        raise HTTPException(status_code=404, detail="Deployment not found")
    return deployment


@router.post("/{deployment_id}/rollback")
def rollback_deployment(deployment_id: int, db: Session = Depends(get_db)):
    """Rollback a deployment (stub for Phase 3)."""
    deployment = db.query(models.Deployment).filter(models.Deployment.id == deployment_id).first()
    if deployment is None:
        raise HTTPException(status_code=404, detail="Deployment not found")
    
    return {
        "message": "Rollback functionality will be implemented in Phase 3",
        "deployment_id": deployment_id,
        "status": "not_implemented"
    }
