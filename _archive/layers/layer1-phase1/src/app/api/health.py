"""
Health check and version endpoints.

Provides basic API health monitoring.
"""

from fastapi import APIRouter

from app.core.config import get_settings

settings = get_settings()
router = APIRouter(tags=["health"])


@router.get("/health")
async def health_check():
    """
    Health check endpoint.

    Returns:
        dict: Health status
    """
    return {
        "status": "healthy",
        "app": settings.app_name,
        "environment": settings.app_env,
    }


@router.get("/version")
async def version():
    """
    Version endpoint.

    Returns:
        dict: Application version
    """
    return {
        "version": settings.version,
        "app": settings.app_name,
    }
