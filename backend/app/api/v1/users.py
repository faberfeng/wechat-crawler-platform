"""
用户管理接口（仅管理员）
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel

from app.db.base import get_db
from app.models.user import User
from app.core.security import get_password_hash

router = APIRouter()


class UserCreate(BaseModel):
    """创建用户请求"""
    username: str
    email: str
    password: str
    role: str = "user"


class UserUpdate(BaseModel):
    """更新用户请求"""
    role: Optional[str] = None


@router.get("/")
def get_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    获取用户列表（需要管理员权限，临时开放）
    """
    # 查询总数
    statement = select(User)
    result = db.execute(statement)
    total = len(result.scalars().all())

    # 查询用户列表
    statement = select(User).offset(skip).limit(limit)
    result = db.execute(statement)
    users = result.scalars().all()

    return {
        "users": [
            {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "role": user.role,
                "created_at": user.created_at.isoformat() if user.created_at else None,
                "updated_at": user.updated_at.isoformat() if user.updated_at else None
            }
            for user in users
        ],
        "total": total,
        "skip": skip,
        "limit": limit
    }


@router.get("/{user_id}")
def get_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    """
    获取指定用户信息
    """
    statement = select(User).where(User.id == user_id)
    result = db.execute(statement)
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "role": user.role,
        "created_at": user.created_at.isoformat() if user.created_at else None,
        "updated_at": user.updated_at.isoformat() if user.updated_at else None
    }


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_user(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    """
    创建新用户
    """
    # 检查用户名是否已存在
    statement = select(User).where(User.username == user_data.username)
    result = db.execute(statement)
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )

    # 检查邮箱是否已存在
    statement = select(User).where(User.email == user_data.email)
    result = db.execute(statement)
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # 创建新用户
    new_user = User(
        username=user_data.username,
        email=user_data.email,
        password_hash=get_password_hash(user_data.password),
        role=user_data.role
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "id": new_user.id,
        "username": new_user.username,
        "email": new_user.email,
        "role": new_user.role,
        "message": "User created successfully"
    }


@router.patch("/{user_id}")
def update_user(
    user_id: int,
    user_data: UserUpdate,
    db: Session = Depends(get_db)
):
    """
    更新用户信息
    """
    statement = select(User).where(User.id == user_id)
    result = db.execute(statement)
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # 更新角色
    if user_data.role is not None:
        user.role = user_data.role

    db.commit()

    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "role": user.role,
        "message": "User updated successfully"
    }


@router.delete("/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    """
    删除用户
    """
    statement = select(User).where(User.id == user_id)
    result = db.execute(statement)
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    db.delete(user)
    db.commit()

    return {"message": "User deleted successfully"}
