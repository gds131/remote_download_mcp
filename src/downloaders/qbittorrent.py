from .base import DownloaderBase
import qbittorrentapi
from src.utils.log import logger

class QBittorrentClient(DownloaderBase):
    """qBittorrent下载器客户端"""
    
    def __init__(self, url: str, username: str, password: str, alias: str = None):
        super().__init__(url, username, password, alias)
        self.client = None
    
    async def _ensure_connected(self):
        """确保连接到qBittorrent"""
        if self.client is None:
            try:
                logger.info(f"[{self.alias}] 正在连接到qBittorrent: {self.url}")
                self.client = qbittorrentapi.Client(
                    host=self.url,
                    username=self.username,
                    password=self.password
                )
                self.client.auth_log_in()
                logger.info(f"[{self.alias}] 成功连接到qBittorrent: {self.url}")
            except Exception as e:
                logger.error(f"[{self.alias}] 连接qBittorrent失败: {str(e)}")
                raise ConnectionError(f"无法连接到qBittorrent: {str(e)}")
    
    async def add_torrent(self, url: str, save_path: str = None) -> dict:
        """添加下载任务"""
        await self._ensure_connected()
        try:
            logger.info(f"[{self.alias}] 添加下载任务到qBittorrent: {url}, 保存路径: {save_path}")
            params = {"urls": url}
            if save_path is not None:
                params["save_path"] = save_path
            result = self.client.torrents_add(**params)
            success = result == "Ok."
            if success:
                logger.info(f"[{self.alias}] 下载任务添加成功: {url}")
            else:
                logger.warning(f"[{self.alias}] 下载任务添加失败: {url}, 结果: {result}")
            return {"success": success, "info": result}
        except Exception as e:
            logger.error(f"[{self.alias}] 添加下载任务失败: {str(e)}")
            raise Exception(f"添加下载任务失败: {str(e)}")
    
    async def ping(self) -> bool:
        """健康检查"""
        await self._ensure_connected()
        return True