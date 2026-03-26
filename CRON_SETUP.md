# 微信公众号抓取定时任务配置

## 说明

此脚本用于配置微信公众号定时抓取的 Cron 任务。

## 使用方法

### 方式一：每天早上 9 点抓取一次

```bash
# 添加到 crontab
0 9 * * * cd ~/Desktop/wechat-crawler-platform && python3 crawl_articles.py --all >> /tmp/wechat_crawl.log 2>&1
```

### 方式二：每天早上 9 点和下午 6 点各抓取一次

```bash
# 添加到 crontab
0 9,18 * * * cd ~/Desktop/wechat-crawler-platform && python3 crawl_articles.py --all >> /tmp/wechat_crawl.log 2>&1
```

### 方式三：每 2 小时抓取一次

```bash
# 添加到 crontab
0 */2 * * * cd ~/Desktop/wechat-crawler-platform && python3 crawl_articles.py --all >> /tmp/wechat_crawl.log 2>&1
```

### 方式四：每天早上 9 点，仅抓取"上海静安"公众号

```bash
# 添加到 crontab
0 9 * * * cd ~/Desktop/wechat-crawler-platform && python3 crawl_articles.py --account-id 1 >> /tmp/wechat_crawl_account_1.log 2>&1
```

### 方式五：每 4 小时抓取一次，限制每次最多抓取 10 篇

```bash
# 添加到 crontab
0 */4 * * * cd ~/Desktop/wechat-crawler-platform && python3 crawl_articles.py --all --limit 10 >> /tmp/wechat_crawl.log 2>&1
```

---

## Cron 表达式说明

```
* * * * * command
│ │ │ │ │
│ │ │ │ └─ 星期几 (0-7, 0和7都表示周日)
│ │ │ └─── 月份 (1-12)
│ │ └───── 日期 (1-31)
│ └─────── 小时 (0-23)
└───────── 分钟 (0-59)
```

### 常用示例

| 表达式 | 说明 |
|--------|------|
| `0 9 * * *` | 每天早上 9:00 |
| `0 9,18 * * *` | 每天 9:00 和 18:00 |
| `0 */2 * * *` | 每 2 小时 |
| `0 9 * * 1` | 每周一早上 9:00 |
| `30 */4 * * *` | 每 4 小时的 30 分 |
| `0 0 * * *` | 每天 0:00 (午夜) |

---

## 日志文件

所有抓取任务的日志都会输出到 `/tmp/wechat_crawl.log` 文件中。

查看实时日志：
```bash
tail -f /tmp/wechat_crawl.log
```

查看最近日志：
```bash
tail -100 /tmp/wechat_crawl.log
```

---

## 添加 Cron 任务

### 方法一：使用配置脚本（推荐）

```bash
cd ~/Desktop/wechat-crawler-platform

# 选择一个方案运行
./setup_cron.sh
```

### 方法二：手动编辑 crontab

```bash
# 编辑 crontab
crontab -e

# 添加上面选择的一个表达式
# 保存退出
```

### 方法三：使用命令添加

```bash
# 添加到现有 crontab
(crontab -l 2>/dev/null; echo "0 9 * * * cd ~/Desktop/wechat-crawler-platform && python3 crawl_articles.py --all >> /tmp/wechat_crawl.log 2>&1") | crontab -
```

---

## 查看 Cron 任务

```bash
# 查看当前 Cron 任务
crontab -l

# 查看 Cron 日志（macOS）
log show --predicate 'process == "cron"' --last 1h

# 或查看系统日志
tail -f /var/log/syslog 2>/dev/null
```

---

## 删除 Cron 任务

```bash
# 编辑 crontab 删除对应行
crontab -e

# 或删除所有 Cron 任务
crontab -r
```

---

## 测试 Cron 任务

在添加 Cron 任务之前，建议先测试脚本：

```bash
# 测试模式（不实际抓取）
cd ~/Desktop/wechat-crawler-platform
python3 crawl_articles.py --all --test

# 测试实际抓取（仅抓取一个公众号）
python3 crawl_articles.py --account-id 1
```

---

## 文章链接配置

由于微信公众号的历史文章抓取功能暂未实现，当前通过环境变量配置文章链接。

### 配置方法

在 crontab 命令前添加环境变量：

```bash
WX_ARTICLE_URLS_1="https://mp.weixin.qq.com/s/文章1,https://mp.weixin.qq.com/s/文章2" \
0 9 * * * cd ~/Desktop/wechat-crawler-platform && python3 crawl_articles.py --account-id 1 >> /tmp/wechat_crawl.log 2>&1
```

或使用配置文件（需要先实现）：

```bash
# 在脚本启动时加载配置文件
. ~/Desktop/wechat-crawler-platform/config/articles.conf
```

---

## 公众号 ID 参考

当前公众号列表：

| ID | 名称 | Biz |
|----|------|-----|
| 1 | 上海静安 | MzA5MzI3NjkyNA== |

查看所有公众号：

```bash
sqlite3 ~/Desktop/wechat-crawler-platform/backend/data/wechat.db "SELECT id, name, biz FROM accounts;"
```

---

## 注意事项

1. **权限问题**：确保脚本有执行权限
   ```bash
   chmod +x ~/Desktop/wechat-crawler-platform/crawl_articles.py
   ```

2. **Python 环境**：确保使用正确的 Python 环境
   - 脚本使用了系统 Python 3.9
   - 需要安装所需依赖：playwright, fastapi, sqlalchemy 等

3. **日志轮转**：推荐使用 logrotate 或手动清理
   ```bash
   # 定期清理日志
   0 2 * * 0 truncate -s 0 /tmp/wechat_crawl.log
   ```

4. **运行权限**：Cron 任务在后台运行，可能遇到权限问题
   - 使用绝对路径
   - 确保数据库文件可写

5. **通知**：可以添加邮件通知或 webhook 通知
   ```bash
   # 示例：发送邮件通知
   python3 crawl_articles.py --all | mail -s "微信抓取完成" your@email.com
   ```

---

## 常见问题

### 1. Cron 任务没有执行

检查：
```bash
# 查看 cron 是不是在运行
ps aux | grep cron

# 查看 cron 日志
log show --predicate 'process == "cron"' --last 1h

# 测试脚本路径是否正确
which python3
```

### 2. 找不到模块

确保在正确的工作目录下运行脚本，或者设置 PYTHONPATH：

```bash
# 设置 PYTHONPATH
export PYTHONPATH=/Users/fengweibo/Desktop/wechat-crawler-platform/backend:$PYTHONPATH
```

### 3. 数据库锁定

SQLite 不支持并发写入，确保没有其他进程在写入数据库：

```bash
# 检查数据库锁
lsof ~/Desktop/wechat-crawler-platform/backend/data/wechat.db
```

---

## 推荐配置

对于"上海静安"公众号，推荐：

**方案：每天早上 9 点和下午 6 点抓取**

```bash
# 添加到 crontab
0 9,18 * * * cd ~/Desktop/wechat-crawler-platform && python3 crawl_articles.py --account-id 1 >> /tmp/wechat_crawl.log 2>&1
```

这个配置：
- ✅ 覆盖主要发稿时间
- ✅ 避免频繁抓取
- ✅ 可以及时获取新文章
- ✅ 对系统压力较小
