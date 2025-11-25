# coding: utf-8
"""Pydantic models shared by the Capirca API layer."""

from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class UserBase(BaseModel):
    username: str = Field(..., max_length=255)
    email: Optional[str] = Field(None, max_length=255)
    role: str = Field("user", max_length=50)


class UserCreate(UserBase):
    pass


class User(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class PolicyBase(BaseModel):
    name: str
    description: Optional[str] = None
    content: str
    status: Optional[str] = "draft"


class PolicyCreate(PolicyBase):
    created_by: Optional[int] = None


class PolicyUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    content: Optional[str] = None
    status: Optional[str] = None


class Policy(PolicyBase):
    id: int
    version: int
    created_at: datetime
    updated_at: datetime
    created_by: Optional[int] = None

    class Config:
        from_attributes = True


class NetworkObjectBase(BaseModel):
    name: str
    addresses: List[str]
    description: Optional[str] = None


class NetworkObjectCreate(NetworkObjectBase):
    pass


class NetworkObjectUpdate(BaseModel):
    name: Optional[str] = None
    addresses: Optional[List[str]] = None
    description: Optional[str] = None


class NetworkObject(NetworkObjectBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ServiceObjectBase(BaseModel):
    name: str
    ports: List[str]
    protocols: List[str]
    description: Optional[str] = None


class ServiceObjectCreate(ServiceObjectBase):
    pass


class ServiceObjectUpdate(BaseModel):
    name: Optional[str] = None
    ports: Optional[List[str]] = None
    protocols: Optional[List[str]] = None
    description: Optional[str] = None


class ServiceObject(ServiceObjectBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class DeploymentBase(BaseModel):
    policy_id: int
    platform: str
    target: str
    status: Optional[str] = "pending"
    output_content: Optional[str] = None
    error_message: Optional[str] = None


class DeploymentCreate(DeploymentBase):
    deployed_by: Optional[int] = None


class Deployment(DeploymentBase):
    id: int
    deployed_at: Optional[datetime]
    created_at: datetime
    deployed_by: Optional[int]

    class Config:
        from_attributes = True


class ValidationError(BaseModel):
    severity: str
    message: str
    line_number: Optional[int] = None
    validation_type: str


class ValidationResult(BaseModel):
    is_valid: bool
    errors: List[ValidationError] = Field(default_factory=list)
