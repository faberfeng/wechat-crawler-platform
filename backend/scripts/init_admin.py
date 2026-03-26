"""
初始化默认管理员账号

运行此脚本将创建默认超级管理员账号：
- 用户名: admin
- 邮箱: admin@example.com
- 密码: admin123

⚠️ 首次登录后请立即修改密码！
"""
import asyncio
import sys
from pathlib import Path

# 添加项目根目录到 Python 路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import select
from app.db.base import engine, get_db
from app.core.security import get_password_hash
from app.models.user import User


async def create_admin_user():
    """创建默认管理员用户"""

    # 检查管理员是否已存在
    from sqlalchemy.ext.asyncio import AsyncSession

    async with engine.begin() as conn:
        statement = select(User).where(User.email == "admin@example.com")
        result = await conn.execute(statement)
        existing_admin = result.scalar_one_or_none()

        if existing_admin:
            print("✅ 管理员账号已存在，无需创建")
            print(f"   用户名: {existing_admin.username}")
            print(f"   邮箱: {existing_admin.email}")
            print(f"   角色: {existing_admin.role}")
            return

    # 创建新管理员
    admin_user = User(
        username="admin",
        email="admin@example.com",
        password_hash=get_password_hash("admin123"),
        role="admin"
    )

    async with AsyncSession(engine) as session:
        session.add(admin_user)
        await session.commit()

        print("✅ 默认管理员账号创建成功！")
        print("\n登录信息：")
        print("-" * 40)
        print("用户名: admin")
        print("邮箱: admin@example.com")
        print("密码: admin123")
        print("-" * 40)
        print("\n⚠️ 重要提示：")
        print("   请首次登录后立即修改密码！")
        print("   请确保修改 .env 中的 SECRET_KEY！")


if __name__ == "__main__":
    print("=" * 50)
    print("   初始化默认管理员账号")
    print("=" * 50)
    print()

    try:
        asyncio.run(create_admin_user())
    except Exception as e:
        print(f"❌ 创建管理员失败: {e}")
        sys.exit(1)
