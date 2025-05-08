from db.connection import get_connection, close_connection
from db.utils import db_exception_handler

@db_exception_handler
def save_message(sender, receiver, msg_time, window_name, content):
    """
    保存一条聊天消息到chat_message表。
    :param sender: 发送者
    :param receiver: 接收者
    :param msg_time: 消息时间（datetime或str）
    :param window_name: 窗口名称
    :param content: 消息内容
    """
    conn = get_connection()
    try:
        cursor = conn.cursor()
        sql = """
            INSERT INTO chat_message (sender, receiver, msg_time, window_name, content)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(sql, (sender, receiver, msg_time, window_name, content))
        conn.commit()
        print(f"[DB写入成功] sender={sender}, receiver={receiver}, msg_time={msg_time}, window_name={window_name}, content={content}")
    finally:
        close_connection(conn) 