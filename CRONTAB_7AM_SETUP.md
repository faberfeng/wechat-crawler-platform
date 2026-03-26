# Crontab 定时任务配置 - 每天 7:00

## 使用说明

### 方式一：手动配置（推荐）

1. **编辑 crontab：**
   ```bash
   crontab -e
   ```

2. **添加以下内容：**
   ```bash
   # 微信公众号定时抓取 - 每天 7:00
   0 7 * * * cd ~/Desktop/wechat-crawler-platform && python3 crawl_articles.py --account-id 1 >> /tmp/wechat_crawl.log 2>&1
   ```

3. **保存并退出（如果是 vim，按 :wq）**

### 方式二：使用配置文件

1. **配置文件已准备好：**
   ```
   ~/Desktop/wechat-crawler-platform/crontab_7am.conf
   ```

2. **加载数据配置：**
   ```bash
   crontab ~/Desktop/wechat-crawler-platform/crontab_7am.conf
   ```

3. **验证配置：**
   ```bash
   crontab -l
   ```

---

## 配置详情

- **执行时间：** 每天早上 7:00
- **抓取对象：** 上海静安公众号 (ID: 1)
- **日志文件：** /tmp/wechat_crawl.log
- **执行脚本：** ~/Desktop/wechat-crawler-platform/crawl_articles.py

---

## 验证和监控

### 查看定时任务
```bash
crontab -l
```

### 查看实时日志
```bash
tail -f /tmp/wechat_crawl.log
```

### 手动测试
```bash
cd ~/Desktop/wechat-crawler-platform
python3 crawl_articles.py --account-id 1
```

---

## 删除定时任务

```bash
crontab -e
# 删除对应行后保存
```

---

## 修改执行时间

修改第一个数字（分钟）和第二个数字（小时）：

```bash
# 每天 8:00
0 8 * * * ...

# 每天 9:30
30 9 * * * ...

# 每隔 6 小时
0 */6 * * * ...
```
