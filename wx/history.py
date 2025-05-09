from typing import Dict, List, Tuple
from db.crud import get_chat_history_by_window_name
from wx.config import LISTEN_LIST

# 内存缓存，key为window_name，value为历史消息元组列表
data: Dict[str, List[Tuple]] = {}

def load_recent_histories(listen_list: List[str] = None, limit: int = 5) -> None:
	"""
	加载所有监听窗口的最近聊天记录到内存
	:param listen_list: 监听窗口名列表
	:param limit: 每个窗口加载的最大消息数
	"""
	global data
	listen_list = listen_list or LISTEN_LIST
	for window_name in listen_list:
		history = get_chat_history_by_window_name(window_name, limit=limit)
		data[window_name] = list(history)


def get_recent_history(window_name: str) -> List[Tuple]:
	"""
	获取指定窗口的历史聊天记录
	:param window_name: 聊天窗口名
	:return: 消息元组列表
	"""
	return data.get(window_name, [])


def add_message_to_history(window_name: str, msg_or_tuple) -> None:
	"""
	将新消息追加到内存缓存的历史消息列表中
	:param window_name: 聊天窗口名
	:param msg_or_tuple: 消息对象或元组，结构与数据库一致
	"""
	from datetime import datetime
	import json
	if not window_name:
		return
	# 如果是元组，直接追加
	msg = msg_or_tuple
	msg_id = getattr(msg, 'id', None)
	sender = getattr(msg, 'sender', window_name)
	sender_remark = getattr(msg, 'sender_remark', '')
	msg_time = getattr(msg, 'time', None)
	if hasattr(msg_time, 'strftime'):
		msg_time = msg_time.strftime('%Y-%m-%d %H:%M:%S')
	elif isinstance(msg_time, datetime):
		msg_time = msg_time.strftime('%Y-%m-%d %H:%M:%S')
	type_ = getattr(msg, 'type', '')
	content = getattr(msg, 'content', '')
	info = getattr(msg, 'info', None)
	info_str = json.dumps(info, ensure_ascii=False) if info is not None else ''
	msg_tuple = (None, msg_id, sender, sender_remark, msg_time, window_name, type_, content, info_str)
	data[window_name].append(msg_tuple) 