from typing import Any, Dict, Optional, List
from .http_client import http_get, http_post
import time

class QywxClient:
	"""企业微信API客户端"""
	def __init__(self, corp_id: str, corp_secret: str):
		self.corp_id = corp_id
		self.corp_secret = corp_secret
		self._access_token: Optional[str] = None
		self._token_expire: float = 0

	def get_access_token(self) -> str:
		if self._access_token and time.time() < self._token_expire - 60:
			return self._access_token
		url = "https://qyapi.weixin.qq.com/cgi-bin/gettoken"
		params = {"corpid": self.corp_id, "corpsecret": self.corp_secret}
		data = http_get(url, params=params)
		if data.get("errcode") != 0:
			raise Exception(f"获取access_token失败: {data}")
		self._access_token = data["access_token"]
		self._token_expire = time.time() + data.get("expires_in", 7200)
		return self._access_token

	def post(self, api: str, payload: Dict[str, Any]) -> Dict[str, Any]:
		token = self.get_access_token()
		url = f"https://qyapi.weixin.qq.com{api}?access_token={token}"
		return http_post(url, data=payload)

	def get_all_userids(self, department_id: int = 1) -> List[str]:
		"""
		获取企业微信指定部门及其子部门下所有成员的userid
		"""
		userids: List[str] = []
		url = "/cgi-bin/user/list"
		token = self.get_access_token()
		api_url = f"https://qyapi.weixin.qq.com{url}"
		params = {
			"access_token": token,
			"department_id": department_id,
			"fetch_child": 1
		}
		data = http_get(api_url, params=params)
		if data.get("errcode") == 0 and "userlist" in data:
			for user in data["userlist"]:
				userids.append(user["userid"])
		else:
			print(f"获取成员失败: {data}")
		return userids

	def get_all_departments(self) -> List[Dict]:
		"""
		获取企业微信下所有部门信息
		返回值为部门字典列表，每个字典包含id、name、parentid等字段
		"""
		url = "/cgi-bin/department/list"
		token = self.get_access_token()
		api_url = f"https://qyapi.weixin.qq.com{url}"
		params = {"access_token": token}
		data = http_get(api_url, params=params)
		if data.get("errcode") == 0 and "department" in data:
			return data["department"]
		else:
			print(f"获取部门失败: {data}")
		return [] 