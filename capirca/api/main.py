# coding: utf-8
"""FastAPI application for Capirca Phase 2."""

from __future__ import annotations

from fastapi import FastAPI

from capirca.api.config import get_settings
from capirca.api.routers import policies, network_objects, service_objects, deployments

settings = get_settings()

app = FastAPI(title=settings.api_title, version=settings.api_version)

app.include_router(policies.router, prefix=settings.api_prefix)
app.include_router(network_objects.router, prefix=settings.api_prefix)
app.include_router(service_objects.router, prefix=settings.api_prefix)
app.include_router(deployments.router, prefix=settings.api_prefix)


@app.get("/")
def read_root():
    """Health endpoint."""
    return {"status": "ok", "version": settings.api_version}
