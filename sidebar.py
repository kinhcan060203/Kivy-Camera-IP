from typing import Any
from kivymd.color_definitions import colors
from kivymd.uix.button import MDFlatButton,MDRaisedButton
from kivy.properties import StringProperty,NumericProperty, ColorProperty,ListProperty,ObjectProperty
from kivy.metrics import dp
from kivy.animation import Animation
from kivymd.uix.dialog import MDDialog
from kivymd.uix.screen import MDScreen
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.navigationdrawer.navigationdrawer import MDNavigationDrawer
from kivymd.uix.boxlayout import MDBoxLayout



class CameraItem(MDBoxLayout):
    text = StringProperty("")
    secondary_text = StringProperty("")
    def __init__(self, text='',secondary_text='',*args: Any, **kwds: Any) -> Any:
        super(CameraItem, self).__init__(**kwds)
        self.text = text
        self.secondary_text = secondary_text

class SidebarManager(MDBoxLayout):
    
    def __init__(self, *args: Any, **kwds: Any) -> Any:
        super(SidebarManager, self).__init__(**kwds)
    def add_cameraItem(self,item):
        name = item["name"]
        rtsp = item["rtsp"]
        desc = item["desc"]
        self.ids.camera_manager.add_widget(CameraItem(name,desc))
        