from db.crud import save_message
from datetime import datetime
import json

def process_and_save_message(chat, msg_item):
	"""
	处理并保存消息对象到数据库。
	:param chat: 聊天窗口名
	:param msg_item: 消息对象，需有content、type等属性
	"""
	msg_id = getattr(msg_item, 'id', None)
	sender = getattr(msg_item, 'sender', chat)
	sender_remark = getattr(msg_item, 'sender_remark', '')
	msg_time = getattr(msg_item, 'time', datetime.now())
	window_name = chat
	type_ = getattr(msg_item, 'type', '')
	content = getattr(msg_item, 'content', '')
	info = getattr(msg_item, 'info', None)
	if isinstance(msg_time, datetime):
		msg_time = msg_time.strftime('%Y-%m-%d %H:%M:%S')
	info_str = json.dumps(info, ensure_ascii=False) if info is not None else ''
	save_message(msg_id, sender, sender_remark, msg_time, window_name, type_, content, info_str) 