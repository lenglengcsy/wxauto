from wxautox import WeChat
import time
from typing import List, Dict, Any
from collections import defaultdict
from wx.history import get_recent_history

class MessageListener:
	def __init__(self, listen_list: List[str] = None, wait: int = 1):
		self.wx = WeChat()
		self.listen_list = listen_list or []
		self.wait = wait
		self._init_listeners()

	def _init_listeners(self):
		for who in self.listen_list:
			self.wx.AddListenChat(who=who, savepic=True, savefile=True, savevoice=True, parseurl=True)

	def listen_once(self) -> Dict[str, Any]:
		"""
		获取一次监听到的新消息。
		返回格式与wxautox的GetListenMessage一致。
		"""
		return self.wx.GetListenMessage()

	def listen_forever(self, callback):
		"""
		持续监听消息，每当有新消息时调用callback。
		callback参数为(window_name, msg_item)
		"""
		while True:
			msgs = self.listen_once()


			# 用zip将监听名称与消息内容绑定
			for chat in msgs:
				# 收集每个窗口的多条消息
				window_messages = []
				msg = msgs.get(chat)   # 获取消息内容
				item = None
				for item in msg:
			# for chat_msgs in msgs.values():
			# 	for item in chat_msgs:
					# if item.sender in ('Self', 'SYS'):
					if item.sender in ('SYS', ):
						continue
					# chat_name = item.details['chat_name']
					if item.details['chat_type'] in ('friend', ) or item.details['chat_type'] in ('group', ) and f'@{self.wx.nickname}' in item.content:
						window_messages.append(item)
						# callback(chat, item.details['chat_name'], item)
					# if item.details['chat_type'] in ('group', ) and f'@{self.wx.nickname}' in item.content:
						# window_messages[chat_name].append(item)
						# callback(chat, item.details['chat_name'], item)
				if item:
					callback(chat, item, window_messages)
			# time.sleep(self.wait) 
			time.sleep(10) 

			# # 收集每个窗口的多条消息
			# window_messages = defaultdict(list)
			# for chat in msgs:
			# 	msg = msgs.get(chat)
			# 	for item in msg:
			# 		if item.sender in ('Self', 'SYS'):
			# 			continue
			# 		chat_name = item.details['chat_name']
			# 		if hasattr(item, 'content') and item.content:
			# 			window_messages[chat_name].append(item)
			# # 合并消息并处理
			# for chat_name, items in window_messages.items():
			# 	if not items:
			# 		continue
			# 	# 1. 获取历史聊天记录
			# 	history = get_recent_history(chat_name)
			# 	# 2. 组装additional_messages
			# 	additional_messages = []
			# 	# 2.1 先加历史消息
			# 	for row in history:
			# 		additional_messages.append({
			# 			"role": "user",
			# 			"type": "text",
			# 			"content": row[7]  # content字段
			# 		})
			# 	# 2.2 再加本次新消息
			# 	for item in items:
			# 		additional_messages.append({
			# 			"role": "user",
			# 			"type": "text",
			# 			"content": item.content
			# 		})
			# 	# 3. 示例：调用coze（如需集成请替换为实际调用）
			# 	# from llm.coze.client import CozeClient
			# 	# coze_client = CozeClient()
			# 	# coze_client.send_message(
			# 	# 	message=items[-1].content,
			# 	# 	user_id=str(getattr(items[-1], 'sender', 'default_user')),
			# 	# 	additional_messages=additional_messages
			# 	# )
			# 	# 保留原有callback逻辑
			# 	for item in items:
			# 		callback(chat_name, item)
			# time.sleep(self.wait) 