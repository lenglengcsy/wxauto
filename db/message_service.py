from db.crud import save_message
from datetime import datetime

def process_and_save_message(chat, msg_item):
    """
    处理并保存消息对象到数据库。
    :param chat: 聊天窗口名
    :param msg_item: 消息对象，需有content、type等属性
    """
    sender = getattr(msg_item, 'sender', chat)
    receiver = getattr(msg_item, 'receiver', '')
    msg_time = getattr(msg_item, 'time', datetime.now())
    window_name = chat
    content = getattr(msg_item, 'content', '')
    if isinstance(msg_time, datetime):
        msg_time = msg_time.strftime('%Y-%m-%d %H:%M:%S')
    save_message(sender, receiver, msg_time, window_name, content) 