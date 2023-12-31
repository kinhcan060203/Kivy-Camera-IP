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


        
class RegisterScreen(MDScreen):
    name = "register_screen"
    submit_success = ObjectProperty(int)  
    radius:[12,0,0,12]
    
    def __init__(self, *args: Any, **kwds: Any) -> Any:
        super(RegisterScreen, self).__init__(**kwds)
        self.confirmForm = None


    def check_valid(self):
        nameText = self.ids.name.text
        rtspText = self.ids.rtsp.text
        desc = self.ids.desc.text
        if len(nameText) > 0  and len(desc)>0:
            self.show_confirm()
            return True
        return False
    
    
    def show_confirm(self):
        self.confirmForm = MDDialog(
            title="ADD CAMERA", 
            text="Are you sure to add the camera?", 
            buttons=[
                MDFlatButton(
                    text="CANCEL",
                    theme_text_color="Custom",
                    text_color="blue",
                    on_release=lambda x:self.confirmForm.dismiss()
                ),
                MDRaisedButton(
                    text="ACCEPT",
                    theme_text_color="Custom",
                    text_color="black",
                    on_release=lambda x:self.submit_form()
                ),
            ],
        )
        self.confirmForm.open()

     
    def submit_form(self):
        nameText = self.ids.name.text
        rtspText = self.ids.rtsp.text
        desc = self.ids.desc.text
        
        self.confirmForm.dismiss()

        self.submit_success({
            "name":nameText,
            "rtsp":rtspText,
            "desc":desc
        })
        
        self.ids.name.text = ''
        self.ids.rtsp.text = ''
        self.ids.desc.text = ''