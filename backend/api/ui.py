from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from backend.db import get_db
from backend.services import rfp as svc

router = APIRouter()
templates = Jinja2Templates(directory="backend/templates")

@router.get("/", response_class=HTMLResponse)
async def home(request: Request, db: AsyncSession = Depends(get_db)):
    return templates.TemplateResponse("index.html", {"request": request, "title": "Vendor RFP Agent", "requirements": await svc.list_requirements(db)})

@router.post("/ui/requirements")
async def ui_add(text: str = Form(...), section: str = Form("general"), weight: int = Form(3), db: AsyncSession = Depends(get_db)):
    await svc.add_requirement(db, text, section, weight)
    return RedirectResponse("/", status_code=303)

@router.post("/ui/draft")
async def ui_draft(db: AsyncSession = Depends(get_db)):
    await svc.draft_answers(db)
    return RedirectResponse("/", status_code=303)
