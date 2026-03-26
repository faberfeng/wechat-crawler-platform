#!/usr/bin/env python3
"""
设置 crontab 定时任务的 Python 脚本
"""
import subprocess
import os

def setup_cron():
    """设置每天早上7点的定时任务"""

    # 读取当前 crontab
    result = subprocess.run(['crontab', '-l'], capture_output=True, text=True)
    current_cron = result.stdout if result.returncode == 0 else ""

    # 过滤掉旧的抓取任务
    lines = []
    skip_empty = True
    for line in current_cron.split('\n'):
        if 'crawl_articles.py' in line:
            continue
        if line.strip() or not skip_empty:
            lines.append(line)
        skip_empty = False

    # 添加新任务
    new_task = "\n# 微信公众号定时抓取 - 每天 7:00\n"
    new_task += "0 7 * * * cd ~/Desktop/wechat-crawler-platform && python3 crawl_articles.py --account-id 1 >> /tmp/wechat_crawl.log 2>&1\n"

    new_cron = '\n'.join(lines) + new_task

    # 写入临时文件
    tmp_file = '/tmp/new_crontab'
    with open(tmp_file, 'w') as f:
        f.write(new_cron)

    # 加载新的 crontab
    result = subprocess.run(['crontab', tmp_file], capture_output=True, text=True)

    if result.returncode == 0:
        print("✓ 定时任务配置成功")
        print("\n当前 Cron 任务：")
        print(new_cron)
        print("\n配置详情：")
        print("  - 抓取时间：每天 7:00")
        print("  - 抓取对象：上海静安公众号")
        print("  - 日志文件：/tmp/wechat_crawl.log")
        print("\n查看日志：")
        print("  tail -f /tmp/wechat_crawl.log")
        print("\n查看任务：")
        print("  crontab -l")
        return True
    else:
        print(f"✗ 配置失败: {result.stderr}")
        return False

if __name__ == '__main__':
    success = setup_cron()
    if success:
        print("\n" + "="*60)
        print("✓ 定时任务设置完成！每天早上7点会自动运行")
        print("="*60)
    else:
        print("\n配置失败，请手动配置")
