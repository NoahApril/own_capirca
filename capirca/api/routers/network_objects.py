# coding: utf-8
"""API router for network object management."""

from __future__ import annotations

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from capirca.db import models
from capirca.db.base import get_db
from capirca.api.models.schemas import (
    NetworkObject,
    NetworkObjectCreate,
    NetworkObjectUpdate,
)

router = APIRouter(prefix="/network-objects", tags=["network_objects"])


@router.get("", response_model=List[NetworkObject])
def list_network_objects(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """List all network objects."""
    objects = db.query(models.NetworkObject).offset(skip).limit(limit).all()
    return objects


@router.post("", response_model=NetworkObject, status_code=status.HTTP_201_CREATED)
def create_network_object(
    network_object: NetworkObjectCreate,
    db: Session = Depends(get_db),
):
    """Create a new network object."""
    existing = (
        db.query(models.NetworkObject)
        .filter(models.NetworkObject.name == network_object.name)
        .first()
    )
    if existing:
        raise HTTPException(status_code=400, detail="Network object already exists")
    
    db_object = models.NetworkObject(
        name=network_object.name,
        addresses=network_object.addresses,
        description=network_object.description,
    )
    db.add(db_object)
    db.commit()
    db.refresh(db_object)
    return db_object


@router.get("/{object_id}", response_model=NetworkObject)
def get_network_object(object_id: int, db: Session = Depends(get_db)):
    """Get a network object by ID."""
    obj = db.query(models.NetworkObject).filter(models.NetworkObject.id == object_id).first()
    if obj is None:
        raise HTTPException(status_code=404, detail="Network object not found")
    return obj


@router.put("/{object_id}", response_model=NetworkObject)
def update_network_object(
    object_id: int,
    network_object: NetworkObjectUpdate,
    db: Session = Depends(get_db),
):
    """Update a network object."""
    obj = db.query(models.NetworkObject).filter(models.NetworkObject.id == object_id).first()
    if obj is None:
        raise HTTPException(status_code=404, detail="Network object not found")
    
    if network_object.name is not None:
        obj.name = network_object.name
    if network_object.addresses is not None:
        obj.addresses = network_object.addresses
    if network_object.description is not None:
        obj.description = network_object.description
    
    db.commit()
    db.refresh(obj)
    return obj


@router.delete("/{object_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_network_object(object_id: int, db: Session = Depends(get_db)):
    """Delete a network object."""
    obj = db.query(models.NetworkObject).filter(models.NetworkObject.id == object_id).first()
    if obj is None:
        raise HTTPException(status_code=404, detail="Network object not found")
    
    db.delete(obj)
    db.commit()
    return None
