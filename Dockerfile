# 1. 使用官方 Python 轻量级镜像 (Linux环境)
FROM python:3.12-slim

# 2. 设置容器内的工作目录
WORKDIR /app

# 3. 复制依赖清单到容器中
COPY requirements.txt .

# 4. 安装依赖 (无缓存模式，减小体积)
RUN pip install --no-cache-dir -r requirements.txt

# 5. 复制项目所有代码到容器中
COPY . .

# 6. 暴露 5000 端口 (Flask 默认端口)
EXPOSE 5000

# 7. 启动命令
CMD ["python", "app.py"]