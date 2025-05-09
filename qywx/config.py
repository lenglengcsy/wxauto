from typing import TypedDict

class QywxConfig(TypedDict):
	corp_id: str
	corp_secret: str
	agentid: int

# 企业微信配置
QYWX_CONFIG: QywxConfig = {
	"corp_id": "ww91ee8350415bca9a",
	"corp_secret": "81Y13qlus6811SeD9c_CmaZpiNbG4C4kByfprnqtbMs",
	"agentid": 1000008
} 