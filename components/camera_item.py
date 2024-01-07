from typing import Any
from kivy.properties import StringProperty, NumericProperty, ColorProperty, ListProperty, ObjectProperty,BooleanProperty
from kivy.utils import get_color_from_hex
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from datetime import datetime

# KV Language string for the UI layout
KV = '''
<CameraItem>:
    id: "camera"
    padding: dp(5)
    size_hint_y: None
    height: dp(110)
    MDNavigationDrawer:
        md_bg_color: "#CC66FF" if root.selected else "#BFCAE6"
        
        type: "standard"
        size_hint_x: 0.95
        elevation: 3
        radius: [16, 16, 16, 16]
        padding: 5
        MDBoxLayout:
            radius: [8, 8, 8, 8]
            spacing: dp(8)
            padding: 5
            orientation: "vertical"
            canvas.before:
                RoundedRectangle:
                    size: self.size
                    pos: self.pos
                    texture: Gradient.horizontal(get_color_from_hex("#66CC99"), get_color_from_hex("#0099FF"))
                    radius: [6, 6, 6, 6]
            MDBoxLayout:
                orientation: "horizontal"
                size_hint_y: 0.65
                id: contents
                FitImage:
                    id: image
                    radius: 2
                    line_color: 0, 0, 0, 0
                    size_hint: None, 0.80
                    width: dp(60)
                    source: root.content["avatar"]
                    pos_hint: {"right": 0.9, "center_y": 0.5}
                MDExpansionPanelTwoLine:
                    md_bg_color: "red"
                    _txt_left_pad: dp(12)
                    _txt_right_pad: dp(12)
                    _txt_bot_pad: dp(4)
                    _txt_top_pad: dp(4)
                    size_hint_x: 0.95
                    size_hint_y: 1
                    pos_hint: {"top": 1, "center_x": 0.5}
                    secondary_text: root.content['desc']
                    text: root.content['name']
                    font_size: "22dp"
                    font_style: "H6"
            StatusBar:
                size_hint_y: 0.35
                pos_hint: {"center_x": 0.5, "center_y": 0.5}
                padding: [0, dp(12), 0, dp(8)]
<StatusBar>:

    canvas.before:
        Color:
            rgba: get_color_from_hex("#CCCCCC")
        Line:
            points: self.x, self.y + self.height, self.x + self.width, self.y + self.height
            width: 0.1
    MDLabel:
        id: status_text
        text: root.status_text
        pos_hint: {"center_y": 0.5}
        font_size: '15sp'
        color: root.status_color
    MDIcon:
        id: status_icon
        pos_hint: {"right": 1, "center_y": 0.5}
        icon: root.status_icon
        font_size: '25sp'
        color: root.status_color
'''

Builder.load_string(KV)
class StatusBar(MDBoxLayout):
    status_text = StringProperty("No data")
    status_color =StringProperty("#FF3333")
    status_icon =StringProperty("alert-circle")
    

class CameraItem(MDBoxLayout):
    content = ObjectProperty({})
    selected = BooleanProperty(False)
    danger_line_color = ColorProperty("#FF3333")
    active_line_color =ColorProperty("#3366FF")
    normal_line_color =ColorProperty([0, 0, 0, 0])
    
    
    def __init__(self, *args: Any, **kwds: Any) -> Any:
        super(CameraItem, self).__init__(**kwds)
        self.bind(on_touch_up=self.on_release)
        self.selected = False

    def on_release(self, instance, touch):
        if self.parent.parent.get_selected():
            return
        if self.collide_point(*touch.pos):
            self.select()
        else:
            self.unselect()

    def select(self):
        self.selected = True
        detail_manager = MDApp.get_running_app().root.ids.detail_manager
        detail_manager.update_item(self.content)
        self.parent.md_bg_color = self.active_line_color
        

    def unselect(self):
        self.selected = False
        self.parent.md_bg_color = self.normal_line_color

    def check(self):
        if self.selected:
            self.parent.md_bg_color = self.danger_line_color

    def uncheck(self):
        if self.selected:   
            self.parent.md_bg_color = self.active_line_color
