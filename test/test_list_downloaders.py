#!/usr/bin/env python3
"""测试 list_downloaders 函数"""
import asyncio
import sys
import os
from pathlib import Path

# 添加项目根目录到Python路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.server import list_downloaders

async def main():
    """测试 list_downloaders 函数"""
    print("测试 list_downloaders 函数...")
    result = await list_downloaders()
    print("list_downloaders 返回结果:")
    print(result)
    print("\n格式说明:")
    print("- aliases: 下载器别名列表")
    print("- default: 默认下载器别名")
    print("- count: 下载器数量")

if __name__ == "__main__":
    asyncio.run(main())