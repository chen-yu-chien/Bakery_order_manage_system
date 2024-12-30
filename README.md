# Bakery_order_manage_system
## Docker 系統部屬
**部屬指令**
* 前端
    ```shell
    cd D:\Backery_Order_Manage_System\frontend\
    docker compose up --build
    ```
* 後端
    ```shell
    cd D:\Backery_Order_Manage_System\backend\
    docker compose up --build
    ```
## k3s 系統部屬
使用 docker 內建 Kubernetes 進行 k3s clusters 部屬，開始前須先啟用 docker 中的 Kubernetes
 
**步驟說明（假設專案檔位於 D 槽）**
1. 啟用系統前須先啟動 MinIO Server
    ```shell
     cd D:
     .\minio.exe server D:\minio\ --console-address :9001
    ```
2. 啟動前端及後端 clusters
   * 前端  
        ```shell
        cd D:\Backery_Order_Manage_System\frontend\
        kubectl apply -f frontend-deployment.yaml
        ```
    * 後端
        ```shell
        cd D:\Backery_Order_Manage_System\backend\
        kubectl apply -f backend-deployment.yaml
        ```
3. 確認 Deployment、Services、Pods、Nodes 正常啟用
   ```shell
    kubectl get pods
    kubectl get svc
    kubectl get deployment
    kubectl get nodes
   ```
4. 若需刪除已不屬之 Deployment、Services、Pods，可執行 Delete 指令
   ```shell
    kubectl delete all --all --all-namespaces
   ```