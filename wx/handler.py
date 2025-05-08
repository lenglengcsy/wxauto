from db.message_service import process_and_save_message

def handle_message(chat, msg_item):
    print(f"收到消息：发送者={chat}, 类型={getattr(msg_item, 'type', None)}")
    # 打印msg_item的所有字段和值
    for attr in dir(msg_item):
        if not attr.startswith('__') and not callable(getattr(msg_item, attr)):
            print(f"  {attr}: {getattr(msg_item, attr)}")
    process_and_save_message(chat, msg_item) 