import logging
import os
from pathlib import Path
from logging.handlers import RotatingFileHandler

def setup_logger(name: str = "remote-download") -> logging.Logger:
    """设置日志配置
    
    Args:
        name: 日志名称
    
    Returns:
        logging.Logger: 配置好的日志记录器
    """
    # 创建日志目录
    if os.getenv('DOCKER_ENV'):
        # Docker环境下使用固定路径
        log_dir = Path('/app/logs')
    else:
        # 本地环境下使用项目目录下的logs文件夹
        log_dir = Path(__file__).parent.parent.parent / 'logs'
    log_dir.mkdir(exist_ok=True)
    
    # 配置日志处理器
    file_handler = RotatingFileHandler(
        log_dir / 'remote-download.log',
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=5  # 保留5个备份文件
    )
    
    # 配置日志格式
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(funcName)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            file_handler
        ]
    )
    
    # 获取日志记录器
    logger = logging.getLogger(name)
    logger.info(f"日志目录: {log_dir}")
    
    return logger

# 创建默认日志记录器
logger = setup_logger()
