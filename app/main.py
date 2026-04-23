import os
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config import settings
from app.database import engine
from app import models

# ──────────────────────────────────────────────
# Lifespan: create tables on startup
# ──────────────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create all tables if they don't exist
    models.Base.metadata.create_all(bind=engine)
    print("[OK] Database tables ready")
    yield
    print("[--] Shutting down...")


# ──────────────────────────────────────────────
# App instance
# ──────────────────────────────────────────────
app = FastAPI(
    title="Policy Consultant API",
    description=(
        "Production-ready backend for an Insurance Consultant platform. "
        "Includes user/admin authentication, contact inquiries, and admin dashboard APIs."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# ──────────────────────────────────────────────
# CORS Middleware
# ──────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ──────────────────────────────────────────────
# Global exception handler
# ──────────────────────────────────────────────
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": "An internal server error occurred. Please try again later."},
    )

# ──────────────────────────────────────────────
# Register Routers
# ──────────────────────────────────────────────
from app.routes.auth_routes import router as auth_router
from app.routes.contact_routes import router as contact_router
from app.routes.admin_routes import router as admin_router

app.include_router(auth_router)
app.include_router(contact_router)
app.include_router(admin_router)

# ──────────────────────────────────────────────
# Health check
# ──────────────────────────────────────────────
@app.get("/", tags=["Health"])
def root():
    return {"status": "ok", "message": "Policy Consultant API is running"}


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "healthy", "version": "1.0.0"}


# ──────────────────────────────────────────────
# Entry point for local dev
# ──────────────────────────────────────────────
if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 10000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
