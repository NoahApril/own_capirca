# coding: utf-8
"""Database initialization script for Capirca Phase 2."""

from __future__ import annotations

from capirca.db.base import engine, Base
from capirca.db import models


def init_db():
    """Initialize the database by creating all tables."""
    Base.metadata.create_all(bind=engine)
    print("Database initialized successfully!")


if __name__ == "__main__":
    init_db()
