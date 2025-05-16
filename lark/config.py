# lark/config.py

from typing import Optional, Dict
import requests

# 飞书API相关配置
LARK_APP_ID: str = "cli_a89722b1e925500d"
LARK_APP_SECRET: str = "DvtLXTWVxJneNJyFhCoWnfTFlauD3Mq0"

# 用户 access_token 和 refresh_token，需定期刷新
LARK_USER_ACCESS_TOKEN: Optional[str] = None
LARK_USER_REFRESH_TOKEN: Optional[str] = None

LARK_TENANT_ACCESS_TOKEN = "你的TenantAccessToken"

# 你可以只填你实际用到的token，建议优先用UserAccessToken 

# ================== 授权码获取相关函数 ==================

def get_app_access_token(app_id: str = LARK_APP_ID, app_secret: str = LARK_APP_SECRET) -> str:
	"""
	通过 app_id 和 app_secret 获取 app_access_token
	"""
	url = "https://open.feishu.cn/open-apis/auth/v3/app_access_token/internal"
	resp = requests.post(url, json={"app_id": app_id, "app_secret": app_secret})
	data = resp.json()
	if data.get("code") == 0:
		return data["app_access_token"]
	else:
		raise Exception(f"获取app_access_token失败: {data}")


def get_user_access_token(app_access_token: str, code: str) -> Dict:
	"""
	通过用户授权code换取user_access_token和refresh_token
	"""
	url = "https://open.feishu.cn/open-apis/authen/v1/access_token"
	headers = {"Authorization": f"Bearer {app_access_token}"}
	resp = requests.post(url, headers=headers, json={"grant_type": "authorization_code", "code": code})
	data = resp.json()
	if data.get("code") == 0:
		return data["data"]
	else:
		raise Exception(f"获取user_access_token失败: {data}")


def refresh_user_access_token(app_access_token: str, refresh_token: str) -> Dict:
	"""
	通过refresh_token刷新user_access_token
	"""
	url = "https://open.feishu.cn/open-apis/authen/v1/refresh_access_token"
	headers = {"Authorization": f"Bearer {app_access_token}"}
	resp = requests.post(url, headers=headers, json={"grant_type": "refresh_token", "refresh_token": refresh_token})
	data = resp.json()
	if data.get("code") == 0:
		return data["data"]
	else:
		raise Exception(f"刷新user_access_token失败: {data}") 