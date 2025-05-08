from typing import Any
import pytest
from llm.coze.client import CozeClient


def test_send_message() -> None:
	"""
	测试CozeClient的send_message方法是否能正常调用并返回结果。
	注意：需要在llm/coze/config.py中填写有效的API Key和Bot ID。
	"""
	client = CozeClient()
	test_message = "你好，Coze！"
	user_id = "test_user_001"
	response: Any = client.send_message(message=test_message, user_id=user_id)
	print("Coze返回：", response)
	# assert response is not None
	# assert isinstance(response, dict)
	# # 判断返回内容包含关键字段
	# assert "id" in response
	# assert "bot_id" in response
	# assert "status" in response 