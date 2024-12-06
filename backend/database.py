from mysql import connector

# 数据库连接配置
db_config = {
    'user': 'root',
    'password': 'local_0944133',
    'host': 'host.docker.internal',
    'database': 'bakery',
}

# 连接数据库
def get_db_connection():
    try:
        return connector.connect(**db_config)
    except connector.Error as err:
        print(f"Error: {err}")
        return None