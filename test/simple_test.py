import asyncio
from mcp.client.streamable_http import StreamableHTTPTransport
import anyio
from anyio.streams.memory import MemoryObjectReceiveStream, MemoryObjectSendStream
from mcp.shared.message import SessionMessage
from mcp.types import JSONRPCRequest, JSONRPCMessage

async def main():
    # 创建传输层
    transport = StreamableHTTPTransport("http://localhost:8000/mcp")
    
    # 创建内存流
    read_stream_writer, read_stream = anyio.create_memory_object_stream[SessionMessage | Exception](0)
    write_stream, write_stream_reader = anyio.create_memory_object_stream[SessionMessage](0)
    
    # 创建HTTP客户端
    import httpx
    client = httpx.AsyncClient()
    
    try:
        # 读取流的任务
        async def read_from_stream():
            async for message in read_stream:
                print(f"收到消息: {message}")
        
        # 启动读取任务
        async with anyio.create_task_group() as tg:
            tg.start_soon(read_from_stream)
            
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
            ctx = type('Context', (), {
                'client': client,
                'session_id': transport.session_id,
                'session_message': init_session_message,
                'metadata': None,
                'read_stream_writer': read_stream_writer
            })()
            
            await transport._handle_post_request(ctx)
            
            # 等待一段时间
            await asyncio.sleep(2)
            
    finally:
        # 清理资源
        await client.aclose()
        await read_stream_writer.aclose()
        await write_stream.aclose()

if __name__ == "__main__":
    asyncio.run(main())