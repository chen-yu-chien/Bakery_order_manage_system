from flask import Blueprint, Flask, Response, jsonify, request
from database import get_db_connection
import json

# 建立 Blueprint
customers_blueprint = Blueprint('customers', __name__)

@customers_blueprint.route('/customer', methods=['GET', 'POST', 'PUT', 'DELETE'])
def manage_customer():
    conn = get_db_connection()
    cursor = conn.cursor()

    # if request.method == 'GET':
    #     name = request.args.get('name')  # 从查询参数获取名称
    #     if name:
    #         cursor.execute("SELECT * FROM customers WHERE name = %s", (name,))
    #     else:
    #         cursor.execute("SELECT * FROM customers")
    #     customers = cursor.fetchall()
    #     # 转换为字典形式以便于返回
    #     customer_list = [{'id': customer[0], 'name': customer[1], 'telephone': str(customer[2]), 'address': customer[3]} for customer in customers]
    #     print(customer_list)
    #     # 使用 json.dumps 确保中文正常显示
    #     response_json = json.dumps(customer_list, ensure_ascii=False)
    #     return Response(response_json, content_type='application/json; charset=utf-8')

    if request.method == 'POST':
        new_bread = request.json  # 假設你是從請求體接收 JSON 數據

        # 確認 new_bread 是一個字典，並提取具體的值
        name = new_bread.get('name')
        telephone = new_bread.get('telephone')
        address = new_bread.get('address')

        if not all([name, telephone, address]):
            return "Missing required bread data", 400

        try:
            # 插入資料到資料庫
            cursor.execute(
                "INSERT INTO customers (name, telephone, address) VALUES (%s, %s, %s)", 
                (name, telephone, address)
            )
            conn.commit()
            return jsonify({'message': '顧客已新增'}), 201
        except Exception as e:
            print(f"Error: {e}")
            return jsonify({'message': '資料庫錯誤'}), 500
    
    conn.commit()
    cursor.close()
    conn.close()
    return '', 204

@customers_blueprint.route('/dumpCustomers', methods=['GET'])
def dump_customers():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM customers")
    customers = cursor.fetchall()
    customer_list = [{'id': customers[0], 'name': customers[1], 'telephone': customers[2], 'address': customers[3]} for customers in customers]
    
    # 转换为 JSON 并保存到文件
    with open('customers_dump.json', 'w') as f:
        json.dump(customer_list, f)
    
    cursor.close()
    conn.close()
    return jsonify({'message': '数据已转储到 customers_dump.json'})

@customers_blueprint.route('/load', methods=['POST'])
def load_customers():
    conn = get_db_connection()
    cursor = conn.cursor()

    # 从 JSON 文件加载数据
    with open('customers_dump.json', 'r') as f:
        customer_list = json.load(f)
        for customer in customer_list:
            cursor.execute("INSERT INTO customers (name, telephone, address) VALUES (%s, %s, %s)",
                           (customer['name'], customer['telephone'], customer['address']))
   
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message': '数据已加载到数据库'})


@customers_blueprint.route('/customer/<int:customerid>', methods=['GET'])
def get_customer_info(customerid):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM customers WHERE id = %s", (customerid,))
    customer = cursor.fetchone()
    cursor.close()
    conn.close()
    
    if customer:
        customer_info = {'id': customer[0], 'name': customer[1], 'telephone': customer[2], 'address': customer[3]}
        response_json = json.dumps(customer_info, ensure_ascii=False)
        return Response(response_json, content_type='application/json; charset=utf-8')
    else:
        return jsonify({'error': 'Customer not found'}), 404