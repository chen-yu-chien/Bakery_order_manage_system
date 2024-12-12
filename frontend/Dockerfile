# 使用 Nginx 作為靜態資源伺服器
FROM nginx:alpine

# 設置工作目錄
WORKDIR /usr/share/nginx/html

# 複製靜態文件到容器內的 Nginx 路徑
COPY . .

# 暴露 Nginx 服務埠
EXPOSE 80

# 啟動 Nginx
CMD ["nginx", "-g", "daemon off;"]
