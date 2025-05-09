from typing import Dict, List, Tuple
from db.crud import get_chat_history_by_window_name
from wx.config import LISTEN_LIST

# 内存缓存，key为window_name，value为历史消息元组列表
data: Dict[str, List[Tuple]] = {}

def load_recent_histories(listen_list: List[str] = None, limit: int = 20) -> None:
	"""
	加载所有监听窗口的最近聊天记录到内存
	:param listen_list: 监听窗口名列表
	:param limit: 每个窗口加载的最大消息数
	"""
	global data
	listen_list = listen_list or LISTEN_LIST
	for window_name in listen_list:
		history = get_chat_history_by_window_name(window_name, limit=limit)
		data[window_name] = history


def get_recent_history(window_name: str) -> List[Tuple]:
	"""
	获取指定窗口的历史聊天记录
	:param window_name: 聊天窗口名
	:return: 消息元组列表
	"""
	return data.get(window_name, []) 