import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from llm import GPT
from wxauto import WeChatC
import time
import wxauto.utils as wxutils
# from dotenv import load_dotenv

# 读取相关环境变量
# load_dotenv()

# gpt = GPT(
#     api_key = os.getenv('OPENAI_API_KEY'),
#     base_url = os.getenv('OPENAI_BASE_URL'),
#     prompt="你是一个智能助手，用于回复人们的各种问题"
# )

wx = WeChatC()
# 指定监听目标
listen_list = [
    'AI小助手',
]
for i in listen_list:
    wx.AddListenChat(who=i, savepic=True, savefile=True, savevoice=True)  # 添加监听对象
    # wx.get_listen_message_background(i)
    
# wx.resize_main_window(50,50)
# 持续监听消息，有消息则对接大模型进行回复
wait = 1  # 设置1秒查看一次是否有新消息
while True:
    msgs = wx.GetListenMessage()
    # msgs = wx.GetAllNewMessage()
    for chat in msgs:
        msg = msgs.get(chat)   # 获取消息内容
        for i in msg:
            if i.type == 'friend':
                # ===================================================
                # 处理消息逻辑
                
                # reply = gpt.chat(i.content)
                reply = "OK"                
                # ===================================================
                print(f'msg：{i.content}')
                wx.show_main_window_no_activate()
                # 回复消息
                chat.SendMsg(reply)  # 回复
    time.sleep(wait)
