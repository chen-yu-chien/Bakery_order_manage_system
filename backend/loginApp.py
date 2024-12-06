from flask import Blueprint, Flask, jsonify, request, session
# from mysql import connector
from flask_cors import CORS
from database import get_db_connection

# 建立 Blueprint
login_blueprint = Blueprint('login', __name__)

@login_blueprint.route('/login', methods=['POST'])
def login():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    username = request.json.get('username')
    password = request.json.get('password')
    
    cursor.execute("SELECT * FROM staffs WHERE username = %s AND password = %s", (username, password))
    user = cursor.fetchone()
    
    cursor.close()
    conn.close()
    
    if user:
        return jsonify({'message': '登入成功', 'success': True}), 200
    else:
        return jsonify({'message': '帳號密碼錯誤', 'success': False}), 401