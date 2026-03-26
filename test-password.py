#!/usr/bin/env python3
"""测试密码哈希和验证"""

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 测试生成密码哈希
plain_password = "admin123"
hashed = pwd_context.hash(plain_password)
print(f"明文密码: {plain_password}")
print(f"生成的哈希: {hashed}")
print(f"哈希长度: {len(hashed)}")
print()

# 测试验证
test_passwords = ["admin123", "wrong_password", "admin"]
for pwd in test_passwords:
    result = pwd_context.verify(pwd, hashed)
    print(f"验证 '{pwd}': {'✓ 成功' if result else '✗ 失败'}")
print()

# 测试数据库中的哈希
db_hash = "240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9"
print(f"数据库中的哈希: {db_hash}")
print(f"是否为 bcrypt 哈希: {db_hash.startswith('$2b$')}")

try:
    result = pwd_context.verify("admin123", db_hash)
    print(f"验证 'admin123' 对数据库哈希: {'✓ 成功' if result else '✗ 失败'}")
except Exception as e:
    print(f"验证失败异常: {type(e).__name__}: {e}")
