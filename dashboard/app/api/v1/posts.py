from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.models.post import Post
from app.services.user_db import get_user_db
from app.services.user_manager import current_active_user
from app.models.user import User
from app.db.session import get_async_session
from app.schemas.post import PostCreate, PostRead

router = APIRouter()

@router.post("/", response_model=PostRead)
async def create_post(
    post: PostCreate,
    user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session)
):
    db_post = Post(title=post.title, content=post.content, user_id=user.id)
    session.add(db_post)
    await session.commit()
    await session.refresh(db_post)
    return db_post

@router.get("/", response_model=List[PostRead])
async def list_posts(session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(Post.__table__.select())
    return result.scalars().all()
