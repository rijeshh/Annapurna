# apps/api/routers/auth.py

from fastapi import APIRouter, HTTPException, Response
import os
from schemas import LoginRequest

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login")
def login(data: LoginRequest, response: Response):
    correct_password = os.getenv("ADMIN_PASSWORD")

    if data.password != correct_password:
        raise HTTPException(status_code=401, detail="Wrong password")

    # set httpOnly cookie — JavaScript can't read this, only the browser sends it
    response.set_cookie(
        key="admin_token",
        value="authenticated",
        httponly=True,
        samesite="lax"
    )
    return {"message": "Logged in"}

@router.post("/logout")
def logout(response: Response):
    response.delete_cookie("admin_token")
    return {"message": "Logged out"}