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

"""SQLAlchemy ORM models for Capirca Phase 2 database schema."""

from datetime import datetime

from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, JSON
from sqlalchemy.orm import relationship

from capirca.db.base import Base


class User(Base):
    """User model for policy ownership and audit trails."""
    
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), unique=True, nullable=False, index=True)
    email = Column(String(255), nullable=True)
    role = Column(String(50), default="user", nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    policies = relationship("Policy", back_populates="creator")
    deployments = relationship("Deployment", back_populates="deployer")


class Policy(Base):
    """Policy model storing Capirca .pol file content and metadata."""
    
    __tablename__ = "policies"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    content = Column(Text, nullable=False)
    version = Column(Integer, default=1, nullable=False)
    status = Column(String(50), default="draft", nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    creator = relationship("User", back_populates="policies")
    deployments = relationship("Deployment", back_populates="policy")
    validation_results = relationship("ValidationResult", back_populates="policy")


class NetworkObject(Base):
    """Network object model for reusable address definitions."""
    
    __tablename__ = "network_objects"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, nullable=False, index=True)
    addresses = Column(JSON, nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class ServiceObject(Base):
    """Service object model for reusable port/protocol definitions."""
    
    __tablename__ = "service_objects"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, nullable=False, index=True)
    ports = Column(JSON, nullable=False)
    protocols = Column(JSON, nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class Deployment(Base):
    """Deployment model tracking policy deployments to platforms."""
    
    __tablename__ = "deployments"
    
    id = Column(Integer, primary_key=True, index=True)
    policy_id = Column(Integer, ForeignKey("policies.id"), nullable=False)
    platform = Column(String(100), nullable=False)
    target = Column(String(255), nullable=False)
    status = Column(String(50), default="pending", nullable=False)
    deployed_at = Column(DateTime, nullable=True)
    deployed_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    output_content = Column(Text, nullable=True)
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    policy = relationship("Policy", back_populates="deployments")
    deployer = relationship("User", back_populates="deployments")


class ValidationResult(Base):
    """Validation result model storing validation checks on policies."""
    
    __tablename__ = "validation_results"
    
    id = Column(Integer, primary_key=True, index=True)
    policy_id = Column(Integer, ForeignKey("policies.id"), nullable=False)
    validation_type = Column(String(50), nullable=False)
    severity = Column(String(20), nullable=False)
    message = Column(Text, nullable=False)
    line_number = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    policy = relationship("Policy", back_populates="validation_results")
