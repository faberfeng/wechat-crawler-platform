#!/bin/bash

# 快速添加微信文章链接脚本
# 支持从剪贴板、命令行参数或交互式输入

PROJECT_DIR="$HOME/Desktop/wechat-crawler-platform"
CONFIG_FILE="$PROJECT_DIR/config/article_urls.txt"
ACCOUNT_ID=1  # 默认公众号 ID（上海静安）

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}=========================================="
echo -e "微信文章链接快速添加工具"
echo -e "==========================================${NC}"
echo ""

# 确保 config 目录存在
mkdir -p "$(dirname "$CONFIG_FILE")"

# 函数：显示帮助
show_help() {
    echo -e "${YELLOW}使用方法：${NC}"
    echo ""
    echo "  $0 [选项]"
    echo ""
    echo "选项："
    echo "  -l, --link URL      添加单个文章链接"
    echo "  -L, --links URL1,URL2  添加多个文章链接（逗号分隔）"
    echo "  -p, --paste         从剪贴板读取链接"
    echo "  -i, --interactive   交互式输入链接"
    echo "  -s, --show          显示当前配置文件"
    echo "  -c, --clear         清空配置"
    echo "  -a, --account ID    指定公众号 ID（默认: 1）"
    echo "  -r, --run           添加后立即运行抓取"
    echo "  -h, --help          显示此帮助信息"
    echo ""
    echo "示例："
    echo "  $0 --link 'https://mp.weixin.qq.com/s/xxx'"
    echo "  $0 --paste --run"
    echo "  $0 --interactive"
}

# 函数：从剪贴板读取（Mac）
paste_from_clipboard() {
    if command -v pbpaste &> /dev/null; then
        pbpaste
    elif command -v xclip &> /dev/null; then
        xclip -selection clipboard -o
    elif command -v xsel &> /dev/null; then
        xsel --clipboard --output
    else
        echo "❌ 无法访问剪贴板，不支持你的系统"
        return 1
    fi
}

# 函数：显示当前配置
show_config() {
    if [ -f "$CONFIG_FILE" ]; then
        echo -e "${YELLOW}当前配置：${NC}"
        cat "$CONFIG_FILE"
        echo ""
    else
        echo "配置文件不存在，还没有配置任何链接"
    fi
}

# 函数：清空配置
clear_config() {
    if [ -f "$CONFIG_FILE" ]; then
        backup_file="${CONFIG_FILE}.backup.$(date +%Y%m%d_%H%M%S)"
        cp "$CONFIG_FILE" "$backup_file"
        echo -e "${GREEN}✓ 配置已备份到: $backup_file${NC}"

        echo "" > "$CONFIG_FILE"
        echo -e "${GREEN}✓ 配置已清空${NC}"
    else
        echo "配置文件不存在"
    fi
}

