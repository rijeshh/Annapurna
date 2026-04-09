# apps/api/routers/transactions.py

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from typing import Literal
import openpyxl
import io

from database import SessionLocal
from models import Transaction
from schemas import TransactionCreate, TransactionResponse
from dependencies import get_db, require_auth

router = APIRouter(prefix="/transactions", tags=["transactions"])

# ── List all (with optional filter) ───────────────────────────
@router.get("/", response_model=list[TransactionResponse])
def list_transactions(
    type: Literal["income", "expense"] | None = None,
    db: Session = Depends(get_db),
    _=Depends(require_auth)
):
    query = db.query(Transaction)
    if type:
        query = query.filter(Transaction.type == type)
    return query.order_by(Transaction.created_at.desc()).all()

# ── Create new transaction ─────────────────────────────────────
@router.post("/", response_model=TransactionResponse, status_code=201)
def create_transaction(
    data: TransactionCreate,
    db: Session = Depends(get_db),
    _=Depends(require_auth)
):
    new_transaction = Transaction(**data.model_dump())
    db.add(new_transaction)
    db.commit()
    db.refresh(new_transaction)
    return new_transaction

# ── Delete a transaction ───────────────────────────────────────
@router.delete("/{id}", status_code=204)
def delete_transaction(
    id: int,
    db: Session = Depends(get_db),
    _=Depends(require_auth)
):
    transaction = db.query(Transaction).filter(Transaction.id == id).first()
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    db.delete(transaction)
    db.commit()

# ── Export to Excel ────────────────────────────────────────────
@router.get("/export")
def export_transactions(
    db: Session = Depends(get_db),
    _=Depends(require_auth)
):
    transactions = db.query(Transaction).order_by(Transaction.created_at.desc()).all()

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Transactions"

    # header row
    ws.append(["ID", "Amount", "Type", "Category", "Note", "Date"])

    # data rows
    for t in transactions:
        ws.append([t.id, t.amount, t.type, t.category, t.note, str(t.created_at)])

    # save to memory, not disk
    buffer = io.BytesIO()
    wb.save(buffer)
    buffer.seek(0)

    return StreamingResponse(
        buffer,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=transactions.xlsx"}
    )