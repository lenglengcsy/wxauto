from db.connection import get_connection, close_connection
from db.utils import db_exception_handler
from typing import List, Tuple, Optional

@db_exception_handler
def save_message(msg_id, sender, sender_remark, msg_time, window_name, type_, content, quote_msg, info):
    """
    保存一条聊天消息到chat_message表。
    :param msg_id: 消息ID
    :param sender: 发送者
    :param sender_remark: 发送者备注
    :param msg_time: 消息时间（datetime或str）
    :param window_name: 窗口名称
    :param type_: 消息类型
    :param content: 消息内容
    :param quote_msg: 引用的消息内容
    :param info: 消息信息
    """
    conn = get_connection()
    try:
        cursor = conn.cursor()
        sql = """
            INSERT INTO chat_message (msg_id, sender, sender_remark, msg_time, window_name, type, content, quote_msg, info)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(sql, (msg_id, sender, sender_remark, msg_time, window_name, type_, content, quote_msg, info))
        conn.commit()
        print(f"[DB写入成功] msg_id={msg_id}, sender={sender}, sender_remark={sender_remark}, msg_time={msg_time}, window_name={window_name}, type={type_}, content={content}, quote_msg={quote_msg}, info={info}")
    finally:
        close_connection(conn)

@db_exception_handler
def get_chat_history_by_window_name(window_name: str, limit: int = 50) -> Optional[List[Tuple]]:
	"""
	根据window_name查询历史聊天记录，按msg_time升序排列。
	:param window_name: 聊天窗口名
	:param limit: 返回的最大消息条数，默认50
	:return: 消息元组列表（id, msg_id, sender, sender_remark, msg_time, window_name, type, content, quote_msg, info）
	"""
	conn = get_connection()
	try:
		cursor = conn.cursor()
		sql = (
			"SELECT id, msg_id, sender, sender_remark, msg_time, window_name, type, content, quote_msg, info "
			"FROM chat_message WHERE window_name = %s ORDER BY msg_time ASC LIMIT %s"
		)
		cursor.execute(sql, (window_name, limit))
		rows = cursor.fetchall()
		return rows
	finally:
		close_connection(conn) 