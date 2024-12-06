from flask import Blueprint, Flask, Response, jsonify, request
# from mysql import connector
from database import get_db_connection
import json
import requests

# 建立 Blueprint
orders_blueprint = Blueprint('orders', __name__)

@orders_blueprint.route('/orders', methods=['GET', 'PUT'])
def manage_order():
    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == 'GET':
        orderdate = request.args.get('orderdate')  # 从查询参数获取名称
        breadname = request.args.get('breadname')
        pickup = request.args.get('pickup')

        if orderdate:
            if breadname:
                if pickup:
                    cursor.execute("SELECT * FROM orders WHERE orderdate = %s AND breadid = (SELECT id FROM breads WHERE name = %s) AND pickup = %s", (orderdate, breadname, pickup))
                else:
                    cursor.execute("SELECT * FROM orders WHERE orderdate = %s AND breadid = (SELECT id FROM breads WHERE name = %s)", (orderdate, breadname))
            else:
                if pickup:
                    cursor.execute("SELECT * FROM orders WHERE orderdate = %s AND pickup = %s", (orderdate, pickup))
                else:
                    cursor.execute("SELECT * FROM orders WHERE orderdate = %s", (orderdate,))
        else:
            if breadname:
                if pickup:
                    cursor.execute("SELECT * FROM orders WHERE breadid = (SELECT id FROM breads WHERE name = %s) AND pickup = %s", (breadname, pickup))
                else:
                    cursor.execute("SELECT * FROM orders WHERE breadid = (SELECT id FROM breads WHERE name = %s)", (breadname,))
            else:
                if pickup:
                    cursor.execute("SELECT * FROM orders WHERE pickup = %s", (pickup,))
                else:
                    cursor.execute("SELECT * FROM orders")
        
        orders = cursor.fetchall()
        # 转换为字典形式以便于返回
        orders_list = [{'id': order[0], 'customerName': get_customer_info(order[1], 'name'), 
                        'customerTelephone': get_customer_info(order[1], 'telephone'), 
                        'customerAddress': get_customer_info(order[1], 'address'), 'orderdate': order[2].strftime('%Y-%m-%d'), 
                        'breadName': get_bread_name(order[3]), 'quantity': order[4], 'pickup': get_pickup(order[5])} for order in orders]
        print(orders_list)
        # 使用 json.dumps 确保中文正常显示
        response_json = json.dumps(orders_list, ensure_ascii=False)
        return Response(response_json, content_type='application/json; charset=utf-8')
    
    if request.method == 'PUT':
        updated_order = request.json

        id = updated_order.get('id')
        pickup = updated_order.get('pickup')

        try:
            cursor.execute("UPDATE orders SET pickup=%s WHERE id=%s",(pickup, id))
            conn.commit()
            return jsonify({'message': '訂單已更新'})
        except Exception as e:
            print(f"Error: {e}")
            return jsonify({'message': '訂單更新錯誤', 'Error': e}), 500
    
    conn.commit()
    cursor.close()
    conn.close()
    return '', 204

@orders_blueprint.route('/dumpOrders', methods=['GET'])
def dump_orders():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM orders")
    orders = cursor.fetchall()
    order_list = [{'id': order[0], 'customerid': order[1], 'orderdate': order[2], 'breadid': order[3], 'quantity': order[4], 'pickup': order[5]} for order in orders]
    
    # 转换为 JSON 并保存到文件
    with open('orders_dump.json', 'w') as f:
        json.dump(order_list, f)
    
    cursor.close()
    conn.close()
    return jsonify({'message': '数据已转储到 orders_dump.json'})

@orders_blueprint.route('/loadOrders', methods=['POST'])
def load_orders():
    conn = get_db_connection()
    cursor = conn.cursor()

    # 从 JSON 文件加载数据
    with open('orders_dump.json', 'r') as f:
        order_list = json.load(f)
        for order in order_list:
            cursor.execute("INSERT INTO orders (customerid, orderdate, breadid, quantity, pickup) VALUES (%s, %s, %s, %s, %s)",
                           (order['customerid'], order['orderdate'], order['breadid'], order['quantity'], order['pickup']))
   
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message': '数据已加载到数据库'})

# 获取 customername 的函数
def get_customer_info(customerid, field: str):
    try:
        response = requests.get(f'http://localhost:5000/customers/customer/{customerid}')
        if response.status_code == 200:
            if field == 'name':
                return response.json().get('name')
            elif field == 'telephone':
                return response.json().get('telephone')
            elif field == 'address':
                return response.json().get('address')
            return response.json()
        else:
            return None
    except requests.RequestException as e:
        print(f"Error: {e}")
        return None

# 获取 breadname 的函数
def get_bread_name(breadid):
    try:
        response = requests.get(f'http://localhost:5000/bread/bread/{breadid}')
        if response.status_code == 200:
            return response.json().get('name')
        else:
            return None
    except requests.RequestException as e:
        print(f"Error: {e}")
        return None    

def get_pickup(pickup):
    if pickup == -1:
        return '已取貨'
    elif pickup == 0:
        return '自取'
    else:
        return '宅配'