# 函数：添加链接到配置
add_links() {
    local new_urls="$1"
    local account_id="$2"

    # 验证链接格式
    if [[ ! "$new_urls" =~ ^https?://mp\.weixin\.qq\.com/s/ ]]; then
        echo -e "${YELLOW}⚠️  警告: 链接格式可能不正确${NC}"
        echo "正确的格式应该是: https://mp.weixin.qq.com/s/xxx"
    fi

    # 读取现有配置
    existing_links=""
    if [ -f "$CONFIG_FILE" ]; then
        while IFS='=' read -r id urls; do
            if [[ "$id" == "$ACCOUNT_ID" ]]; then
                existing_links="$urls"
            fi
        done < "$CONFIG_FILE"
    fi

    # 合并新旧链接
    if [ -n "$existing_links" ]; then
        # 去重
        all_links="$existing_links,$new_urls"
        unique_links=$(echo "$all_links" | tr ',' '\n' | sort -u | tr '\n' ',' | sed 's/,$//')
    else
        unique_links="$new_urls"
    fi

    # 限制链接数量（最多100个）
    link_count=$(echo "$unique_links" | tr ',' '\n' | wc -l | awk '{print $1}')
    if [ "$link_count" -gt 100 ]; then
        echo -e "${YELLOW}⚠️  警告: 链接数量过多，仅保留最新的100个${NC}"
        unique_links=$(echo "$unique_links" | tr ',' '\n' | tail -100 | tr '\n' ',' | sed 's/,$//')
    fi

    # 更新配置文件
    # 保留其他账号的配置
    temp_file=$(mktemp)
    if [ -f "$CONFIG_FILE" ]; then
        while IFS='=' read -r id urls; do
            if [[ "$id" != "$account_id" ]]; then
                echo "$id=$urls" >> "$temp_file"
            fi
        done < "$CONFIG_FILE"
    fi

    # 添加更新后的配置
    echo "$account_id=$unique_links" >> "$temp_file"

    # 移动到原位置
    mv "$temp_file" "$CONFIG_FILE"

    echo ""
    echo -e "${GREEN}✓ 链接添加成功！${NC}"
    echo ""
    echo "公众号 ID: $account_id"
    echo "添加链接数: $(echo "$new_urls" | tr ',' '\n' | wc -l | awk '{print $1}')"
    echo "总链接数: $(echo "$unique_links" | tr ',' '\n' | wc -l | awk '{print $1}')"
    echo "配置文件: $CONFIG_FILE"
}

# 函数：运行抓取
run_crawl() {
    echo ""
    echo -e "${BLUE}=========================================="
    echo -e "运行抓取任务"
    echo -e "==========================================${NC}"
    echo ""

    cd "$PROJECT_DIR"

    # 显示将要抓取的链接
    if [ -f "$CONFIG_FILE" ]; then
        echo -e "${YELLOW}将要抓取的链接：${NC}"
        while IFS='=' read -r id urls; do
            if [[ "$id" == "$ACCOUNT_ID" ]]; then
                count=$(echo "$urls" | tr ',' '\n' | wc -l | awk '{print $1}')
                echo "公众号 ID $id: $count 个链接"
            fi
        done < "$CONFIG_FILE"
    fi

    echo ""
    echo "开始抓取..."
    echo ""

    # 运行抓取
    python3 crawl_articles.py --account-id "$ACCOUNT_ID"
}

# 主程序

# 解析参数
LINKS=""
INTERACTIVE=false
SHOW=false
CLEAR=false
RUN_CRAWL=false

while [[ $# -gt 0 ]]; do
    case $1 in
        -l|--link)
            if [ -n "$2" ]; then
                LINKS="$2"
                shift 2
            else
                echo "错误: --link 需要一个参数"
                exit 1
            fi
            ;;
        -L|--links)
            if [ -n "$2" ]; then
                LINKS="$2"
                shift 2
            else
                echo "错误: --links 需要一个参数"
                exit 1
            fi
            ;;
        -p|--paste)
            clipboard_content=$(paste_from_clipboard)
            if [ $? -eq 0 ]; then
                echo -e "${YELLOW}从剪贴板读取到:${NC}"
                echo "$clipboard_content"
                echo ""
                LINKS="$clipboard_content"
            fi
            shift
            ;;
        -i|--interactive)
            INTERACTIVE=true
            shift
            ;;
        -s|--show)
            SHOW=true
            shift
            ;;
        -c|--clear)
            CLEAR=true
            shift
            ;;
        -a|--account)
            if [ -n "$2" ]; then
                ACCOUNT_ID="$2"
                shift 2
            else
                echo "错误: --account 需要一个参数"
                exit 1
            fi
            ;;
        -r|--run)
            RUN_CRAWL=true
            shift
            ;;
        -h|--help)
            show_help
            exit 0
            ;;
        *)
            echo "未知选项: $1"
            show_help
            exit 1
            ;;
    esac
done

# 执行命令

if $SHOW; then
    show_config
    exit 0
fi

if $CLEAR; then
    clear_config
    exit 0
fi

# 交互式输入
if $INTERACTIVE; then
    echo -e "${YELLOW}请输入文章链接（多个链接用空格或逗号分隔）：${NC}"
    echo -e "提示: 也可以先复制链接，然后使用 --paste 选项"
    echo ""
    read -p "> " input_links

    if [ -z "$input_links" ]; then
        echo -e "${YELLOW}⚠️  未输入任何链接${NC}"
        exit 0
    fi

    # 将空格转换为逗号
    input_links=$(echo "$input_links" | tr ' ' ',')

    LINKS="$input_links"
fi

# 如果没有提供链接，尝试从剪贴板
if [ -z "$LINKS" ]; then
    echo ""
    echo -e "${YELLOW}未提供链接，尝试从剪贴板读取...${NC}"

    clipboard_content=$(paste_from_clipboard)
    if [ $? -eq 0 ] && [ -n "$clipboard_content" ]; then
        echo -e "${GREEN}✓ 从剪贴板读取到:${NC}"
        echo "$clipboard_content"
        echo ""
        read -p "是否使用此链接？[Y/n]: " use_clipboard

        if [[ ! "$use_clipboard" =~ ^[Nn]$ ]]; then
            LINKS="$clipboard_content"
        else
            echo "已取消"
            exit 0
        fi
    else
        echo -e "${YELLOW}⚠️  剪贴板为空或无法读取${NC}"
        echo ""
        echo "使用方法："
        echo "  1. 复制微信文章链接"
        echo "  2. 运行: $0 --paste"
        echo "  3. 或运行: $0 --link '链接地址'"
        echo ""
        exit 0
    fi
fi

# 添加链接
add_links "$LINKS" "$ACCOUNT_ID"

# 运行抓取
if $RUN_CRAWL; then
    run_crawl
fi

echo ""
echo -e "${GREEN}=========================================="
echo -e "完成！"
echo -e "==========================================${NC}"
echo ""
echo -e "下次自动运行: ${YELLOW}每天早上7:00${NC}"
echo -e "查看日志: ${BLUE}tail -f /tmp/wechat_crawl.log${NC}"
echo -e "手动运行: ${BLUE}python3 crawl_articles.py --account-id $ACCOUNT_ID${NC}"
