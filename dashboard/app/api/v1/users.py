from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas.user import UserRead

router = APIRouter()

