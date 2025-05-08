from typing import Optional, Any, Dict, List
from llm.coze.config import get_coze_config
# 正确导入cozepy的Coze类
from cozepy.coze import Coze as RawCozeClient
from cozepy.auth import TokenAuth
from cozepy.chat import Message


class CozeClient:
	def __init__(self) -> None:
		config = get_coze_config()
		self.api_key: str = config["api_key"]
		self.bot_id: str = config["bot_id"]
		self.base_url: str = config["base_url"]
		# 构造cozepy的Auth对象
		self.auth: TokenAuth = TokenAuth(token=self.api_key)
		self.client: RawCozeClient = RawCozeClient(
			auth=self.auth,
			base_url=self.base_url
		)

	def send_message(self, message: str, user_id: Optional[str] = None, **kwargs: Any) -> Dict[str, Any]:
		"""
		发送消息到coze平台，自动轮询并返回最终消息内容。
		:param message: 用户输入的消息内容
		:param user_id: 可选，用户唯一标识
		:param kwargs: 其他可选参数
		:return: 包含chat对象和所有消息内容的字典
		"""
		user_message = Message(
			role="user",
			type="question",
			content=message,
			content_type="text"
		)
		chat_poll = self.client.chat.create_and_poll(
			bot_id=self.bot_id,
			user_id=user_id or "default_user",
			additional_messages=[user_message],
			**kwargs
		)
		return {
			"chat": chat_poll.chat.model_dump() if hasattr(chat_poll.chat, "model_dump") else dict(chat_poll.chat),
			"messages": [m.model_dump() if hasattr(m, "model_dump") else dict(m) for m in chat_poll.messages]
		} 