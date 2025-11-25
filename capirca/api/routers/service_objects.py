# coding: utf-8
"""API router for service object management."""

from __future__ import annotations

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from capirca.db import models
from capirca.db.base import get_db
from capirca.api.models.schemas import (
    ServiceObject,
    ServiceObjectCreate,
    ServiceObjectUpdate,
)

router = APIRouter(prefix="/service-objects", tags=["service_objects"])


@router.get("", response_model=List[ServiceObject])
def list_service_objects(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """List all service objects."""
    objects = db.query(models.ServiceObject).offset(skip).limit(limit).all()
    return objects


@router.post("", response_model=ServiceObject, status_code=status.HTTP_201_CREATED)
def create_service_object(
    service_object: ServiceObjectCreate,
    db: Session = Depends(get_db),
):
    """Create a new service object."""
    existing = (
        db.query(models.ServiceObject)
        .filter(models.ServiceObject.name == service_object.name)
        .first()
    )
    if existing:
        raise HTTPException(status_code=400, detail="Service object already exists")
    
    db_object = models.ServiceObject(
        name=service_object.name,
        ports=service_object.ports,
        protocols=service_object.protocols,
        description=service_object.description,
    )
    db.add(db_object)
    db.commit()
    db.refresh(db_object)
    return db_object


@router.get("/{object_id}", response_model=ServiceObject)
def get_service_object(object_id: int, db: Session = Depends(get_db)):
    """Get a service object by ID."""
    obj = db.query(models.ServiceObject).filter(models.ServiceObject.id == object_id).first()
    if obj is None:
        raise HTTPException(status_code=404, detail="Service object not found")
    return obj


@router.put("/{object_id}", response_model=ServiceObject)
def update_service_object(
    object_id: int,
    service_object: ServiceObjectUpdate,
    db: Session = Depends(get_db),
):
    """Update a service object."""
    obj = db.query(models.ServiceObject).filter(models.ServiceObject.id == object_id).first()
    if obj is None:
        raise HTTPException(status_code=404, detail="Service object not found")
    
    if service_object.name is not None:
        obj.name = service_object.name
    if service_object.ports is not None:
        obj.ports = service_object.ports
    if service_object.protocols is not None:
        obj.protocols = service_object.protocols
    if service_object.description is not None:
        obj.description = service_object.description
    
    db.commit()
    db.refresh(obj)
    return obj


@router.delete("/{object_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_service_object(object_id: int, db: Session = Depends(get_db)):
    """Delete a service object."""
    obj = db.query(models.ServiceObject).filter(models.ServiceObject.id == object_id).first()
    if obj is None:
        raise HTTPException(status_code=404, detail="Service object not found")
    
    db.delete(obj)
    db.commit()
    return None
