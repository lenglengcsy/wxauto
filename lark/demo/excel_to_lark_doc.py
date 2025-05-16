from typing import List
import pandas as pd

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)

from utils.excel_utils import read_jiaikucun_excel
import lark_oapi as lark
from lark_oapi.api.docx.v1 import *
from lark_oapi.api.docx.v1.model import *
from lark.config import LARK_USER_ACCESS_TOKEN
from lark_oapi.core import JSON


def get_excel_table_blocks(file_path: str) -> List[Block]:
	df = read_jiaikucun_excel(file_path)
	table_property = TableProperty.builder() \
		.row_size(len(df) + 1) \
		.column_size(len(df.columns)) \
		.header_row(True) \
		.build()
	cells = []
	# 表头
	for col in df.columns:
		text_run = TextRun.builder().content(str(col)).build()
		text_element = TextElement.builder().text_run(text_run).build()
		cell_str = JSON.marshal(text_element)
		cells.append(cell_str)
	# 数据
	for _, row in df.iterrows():
		for col in df.columns:
			text_run = TextRun.builder().content(str(row[col])).build()
			text_element = TextElement.builder().text_run(text_run).build()
			cell_str = JSON.marshal(text_element)
			cells.append(cell_str)
	table = Table.builder().cells(cells).property(table_property).build()
	block = Block.builder().table(table).block_type(12).build()
	return [block]


def get_or_create_doc(client, title: str, folder_token: str = None) -> str:
	# 这里只演示新建，实际可先查找
	req_body = CreateDocumentRequestBody.builder().title(title)
	if folder_token:
		req_body.folder_token(folder_token)
	request = CreateDocumentRequest.builder().request_body(req_body.build()).build()
	option = lark.RequestOption.builder().user_access_token(LARK_USER_ACCESS_TOKEN).build()
	resp = client.docx.v1.document.create(request, option)
	if not resp.success():
		raise Exception(f"创建文档失败: {resp.msg}")
	return resp.data.document.document_id


def insert_table_to_doc(client, document_id: str, blocks: List[Block]):
	# 飞书文档根block_id固定为'doc-content'
	root_block_id = 'doc-content'
	option = lark.RequestOption.builder().user_access_token(LARK_USER_ACCESS_TOKEN).build()
	# 插入表格
	req_body = CreateDocumentBlockChildrenRequestBody.builder().children(blocks).build()
	req = CreateDocumentBlockChildrenRequest.builder() \
		.document_id(document_id) \
		.block_id(root_block_id) \
		.request_body(req_body) \
		.build()
	resp = client.docx.v1.document_block_children.create(req, option)
	if not resp.success():
		raise Exception(f"插入表格失败: {resp.msg}")


def main():
	client = lark.Client.builder().enable_set_token(True).build()
	file_path = 'data/jiaikucun.xls'
	title = '嘉爱库存'
	blocks = get_excel_table_blocks(file_path)
	document_id = get_or_create_doc(client, title)
	insert_table_to_doc(client, document_id, blocks)
	print('同步完成')


if __name__ == '__main__':
	main() 