import yaml
from pathlib import Path
from typing import Dict, Any
import os
from src.utils.log import logger

# 优先使用环境变量指定的配置文件路径，否则使用默认路径
CONFIG_PATH = Path(os.environ.get('CONFIG_PATH', '/app/config/downloaders.yaml'))

# 如果在开发环境中，尝试使用项目目录中的配置文件
if not CONFIG_PATH.exists():
    dev_config_path = Path(__file__).parent.parent / 'config' / 'downloaders.yaml'
    if dev_config_path.exists():
        CONFIG_PATH = dev_config_path

class DownloaderConfig:
    def __init__(self, alias: str, type_: str, url: str, username: str, password: str, save_path: str = "/downloads"):
        self.alias = alias
        self.type = type_
        self.url = url
        self.username = username
        self.password = password
        self.save_path = save_path

class ConfigManager:
    _instance = None
    _config: Dict[str, DownloaderConfig] = {}
    _default_alias: str = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._load_config()
        return cls._instance
    
    def _load_config(self):
        """从YAML文件加载配置"""
        logger.info(f"加载配置文件: {CONFIG_PATH}")
        if not CONFIG_PATH.exists():
            logger.error(f"配置文件不存在: {CONFIG_PATH}")
            raise FileNotFoundError(f"配置文件不存在: {CONFIG_PATH}")
        
        try:
            with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
            
            for alias, cfg in data.get('downloaders', {}).items():
                self._config[alias] = DownloaderConfig(
                    alias=alias,
                    type_=cfg['type'],
                    url=cfg['url'],
                    username=cfg['username'],
                    password=cfg['password'],
                    save_path=cfg.get('save_path', '/downloads')
                )
            
            self._default_alias = data.get('default_downloader')
            logger.info(f"成功加载配置，找到 {len(self._config)} 个下载器实例")
            if self._default_alias:
                logger.info(f"默认下载器: {self._default_alias}")
        except Exception as e:
            logger.error(f"加载配置文件失败: {str(e)}")
            raise
    
    def get_downloader(self, alias: str) -> DownloaderConfig:
        if alias not in self._config:
            raise ValueError(f"未知的下载器别名: {alias}，可用别名: {list(self._config.keys())}")
        return self._config[alias]
    
    def list_aliases(self) -> list[str]:
        return list(self._config.keys())
    
    def get_default(self) -> str:
        return self._default_alias

settings = ConfigManager()