#!/usr/bin/env python3
"""测试健康检查功能"""
import asyncio
import sys
import os
from pathlib import Path

# 添加项目根目录到Python路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.server import health_check

async def main():
    """测试健康检查"""
    print("开始测试健康检查...")
    result = await health_check()
    print("健康检查结果:")
    print(f"服务状态: {result['status']}")
    print("\n下载器状态:")
    for alias, info in result['downloaders'].items():
        print(f"{alias}: {info['status']}")
        if 'url' in info:
            print(f"  URL: {info['url']}")
        if 'username' in info:
            print(f"  用户名: {info['username']}")

if __name__ == "__main__":
    asyncio.run(main())