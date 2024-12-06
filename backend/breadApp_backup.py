from flask import Blueprint, jsonify, request
from minio import Minio
# from mysql import connector
from database import get_db_connection
import json
from werkzeug.utils import secure_filename

# 建立 Blueprint
bread_blueprint = Blueprint('bread', __name__)

@bread_blueprint.route('/bread', methods=['GET', 'POST', 'PUT', 'DELETE'])
def manage_bread():
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
        bread_list = [{'id': bread[0], 'name': bread[1], 'price': bread[2], 'description': bread[3], 'stock': bread[4], 'imgUrl': bread[5]} 
                      for bread in breads]
        print(bread_list)
        return jsonify(bread_list)

    if request.method == 'POST':
        new_bread = request.json  # 假設你是從請求體接收 JSON 數據

        # 確認 new_bread 是一個字典，並提取具體的值
        name = new_bread.get('name')
        price = new_bread.get('price')
        description = new_bread.get('description')
        stock = new_bread.get('stock')

        if not all([name, price, description, stock]):
            return "Missing required bread data", 400

        try:
            # 插入資料到資料庫
            cursor.execute(
                "INSERT INTO breads (name, price, description, stock) VALUES (%s, %s, %s, %s)", 
                (name, price, description, stock)
            )
            conn.commit()
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
        return jsonify({'name': bread_name[0]})
    else:
        return jsonify({'error': 'Bread not found'}), 404
