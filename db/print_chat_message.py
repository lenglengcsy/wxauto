from db.utils import list_chat_messages
import pprint

def main():
    result = list_chat_messages()
    print(f"共{len(result)}条记录，前10条如下：")
    pprint.pprint(result[:10])

if __name__ == '__main__':
    main() 