from typing import Optional, Dict, Any
from .client import QywxClient

def send_text_message(
	client: QywxClient,
	touser: Optional[str] = None,
	toparty: Optional[str] = None,
	totag: Optional[str] = None,
	agentid: int = 0,
	content: str = "",
	safe: int = 0,
	enable_id_trans: int = 0,
	enable_duplicate_check: int = 0,
	duplicate_check_interval: int = 1800
) -> Dict[str, Any]:
	"""
	发送文本消息到企业微信
	"""
	payload = {
		"msgtype": "text",
		"agentid": agentid,
		"text": {"content": content},
		"safe": safe,
		"enable_id_trans": enable_id_trans,
		"enable_duplicate_check": enable_duplicate_check,
		"duplicate_check_interval": duplicate_check_interval
	}
	if touser:
		payload["touser"] = touser
	if toparty:
		payload["toparty"] = toparty
	if totag:
		payload["totag"] = totag
	return client.post("/cgi-bin/message/send", payload) 