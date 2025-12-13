from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

router = APIRouter()


# @router.get("/users/me", response_model=UserOut)
# def me(current_user=Depends(get_current_user)):
#     return current_user
