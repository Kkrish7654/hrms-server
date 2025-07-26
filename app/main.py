"""
HRMS Backend - FastAPI Application Entry Point
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from loguru import logger
from starlette.middleware.sessions import SessionMiddleware
from contextlib import asynccontextmanager

from app.core.settings import settings
from app.core.database import async_engine, Base
from app.api.health import router as health_router
# Import other routers here

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Async context manager for FastAPI application lifecycle."""
    logger.info("Application starting up...")
    try:
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Error during startup: {str(e)}")
        raise
    yield
    logger.info("Application shutting down...")
    try:
        await async_engine.dispose()
        logger.info("Database connections closed")
    except Exception as e:
        logger.error(f"Error during shutdown: {str(e)}")
        raise

def create_application() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        debug=settings.debug,
        openapi_url="/api/v1/openapi.json",
        docs_url="/docs",
        redoc_url="/redoc",
        lifespan=lifespan,
        description="""
        HRMS Backend API provides endpoints for managing human resources data including:
        * User Management
        * Employee Records
        * Attendance Tracking
        * Leave Management
        * Payroll Processing
        """,
    )

    # Middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    app.add_middleware(
        TrustedHostMiddleware, 
        allowed_hosts=["localhost", "127.0.0.1", settings.base_url]
    )
    
    app.add_middleware(
        SessionMiddleware, 
        secret_key=settings.secret_key
    )

    app.include_router(health_router, prefix="/api/v1", tags=["health"])
    # Include other routers here with their tags

    return app

# Create the FastAPI application instance
app = create_application()

# Optional: Add startup/shutdown event handlers if needed