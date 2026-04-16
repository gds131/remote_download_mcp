import asyncio
import sys
import os
from pathlib import Path

# 添加项目根目录到Python路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.server import add_download

async def main():
    # 直接调用add_download函数
    result = await add_download(
        download_url="magnet:?xt=urn:btih:6436a4867a4935c39096d46324941818616059f0&dn=test&tr=udp://tracker.openbittorrent.com:80&tr=udp://tracker.internetwarriors.net:1337&tr=udp://tracker.leechers-paradise.org:6969&tr=udp://tracker.coppersurfer.tk:6969&tr=udp://exodus.desync.com:6969",
        downloader_alias="qb1",
        save_path="tv"
    )
    
    print("下载任务提交结果:")
    print(result)

if __name__ == "__main__":
    asyncio.run(main())