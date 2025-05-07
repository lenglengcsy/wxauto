from .wxauto import WeChat

class WeChatC(WeChat):
    """
    WeChatC类，继承自WeChat，可以重写或增加方法以实现自定义需求。
    """
    def custom_method(self, msg):
        """
        示例自定义方法：打印一条自定义消息。
        """
        print(f"[WeChatC自定义方法] {msg}") 