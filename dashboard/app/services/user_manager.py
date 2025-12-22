from email.message import EmailMessage
import uuid

from fastapi import Depends, Request, HTTPException, status, BackgroundTasks
from fastapi_users import BaseUserManager, FastAPIUsers, UUIDIDMixin, models
from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
    JWTStrategy,
)
from fastapi_users.db import SQLAlchemyUserDatabase
from app.core.config import settings
from app.models.user import User
from app.services.user_db import get_user_db
from app.mail.service import send_verification_email, send_reset_password_email


class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    reset_password_token_secret = settings.DATABASE_URL
    verification_token_secret = settings.DATABASE_URL

    def __init__(self, user_db: SQLAlchemyUserDatabase, background_tasks: BackgroundTasks):
        super().__init__(user_db)
        self.background_tasks = background_tasks

    async def authenticate(self, credentials):
        user = await super().authenticate(credentials)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={
                    "error": "INVALID_CREDENTIALS",
                    "message": "Wrong email or password"
                }
            )
        return user
    
    async def update_password(self, user: User, password: str):
        user.hashed_password = self.password_helper.hash(password)
    
    async def on_after_register(self, user: User, request: Request | None = None):
        print(f"User {user.id} has registered.")


    async def on_after_forgot_password(
        self, user: User, token: str, request: Request | None = None
    ):  
        self.background_tasks.add_task(send_reset_password_email, user, token)
        print(f"User {user.id} has forgot their password. Reset token: {token}")


    async def on_after_request_verify(
        self, user: User, token: str, request: Request | None = None
    ):
        self.background_tasks.add_task(send_verification_email, user, token)
        print(f"Verification requested for user {user.id}. Verification token: {token}")



async def get_user_manager(background_tasks: BackgroundTasks, user_db: SQLAlchemyUserDatabase = Depends(get_user_db)):
    yield UserManager(user_db, background_tasks)


bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")


def get_jwt_strategy() -> JWTStrategy[models.UP, models.ID]:
    return JWTStrategy(secret=settings.DATABASE_URL, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[User, uuid.UUID](get_user_manager, [auth_backend])

current_active_user = fastapi_users.current_user(active=True)