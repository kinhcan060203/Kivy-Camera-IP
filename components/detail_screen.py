from typing import Any
from kivy.properties import StringProperty,NumericProperty, ColorProperty,ListProperty,ObjectProperty
from kivy.animation import Animation
from kivy.lang import Builder
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.utils import get_color_from_hex
from kivymd.uix.boxlayout import MDBoxLayout
from datetime import datetime
from kivymd.uix.fitimage.fitimage import FitImage
from kivymd.uix.scrollview import MDScrollView


KV='''

<DetailScreen>:
    orientation: "vertical"

    MDBoxLayout:
        orientation: "horizontal"
        size_hint_y: 0.6
        md_bg_color:"#00B2BF"
        padding:10
        AvatarLayout:
            size_hint:None,None
            pos_hint: {"center_y": 0.5, "center_x": 0.5}
            id: avatar
            width:dp(150)
            height:dp(120)
            radius: 0
            line_color: 0, 0, 0, 0
            source: root.source_image
        InfoLayout:
            size_hint_x: 0.65
            size_hint_y: 1
            MDGridLayout:
                padding: dp(5)
                cols: 2
                row_default_height: dp(40)

                MDLabel:
                    text: 'Name:'
                    font_size: dp(17)
                    color:root.title_color
                    
                MDLabel:
                    id: name
                    text: ''
                    font_size: dp(15)
                    halign:"right"

                MDLabel:
                    text: 'Created at:'
                    font_size: dp(17)
                    color:root.title_color
                    
                MDLabel:
                    id: created_at
                    text: ''
                    font_size: dp(15)
                    halign:"right"
                MDLabel:
                    text: 'Last stoped:'
                    font_size: dp(17)
                    color:root.title_color
                    
                MDLabel:
                    id: last_stopped
                    text: ''
                    font_size: dp(15)
                    halign:"right"
                    

    DescriptionLayout:
        size_hint_y: 0.4
        MDGridLayout:
            md_bg_color:"#6EC3C9"
            padding: dp(10)
            cols: 1
            row_force_default: True
            row_default_height: dp(20)
            spacing:5
            MDLabel:
                text: 'Description:'
                font_style:"H6"
                font_size:dp(17)
                color:root.title_color
    
            MDLabel:
                id: desc
                text: ''
                font_size: dp(15)

            MDLabel:
     
                text: 'IP Address:'
                font_style:"H6"
                font_size: dp(17)
                color:root.title_color
            MDLabel:
                id: rtsp
                text: ''
                font_size: dp(15)


'''

Builder.load_string(KV)
class DetailScreen(MDBoxLayout):
    source_image = StringProperty("assets/images/doremon_2.jpeg")
    title_color = StringProperty("#0066FF")


class AvatarLayout(FitImage):
    pass



class InfoLayout(MDScrollView):
    
    pass

class DescriptionLayout(MDScrollView):
    pass