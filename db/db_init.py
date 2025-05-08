import MySQLdb
from db.config import DB_CONFIG

def init_chat_message_table():
    conn = MySQLdb.connect(
        host=DB_CONFIG['host'],
        port=DB_CONFIG['port'],
        user=DB_CONFIG['user'],
        passwd=DB_CONFIG['password'],
        db=DB_CONFIG['database'],
        charset=DB_CONFIG['charset']
    )
    cursor = conn.cursor()
    # cursor.execute("DROP TABLE IF EXISTS chat_message;")
    sql = '''
    CREATE TABLE IF NOT EXISTS chat_message (
        id INT AUTO_INCREMENT PRIMARY KEY COMMENT '消息ID',
        msg_id VARCHAR(255) COMMENT '消息id',
        sender VARCHAR(255) NOT NULL COMMENT '发送者',
        sender_remark VARCHAR(255) COMMENT '发送者备注名',
        msg_time DATETIME NOT NULL COMMENT '时间',
        window_name VARCHAR(255) NOT NULL COMMENT '窗口名称',
        type VARCHAR(64) COMMENT '消息类型',
        content TEXT COMMENT '内容',
        info TEXT COMMENT '原始消息信息'
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    '''
    cursor.execute(sql)
    conn.commit()
    cursor.close()
    conn.close()
    print('chat_message表初始化完成')

if __name__ == '__main__':
    init_chat_message_table() 