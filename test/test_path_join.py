import sys
import os
from pathlib import Path

# 添加项目根目录到Python路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.config import ConfigManager

# 测试路径拼接功能
ConfigManager._instance = None
config = ConfigManager()

# 获取下载器配置
qb_config = config.get_downloader('qb1')
print(f"qBittorrent save_path: {qb_config.save_path}")

tr_config = config.get_downloader('tr1')
print(f"Transmission save_path: {tr_config.save_path}")

# 测试路径拼接逻辑
def test_path_join(base_path, user_path):
    final_path = base_path
    if user_path:
        final_path = final_path.rstrip('/')
        user_path = user_path.lstrip('/')
        if user_path:
            final_path = f"{final_path}/{user_path}"
    return final_path

# 测试不同场景
test_cases = [
    ("/downloads", None, "/downloads"),
    ("/downloads", "", "/downloads"),
    ("/downloads", "/", "/downloads"),
    ("/downloads", "test", "/downloads/test"),
    ("/downloads", "/test", "/downloads/test"),
    ("/downloads/", "test", "/downloads/test"),
    ("/downloads", "test/path", "/downloads/test/path"),
    ("/downloads/", "/test/path", "/downloads/test/path"),
]

print("\n测试路径拼接功能:")
for base, user, expected in test_cases:
    result = test_path_join(base, user)
    status = "✓" if result == expected else "✗"
    print(f"{status} {base} + {user!r} = {result!r} (期望: {expected!r})")
