from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.skills import router as skills_router
from api.projects import router as projects_router
from api.files import router as files_router
from api.websocket import router as websocket_router
from api.preview import router as preview_router
from api.auth import router as auth_router
from api.chat import router as chat_router
import os

app = FastAPI(title="Career Lexicon Wrapper API")

# CORS configuration - supports both development and production
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:5173")

# Parse CORS origins (comma-separated in production)
allowed_origins = [origin.strip() for origin in CORS_ORIGINS.split(",")]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(auth_router)
app.include_router(skills_router)
app.include_router(projects_router)
app.include_router(files_router)
app.include_router(websocket_router)
app.include_router(preview_router)
app.include_router(chat_router)

@app.get("/health")
async def health_check():
    """
    Comprehensive health check endpoint.
    Returns the health status of the application and its dependencies.
    """
    from sqlalchemy.orm import Session
    from database import SessionLocal
    import os

    checks = {
        "status": "healthy",
        "timestamp": None,
        "environment": os.getenv("ENVIRONMENT", "development"),
        "dependencies": {
            "database": "unknown",
            "anthropic_api": "unknown"
        }
    }

    from datetime import datetime
    checks["timestamp"] = datetime.utcnow().isoformat()

    # Test database connection
    try:
        db = SessionLocal()
        db.execute("SELECT 1")
        db.close()
        checks["dependencies"]["database"] = "healthy"
    except Exception as e:
        checks["dependencies"]["database"] = f"unhealthy: {str(e)}"
        checks["status"] = "unhealthy"

    # Test Anthropic API key is present (not actually calling API to save costs)
    try:
        anthropic_key = os.getenv("ANTHROPIC_API_KEY")
        if anthropic_key and anthropic_key.startswith("sk-ant-"):
            checks["dependencies"]["anthropic_api"] = "configured"
        else:
            checks["dependencies"]["anthropic_api"] = "not_configured"
            checks["status"] = "degraded"
    except Exception as e:
        checks["dependencies"]["anthropic_api"] = f"error: {str(e)}"
        checks["status"] = "degraded"

    return checks

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
