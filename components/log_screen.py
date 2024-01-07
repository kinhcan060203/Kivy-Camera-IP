
from typing import Any
from kivy.properties import StringProperty,NumericProperty, ColorProperty,ListProperty,ObjectProperty
from kivy.animation import Animation
from kivy.lang import Builder
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.utils import get_color_from_hex
from datetime import datetime


KV='''
<LogScreen>:
    RecycleView:
        id: chat_rv
        data: root.data
        viewclass: "ChatBubble"
        scroll_y: 0
        padding: [0, 80, 0, 0]
        RecycleBoxLayout:
            id: box
            padding: dp(10)
            spacing: dp(15)
            orientation: "vertical"
            size_hint_y: None
            height: self.minimum_size[1]
            default_size_hint: 1, None

'''


Builder.load_string(KV)
from kivymd.uix.screen import MDScreen
class LogScreen(MDScreen):
    name = StringProperty("log_screen")
    data = ListProperty([])

    def __init__(self, *args: Any, **kwds: Any) -> Any:
        super(LogScreen, self).__init__(**kwds)

    def add_message(self,content):
        self.data.append(content)
