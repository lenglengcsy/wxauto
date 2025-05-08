import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import unittest
from db.connection import get_connection, close_connection

class TestDBConnection(unittest.TestCase):
    def test_connect(self):
        conn = None
        try:
            conn = get_connection()
            self.assertIsNotNone(conn)
        finally:
            close_connection(conn)

if __name__ == '__main__':
    unittest.main() 