# 其他数据库相关的工具函数

def db_exception_handler(func):
    """数据库操作异常处理装饰器"""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"数据库操作异常: {e}")
            return None
    return wrapper

from db.connection import get_connection, close_connection

@db_exception_handler
def list_tables():
    """列出当前数据库中的所有表名"""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SHOW TABLES;")
        tables = [row[0] for row in cursor.fetchall()]
        return tables
    finally:
        close_connection(conn)

@db_exception_handler
def list_databases():
    """列出当前数据库实例中的所有数据库名"""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SHOW DATABASES;")
        dbs = [row[0] for row in cursor.fetchall()]
        return dbs
    finally:
        close_connection(conn)

@db_exception_handler
def list_chat_messages():
    """查询chat_message表中的所有内容"""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM chat_message;")
        rows = cursor.fetchall()
        return rows
    finally:
        close_connection(conn) 

