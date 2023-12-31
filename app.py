from kivy.lang import Builder
from kivymd.app import MDApp
import requests
from kivymd.color_definitions import colors,palette
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.screen import MDScreen
from kivy.metrics import dp
from utils import KivyCamera,SnackbarManager
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.animation import Animation
import cv2
from kivymd.uix.dialog import MDDialog
from typing import Any
from kivymd.uix.button import MDFlatButton,MDRaisedButton
from kivy.properties import StringProperty,NumericProperty, ColorProperty,ListProperty,ObjectProperty
from register import RegisterScreen
from sidebar import SidebarManager


allow_action_list =  {
    "running":["performance","balanced","mode","stop"],
    "stop":["init"],
    "ready":["start"]
}

database = {
    "user1" :{
        "email": "anhnh.t1.1821@gmail.com",
        "status":"stop",
        "detail":{
            "rtsp":f"",
        }
    },
    "user2" :{
        "email": "lamngocanh060203@gmail.com",
        "status":"running",
        "detail":{
            "rtsp":f"",
        }
        
    }
}
class HomeScreen(MDScreen):
    pass
class SettingsScreen(MDScreen):
    pass


        
class MainApp(MDApp):
    def __init__(self, **kwargs):
        super(MainApp, self).__init__(**kwargs)
        Builder.load_file('kv/utils.kv') 
        Builder.load_file('kv/register.kv') 
        Builder.load_file('kv/home.kv') 
        Builder.load_file('kv/settings.kv') 
        Builder.load_file('kv/sidebar.kv') 
        self.menu=[]
        self.snackbarManager = SnackbarManager()
        self.user = database["user1"]
        self.current_page = "home_screen"
        
    def build(self):
        return Builder.load_file('kv/main.kv') 
    def on_start(self):
        self.root.ids.sideBar.set_state()
    def _init_camera(self,rtps):
        try:
            self.capture = cv2.VideoCapture(rtps)
            self.my_camera = KivyCamera(capture=self.capture, fps=2)
        except Exception as e:
            return False
        return True
        
    def submit_success_camera(self,item):
        self.root.ids.sidebar_manager.add_cameraItem(item)
        self.redirect_page("home_screen")

    def redirect_page(self, place):
        self.root.ids.screen_manager.current = place
        self.current_page = place
        if self.menu:
            self.menu.dismiss()
    def on_stop(self):
        pass
        # if self.capture:
        #     self.capture.release()
        
        
    def _auth_session(self, session):
        # check database status của username
        return True
        
    def show_dropdown(self,instance):
        
        menu_items = [
            {
                "viewclass": "IconListItem",
                "icon": "home-variant",
                "height": dp(56),
                "text": f"Nhà",
                "bg_color":(0,1,1,1) if self.current_page=="home_screen" else (0,1,1,0.2),
                "font_style":"H6",
                "on_release": lambda :self.redirect_page("home_screen"),
        
            } ,
            {
                "viewclass": "IconListItem",
                "icon": "cog",
                "height": dp(56),
                "text": f"Cài Đặt",
                "bg_color":(0,1,1,1) if self.current_page=="settings_screen" else (0,1,1,0.2),
                "on_release": lambda :self.redirect_page("settings_screen"),
                
            }
            ]
        self.menu = MDDropdownMenu(
            caller=instance,
            items=menu_items,
            position="bottom",
            width_mult=3,
            background_color= "pink",
            opening_time=0.3,
        )
    
        self.menu.open()

 



    # def sidebar_abtn_pressed(self,action):
    #     self._disabledAllActionButton(session=self.user)

    #     try:
    #         match action:
    #             case "init":
    #                 response = requests.post("http://127.0.0.1:5005/")
    #             case "start":   
    #                 response = requests.post("http://127.0.0.1:5005/start")
    #             case "stop":   
    #                 response = requests.post("http://127.0.0.1:5005/stop")
      
    #             case "performance":   
    #                 response = requests.post("http://127.0.0.1:5005/performance")
         
    #         response=response.json()
                
    #     except Exception as e:
    #         response = {
    #             "status_code":0,
    #             "message":"Something went wrong",
    #             "detail":{
    #                 "message":e
    #             }
    #         }
            
    #     self.filter_response(response,action)
    #     # self._enabledWithStatus(session=self.user)
    #     return response
    
    
    # def filter_response(self, response,action):

    #     if response["status_code"] == 0:
    #         self.snackbarManager.show_snackBar("warning",response,True)
    #     elif response["status_code"] == 404:
    #         self.snackbarManager.show_snackBar("failed",response,True)
    #     elif response["status_code"] ==200:
    #         self.snackbarManager.show_snackBar("success",response)
    #         self.user["status"] = response["status"]
            
    #         match action:
    #             case "init":
    #                 rtsp = self.user["detail"]["rtsp"]
    #                 is_ok = self._init_camera(rtsp)
    #             case "start":
    #                 self.root.ids.home.ids.camera.add_widget(self.my_camera)
    #             case "stop":
    #                 self.root.ids.home.ids.camera.remove_widget(self.my_camera)
    #                 self.capture.release()
                    
                    
if __name__ == '__main__':
    MainApp().run()