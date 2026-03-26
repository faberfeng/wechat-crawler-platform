#!/bin/bash

# 快速配置定时任务脚本（非交互式）
# 自动配置每天早上 9 点和下午 6 点抓取"上海静安"公众号

echo "正在配置定时任务..."

# 检查并创建配置目录
CONFIG_DIR="$HOME/Desktop/wechat-crawler-platform/config"
mkdir -p "$CONFIG_DIR"

# 创建文章链接配置文件（示例）
cat > "$CONFIG_DIR/article_urls.txt" << 'EOF'
# 公众号文章链接配置
# 格式：公众号ID=文章链接1,文章链接2,文章链接3
#
# 示例：
# 1=https://mp.weixin.qq.com/s/文章1,https://mp.weixin.qq.com/s/文章2
#
# 当前配置：
1=https://mp.weixin.qq.com/s/ZKXjKURWMMStlij6OhUbiA
EOF

echo "✓ 配置文件已创建: $CONFIG_DIR/article_urls.txt"

# 备份当前 crontab
crontab -l 2>/dev/null > ~/.crontab.backup.$(date +%Y%m%d_%H%M%S) 2>&1 || true

# 检查是否已存在相同的任务
if crontab -l 2>/dev/null | grep -q "crawl_articles.py"; then
    echo "⚠️  已检测到抓取任务："
    crontab -l 2>/dev/null | grep "crawl_articles.py"
    echo ""
    read -p "是否删除现有任务并重新配置？[Y/n]: " replace

    if [[ "$replace" =~ ^[Nn]$ ]]; then
        echo "已取消配置"
        exit 0
    fi

    # 删除现有任务
    crontab -l 2>/dev/null | grep -v "crawl_articles.py" | crontab -
fi

# 添加新的定时任务
(crontab -l 2>/dev/null; cat << CRONFILE
# 微信公众号定时抓取 - 每天 9:00 和 18:00
0 9,18 * * * cd ~/Desktop/wechat-crawler-platform && WX_ARTICLE_URLS_1=\$(cat config/article_urls.txt | grep '^1=' | cut -d'=' -f2) python3 crawl_articles.py --account-id 1 >> /tmp/wechat_crawl.log 2>&1
CRONFILE
) | crontab -

echo "✓ 定时任务已配置："
echo "  - 抓取对象：上海静安公众号"
echo "  - 抓取时间：每天 9:00 和 18:00"
echo "  - 日志文件：/tmp/wechat_crawl.log"
echo ""

# 验证配置
echo "当前 Cron 任务："
crontab -l | grep -A2 "微信公众号" | grep -v "^#" | sed 's/^/  /'
echo ""

echo "测试运行？[Y/n]: " test_run

if [[ ! "$test_run" =~ ^[Nn]$ ]]; then
    echo ""
    echo "正在运行测试抓取..."
    WX_ARTICLE_URLS_1=$(cat "$CONFIG_DIR/article_urls.txt" | grep '^1=' | cut -d'=' -f2)
    cd ~/Desktop/wechat-crawler-platform
    WX_ARTICLE_URLS_1="$WX_ARTICLE_URLS_1" python3 crawl_articles.py --account-id 1 | head -20
fi

echo ""
echo "=========================================="
echo "✓ 配置完成"
echo "=========================================="
echo ""
echo "查看日志："
echo "  tail -f /tmp/wechat_crawl.log"
echo ""
echo "查看任务："
echo "  crontab -l"
echo ""
echo "编辑任务："
echo "  crontab -e"
echo ""
