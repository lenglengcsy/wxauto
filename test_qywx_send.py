from qywx.api.client import QywxClient
from qywx.api.message import send_text_message
from qywx.config import QYWX_CONFIG

if __name__ == "__main__":
	client = QywxClient(
		corp_id=QYWX_CONFIG["corp_id"],
		corp_secret=QYWX_CONFIG["corp_secret"]
	)
	departments = client.get_all_departments()
	print(departments) 