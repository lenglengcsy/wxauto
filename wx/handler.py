from db.message_service import process_and_save_message
from lib.cozepy.chat import MessageType
from llm.coze.client import CozeClient
from wxautox import WeChat
from typing import Any
from wx.history import get_recent_history, add_message_to_history
from cozepy.chat import Message

def handle_message(chat, msg_item: Any, window_messages: list) -> None:
	"""
	处理收到的消息：
	1. 保存消息到数据库
	2. 发送消息到coze，获取回复
	3. 通过wxautox发送回复给用户
	:param chat: 聊天窗口名
	:param msg_item: 消息对象，需有content属性
	"""
	fields = [
		'type', 'content', 'sender', 'sender_remark', 'info', 'control', 'id', 'details'
	]
	field_str = ', '.join(f"{field}={getattr(msg_item, field, None)}" for field in fields)
	for msg in window_messages[:]:
		print(f"收到消息：窗口={chat.who}, {field_str}")
		process_and_save_message(chat.who, msg)
		add_message_to_history(chat.who, msg)
		if msg.sender in ('Self', ):
			window_messages.remove(msg)

	if not window_messages:
		return
	
	# # 只处理文本消息
	# if not hasattr(msg_item, 'content') or not msg_item.content:
	# 	return
	additional_messages = []

	# 1. 获取历史聊天记录
	history = get_recent_history(chat.who)
	# 2. 组装additional_messages
	additional_messages = []
	# 2.1 先加历史消息
	for row in history:
		role="user"
		type="question"
		if row[2] != msg.sender_remark:
			role = 'assistant'
			type = 'answer'
		user_message = Message(
			role=role,
			type=type,
			content=row[7],
			content_type="text"
		)
		additional_messages.append(user_message)
	
	# for item in window_messages:
	# 	user_message = Message(
	# 		role="user",
	# 		type="question",
	# 		content=item.content,
	# 		content_type="text"
	# 	)
	# 	additional_messages.append(user_message)
	item = window_messages[0]
	# 调用coze获取回复
	coze_client = CozeClient()
	coze_response = coze_client.send_message(additional_messages, user_id=item.sender_remark)
	# 提取coze回复内容（取最后一条role为assistant的消息）
	reply = None
	for m in reversed(coze_response.get('messages', [])):
		if m.get('role') == 'assistant' and m.get('content') and m['type'] == MessageType.ANSWER:
			reply = m['content']
			break
	if not reply:
		reply = "[机器人未返回有效内容]"

	# 发送回复到微信
	# msg_item.quote(reply)
	# wx = WeChat()
	# wx.SendMsg(reply) 
	msg_item.quote(reply, at=[msg_item.sender])