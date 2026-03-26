"""
认证相关接口
"""
from fastapi import APIRouter, Depends, HTTPException, status, Body, Header
from fastapi.security import OAuth2PasswordRequestForm, HTTPBearer
from sqlalchemy import select
from sqlalchemy.orm import Session
from datetime import timedelta, datetime
from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional

from app.db.base import get_db
from app.models.user import User
from app.core.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    decode_access_token
)
from app.core.config import settings

router = APIRouter()

# HTTP Bearer 认证（用于从 Authorization 头提取 token）
security = HTTPBearer()


class UserRegister(BaseModel):
    """用户注册请求"""
    username: str
    email: EmailStr
    password: str

    @field_validator('username')
    def validate_username(cls, v):
        if len(v) < 3 or len(v) > 20:
            raise ValueError('用户名长度必须在 3-20 个字符之间')
        return v

    @field_validator('password')
    def validate_password(cls, v):
        if len(v) < 6:
            raise ValueError('密码长度不能少于 6 位')
        return v


class UserResponse(BaseModel):
    """用户响应"""
    id: int
    username: str
    email: str
    role: str
    created_at: str


class TokenResponse(BaseModel):
    """Token 响应"""
    access_token: str
    token_type: str
    user: dict


class ChangePasswordRequest(BaseModel):
    """修改密码请求"""
    current_password: str
    new_password: str

    @field_validator('new_password')
    def validate_new_password(cls, v):
        if len(v) < 6:
            raise ValueError('新密码长度不能少于 6 位')
        return v


class UpdateUserRequest(BaseModel):
    """更新用户信息请求"""
    username: Optional[str] = None
    email: Optional[EmailStr] = None

    @field_validator('username')
    def validate_username(cls, v):
        if v is not None and (len(v) < 3 or len(v) > 20):
            raise ValueError('用户名长度必须在 3-20 个字符之间')
        return v


class DeleteUserRequest(BaseModel):
    """删除用户请求"""
    password: str


@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(
    user_data: UserRegister,
    db: Session = Depends(get_db)
):
    """
    用户注册
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
        role="user"  # 默认为普通用户
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "id": new_user.id,
        "username": new_user.username,
        "email": new_user.email,
        "role": new_user.role,
        "message": "User registered successfully"
    }


@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    用户登录（OAuth2 密码流程）
    """
    # 查找用户（通过用户名或邮箱）
    statement = select(User).where(
        (User.username == form_data.username) | (User.email == form_data.username)
    )
    result = db.execute(statement)
    user = result.scalar_one_or_none()

    # 验证用户存在性
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 验证密码
    if not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 创建访问令牌
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)},
        expires_delta=access_token_expires
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": user.role
        }
    }


@router.post("/logout")
def logout(db: Session = Depends(get_db)):
    """
    用户登出（客户端需要删除 token）
    """
    return {"message": "Successfully logged out"}


@router.get("/me")
def get_current_user_info(
    credentials = Depends(security),
    db: Session = Depends(get_db)
):
    """
    获取当前用户信息
    """
    # 从 credentials 中提取 token
    token = credentials.credentials

    # 解析 token 获取用户 ID
    try:
        payload = decode_access_token(token)
        if not payload or 'sub' not in payload:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )

        user_id = int(payload['sub'])
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
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )


@router.patch("/me/password")
def change_password(
    password_data: ChangePasswordRequest,
    credentials = Depends(security),
    db: Session = Depends(get_db)
):
    """
    修改当前用户密码
    """
    # 从 token 获取用户 ID
    token = credentials.credentials
    try:
        payload = decode_access_token(token)
        if not payload or 'sub' not in payload:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )

        user_id = int(payload['sub'])
        statement = select(User).where(User.id == user_id)
        result = db.execute(statement)
        user = result.scalar_one_or_none()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        # 验证当前密码
        if not verify_password(password_data.current_password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Current password is incorrect"
            )

        # 验证新密码不同于旧密码
        if password_data.current_password == password_data.new_password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="New password must be different from current password"
            )

        # 更新密码
        user.password_hash = get_password_hash(password_data.new_password)
        user.updated_at = datetime.now()
        db.commit()

        return {"message": "Password changed successfully"}

    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )


@router.patch("/me")
def update_profile(
    user_data: UpdateUserRequest,
    credentials = Depends(security),
    db: Session = Depends(get_db)
):
    """
    更新当前用户信息
    """
    # 从 token 获取用户 ID
    token = credentials.credentials
    try:
        payload = decode_access_token(token)
        if not payload or 'sub' not in payload:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )

        user_id = int(payload['sub'])
        statement = select(User).where(User.id == user_id)
        result = db.execute(statement)
        user = result.scalar_one_or_none()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        # 如果要更新用户名，检查是否已存在
        if user_data.username and user_data.username != user.username:
            statement = select(User).where(
                (User.username == user_data.username) & (User.id != user_id)
            )
            result = db.execute(statement)
            if result.scalar_one_or_none():
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Username already exists"
                )
            user.username = user_data.username

        # 如果要更新邮箱，检查是否已存在
        if user_data.email and user_data.email != user.email:
            statement = select(User).where(
                (User.email == user_data.email) & (User.id != user_id)
            )
            result = db.execute(statement)
            if result.scalar_one_or_none():
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already exists"
                )
            user.email = user_data.email

        user.updated_at = datetime.now()
        db.commit()
        db.refresh(user)

        return {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": user.role,
            "updated_at": user.updated_at.isoformat() if user.updated_at else None,
            "message": "Profile updated successfully"
        }

    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )


@router.delete("/me")
def delete_account(
    delete_data: DeleteUserRequest = Body(...),
    credentials = Depends(security),
    db: Session = Depends(get_db)
):
    """
    删除当前账号（需要密码确认）
    """
    # 从 token 获取用户 ID
    token = credentials.credentials
    try:
        payload = decode_access_token(token)
        if not payload or 'sub' not in payload:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )

        user_id = int(payload['sub'])
        statement = select(User).where(User.id == user_id)
        result = db.execute(statement)
        user = result.scalar_one_or_none()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        # 验证密码
        if not verify_password(delete_data.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password is incorrect"
            )

        # 管理员不能删除自己
        if user.role == "admin":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot delete admin account"
            )

        # 删除用户
        db.delete(user)
        db.commit()

        return {"message": "Account deleted successfully"}

    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )
