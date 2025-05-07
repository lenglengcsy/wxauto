from .wxauto import WeChat
import wxauto.uiautomation as uia
import wxauto.utils as wxutils
import ctypes

class WeChatC(WeChat):
    """
    WeChatC类，继承自WeChat，可以重写或增加方法以实现自定义需求。
    """
    def custom_method(self, msg):
        """
        示例自定义方法：打印一条自定义消息。
        """
        print(f"[WeChatC自定义方法] {msg}") 

    def set_main_window_inactive(self):
        """
        让微信主界面处于非激活状态（切换到桌面或其他窗口）。
        """
        # 切换到桌面（Win+D）
        uia.SendKeys('{Win}d') 

    def set_focus_to_previous_window(self):
        """
        切换到上一个激活的窗口（Alt+Tab）。
        """
        # 模拟Alt+Tab切换到上一个窗口
        # 这里用SendKeys模拟，部分系统可能需要管理员权限
        uia.SendKeys('%{TAB}') 

    def resize_main_window(self, width, height):
        """
        将微信主窗口缩放到指定宽高。
        :param width: 目标宽度
        :param height: 目标高度
        """
        hwnd = wxutils.FindWindow(classname='WeChatMainWndForPC')
        if hwnd:
            # 获取屏幕尺寸，防止超出屏幕
            user32 = ctypes.windll.user32
            screen_width = user32.GetSystemMetrics(0)
            screen_height = user32.GetSystemMetrics(1)
            # 保证窗口不会超出屏幕
            x = min(max(0, screen_width - width - 20), screen_width - width)
            y = min(max(0, screen_height - height - 20), screen_height - height)
            wxutils.win32gui.ShowWindow(hwnd, 1)
            wxutils.win32gui.MoveWindow(hwnd, x, y, width, height, True)
        else:
            print("未找到微信主窗口，无法缩放。") 

    def get_listen_message_background(self, who=None):
        """
        后台监听消息，不切换聊天窗口，不弹出对话框。
        who: 指定监听的对象名，None为所有监听对象
        返回：消息字典，结构同GetListenMessage
        """
        # 直接遍历self.listen，不调用ChatWith等会切换窗口的方法
        msgs = {}
        listen_targets = [who] if who and who in self.listen else list(self.listen.keys())
        for target in listen_targets:
            chat = self.listen[target]
            msg = chat.GetNewMessage(savepic=chat.savepic, savefile=chat.savefile, savevoice=chat.savevoice)
            if msg:
                msgs[chat] = msg
        return msgs 
    
    def show_main_window_no_activate(self):
        hwnd = wxutils.FindWindow(classname='WeChatMainWndForPC')
        if hwnd:
            wxutils.win32gui.ShowWindow(hwnd, 4)  # SW_SHOWNA