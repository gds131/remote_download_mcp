import os
import asyncio
import sys
from mcp.server.fastmcp import FastMCP
from src.config import settings
from src.downloaders.qbittorrent import QBittorrentClient
from src.downloaders.transmission import TransmissionClient
from src.utils import join_paths
from src.utils.log import logger

mcp = FastMCP("remote-download", host="0.0.0.0")

# 下载器实例缓存
_downloader_instances: dict[str, any] = {}

def get_downloader(alias: str):
    """根据别名获取或创建下载器实例"""
    if alias not in _downloader_instances:
        cfg = settings.get_downloader(alias)
        
        if cfg.type == "qbittorrent":
            _downloader_instances[alias] = QBittorrentClient(
                url=cfg.url,
                username=cfg.username,
                password=cfg.password,
                alias=alias
            )
        elif cfg.type == "transmission":
            _downloader_instances[alias] = TransmissionClient(
                url=cfg.url,
                username=cfg.username,
                password=cfg.password,
                alias=alias
            )
        else:
            raise ValueError(f"不支持的下载器类型: {cfg.type}")
    
    return _downloader_instances[alias]

@mcp.tool()
async def add_download(
    download_url: str,
    downloader_alias: str,
    save_path: str = None
) -> dict:
    """
    提交资源到远端下载器进行下载。
    
    使用场景：用户提供了 magnet/http/ftp 下载链接时使用。
    
    参数说明：
        download_url: 资源下载地址，支持格式：
            - magnet: magnet:?xt=urn:btih:...
            - http/https: http://example.com/file.torrent
            - ftp: ftp://example.com/file.iso
        downloader_alias: 下载器别名，是用户提前维护的qb/tr下载器的配置，
            不可猜测，常见示例：qb1, qb2, tr1, tr-home（完全取决于用户配置）
        save_path: 相对保存路径（可选），基于下载器根目录拼接，
            示例："movies", "tvshows/season1", "software"，不传则使用下载器默认路径
    
    工作流程：
        1. 若用户未提供 downloader_alias → 调用 list_downloaders 获取默认下载器别名
        2. 若用户未提供 save_path → 则使用默认路径
        3. 确认后调用本工具提交任务
    
    限制说明：
        - 本工具仅提交下载任务，不返回下载进度、速度、状态
        - 不支持暂停、恢复、删除等任务管理操作
        - 保存路径为相对路径，最终路径由服务端拼接配置中的根目录
    
    响应示例：
        成功：{"success": true, "message": "下载任务已提交", "downloader": "qb1", "save_path": "/downloads/movies"}
        失败：{"success": false, "message": "下载任务提交失败", "info": "错误详情"}
    """
    logger.info(f"收到下载任务请求: {download_url}, 下载器: {downloader_alias}, 保存路径: {save_path}")
    
    # 获取下载器配置
    cfg = settings.get_downloader(downloader_alias)
    downloader = get_downloader(downloader_alias)
    
    # 拼接保存路径
    final_save_path = join_paths(cfg.save_path, save_path)
    logger.info(f"拼接后的保存路径: {final_save_path}")
    
    try:
        result = await downloader.add_torrent(
            url=download_url,
            save_path=final_save_path
        )
        success = result.get("success", False)
        if success:
            logger.info(f"下载任务提交成功: {download_url}")
        else:
            logger.warning(f"下载任务提交失败: {download_url}")
        return {
            "success": success,
            "message": "下载任务已提交" if success else "下载任务提交失败",
            "downloader": downloader_alias,
            "save_path": final_save_path,
            "info": result.get("info")
        }
    except Exception as e:
        logger.error(f"提交下载任务时发生错误: {str(e)}")
        raise

@mcp.tool()
async def list_downloaders() -> dict:
    """列出所有配置的下载器别名"""
    return {
        "aliases": settings.list_aliases(),
        "default": settings.get_default(),
        "count": len(settings.list_aliases())
    }

@mcp.tool()
async def health_check():
    """
    检查服务端与所有配置下载器的连接状态。
    
    使用场景：
        1. 用户反馈下载失败或提交无响应时
        2. 诊断下载器连接问题
        3. 验证服务可用性
    
    响应内容：
        - status: "ok"（至少一个下载器可用）或 "degraded"（全部不可用）
        - downloaders: 各下载器的连接状态，"connected" 或 "disconnected: 错误信息"
    
    注意：本工具不返回下载任务状态，仅检测服务端到下载器的网络连接。
    """
    downloaders_info = {}
    
    async def check_downloader(alias):
        try:
            # 获取下载器配置
            cfg = settings.get_downloader(alias)
            # 测试连接
            dl = get_downloader(alias)
            # 使用to_thread包装同步操作，确保并行执行
            await asyncio.to_thread(lambda: asyncio.run(dl.ping()))
            # 构建下载器信息
            return alias, {
                "alias": alias,
                "status": "connected",
                "type": cfg.type,
                "url": cfg.url,
                "username": cfg.username,
                "save_path": cfg.save_path
            }
        except Exception as e:
            # 获取下载器配置（即使连接失败）
            try:
                cfg = settings.get_downloader(alias)
                return alias, {
                    "alias": alias,
                    "status": f"disconnected: {str(e)}",
                    "type": cfg.type,
                    "url": cfg.url,
                    "username": cfg.username,
                    "save_path": cfg.save_path
                }
            except Exception:
                return alias, {
                    "status": f"error: {str(e)}"
                }
    
    # 并行测试所有下载器
    results = await asyncio.gather(*[check_downloader(alias) for alias in settings.list_aliases()])
    
    # 整理结果
    for alias, info in results:
        downloaders_info[alias] = info
    
    return {
        "status": "ok" if any(info.get("status") == "connected" for info in downloaders_info.values()) else "degraded",
        "downloaders": downloaders_info
    }

if __name__ == "__main__":
    # 启动前验证下载器连通性
    logger.info("启动前验证下载器连通性...")
    try:
        # 运行 health_check 函数验证下载器连接
        result = asyncio.run(health_check())
        logger.info(f"下载器连通性验证结果: {result}")
        
        # 检查是否有可用的下载器
        if result.get("status") == "ok":
            logger.info("至少有一个下载器连接正常，服务启动中...")
        else:
            logger.error("所有下载器连接失败，服务将停止启动。")
            sys.exit(1)
            
    except Exception as e:
        logger.error(f"验证下载器连通性时发生错误: {str(e)}")
        logger.error("服务将停止启动。")
        sys.exit(1)
    
    # 启动 MCP 服务
    mcp.run(transport="sse")
