from flask import Flask
from flask_cors import CORS
from breadApp import bread_blueprint
from customersApp import customers_blueprint
from loginApp import login_blueprint
from ordersApp import orders_blueprint

app = Flask(__name__)
CORS(app)


# 註冊 Blueprint
app.register_blueprint(bread_blueprint, url_prefix="/bread")
app.register_blueprint(customers_blueprint, url_prefix="/customers")
app.register_blueprint(login_blueprint, url_prefix="/login")
app.register_blueprint(orders_blueprint, url_prefix="/orders")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)