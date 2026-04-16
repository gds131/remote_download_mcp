from abc import ABC, abstractmethod

class DownloaderBase(ABC):
    """下载器抽象基类"""
    
    def __init__(self, url: str, username: str, password: str, alias: str = None):
        self.url = url
        self.username = username
        self.password = password
        self.alias = alias
    
    @abstractmethod
    async def add_torrent(self, url: str, save_path: str) -> dict:
        """添加下载任务"""
        pass
    
    @abstractmethod
    async def ping(self) -> bool:
        """健康检查"""
        pass