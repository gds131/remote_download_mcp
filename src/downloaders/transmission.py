from .base import DownloaderBase
from transmission_rpc import Client as TransmissionClientRPC
from src.utils.log import logger

class TransmissionClient(DownloaderBase):
    """Transmission下载器客户端"""
    
    def __init__(self, url: str, username: str, password: str, alias: str = None):
        super().__init__(url, username, password, alias)
        self.client = None
    
    async def _ensure_connected(self):
        """确保连接到Transmission"""
        if self.client is None:
            try:
                # 解析url，提取host和port
                from urllib.parse import urlparse
                parsed_url = urlparse(self.url)
                host = parsed_url.hostname
                port = parsed_url.port or 9091
                
                logger.info(f"[{self.alias}] 正在连接到Transmission: {host}:{port}")
                self.client = TransmissionClientRPC(
                    host=host,
                    port=port,
                    username=self.username,
                    password=self.password
                )
                logger.info(f"[{self.alias}] 成功连接到Transmission: {host}:{port}")
            except Exception as e:
                logger.error(f"[{self.alias}] 连接Transmission失败: {str(e)}")
                raise ConnectionError(f"无法连接到Transmission: {str(e)}")
    
    async def add_torrent(self, url: str, save_path: str = None) -> dict:
        """添加下载任务"""
        await self._ensure_connected()
        try:
            logger.info(f"[{self.alias}] 添加下载任务到Transmission: {url}, 保存路径: {save_path}")
            params = {"torrent": url}
            if save_path is not None:
                params["download_dir"] = save_path
            result = self.client.add_torrent(**params)
            success = result is not None and hasattr(result, 'hashString')
            if success:
                logger.info(f"[{self.alias}] 下载任务添加成功: {url}, info_hash: {result.hashString}")
            else:
                logger.warning(f"[{self.alias}] 下载任务添加失败: {url}")
            return {"success": success, "info_hash": result.hashString if success else None, "info": result}
        except Exception as e:
            logger.error(f"[{self.alias}] 添加下载任务失败: {str(e)}")
            raise Exception(f"添加下载任务失败: {str(e)}")
    
    async def ping(self) -> bool:
        """健康检查"""
        await self._ensure_connected()
        # 尝试获取会话信息，真正测试连接是否成功
        self.client.session_stats()
        return True