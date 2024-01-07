from kivy.properties import StringProperty, NumericProperty, ColorProperty, ListProperty, ObjectProperty, BooleanProperty, AliasProperty
from kivy.lang import Builder
from kivy.utils import get_color_from_hex
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDFlatButton
from kivy.animation import Animation
from kivymd.uix.fitimage import FitImage
from kivymd.uix.behaviors import TouchBehavior
from datetime import datetime
from typing import Any

KV = """
<ChatBubble>:
    orientation: "horizontal"
    size_hint: 1,None
    height:self.minimum_height
    canvas.before:
        Color:
            rgba: get_color_from_hex("#99FFCC")
        Line:
            points: self.x, self.y-5, self.x + self.width, self.y-5
            width: 0.4
    MDLabel:
        adaptive_height: True
        id: label
        padding: [dp(8), dp(8)]
        text_color: 1, 1, 1, 1
        text: root.text
        size_hint: 0.5,None
        on_touch_up: root.show_detail_message(*args) if root.detail else None
        height: self.texture_size[1]
        canvas.before:
            Color:
                rgba: get_color_from_hex("#993399") if root.selected else get_color_from_hex("#1E90FF")
            RoundedRectangle:
                size: self.size
                pos: self.pos
                radius: [(dp(-10), dp(10)), dp(8), dp(8), dp(8)]

    MDLabel:
        padding: [dp(4), dp(4)]
        text: root.created_at
        halign: "right"
        adaptive_height: True
        theme_text_color: "Custom"
        text_color: "black"
        size_hint_x: 0.5


<Issues@MDBoxLayout>:
    size_hint: None, None
    width: "150dp"
    height: "100dp"
    padding: 4
    spacing: 4
    orientation: "vertical"
    canvas:
        Color:
            rgba: get_color_from_hex("#993399")
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [dp(8), dp(8), dp(8), (dp(-10), dp(15))]
    FitImage:
        size_hint_x: 1
        size_hint_y: 1
        pos_hint: {"top": 1}
        id: avatar
        radius: 0
        line_color: 0, 0, 0, 0
        size_hint: 0.95, 0.95
        source: root.source_image
    MDLabel:
        text: root.created_at
        size_hint_x: 1
        size_hint_y: None
        halign: "center"
        height: dp(10)
        id: time_label
        theme_text_color: "Custom"
        text_color: "white"
        font_size: '14sp'
"""

Builder.load_string(KV)


class Issues(MDBoxLayout):
    source_image = StringProperty("assets/images/doremon_2.jpeg")
    created_at = StringProperty("")

from kivy.clock import Clock

class ChatBubble(MDBoxLayout):
    send_by_user = BooleanProperty(False)
    selected = BooleanProperty(False)
    created_at = StringProperty("")
    text = StringProperty("")
    detail = ObjectProperty({})

    def __init__(self, *args: Any, **kwds: Any) -> Any:
        super(ChatBubble, self).__init__(**kwds)
        Clock.schedule_once(lambda x: self._init_issue())

    def _init_issue(self):
        self.issues_widget = Issues(
            created_at=self.created_at,
            source_image=self.detail.get("source_image", "")
        )
 

    def show_detail_message(self, instance, touch, is_show=True):
        try:
            target = self.ids.label
            if target.collide_point(*touch.pos):
                self.selected = True
                if is_show:
                    self.issues_widget.pos = (target.pos[0] + target.width + 18, touch.pos[1])
                    self.parent.add_widget(self.issues_widget)
            else:
                self.selected = False
                self.parent.remove_widget(self.issues_widget)
        except Exception as e:
            pass
