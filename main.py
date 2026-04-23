# Root entry point — required for Render deployment
# Render runs: uvicorn main:app --host 0.0.0.0 --port 10000
from app.main import app

__all__ = ["app"]
