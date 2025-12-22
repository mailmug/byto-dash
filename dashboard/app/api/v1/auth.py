from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserRead, UserUpdate
from app.db.session import get_async_session
from app.models.user import User
from app.services.user_manager import UserManager, current_active_user, get_user_manager
from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter()


@router.patch("/auth/update-profile", response_model=UserRead)
async def update_profile(
    data: UserUpdate,
    current_user: User = Depends(current_active_user),
    user_manager: UserManager = Depends(get_user_manager),
    session: AsyncSession = Depends(get_async_session),
):
    if data.name is not None:
        current_user.name = data.name

    if data.password is not None:
        await user_manager.update_password(
            current_user,
            data.password
        )

    session.add(current_user)
    await session.commit()
    await session.refresh(current_user)

    return current_user