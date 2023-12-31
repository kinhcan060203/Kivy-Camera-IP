from typing import Any
from kivymd.color_definitions import colors
from kivymd.uix.button import MDFlatButton,MDRaisedButton
from kivy.properties import StringProperty,NumericProperty, ColorProperty,ListProperty
from kivymd.uix.list import OneLineIconListItem
from kivy.metrics import dp
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics.texture import Texture
import cv2
from kivymd.uix.snackbar import BaseSnackbar
from kivy.animation import Animation
from kivymd.uix.dialog import MDDialog




class IconListItem(OneLineIconListItem):
    icon = StringProperty()



class CustomSnackbar(BaseSnackbar):
    text = StringProperty(None)
    icon = StringProperty(None)
    font_size = NumericProperty("15sp")
    text_color = StringProperty("#FFFFFF")

class KivyCamera(Image):
    def __init__(self, capture, fps, **kwargs):
        super(KivyCamera, self).__init__(**kwargs)
        self.capture = capture
        Clock.schedule_interval(self.update, 1.0 / fps)

    def update(self):
        for _ in range(5):
            ret, frame = self.capture.read()
        if ret:
            buf1 = cv2.flip(frame, 0)
            buf = buf1.tostring()
            image_texture = Texture.create(
                size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            self.texture = image_texture
            
            
            
class SnackbarManager:
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
            snackBar.md_bg_color = "#FFCC00"
        elif type == "warning":
            snackBar = self.snackBar_Warning(message,detail)
            snackBar.md_bg_color = "#FF3333"

        return snackBar
  
    def die(self,instance):
        anim = Animation(top=0, duration=.3, t='out_quad')
        anim.bind(on_complete=lambda *args: Window.remove_widget(instance))
        anim.start(instance)
        
    def open(self,instance):
        Window.add_widget(instance)
        anim = Animation(y=10, duration=.3, t='out_quad')
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
    





# app.py
# def _enabledWithStatus(self,session):
#     if not self._auth_session(session):
#         return False
    
#     for id_btn,button in self.root.ids.home.ids.items():
#         if id_btn.startswith("abtn"):
#             if id_btn.rsplit("_",1)[-1] in allow_action_list[session["status"]]:
#                 self._enabledButton(button,colors["Orange"]["300"])
#             else:
#                 self._disabledButton(button)
#     return True
    
# def on_press(self,button):
#     button.md_bg_color = colors["Orange"]["600"]
    
# def _disabledButton(self,button):
#     button.disabled = True
#     button.line_width=1
# def _enabledButton(self,button,color):
#     button.disabled = False
#     button.md_bg_color = color
#     button.line_width=2
    
# def _disabledAllActionButton(self,session):
#     if not self._auth_session(session):
#         return False
    
#     for id_btn,button in self.root.ids.home.ids.items():
#         if id_btn.startswith("abtn"):
#             self._disabledButton(button)
#     return True
    