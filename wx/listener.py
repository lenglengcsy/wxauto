from wxautox import WeChat
import time
from typing import List, Dict, Any

class MessageListener:
    def __init__(self, listen_list: List[str] = None, wait: int = 1):
        self.wx = WeChat()
        self.listen_list = listen_list or []
        self.wait = wait
        self._init_listeners()

    def _init_listeners(self):
        for who in self.listen_list:
            self.wx.AddListenChat(who=who, savepic=True, savefile=True, savevoice=True)

    def listen_once(self) -> Dict[str, Any]:
        """
        获取一次监听到的新消息。
        返回格式与wxautox的GetListenMessage一致。
        """
        return self.wx.GetListenMessage()

    def listen_forever(self, callback):
        """
        持续监听消息，每当有新消息时调用callback。
        callback参数为(window_name, msg_item)
        """
        while True:
            msgs = self.listen_once()
            # 用zip将监听名称与消息内容绑定
            for name, chat_msgs in zip(self.listen_list, msgs.values()):
                for item in chat_msgs:
                    callback(name, item)
            time.sleep(self.wait) 