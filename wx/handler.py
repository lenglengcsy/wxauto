from db.message_service import process_and_save_message
from lib.cozepy.chat import MessageType
from llm.coze.client import CozeClient
from wxautox import WeChat
from typing import Any

def handle_message(wx, chat: str, msg_item: Any) -> None:
    """
    处理收到的消息：
    1. 保存消息到数据库
    2. 发送消息到coze，获取回复
    3. 通过wxautox发送回复给用户
    :param chat: 聊天窗口名
    :param msg_item: 消息对象，需有content属性
    """
    fields = [
        'type', 'content', 'sender', 'sender_remark', 'info', 'control', 'id', 'details'
    ]
    field_str = ', '.join(f"{field}={getattr(msg_item, field, None)}" for field in fields)
    print(f"收到消息：窗口={chat}, {field_str}")
    process_and_save_message(chat, msg_item)

    # 只处理文本消息
    if not hasattr(msg_item, 'content') or not msg_item.content:
        return

    # 调用coze获取回复
    coze_client = CozeClient()
    coze_response = coze_client.send_message(message=msg_item.content, user_id=str(getattr(msg_item, 'sender', 'default_user')))
    # 提取coze回复内容（取最后一条role为assistant的消息）
    reply = None
    for m in reversed(coze_response.get('messages', [])):
        if m.get('role') == 'assistant' and m.get('content') and m['type'] == MessageType.ANSWER:
            reply = m['content']
            break
    if not reply:
        reply = "[机器人未返回有效内容]"

    # 发送回复到微信
    # msg_item.quote(reply)
    # wx = WeChat()
    wx.SendMsg(reply) 