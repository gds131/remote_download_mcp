FROM python:3.10-alpine

WORKDIR /app

# 安装依赖和必要的系统包
RUN apk add --no-cache gcc musl-dev

# 使用国内pip镜像源
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 复制源码
COPY src/ ./src/

# 复制默认配置文件
COPY config/ ./config/

# 创建配置目录（外挂卷挂载点）
RUN mkdir -p /app/config

EXPOSE 8000

# HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
#     CMD python -c "import urllib.request, os; port = os.getenv('MCP_PORT', '8000'); urllib.request.urlopen('http://localhost:' + port + '/sse')"

CMD ["python", "-m", "src.server"]