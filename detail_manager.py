from typing import Any
from kivy.properties import StringProperty, NumericProperty, ColorProperty, ListProperty, ObjectProperty
from kivy.animation import Animation
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from datetime import datetime
from components.detail_screen import DetailScreen
from kivymd.uix.fitimage.fitimage import FitImage

KV = '''
<DetailManager>:
    orientation: "vertical"
    DetailScreen:
        id: detail_screen
'''

Builder.load_string(KV)

class DetailManager(MDBoxLayout):
    def __init__(self, *args: Any, **kwds: Any) -> Any:
        super(DetailManager, self).__init__(**kwds)

    def update_item(self, info):
        # Update the DetailScreen with the provided information
        # print(info)
        detail_screen = self.ids.detail_screen
        detail_screen.ids.name.text = info.get("name", "")
        detail_screen.ids.desc.text = info.get("desc", "")
        detail_screen.ids.rtsp.text = info.get("rtsp", "")
        detail_screen.ids.created_at.text = info.get("date", {}).get("created_at", '')
        detail_screen.ids.last_stopped.text = info.get("date", {}).get("last_stopped", '')  # Fixed typo in key name
        detail_screen.ids.avatar.source = info.get("avatar", "assets/images/doremon.jpeg")
