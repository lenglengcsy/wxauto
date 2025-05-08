from db.message_service import process_and_save_message

def handle_message(chat, msg_item):
    fields = [
        'type', 'content', 'sender', 'sender_remark', 'info', 'control', 'id', 'details'
    ]
    field_str = ', '.join(f"{field}={getattr(msg_item, field, None)}" for field in fields)
    print(f"收到消息：窗口={chat}, {field_str}")
    process_and_save_message(chat, msg_item) 