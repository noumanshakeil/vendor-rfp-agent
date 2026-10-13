from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession
from backend.db import get_db
from backend.services import rfp as svc

class ReqIn(BaseModel):
    text: str = Field(min_length=5)
    section: str = "general"
    weight: int = 1

router = APIRouter()

@router.get("")
async def list_requirements(db: AsyncSession = Depends(get_db)):
    rows = await svc.list_requirements(db)
    return {"requirements": [{"id": r.id, "section": r.section, "text": r.text, "weight": r.weight, "answer": r.answer, "confidence": r.confidence, "status": r.status} for r in rows]}

@router.post("")
async def create(payload: ReqIn, db: AsyncSession = Depends(get_db)):
    r = await svc.add_requirement(db, payload.text, payload.section, payload.weight)
    return {"id": r.id}

@router.post("/draft-answers")
async def draft(db: AsyncSession = Depends(get_db)):
    rows = await svc.draft_answers(db)
    return {"drafted": len(rows)}
