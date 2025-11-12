from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.skills import router as skills_router
from api.projects import router as projects_router
from api.files import router as files_router
from api.websocket import router as websocket_router
from api.preview import router as preview_router
from api.auth import router as auth_router

app = FastAPI(title="Career Lexicon Wrapper API")

# CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite default port
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

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
