from typing import Any
import pandas as pd


def read_jiaikucun_excel(file_path: str) -> pd.DataFrame:
	"""
	读取嘉爱库存Excel表格数据到DataFrame。
	:param file_path: Excel文件路径
	:return: 表格数据，pandas DataFrame
	"""
	return pd.read_excel(file_path)


if __name__ == "__main__":
	file_path = "data/jiaikucun.xls"
	df = read_jiaikucun_excel(file_path)
	for idx, row in df.iterrows():
		print(row.to_dict()) 