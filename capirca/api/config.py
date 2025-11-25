# coding: utf-8
"""Configuration utilities for the Capirca API."""

from __future__ import annotations

try:
    from pydantic_settings import BaseSettings
except ImportError:
    from pydantic import BaseSettings

from pydantic import Field


class Settings(BaseSettings):
    api_title: str = "Capirca Phase 2 API"
    api_version: str = "2.0"
    api_prefix: str = "/api"
    database_url: str = Field(
        "sqlite+pysqlite:///capirca_phase2.db",
        description="SQLAlchemy-compatible database URL",
    )
    naming_definitions_directory: str = Field(
        "./def",
        description="Path to Capirca definition files for validation",
    )

    class Config:
        env_prefix = "CAPIRCA_"
        env_file = ".env"
        case_sensitive = False


def get_settings() -> Settings:
    return Settings()
