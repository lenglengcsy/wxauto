from wx.listener import MessageListener
from wx.config import LISTEN_LIST
from wx.handler import handle_message

if __name__ == "__main__":
    listener = MessageListener(listen_list=LISTEN_LIST, wait=1)
    print("开始监听微信消息...")
    listener.listen_forever(handle_message)
