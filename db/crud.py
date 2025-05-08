from db.connection import get_connection, close_connection
from db.utils import db_exception_handler

@db_exception_handler
def save_message(msg_id, sender, sender_remark, msg_time, window_name, type_, content, info):
    """
    保存一条聊天消息到chat_message表。
    :param msg_id: 消息ID
    :param sender: 发送者
    :param sender_remark: 发送者备注
    :param msg_time: 消息时间（datetime或str）
    :param window_name: 窗口名称
    :param type_: 消息类型
    :param content: 消息内容
    :param info: 消息信息
    """
    conn = get_connection()
    try:
        cursor = conn.cursor()
        sql = """
            INSERT INTO chat_message (msg_id, sender, sender_remark, msg_time, window_name, type, content, info)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(sql, (msg_id, sender, sender_remark, msg_time, window_name, type_, content, info))
        conn.commit()
        print(f"[DB写入成功] msg_id={msg_id}, sender={sender}, sender_remark={sender_remark}, msg_time={msg_time}, window_name={window_name}, type={type_}, content={content}, info={info}")
    finally:
        close_connection(conn) 