# apps/api/dependencies.py

from fastapi import Depends, HTTPException, Request
from database import SessionLocal

# ── DB session ─────────────────────────────────────────────────
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ── Auth check ─────────────────────────────────────────────────
def require_auth(request: Request):
    token = request.cookies.get("admin_token")
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return token  # can be extended to verify the token value