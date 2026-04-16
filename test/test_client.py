import asyncio
import httpx
from mcp.client.streamable_http import streamable_http_client
from mcp.shared.message import SessionMessage
from mcp.types import JSONRPCRequest, JSONRPCMessage

async def main():
    # 使用streamable_http_client上下文管理器
    async with streamable_http_client("http://localhost:8000") as (read_stream, write_stream, get_session_id):
        # 创建初始化请求
        init_request = JSONRPCRequest(
            jsonrpc="2.0",
            method="initialize",
            params={"protocolVersion": "2025-06-18"},
            id="init-1"
        )
        init_message = JSONRPCMessage(init_request)
        init_session_message = SessionMessage(init_message)
        
        # 发送初始化请求
        await write_stream.send(init_session_message)
        
        # 接收初始化响应
        async for message in read_stream:
            if isinstance(message, SessionMessage):
                print(f"收到初始化响应: {message.message}")
                break
        
        # 创建add_download请求
        add_download_request = JSONRPCRequest(
            jsonrpc="2.0",
            method="add_download",
            params={
                "download_url": "magnet:?xt=urn:btih:6436a4867a4935c39096d46324941818616059f0&dn=test&tr=udp://tracker.openbittorrent.com:80&tr=udp://tracker.internetwarriors.net:1337&tr=udp://tracker.leechers-paradise.org:6969&tr=udp://tracker.coppersurfer.tk:6969&tr=udp://exodus.desync.com:6969",
                "downloader_alias": "qb1",
                "save_path": "tv"
            },
            id="add-1"
        )
        add_download_message = JSONRPCMessage(add_download_request)
        add_download_session_message = SessionMessage(add_download_message)
        
        # 发送add_download请求
        await write_stream.send(add_download_session_message)
        
        # 接收add_download响应
        async for message in read_stream:
            if isinstance(message, SessionMessage):
                print(f"收到下载任务响应: {message.message}")
                break

if __name__ == "__main__":
    asyncio.run(main())