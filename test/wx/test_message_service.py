import sys
import os
import unittest
from datetime import datetime

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from db.utils import list_chat_messages
from db.message_service import process_and_save_message

class TestMessageService(unittest.TestCase):
    def test_process_and_save_message(self):
        # 构造模拟消息对象
        class MsgItem:
            def __init__(self, sender, receiver, content, time):
                self.sender = sender
                self.receiver = receiver
                self.content = content
                self.time = time
                self.type = 'friend'
        now = datetime.now()
        msg = MsgItem('测试发送者', '测试接收者', '这是一条测试消息', now)
        chat = '测试窗口'
        process_and_save_message(chat, msg)
        # 查询数据库，验证是否写入
        messages = list_chat_messages()
        self.assertTrue(any(
            m[1] == '测试发送者' and m[2] == '测试接收者' and m[5] == '这是一条测试消息'
            for m in messages
        ))

if __name__ == '__main__':
    unittest.main() 