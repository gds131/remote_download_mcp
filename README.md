

### 项目名称
**remote-download-mcp** - 远程下载管理MCP服务

### 简短描述
基于MCP协议的远程下载服务，支持通过配置文件管理多个下载器实例（qBittorrent/Transmission），让AI助手能够直接提交下载任务。

### 详细描述

#### 🎯 项目简介
remote-download-mcp 是一个基于 [MCP (Model Context Protocol)](https://modelcontextprotocol.io/) 协议的远程下载管理服务。它允许用户通过外挂配置文件定义多个下载器实例（如 qb1、qb2、tr1 等），然后通过 MCP 工具让 AI 助手直接向这些下载器提交下载任务。

#### ✨ 核心功能

- **多下载器支持**：同时管理多个 qBittorrent 和 Transmission 下载器实例
- **配置文件驱动**：通过 YAML 配置文件管理下载器，无需修改代码
- **MCP 协议兼容**：支持任何兼容 MCP 的 AI 助手（如 Claude Desktop、Cursor 等）
- **并行健康检查**：启动时自动并行检测所有下载器连通性
- **简单易用**：通过简单的工具调用即可提交下载任务

#### 🚀 快速开始

**1. 创建配置文件**

```yml
downloaders:
  # qBittorrent 实例1
  qb1: #别名，自行定义
    type: qbittorrent
    url: http://10.10.10.1:8081
    username: test
    password: test
    save_path: /downloads #路径最好和qb/tr下载路径保持一致
    
  # qBittorrent 实例2（可能是不同服务器）
  qb2:
    type: qbittorrent
    url: http://10.10.10.2:8080/
    username: test
    password: test
    save_path: /downloads
    
  # Transmission 实例1
  tr1:
    type: transmission
    url: http://10.10.10.3:9091
    username: test
    password: test
    save_path: /downloads

# 可选：默认下载器
default_downloader: qb1
```

**2. 启动服务**

```bash
docker run -d \
  --name remote-download \
  -p 8000:8000 \
  -v $(pwd)/config:/app/config \
  remote-download-mcp
```

**3. Docker Compose 方式（推荐）**

```yaml
services:
  remote-download:
    image: remote-download-mcp
    container_name: remote-download
    ports:
      - "8000:8000"
    volumes:
      - ./config:/app/config
    restart: unless-stopped
```

#### 📡 MCP 工具

项目提供以下 MCP 工具：

| 工具名 | 功能 | 参数 |
|--------|------|------|
| `add_download` | 提交下载任务 | download_url, downloader_alias, save_path |
| `list_downloaders` | 列出所有下载器 | 无 |
| `health_check` | 检查下载器状态 | 无 |

#### MCP配置
```json
{
  "mcpServers": {
    "remote_downnload": {
      "url": "http://ip:port/sse"
    }
  }
}
```

#### 💡 使用示例

```
用户：帮我下载这个种子 magnet:?xt=urn:btih:abc123...

AI助手调用 add_download:
{
  "download_url": "magnet:?xt=urn:btih:abc123...",
  "downloader_alias": "qb1",
  "save_path": "movies"
}

返回：
{
  "success": true,
  "message": "下载任务已提交",
  "downloader": "qb1",
  "save_path": "/downloads/movies"
}
```

#### 🔧 配置说明

| 字段 | 必填 | 说明 |
|------|------|------|
| type | 是 | 下载器类型，支持 `qbittorrent` 和 `transmission` |
| url | 是 | 下载器访问地址 |
| username | 是 | 下载器用户名 |
| password | 是 | 下载器密码 |
| save_path | 否 | 默认保存路径，默认为 `/downloads` |

#### 🏗️ 技术栈

- Python 3.10+
- [fastmcp](https://github.com/jlowin/fastmcp) - MCP 协议实现
- [qbittorrent-api](https://github.com/rrrooddboorr/qbittorrent-api) - qBittorrent API 客户端
- [transmission-rpc](https://github.com/uit21521675/transmission-rpc) - Transmission API 客户端
- Uvicorn - ASGI 服务器

#### 📋 系统要求

- Docker 20.10+
- qBittorrent 4.3+ 或 Transmission 3.0+
- MCP 兼容的 AI 助手客户端


