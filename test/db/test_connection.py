import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import unittest
from db.connection import get_connection, close_connection
from db.crud import get_chat_history_by_window_name

class TestDBConnection(unittest.TestCase):
    def test_connect(self):
        conn = None
        try:
            conn = get_connection()
            self.assertIsNotNone(conn)
        finally:
            close_connection(conn)

    def test_get_chat_history_by_window_name(self):
        window_name = "测试群聊"
        result = get_chat_history_by_window_name(window_name, limit=10)
        self.assertIsInstance(result, list)
        # 允许为空，但类型必须正确
        if result:
            self.assertIsInstance(result[0], tuple)

if __name__ == '__main__':
    unittest.main() 