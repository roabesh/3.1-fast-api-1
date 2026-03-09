from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User, UserGroup
from app.schemas import UserCreate, UserUpdate, UserResponse
from app.auth import hash_password, get_current_user, require_auth, require_admin

router = APIRouter(prefix="/user", tags=["users"])


@router.post("", response_model=UserResponse, status_code=201)
def create_user(
    data: UserCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    # Only admins can assign admin group
    group = data.group
    if group == UserGroup.ADMIN and (
        not current_user or current_user.group != UserGroup.ADMIN
    ):
        group = UserGroup.USER

    existing = db.execute(
        select(User).where(User.username == data.username)
    ).scalar_one_or_none()
    if existing:
        raise HTTPException(status_code=409, detail="Username already taken")

    user = User(
        username=data.username,
        password_hash=hash_password(data.password),
        group=group,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.get("", response_model=List[UserResponse])
def list_users(
    db: Session = Depends(get_db),
    _=Depends(require_admin),
):
    return db.execute(select(User)).scalars().all()


@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.patch("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    data: UserUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(require_auth),
):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if current_user.group != UserGroup.ADMIN and current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Forbidden")

    # Only admins can change group
    if data.group is not None and current_user.group != UserGroup.ADMIN:
        raise HTTPException(status_code=403, detail="Only admins can change group")

    updates = data.model_dump(exclude_unset=True)
    if "password" in updates:
        user.password_hash = hash_password(updates.pop("password"))
    for field, value in updates.items():
        setattr(user, field, value)

    if "username" in updates:
        existing = db.execute(
            select(User).where(User.username == updates["username"], User.id != user_id)
        ).scalar_one_or_none()
        if existing:
            raise HTTPException(status_code=409, detail="Username already taken")

    db.commit()
    db.refresh(user)
    return user


@router.delete("/{user_id}", status_code=204)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_auth),
):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if current_user.group != UserGroup.ADMIN and current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Forbidden")

    db.delete(user)
    db.commit()
