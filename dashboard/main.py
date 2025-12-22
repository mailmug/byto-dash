from fastapi import FastAPI, Depends, HTTPException, status
# from app.api.v1 import auth, users
from contextlib import asynccontextmanager
from app.api.v1 import posts
from app.services.user_manager import auth_backend, current_active_user, fastapi_users, get_jwt_strategy
from app.schemas.user import RegisterWithTokenResponse, UserRead, UserCreate, UserUpdate
from app.models.user import User
from app.db.session import create_db_and_tables
from fastapi.middleware.cors import CORSMiddleware
from fastapi_users.exceptions import UserAlreadyExists

from app.api.v1 import users
from app.api.v1 import auth


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Not needed if you setup a migration system like Alembic
    await create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(auth.router, prefix="/api/v1", tags=["Auth"])
# app.include_router(users.router, prefix="/api/v1", tags=["Users"])


app.include_router(
    fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["auth"]
)
# app.include_router(
#     fastapi_users.get_register_router(UserRead, UserCreate),
#     prefix="/auth",
#     tags=["auth"],
# )

@app.post(
    "/auth/register",
    response_model=RegisterWithTokenResponse,
)
async def register_and_login(
    user_create: UserCreate,
    user_manager=Depends(fastapi_users.get_user_manager),
):
    try:
        user = await user_manager.create(user_create)
    except UserAlreadyExists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="REGISTER_USER_ALREADY_EXISTS",
        )

    strategy = get_jwt_strategy()
    token = await strategy.write_token(user)

    return RegisterWithTokenResponse(
        user=UserRead.model_validate(user),
        token=token,
    )
    
app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)


@app.get("/authenticated-route")
async def authenticated_route(user: User = Depends(current_active_user)):
    return {"message": f"Hello {user.email}!"}


app.include_router(posts.router, prefix="/posts", tags=["posts"])
