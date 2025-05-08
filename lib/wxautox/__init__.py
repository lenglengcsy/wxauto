# cython: language_level=3
from .wxauto import WeChat
from .elements import WxParam, LoginWnd
from .utils import *
from . import (
    uiautomation,
    errors,
    languages,
    color
)
import win32ui
import tenacity
import comtypes.stream

__version__ = VERSION

__all__ = [
    'WeChat', 
    'VERSION',
    'WxParam',
    'OpenWeChat',
    'LoginWnd'
]
