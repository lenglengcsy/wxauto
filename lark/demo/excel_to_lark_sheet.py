from typing import List
import pandas as pd
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) )
from utils.excel_utils import read_jiaikucun_excel
import lark_oapi as lark
from lark_oapi.api.sheets.v3 import *
from lark_oapi.api.sheets.v3.model import Spreadsheet, QuerySpreadsheetSheetRequest
import requests
from lark_oapi.api.drive.v2 import *
from lark_oapi.api.drive.v2.model import PatchPermissionPublicRequest, PermissionPublic
from lark.config import get_app_access_token

def add_collaborator(spreadsheet_token: str, open_id: str, user_access_token: str):
	url = f"https://open.feishu.cn/open-apis/sheets/v3/spreadsheets/{spreadsheet_token}/collaborators/add"
	headers = {
		"Authorization": f"Bearer {user_access_token}",
		"Content-Type": "application/json"
	}
	data = {
		"collaborators": [
			{"open_id": open_id}
		]
	}
	resp = requests.post(url, headers=headers, json=data)
	print("添加协作者响应:", resp.text)
	if resp.status_code != 200 or resp.json().get("code") != 0:
		raise Exception(f"添加协作者失败: {resp.text}")


def set_sheet_permission(spreadsheet_token: str, user_access_token: str):
	url = "https://open.feishu.cn/open-apis/drive/v1/permissions/public"
	headers = {
		"Authorization": f"Bearer {user_access_token}",
		"Content-Type": "application/json"
	}
	data = {
		"token": spreadsheet_token,
		"type": "sheet",
		"permission_public": {
			"external_access": False,
			"security_entity": "tenant",
			"comment_entity": "tenant",
			"share_entity": "tenant",
			"link_share_entity": "tenant"
		}
	}
	resp = requests.patch(url, headers=headers, json=data)
	print("设置权限响应:", resp.text)
	if resp.status_code != 200 or resp.json().get("code") != 0:
		raise Exception(f"设置权限失败: {resp.text}")


def set_sheet_permission_sdk(client, spreadsheet_token: str, option):
	request = PatchPermissionPublicRequest.builder() \
		.token(spreadsheet_token) \
		.type("sheet") \
		.request_body(
			PermissionPublic.builder()
				.external_access_entity("closed")  # 企业外不可访问
				.security_entity("anyone_can_edit")  # 所有人可编辑
				.comment_entity("anyone_can_edit")  # 所有人可评论
				.share_entity("same_tenant")  # 企业内可分享
				.manage_collaborator_entity("collaborator_full_access")  # 协作者完全管理
				.link_share_entity("tenant_readable")  # 企业内可通过链接访问
				.copy_entity("anyone_can_edit")  # 所有人可复制
				.build()
		) \
		.build()
	response = client.drive.v2.permission_public.patch(request, option)
	print("设置权限响应:", response.raw.content)
	if not response.success():
		raise Exception(f"设置权限失败: {response.msg}")


def excel_to_lark_sheet(file_path: str, sheet_title: str = '嘉爱库存') -> str:
	"""
	读取Excel并创建飞书电子表格，写入数据
	:param file_path: Excel文件路径
	:param sheet_title: 飞书Sheet名称
	:return: 新建Sheet的URL
	"""
	# 读取Excel
	df = read_jiaikucun_excel(file_path)
	# 1. 创建电子表格
	client = lark.Client.builder().enable_set_token(True).build()
	LARK_USER_ACCESS_TOKEN = get_app_access_token()
	option = lark.RequestOption.builder().user_access_token(LARK_USER_ACCESS_TOKEN).build()
	create_req_body = Spreadsheet.builder().title(sheet_title).build()
	create_req = CreateSpreadsheetRequest.builder().request_body(create_req_body).build()
	create_resp = client.sheets.v3.spreadsheet.create(create_req, option)
	if not create_resp.success():
		raise Exception(f"创建Sheet失败: {create_resp.msg}")
	spreadsheet_token = create_resp.data.spreadsheet.spreadsheet_token
	# 2. 获取第一个工作表ID（用SDK方式）
	query_req = QuerySpreadsheetSheetRequest.builder() \
		.spreadsheet_token(spreadsheet_token) \
		.build()
	query_resp = client.sheets.v3.spreadsheet_sheet.query(query_req, option)
	if not query_resp.success():
		raise Exception(f"获取Sheet列表失败: {query_resp.msg}")
	
	first_sheet_id = query_resp.data.sheets[0].sheet_id
	# 强制写入A:Z
	range_str = f"{first_sheet_id}!A:Z"

	# 3. 添加自己为协作者，确保有写入权限
	my_open_id = "你的open_id"  # TODO: 替换为实际open_id
	# add_collaborator(spreadsheet_token, my_open_id, LARK_USER_ACCESS_TOKEN)

	# 3.1 设置表格权限为企业内可编辑（SDK方式）
	set_sheet_permission_sdk(client, spreadsheet_token, option)

	# 4. 组织数据
	values: List[List[str]] = [list(map(str, df.columns))]  # 表头
	for _, row in df.iterrows():
		values.append([str(row[col]) for col in df.columns])
	# 5. 用requests插入数据
	headers = {
		"Authorization": f"Bearer {LARK_USER_ACCESS_TOKEN}",
		"Content-Type": "application/json"
	}
	data = {
		"valueRange": {
			"range": range_str,
			"values": values
		},
		"insert_option": "INSERT_ROWS"
	}
	# spreadsheet_token = "PUZysJ9XRhpHpmt1Oohc4PWqn5I"
	
	url_api = f"https://open.feishu.cn/open-apis/sheets/v2/spreadsheets/{spreadsheet_token}/values_prepend"
	print("请求URL:", url_api)
	print("请求数据:", data)
	print("请求headers:", headers)
	resp = requests.post(url_api, headers=headers, json=data)
	print("响应内容:", resp.text)
	if resp.status_code != 200 or resp.json().get("code") != 0:
		raise Exception(f"插入Sheet失败: {resp.text}")
	# 5. 返回Sheet链接
	url = create_resp.data.spreadsheet.url
	return url


def main():
	file_path = 'data/jiaikucun.xls'
	url = excel_to_lark_sheet(file_path)
	print(f'已创建飞书电子表格，访问链接：{url}')


if __name__ == '__main__':
	main() 