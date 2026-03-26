#!/usr/bin/env python3
"""
快速添加微信文章链接（Python版本）
支持从剪贴板、文件、命令行等多种方式
"""

import os
import sys
import subprocess
from pathlib import Path

PROJECT_DIR = Path.home() / "Desktop" / "wechat-crawler-platform"
CONFIG_FILE = PROJECT_DIR / "config" / "article_urls.txt"
ACCOUNT_ID = 1  # 默认公众号 ID


class Colors:
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    RED = '\033[0;31m'
    NC = '\033[0m'

    @classmethod
    def print(cls, color, text):
        print(f"{color}{text}{cls.NC}")


def paste_from_clipboard():
    """从剪贴板读取链接"""
    try:
        if sys.platform == 'darwin':  # macOS
            result = subprocess.run(['pbpaste'], capture_output=True, text=True)
            if result.returncode == 0:
                return result.stdout.strip()
        elif sys.platform.startswith('linux'):
            # 尝试 xclip 或 xsel
            for cmd in [['xclip', '-selection', 'clipboard', '-o'],
                       ['xsel', '--clipboard', '--output']]:
                try:
                    result = subprocess.run(cmd, capture_output=True, text=True)
                    if result.returncode == 0:
                        return result.stdout.strip()
                except FileNotFoundError:
                    continue
    except Exception as e:
        print(f"无法访问剪贴板: {e}")

    return None


def show_config():
    """显示当前配置"""
    if CONFIG_FILE.exists():
        Colors.print(Colors.YELLOW, "当前配置：")
        print(CONFIG_FILE.read_text(encoding='utf-8'))
    else:
        print("配置文件不存在，还没有配置任何链接")


def clear_config():
    """清空配置"""
    if CONFIG_FILE.exists():
        backup_file = str(CONFIG_FILE) + f".backup.{os.popen('date +%Y%m%d_%H%M%S').read().strip()}"

        import shutil
        shutil.copy(CONFIG_FILE, backup_file)
        Colors.print(Colors.GREEN, f"✓ 配置已备份到: {backup_file}")

        CONFIG_FILE.write_text("")
        Colors.print(Colors.GREEN, "✓ 配置已清空")
    else:
        print("配置文件不存在")


def add_links(urls, account_id=ACCOUNT_ID):
    """添加链接到配置"""

    # 验证链接格式
    valid_urls = []
    for url in urls:
        url = url.strip()
        if not url:
            continue

        if not url.startswith('https://mp.weixin.qq.com/s/'):
            Colors.print(Colors.YELLOW, f"⚠️  警告: 链接格式可能不正确: {url[:50]}...")

        valid_urls.append(url)

    if not valid_urls:
        Colors.print(Colors.RED, "❌ 没有有效的链接")
        return False

    # 读取现有配置
    existing_lines = {}
    if CONFIG_FILE.exists():
        for line in CONFIG_FILE.read_text(encoding='utf-8').strip().split('\n'):
            if '=' in line and not line.startswith('#'):
                id_, urls_line = line.split('=', 1)
                existing_lines[id_.strip()] = urls_line.strip()

    # 获取现有链接
    existing_urls = existing_lines.get(str(account_id), "")

    # 合并新旧链接
    if existing_urls:
        all_urls_list = existing_urls.split(',') + valid_urls
        # 去重
        unique_urls = list(dict.fromkeys(all_urls_list))
    else:
        unique_urls = valid_urls

    # 限制链接数量
    max_urls = 100
    if len(unique_urls) > max_urls:
        Colors.print(Colors.YELLOW, f"⚠️  警告: 链接数量过多，仅保留最新的{max_urls}个")
        unique_urls = unique_urls[-max_urls:]

    # 更新配置
    existing_lines[str(account_id)] = ','.join(unique_urls)

    # 写入文件
    CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        for id_, urls_line in existing_lines.items():
            f.write(f"{id_}={urls_line}\n")

    # 显示结果
    print()
    Colors.print(Colors.GREEN, "✓ 链接添加成功！")
    print()
    print(f"公众号 ID: {account_id}")
    print(f"添加链接数: {len(valid_urls)}")
    print(f"总链接数: {len(unique_urls)}")
    print(f"配置文件: {CONFIG_FILE}")

    return True


