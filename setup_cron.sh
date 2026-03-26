#!/bin/bash

# 微信公众号抓取定时任务配置脚本
# 提供交互式配置界面

set -e

PROJECT_DIR="$HOME/Desktop/wechat-crawler-platform"
SCRIPT_PATH="$PROJECT_DIR/crawl_articles.py"
LOG_PATH="/tmp/wechat_crawl.log"

echo "=========================================="
echo "微信公众号抓取定时任务配置"
echo "=========================================="
echo ""

# 检查脚本是否存在
if [ ! -f "$SCRIPT_PATH" ]; then
    echo "❌ 错误：找不到抓取脚本 $SCRIPT_PATH"
    exit 1
fi

# 检查权限
if [ ! -x "$SCRIPT_PATH" ]; then
    echo "⚠️  警告：脚本没有执行权限，正在修复..."
    chmod +x "$SCRIPT_PATH"
    echo "✓ 权限已修复"
fi

echo "请选择抓取模式："
echo ""
echo "1) 抓取所有活跃公众号"
echo "2) 仅抓取'上海静安'公众号 (ID: 1)"
echo ""
read -p "请输入选项 [1-2]: " mode

if [ "$mode" = "1" ]; then
    MODE_ARG="--all"
    MODE_NAME="所有公众号"
elif [ "$mode" = "2" ]; then
    MODE_ARG="--account-id 1"
    MODE_NAME="上海静安公众号"
else
    echo "❌ 无效选项"
    exit 1
fi

echo ""
echo "请选择抓取频率："
echo ""
echo "1) 每天 9:00 抓取一次"
echo "2) 每天 9:00 和 18:00 各抓取一次（推荐）"
echo "3) 每 2 小时抓取一次"
echo "4) 每 4 小时抓取一次（最多 10 篇）"
echo ""
read -p "请输入选项 [1-4]: " freq

case $freq in
    1)
        CRON_EXPR="0 9 * * *"
        FREQ_DESC="每天 9:00"
        LIMIT_ARG=""
        ;;
    2)
        CRON_EXPR="0 9,18 * * *"
        FREQ_DESC="每天 9:00 和 18:00"
        LIMIT_ARG=""
        ;;
    3)
        CRON_EXPR="0 */2 * * *"
        FREQ_DESC="每 2 小时"
        LIMIT_ARG=""
        ;;
    4)
        CRON_EXPR="0 */4 * * *"
        FREQ_DESC="每 4 小时（最多 10 篇）"
        LIMIT_ARG="--limit 10"
        ;;
    *)
        echo "❌ 无效选项"
        exit 1
        ;;
esac

echo ""
echo "=========================================="
echo "配置确认"
echo "=========================================="
echo ""
echo "抓取对象：$MODE_NAME"
echo "抓取频率：$FREQ_DESC"
echo ""

read -p "确认配置？[Y/n]: " confirm

if [[ "$confirm" =~ ^[Nn]$ ]]; then
    echo "已取消"
    exit 0
fi

# 构建完整的 Cron 命令
CRON_CMD="$CRON_EXPR cd $PROJECT_DIR && python3 $SCRIPT_PATH $MODE_ARG $LIMIT_ARG >> $LOG_PATH 2>&1"

# 备份当前 crontab
if [ -f ~/.crontab.backup ]; then
    cp ~/.crontab.backup ~/.crontab.backup.old
fi
crontab -l 2>/dev/null > ~/.crontab.backup 2>&1 || true

# 检查是否已存在相同的任务
if grep -q "crawl_articles.py" ~/.crontab.backup 2>/dev/null; then
    echo ""
    echo "⚠️  检测到已存在的抓取任务："
    echo ""
    grep -n "crawl_articles.py" ~/.crontab.backup | sed 's/^/  /'
    echo ""
    read -p "是否删除现有任务并重新配置？[Y/n]: " replace

    if [[ "$replace" =~ ^[Nn]$ ]]; then
        echo "已取消，现有任务保持不变"
        exit 0
    fi

    # 删除现有任务
    crontab -l 2>/dev/null | grep -v "crawl_articles.py" | crontab -
fi

# 添加新任务
(crontab -l 2>/dev/null; echo "$CRON_CMD") | crontab -

echo ""
echo "=========================================="
echo "✓ 配置完成！"
echo "=========================================="
echo ""
echo "Cron 任务："
echo "  $CRON_CMD"
echo ""
echo "日志文件："
echo "  $LOG_PATH"
echo ""
echo "查看日志："
echo "  tail -f $LOG_PATH"
echo ""
echo "查看 Cron 任务："
echo "  crontab -l"
echo ""
echo "删除 Cron 任务："
echo "  crontab -e  (手动删除对应行)"
echo "  或: crontab -r  (删除所有)"
echo ""

read -p "是否立即运行一次测试抓取？[Y/n]: " test_run

if [[ ! "$test_run" =~ ^[Nn]$ ]]; then
    echo ""
    echo "正在运行测试抓取..."
    echo ""

    cd $PROJECT_DIR

    if [ "$MODE_ARG" = "--all" ]; then
        python3 $SCRIPT_PATH $MODE_ARG $LIMIT_ARG | head -30
    else
        python3 $SCRIPT_PATH $MODE_ARG $LIMIT_ARG
    fi

    if [ $? -eq 0 ]; then
        echo ""
        echo "✓ 测试抓取完成"
    else
        echo ""
        echo "❌ 测试抓取失败"
    fi

    echo ""
    echo "查看详细日志：tail $LOG_PATH"
fi

echo ""
echo "=========================================="
echo "定时任务配置完成"
echo "=========================================="
