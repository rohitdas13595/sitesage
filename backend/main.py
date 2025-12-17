from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.proxy_headers import ProxyHeadersMiddleware
from contextlib import asynccontextmanager
import time

from app.config import get_settings
from app.database import engine, Base
from app.api.seo import router as seo_router
from app.api.auth import router as auth_router
from app.schemas import HealthCheck

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan events for startup and shutdown"""
    # Startup
    print("🚀 Starting SiteSage API...")
    Base.metadata.create_all(bind=engine)
    
    # Simple migration for new columns
    from sqlalchemy import text
    with engine.connect() as conn:
        columns = [
            ("user_id", "INTEGER"),
            ("accessibility", "JSON"),
            ("performance_score", "FLOAT"),
            ("accessibility_score", "FLOAT"),
            ("best_practices_score", "FLOAT"),
            ("lighthouse_seo_score", "FLOAT")
        ]
        for col_name, col_type in columns:
            try:
                conn.execute(text(f"ALTER TABLE seo_reports ADD COLUMN IF NOT EXISTS {col_name} {col_type};"))
                conn.commit()
            except Exception:
                pass
            
    print("✅ Database tables created and updated")
    yield
    # Shutdown
    print("👋 Shutting down SiteSage API...")


# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Automated SEO Performance Analyzer API",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Request timing middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """Add processing time to response headers"""
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


# Proxy headers middleware (for running behind Nginx/Cloudflare)
app.add_middleware(ProxyHeadersMiddleware, trusted_hosts="*")

# CORS middleware (Outer-most to handle preflights first)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS if isinstance(settings.CORS_ORIGINS, list) else [settings.CORS_ORIGINS],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Include routers
app.include_router(auth_router)
app.include_router(seo_router)


# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    """Root endpoint"""
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running",
        "docs": "/docs"
    }


# Health check endpoint
@app.get("/health", response_model=HealthCheck, tags=["Health"])
async def health_check():
    """Health check endpoint"""
    try:
        # Test database connection
        from app.database import SessionLocal
        db = SessionLocal()
        from sqlalchemy import text
        db.execute(text("SELECT 1"))
        db.close()
        db_status = "healthy"
    except Exception as e:
        db_status = f"unhealthy: {str(e)}"
    
    return HealthCheck(
        status="healthy",
        version=settings.APP_VERSION,
        database=db_status
    )


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Handle uncaught exceptions"""
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error",
            "error": str(exc) if settings.DEBUG else "An error occurred"
        }
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )
