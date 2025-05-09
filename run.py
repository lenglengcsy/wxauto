from test.llm.coze.test_client import test_send_message
from wx.listener import MessageListener
from wx.config import LISTEN_LIST
from wx.handler import handle_message
from wx.history import load_recent_histories, data as recent_histories

if __name__ == "__main__":
	load_recent_histories(LISTEN_LIST)
	print("已加载历史聊天记录：")
	for k, v in recent_histories.items():
		print(f"{k}: {len(v)} 条")
	listener = MessageListener(listen_list=LISTEN_LIST, wait=1)
	print("开始监听微信消息...")
	listener.listen_forever(handle_message)
	# test_send_message()