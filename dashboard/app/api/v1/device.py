from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.models.device import Device
from app.services.user_db import get_user_db
from app.services.user_manager import current_active_user
from app.models.user import User
from app.db.session import get_async_session
from app.schemas.device import DeviceCreate, DeviceRead
from sqlalchemy.future import select
from fastapi import HTTPException
from sqlalchemy import select

router = APIRouter()

@router.post("/", response_model=DeviceRead)
async def create_device(
    device_in: DeviceCreate,
    user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session),
):
    device = Device(
        title=device_in.title,
        description=device_in.description,
        type=device_in.type,
        user_id=user.id,
    )

    session.add(device)
    await session.commit()
    await session.refresh(device)

    return device


@router.get("/", response_model=List[DeviceRead])
async def list_devices(
    user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session)
):
    stmt = select(Device).where(Device.user_id == user.id)
    result = await session.execute(stmt)
    devices = result.scalars().all()
    return devices


@router.get("/{device_id}", response_model=DeviceRead)
async def get_device(
    device_id: str,
    user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session),
):
    stmt = select(Device).where(
        Device.id == device_id,
        Device.user_id == user.id
    )
    result = await session.execute(stmt)
    device = result.scalars().first()

    if not device:
        raise HTTPException(status_code=404, detail="Device not found")

    return device


@router.delete("/{device_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_device(
    device_id: str,
    user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session),
):
    # Ensure the device belongs to the user
    stmt = select(Device).where(Device.id == device_id, Device.user_id == user.id)
    result = await session.execute(stmt)
    device = result.scalars().first()

    if not device:
        raise HTTPException(status_code=404, detail="Device not found")

    # Delete the device
    await session.delete(device)
    await session.commit()

    return None
