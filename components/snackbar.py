from typing import Any
from kivy.properties import StringProperty,NumericProperty, ColorProperty,ListProperty
from kivy.metrics import dp
from kivy.clock import Clock
from kivy.core.window import Window
import cv2
from kivymd.uix.snackbar import BaseSnackbar
from kivy.animation import Animation
from kivy.lang import Builder
from kivymd.uix.button import MDFlatButton

KV = '''
<CustomSnackbar>:
    radius :[10,10,0,0]
    top:0
    size_hint_x:1
    pos_hint: {'right': 1}
    size_hint_y:None
    height:dp(60)
    MDIconButton:
        pos_hint: {'center_y': .5}
        icon: root.icon
        opposite_colors: True

    MDLabel:
        id: text_bar
        size_hint_y: None
        height: self.texture_size[1]
        text: root.text
        font_size: dp(17)
        theme_text_color: 'Custom'
        text_color: root.text_color
        shorten: True
        shorten_from: 'right'
        pos_hint: {'center_y': .5}

'''
Builder.load_string(KV) 


class CustomSnackbar(BaseSnackbar):
    
    text = StringProperty(None)
    icon = StringProperty(None)
    font_size = NumericProperty("15sp")
    text_color = StringProperty("#FFFFFF")
    
    
            
            
class Snackbar:
    def __init__(self, *args: Any, **kwds: Any) -> Any:
        self.snackBar = self.snackBar_Success(message="No message!!!")
    def __init_snackBar(self,type,info,show_detail=False):
        message = info["message"] 
        detail = info["detail"] if show_detail and info.get("detail",{}) else {}
        if type == "success":
            snackBar = self.snackBar_Success(message,detail)
            snackBar.md_bg_color = "#66FF33"
        elif type == "failed":
            snackBar = self.snackBar_Failed(message,detail)
            snackBar.md_bg_color = "#FF3333"
        elif type == "warning":
            snackBar = self.snackBar_Warning(message,detail)
            snackBar.md_bg_color = "#FFCC00"

        return snackBar
  
    def die(self,instance):
        anim = Animation(top=0, duration=.4, t='out_quad')
        anim.bind(on_complete=lambda *args: Window.remove_widget(instance))
        anim.start(instance)
        
    def open(self,instance):
        Window.add_widget(instance)
        anim = Animation(top=dp(60), duration=.4, t='out_quad')
        anim.start(self.snackBar)
        Clock.schedule_once(lambda dt: self.die(instance), 3)
    def show_snackBar(self,type,info,show_detail=False):
        self.die(self.snackBar)
        self.snackBar = self.__init_snackBar(type,info,show_detail)
        self.open(self.snackBar)



    def snackBar_Success(self,message="Success!",detail={}):
        snackBar_success =  CustomSnackbar(
            text=message,
            icon="check-circle",
            text_color="white",
            
        )
        snackBar_success.buttons = [
            MDFlatButton(
                text="CANCEL",
                md_bg_color=(1,1,1,0.3),
                on_release=lambda x:self.die(snackBar_success),
            ),
        ]
        return snackBar_success



    def snackBar_Failed(self,message = "Failed",detail={}):

        snackBar_failed = CustomSnackbar(
            text=message,
            icon="alert-circle",
            text_color="black",
        )
        snackBar_failed.buttons = [
            MDFlatButton(
                text="MORE DETAIL",
                text_color="black",
                md_bg_color=(1,1,1,0.3),
                on_release=lambda x:self.show_snackBar("failed",detail)
            ) if detail else MDFlatButton(),
            MDFlatButton(
                text="CANCEL",
                md_bg_color=(1,1,1,0.3),
                on_release=lambda x:self.die(snackBar_failed),
            ),
        ]
        return snackBar_failed

    def snackBar_Warning(self,message="Warning",detail={}):
        snackBar_warning = CustomSnackbar(
            text=message,
            icon="cancel",
            text_color="white",
        )
        snackBar_warning.buttons = [
            MDFlatButton(
                text="MORE DETAIL",
                md_bg_color=(1,1,1,0.3),
                on_release=lambda x:self.show_snackBar("warning",detail) 
            ) if detail else MDFlatButton(),
            MDFlatButton(
                text="CANCEL",
                md_bg_color=(1,1,1,0.3),
                on_release=lambda x:self.die(snackBar_warning),
            ),
        ]
        return snackBar_warning
    
