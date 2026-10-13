from __future__ import annotations
import uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from backend.llm import get_llm
from backend.models import Requirement

async def add_requirement(session: AsyncSession, text: str, section: str, weight: int) -> Requirement:
    req = Requirement(id=uuid.uuid4().hex[:10], text=text, section=section, weight=weight)
    session.add(req); await session.commit(); await session.refresh(req); return req

async def draft_answers(session: AsyncSession) -> list[Requirement]:
    rows = list((await session.execute(select(Requirement).where(Requirement.status == "open"))).scalars())
    llm = get_llm()
    for req in rows:
        result = await llm.complete_json(
            f"Draft an RFP answer JSON with answer and confidence 0-1 for requirement: {req.text}",
            system="You are a proposals lead. Be specific and honest about gaps.",
        )
        req.answer = str(result.get("answer") or result.get("raw") or "Draft pending")
        try:
            req.confidence = float(result.get("confidence") or 0.55)
        except (TypeError, ValueError):
            req.confidence = 0.55
        req.status = "drafted"
    await session.commit()
    return rows

async def list_requirements(session: AsyncSession):
    return list((await session.execute(select(Requirement).order_by(Requirement.created_at.desc()))).scalars())
