-- 微信爬虫平台 - 用户系统数据库迁移
-- 创建时间：2026-03-26

-- 1. 创建用户表
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) DEFAULT 'user',  -- 'admin' or 'user'
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 2. 为 accounts 表添加 user_id 字段
ALTER TABLE accounts ADD COLUMN user_id INTEGER NOT NULL DEFAULT 1;
CREATE INDEX IF NOT EXISTS idx_accounts_user_id ON accounts(user_id);

-- 3. 为 articles 表添加 user_id 字段
ALTER TABLE articles ADD COLUMN user_id INTEGER NOT NULL DEFAULT 1;
CREATE INDEX IF NOT EXISTS idx_articles_user_id ON articles(user_id);

-- 4. 为 crawl_tasks 表添加 user_id 字段
ALTER TABLE crawl_tasks ADD COLUMN user_id INTEGER NOT NULL DEFAULT 1;
CREATE INDEX IF NOT EXISTS idx_crawl_tasks_user_id ON crawl_tasks(user_id);

-- 5. 为 users 表更新时间戳触发器
CREATE TRIGGER IF NOT EXISTS update_users_timestamp
AFTER UPDATE ON users
BEGIN
    UPDATE users SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;

-- 6. 为 accounts 表添加外键约束（可选，如果要严格约束）
-- ALTER TABLE accounts ADD CONSTRAINT fk_accounts_user FOREIGN KEY (user_id) REFERENCES users (id);

-- 7. 为 articles 表添加外键约束（可选，如果要严格约束）
-- ALTER TABLE articles ADD CONSTRAINT fk_articles_user FOREIGN KEY (user_id) REFERENCES users (id);

-- 8. 为 crawl_tasks 表添加外键约束（可选，如果要严格约束）
-- ALTER TABLE crawl_tasks ADD CONSTRAINT fk_crawl_tasks_user FOREIGN KEY (user_id) REFERENCES users (id);

-- 迁移完成提示
-- SELECT 'Migration completed successfully!' as message;
