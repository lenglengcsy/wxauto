import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)

from typing import Optional
from lark.config import (
	LARK_APP_ID, LARK_APP_SECRET,
	LARK_USER_REFRESH_TOKEN,
	get_app_access_token, get_user_access_token, refresh_user_access_token
)

# 注意：首次获取user_access_token需要人工获取code
USER_AUTH_CODE: Optional[str] = None  # 填写实际code后再运行


def test_get_app_access_token():
	"""测试获取app_access_token"""
	app_token = get_app_access_token(LARK_APP_ID, LARK_APP_SECRET)
	print(f"app_access_token: {app_token}")
	return app_token


def test_get_user_access_token():
	"""测试用code换取user_access_token和refresh_token"""
	if not USER_AUTH_CODE:
		print("请先填写USER_AUTH_CODE")
		return
	app_token = get_app_access_token(LARK_APP_ID, LARK_APP_SECRET)
	user_token_data = get_user_access_token(app_token, USER_AUTH_CODE)
	print(f"user_access_token: {user_token_data['access_token']}")
	print(f"refresh_token: {user_token_data['refresh_token']}")
	return user_token_data


def test_refresh_user_access_token():
	"""测试用refresh_token刷新user_access_token"""
	if not LARK_USER_REFRESH_TOKEN:
		print("请先在config.py中填写LARK_USER_REFRESH_TOKEN")
		return
	app_token = get_app_access_token(LARK_APP_ID, LARK_APP_SECRET)
	new_token_data = refresh_user_access_token(app_token, LARK_USER_REFRESH_TOKEN)
	print(f"new user_access_token: {new_token_data['access_token']}")
	print(f"new refresh_token: {new_token_data['refresh_token']}")
	return new_token_data


if __name__ == "__main__":
	print("--- 测试获取 app_access_token ---")
	test_get_app_access_token()
	print("\n--- 测试用 code 换 user_access_token（需手动填写code） ---")
	test_get_user_access_token()
	print("\n--- 测试用 refresh_token 刷新 user_access_token ---")
	test_refresh_user_access_token() 