def run_crawl(account_id=ACCOUNT_ID):
    """运行抓取任务"""
    print()
    Colors.print(Colors.BLUE, "=" * 50)
    Colors.print(Colors.BLUE, "运行抓取任务")
    Colors.print(Colors.BLUE, "=" * 50)
    print()

    os.chdir(PROJECT_DIR)

    # 显示将要抓取的链接
    if CONFIG_FILE.exists():
        Colors.print(Colors.YELLOW, "将要抓取的链接：")
        for line in CONFIG_FILE.read_text(encoding='utf-8').strip().split('\n'):
            if '=' in line and not line.startswith('#'):
                id_, urls = line.split('=', 1)
                if int(id_.strip()) == account_id:
                    link_count = len(urls.split(','))
                    print(f"公众号 ID {id_}: {link_count} 个链接")

    print()
    print("开始抓取...")
    print()

    # 运行抓取
    import subprocess
    result = subprocess.run([
        sys.executable,
        'crawl_articles.py',
        '--account-id', str(account_id)
    ], cwd=PROJECT_DIR)

    return result.returncode == 0


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description='微信文章链接快速添加工具（Python版本）',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s --link 'https://mp.weixin.qq.com/s/xxx'
  %(prog)s --paste --run
  %(prog)s --interactive
  %(prog)s --file links.txt
        """
    )

    parser.add_argument('-l', '--link', help='添加单个文章链接')
    parser.add_argument('-L', '--links', help='添加多个文章链接（逗号分隔）')
    parser.add_argument('-f', '--file', help='从文件读取链接（一行一个）')
    parser.add_argument('-p', '--paste', action='store_true', help='从剪贴板读取链接')
    parser.add_argument('-i', '--interactive', action='store_true', help='交互式输入链接')
    parser.add_argument('-s', '--show', action='store_true', help='显示当前配置')
    parser.add_argument('-c', '--clear', action='store_true', help='清空配置')
    parser.add_argument('-a', '--account', type=int, default=ACCOUNT_ID, help=f'指定公众号 ID（默认: {ACCOUNT_ID}）')
    parser.add_argument('-r', '--run', action='store_true', help='添加后立即运行抓取')

    args = parser.parse_args()

    Colors.print(Colors.BLUE, "=" * 50)
    Colors.print(Colors.BLUE, "微信文章链接快速添加工具")
    Colors.print(Colors.BLUE, "=" * 50)
    print()

    # 显示配置
    if args.show:
        show_config()
        sys.exit(0)

    # 清空配置
    if args.clear:
        clear_config()
        sys.exit(0)

    # 收集链接
    urls = []

    # 从文件读取
    if args.file:
        file_path = Path(args.file)
        if not file_path.exists():
            Colors.print(Colors.RED, f"❌ 文件不存在: {file_path}")
            sys.exit(1)

        file_urls = file_path.read_text(encoding='utf-8').strip().split('\n')
        # 跳过注释行和空行
        urls.extend(u.strip() for u in file_urls if u.strip() and not u.strip().startswith('#'))

        Colors.print(Colors.GREEN, f"✓ 从文件读取到 {len(urls)} 个链接")

    # 从命令行参数
    if args.link:
        urls.append(args.link)

    if args.links:
        urls.extend([u.strip() for u in args.links.split(',')])

    # 从剪贴板
    if args.paste:
        Clipboard = paste_from_clipboard()
        if Clipboard:
            Colors.print(Colors.YELLOW, "从剪贴板读取到:")
            print(Clipboard)
            print()

            response = input("是否使用此链接？[Y/n]: ")
            if not response.lower().startswith('n'):
                urls.append(Clipboard)
            else:
                print("已取消")
                sys.exit(0)
        else:
            Colors.print(Colors.YELLOW, "⚠️  剪贴板为空或无法读取")

    # 交互式输入
    if args.interactive:
        print()
        Colors.print(Colors.YELLOW, "请输入文章链接（多个链接用空格或逗号分隔）：")
        print("提示: 也可以先复制链接，然后使用 --paste 选项")
        print()

        try:
            input_links = input("> ")
            if input_links.strip():
                # 将空格和逗号都作为分隔符
                input_urls = [u.strip() for u in input_links.replace(',', ' ').split() if u.strip()]
                urls.extend(input_urls)
        except KeyboardInterrupt:
            print("\n\n已取消")
            sys.exit(0)

    # 如果没有链接，尝试从剪贴板
    if not urls:
        print()
        Colors.print(Colors.YELLOW, "未提供链接，尝试从剪贴板读取...")

        Clipboard = paste_from_clipboard()
        if Clipboard:
            Colors.print(Colors.GREEN, "✓ 从剪贴板读取到:")
            print(Clipboard)
            print()

            response = input("是否使用此链接？[Y/n]: ")
            if not response.lower().startswith('n'):
                urls.append(Clipboard)
            else:
                print("已取消")
                sys.exit(0)
        else:
            Colors.print(Colors.RED, "❌ 没有可用的链接")
            print()
            print("使用方法：")
            print("  1. 复制微信文章链接")
            print("  2. 运行: python quick_add.py --paste")
            print("  3. 或运行: python quick_add.py --link '链接地址'")
            print()
            sys.exit(1)

    # 添加链接
    success = add_links(urls, args.account)

    if success:
        # 运行抓取
        if args.run:
            run_crawl(args.account)
        else:
            print()
            Colors.print(Colors.GREEN, "=" * 50)
            Colors.print(Colors.GREEN, "完成！")
            Colors.print(Colors.GREEN, "=" * 50)
            print()
            Colors.print(Colors.YELLOW, f"下次自动运行: 每天早上7:00")
            Colors.print(Colors.BLUE, "查看日志: tail -f /tmp/wechat_crawl.log")
            Colors.print(Colors.BLUE, f"手动运行: python crawl_articles.py --account-id {args.account}")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n已取消")
        sys.exit(0)
    except Exception as e:
        print(f"\n错误: {e}", file=sys.stderr)
        sys.exit(1)
