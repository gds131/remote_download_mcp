import asyncio
from mcp.client.http import HTTPClient

async def main():
    # 创建MCP客户端
    client = HTTPClient(url="http://localhost:8000", transport="streamable-http")
    
    # 连接到MCP服务
    await client.connect()
    
    try:
        # 调用add_download工具
        result = await client.call("add_download", {
            "download_url": "magnet:?xt=urn:btih:6436a4867a4935c39096d46324941818616059f0&dn=test&tr=udp://tracker.openbittorrent.com:80&tr=udp://tracker.internetwarriors.net:1337&tr=udp://tracker.leechers-paradise.org:6969&tr=udp://tracker.coppersurfer.tk:6969&tr=udp://exodus.desync.com:6969",
            "downloader_alias": "qb1",
            "save_path": "tv"
        })
        
        print("下载任务提交结果:")
        print(result)
    finally:
        # 关闭连接
        await client.disconnect()

if __name__ == "__main__":
    asyncio.run(main())