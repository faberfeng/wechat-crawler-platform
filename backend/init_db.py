"""
数据库初始化脚本
创建初始管理员用户和测试用户
"""

import sys
import os

# 添加项目路径
sys.path.insert(0, '/Users/fengweibo/Desktop/wechat-crawler-platform/backend')

from passlib.context import CryptContext
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# 使用 pbkdf2_sha256 代替 bcrypt（更稳定）
pwd_context = CryptContext(
    schemes=["pbkdf2_sha256"],
    deprecated="auto"
)

# 数据库 URL
DATABASE_URL = "sqlite:///./data/wechat.db"

# 创建引擎
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 导入模型
from app.db.base import Base
from app.models.user import User

# 创建所有表
Base.metadata.create_all(bind=engine)


def create_initial_users():
    """创建初始用户"""
    db = SessionLocal()

    try:
        # 检查是否已经有 admin 用户
        admin_user = db.query(User).filter(User.username == "admin").first()

        if admin_user:
            print(f"✓ Admin 用户已存在（ID: {admin_user.id}）")
            # 更新密码
            hashed_password = pwd_context.hash("admin123")
            admin_user.password_hash = hashed_password
            db.commit()
            print(f"✓ Admin 密码已更新")
        else:
            # 创建 admin 用户
            admin_user = User(
                username="admin",
                email="admin@wechat-crawler.com",
                password_hash=pwd_context.hash("admin123"),
                role="admin"
            )
            db.add(admin_user)
            db.commit()
            db.refresh(admin_user)
            print(f"✓ Admin 用户创建成功（ID: {admin_user.id}）")

        # 创建测试用户
        test_users = [
            {
                "username": "testuser",
                "email": "testuser@example.com",
                "password": "Test123456",
                "role": "user"
            },
            {
                "username": "demo",
                "email": "demo@example.com",
                "password": "Demo123456",
                "role": "user"
            }
        ]

        for user_data in test_users:
            existing_user = db.query(User).filter(User.username == user_data["username"]).first()
            if existing_user:
                print(f"✓ 用户 {user_data['username']} 已存在")
            else:
                new_user = User(
                    username=user_data["username"],
                    email=user_data["email"],
                    password_hash=pwd_context.hash(user_data["password"]),
                    role=user_data["role"]
                )
                db.add(new_user)
                db.commit()
                db.refresh(new_user)
                print(f"✓ 用户 {user_data['username']} 创建成功")

        # 显示所有用户
        print("\n当前所有用户：")
        users = db.query(User).all()
        for user in users:
            print(f"  - {user.username} ({user.email}) - 角色: {user.role}")
            print(f"    密码哈希（前50字符）: {user.password_hash[:50]}...")

        print("\n✓ 数据库初始化完成！")
        print("\n默认账户信息：")
        print("  管理员账户: admin / admin123")
        print("  测试账户: testuser / Test123456")
        print("  演示账户: demo / Demo123456")

    except Exception as e:
        print(f"✗ 错误: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    print("=" * 50)
    print("  微信公众号抓取平台 - 数据库初始化")
    print("=" * 50)
    print()
    create_initial_users()
