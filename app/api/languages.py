# app/api/languages.py
from __future__ import annotations
from fastapi import APIRouter
from core.language import LANGUAGES

router = APIRouter(prefix="/languages", tags=["languages"])


@router.get("/")
def list_languages():
    return list(LANGUAGES.values())
