# 数据库连接管理
import MySQLdb
from db.config import DB_CONFIG

def get_connection():
    """获取数据库连接"""
    return MySQLdb.connect(
        host=DB_CONFIG['host'],
        port=DB_CONFIG['port'],
        user=DB_CONFIG['user'],
        passwd=DB_CONFIG['password'],
        db=DB_CONFIG['database'],
        charset=DB_CONFIG['charset']
    )

def close_connection(conn):
    """关闭数据库连接"""
    if conn:
        conn.close() 