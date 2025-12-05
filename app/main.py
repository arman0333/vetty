"""Main FastAPI application."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, coins, categories
from app.config import settings
from app import __version__
import httpx
from datetime import datetime, timezone
from typing import Dict, Any

app = FastAPI(
    title="Cryptocurrency Market Updates API",
    description="REST API for fetching cryptocurrency market updates from CoinGecko",
    version=__version__,
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(coins.router)
app.include_router(categories.router)


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Cryptocurrency Market Updates API",
        "version": __version__,
        "docs": "/docs",
        "health": "/health",
        "version_info": "/version",
    }


@app.get("/health")
async def health_check():
    """
    Health check endpoint for the application.
    
    Returns:
        Application health status
    """
    return {
        "status": "healthy",
        "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "service": "cryptocurrency-api",
    }


@app.get("/health/detailed")
async def detailed_health_check():
    """
    Detailed health check including 3rd party service status.
    
    Returns:
        Detailed health status including CoinGecko API connectivity
    """
    health_status: Dict[str, Any] = {
        "status": "healthy",
        "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "service": "cryptocurrency-api",
        "version": __version__,
        "checks": {
            "application": {
                "status": "healthy",
                "message": "Application is running",
            },
            "coingecko_api": {
                "status": "unknown",
                "message": "Not checked",
            },
        },
    }

    # Check CoinGecko API connectivity
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(
                f"{settings.coingecko_api_url}/ping"
            )
            if response.status_code == 200:
                health_status["checks"]["coingecko_api"] = {
                    "status": "healthy",
                    "message": "CoinGecko API is accessible",
                    "response_time_ms": response.elapsed.total_seconds() * 1000,
                }
            else:
                health_status["checks"]["coingecko_api"] = {
                    "status": "degraded",
                    "message": f"CoinGecko API returned status {response.status_code}",
                }
                health_status["status"] = "degraded"
    except httpx.TimeoutException:
        health_status["checks"]["coingecko_api"] = {
            "status": "unhealthy",
            "message": "CoinGecko API request timed out",
        }
        health_status["status"] = "degraded"
    except Exception as e:
        health_status["checks"]["coingecko_api"] = {
            "status": "unhealthy",
            "message": f"Error connecting to CoinGecko API: {str(e)}",
        }
        health_status["status"] = "degraded"

    return health_status


@app.get("/version")
async def version_info():
    """
    Get version information for the application and 3rd party services.
    
    Returns:
        Version information including application version and dependencies
    """
    import sys
    import importlib.metadata

    # Get application version
    app_version = __version__

    # Get Python version
    python_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"

    # Get key dependency versions
    dependencies = {}
    key_packages = [
        "fastapi",
        "uvicorn",
        "httpx",
        "pydantic",
        "python-jose",
    ]

    for package in key_packages:
        try:
            version = importlib.metadata.version(package)
            dependencies[package] = version
        except importlib.metadata.PackageNotFoundError:
            dependencies[package] = "not installed"

    # Get CoinGecko API information
    coingecko_info = {
        "api_url": settings.coingecko_api_url,
        "status": "unknown",
    }

    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            # Try to get API status
            ping_response = await client.get(f"{settings.coingecko_api_url}/ping")
            if ping_response.status_code == 200:
                coingecko_info["status"] = "available"
            else:
                coingecko_info["status"] = f"status_code_{ping_response.status_code}"
    except Exception:
        coingecko_info["status"] = "unavailable"

    return {
        "application": {
            "name": "Cryptocurrency Market Updates API",
            "version": app_version,
            "python_version": python_version,
        },
        "dependencies": dependencies,
        "external_services": {
            "coingecko": coingecko_info,
        },
        "configuration": {
            "default_per_page": settings.default_per_page,
            "coingecko_api_url": settings.coingecko_api_url,
        },
    }

