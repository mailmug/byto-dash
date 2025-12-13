from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.dependencies import get_db
from app.schemas.user import UserCreate, UserLogin
from app.services.user_service import create_user, authenticate_user
from app.core.security import create_access_token

router = APIRouter()


@router.post("/auth/register")
def register(data: UserCreate, db: Session = Depends(get_db)):
    user = create_user(db, data.email, data.password, data.name)
    return {"message": "User registered", "id": user.id}


@router.post("/auth/login")
def login(data: UserLogin, db: Session = Depends(get_db)):
    user = authenticate_user(db, data.email, data.password)
    if not user:
        raise HTTPException(401, "Invalid credentials")

    token = create_access_token({"sub": user.id})
    return {"access_token": token, "token_type": "bearer"}
