# apps/api/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import transactions, auth

app = FastAPI(title="TechShop API")

# ── CORS ───────────────────────────────────────────────────────
# tells FastAPI which frontends are allowed to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",   # Person 1 — web (local)
        "http://localhost:3001",   # Person 3 — dashboard (local)
    ],
    allow_credentials=True,        # needed for cookies to work
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routers ────────────────────────────────────────────────────
app.include_router(auth.router)
app.include_router(transactions.router)

@app.get("/")
def root():
    return {"status": "TechShop API running"}


