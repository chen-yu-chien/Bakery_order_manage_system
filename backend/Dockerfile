# 使用 Python 官方镜像
FROM python:3.9

# 设置工作目录
WORKDIR /app

# 复制 requirements.txt 并安装依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用程序代码
# COPY breadApp.py customersApp.py loginApp.py ordersApp.py .
COPY breadApp.py customersApp.py loginApp.py ordersApp.py app.py database.py .

# 暴露应用程序端口
EXPOSE 5000

# 启动 Flask 应用
CMD ["python", "app.py"]
