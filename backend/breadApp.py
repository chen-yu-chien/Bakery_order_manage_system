import os
from flask import Blueprint, Response, jsonify, request
from minio import Minio
from database import get_db_connection
import json
from werkzeug.utils import secure_filename

# 建立 Blueprint
bread_blueprint = Blueprint('bread', __name__)

filename = None

@bread_blueprint.route('/bread', methods=['GET', 'POST', 'PUT', 'DELETE'])
def manage_bread():
    global filename

    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == 'GET':
        name = request.args.get('name')  # 从查询参数获取名称
        if name:
            cursor.execute("SELECT * FROM breads WHERE name = %s", (name,))
        else:
            cursor.execute("SELECT * FROM breads")
        breads = cursor.fetchall()
        # 转换为字典形式以便于返回
        bread_list = [{'id': bread[0], 'name': bread[1], 'price': float(bread[2]), 'description': bread[3], 'stock': bread[4], 
                       'image_url': bread[5]} for bread in breads] # image_url format: {MINIO_URL}/{BUCKET_NAME}/{obj.object_name}
        print("bread_list", bread_list)
        # 使用 json.dumps 确保中文正常显示
        response_json = json.dumps(bread_list, ensure_ascii=False)
        return Response(response_json, content_type='application/json; charset=utf-8')

    if request.method == 'POST':
        new_bread = request.json  # 假設你是從請求體接收 JSON 數據

        # 確認 new_bread 是一個字典，並提取具體的值
        name = new_bread.get('name')
        price = new_bread.get('price')
        description = new_bread.get('description')
        stock = new_bread.get('stock')
        imgUrl = f"http:172.20.10.6:9000/bakery/{filename}"

        if not all([name, price, description, stock]):
            return "Missing required bread data", 400

        try:
            # 插入資料到資料庫
            if filename:
                cursor.execute(
                    "INSERT INTO breads (name, price, description, stock, imgUrl) VALUES (%s, %s, %s, %s, %s)", 
                    (name, price, description, stock, imgUrl)
                )
            else:
                cursor.execute(
                    "INSERT INTO breads (name, price, description, stock) VALUES (%s, %s, %s, %s)", 
                    (name, price, description, stock)
                )
            conn.commit()
            filename = None
            return jsonify({'message': '面包已新增'}), 201
        except Exception as e:
            print(f"Error: {e}")
            return jsonify({'message': '資料庫錯誤'}), 500
    
    if request.method == 'PUT':
        updated_bread = request.json

        name = updated_bread.get('name')
        price = updated_bread.get('price')
        description = updated_bread.get('description')
        stock = updated_bread.get('stock')

        cursor.execute("UPDATE breads SET name=%s, price=%s, description=%s, stock=%s WHERE id=%s",
                   (updated_bread['name'], updated_bread['price'], updated_bread['description'], updated_bread['stock'], updated_bread['id']))
        conn.commit()
        return jsonify({'message': '麵包已更新'})

    if request.method == 'DELETE':
        bread_id = request.json.get('id')
        cursor.execute("DELETE FROM breads WHERE id=%s", (bread_id,))
        conn.commit()
        return jsonify({'message': '麵包已刪除'})
    
    conn.commit()
    cursor.close()
    conn.close()
    return '', 204

@bread_blueprint.route('/dump', methods=['GET'])
def dump_breads():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM breads")
    breads = cursor.fetchall()
    bread_list = [{'id': bread[0], 'name': bread[1], 'price': bread[2], 'description': bread[3], 'stock': bread[4]} for bread in breads]
    
    # 转换为 JSON 并保存到文件
    with open('breads_dump.json', 'w') as f:
        json.dump(bread_list, f)
    
    cursor.close()
    conn.close()
    return jsonify({'message': '数据已转储到 breads_dump.json'})

@bread_blueprint.route('/load', methods=['POST'])
def load_breads():
    conn = get_db_connection()
    cursor = conn.cursor()

    # 从 JSON 文件加载数据
    with open('breads_dump.json', 'r') as f:
        bread_list = json.load(f)
        for bread in bread_list:
            cursor.execute("INSERT INTO breads (name, price, description, stock) VALUES (%s, %s, %s, %s)",
                           (bread['name'], bread['price'], bread['description'], bread['stock']))
   
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message': '数据已加载到数据库'})

@bread_blueprint.route('/bread/<int:breadid>', methods=['GET'])
def get_bread_name(breadid):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM breads WHERE id = %s", (breadid,))
    bread_name = cursor.fetchone()
    cursor.close()
    conn.close()
    
    if bread_name:
        bread_name = {'name': bread_name[0]}
        response_json = json.dumps(bread_name, ensure_ascii=False)
        return Response(response_json, content_type='application/json; charset=utf-8')
    else:
        return jsonify({'error': 'Bread not found'}), 404

# 初始化 MinIO 客户端
minio_client = Minio(
    "172.20.10.6:9000",  # MinIO 服务地址(學校手機熱點)
    access_key="bakery",
    secret_key="bakerybakery",
    secure=False
)

# 确保 MinIO 上有桶（如果桶不存在，创建它）
bucket_name = "bakery"
if not minio_client.bucket_exists(bucket_name):
    minio_client.make_bucket(bucket_name)

# 上傳檔案到 MinIO 的路由
@bread_blueprint.route('/upload', methods=['POST'])
def upload_file():
    global filename

    print("Received request at /upload")  # Log the request
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file:
        # 确保文件名是安全的
        filename = secure_filename(file.filename)
        
        # 获取文件的大小
        file.seek(0, os.SEEK_END)  # 先将文件指针移到文件末尾
        file_size = file.tell()  # 获取文件大小
        file.seek(0, os.SEEK_SET)  # 重置文件指针到文件开始位置
        
        # 上传文件到 MinIO
        try:
            minio_client.put_object(
                bucket_name,  # 目标桶
                filename,     # 文件名
                file.stream,  # 文件内容
                file_size  # 文件大小
            )
            return jsonify({'message': f'File {filename} uploaded successfully', 'success': True}), 200
        except Exception as e:
            print(f"Error: {e}")
            return jsonify({'error': 'File upload failed', 'Error': e, 'success': False}), 500