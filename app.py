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
class RegisterScreen(MDScreen):
    pass
class CameraItem(MDBoxLayout):
    pass



class MainApp(MDApp):
    def __init__(self, **kwargs):
        super(MainApp, self).__init__(**kwargs)
        Builder.load_file('kv/utils.kv') 
        Builder.load_file('kv/register.kv') 
        Builder.load_file('kv/home.kv') 
        Builder.load_file('kv/settings.kv') 
        
        self.menu=[]
        self.snackbarManager = SnackbarManager()
        self.user = database["user1"]
        self.current_page = "home_screen"
        
    def build(self):
        return Builder.load_file('kv/main.kv') 
    def on_start(self):
        self._enabledWithStatus(self.user)
        self.root.ids.sideBar.set_state()
        
    def _init_camera(self,rtps):
        try:
            self.capture = cv2.VideoCapture(rtps)
            self.my_camera = KivyCamera(capture=self.capture, fps=2)
        except Exception as e:
            return False
        return True
    def add_camera(self):
        print("add_camera")
        self.root.ids.sidebar_manager.ids.camera_manager.add_widget(CameraItem())
        
        
    def confirm_submit(self):
        self.submit_form()
        pass
    def submit_form(self):
        print("submit_form")
        self.add_camera()
        self.close_register()
        
    def close_register(self):
        self.redirect_page("home_screen")
    def on_stop(self):
        if self.capture:
            self.capture.release()
        
    def on_leave(self,instance):
        instance.md_bg_color = "#EEEEEE"
    def on_enter(self,instance):
        instance.md_bg_color = "#DDDDDD"
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
    def redirect_page(self, place):
        self.root.ids.screen_manager.current = place
        self.current_page = place
        if self.menu:
            self.menu.dismiss()
 
    def _enabledWithStatus(self,session):
        if not self._auth_session(session):
            return False
        
        for id_btn,button in self.root.ids.home.ids.items():
            if id_btn.startswith("abtn"):
                if id_btn.rsplit("_",1)[-1] in allow_action_list[session["status"]]:
                    self._enabledButton(button,colors["Orange"]["300"])
                else:
                    self._disabledButton(button)
        return True
        
    def on_press(self,button):
        button.md_bg_color = colors["Orange"]["600"]
        
    def _disabledButton(self,button):
        button.disabled = True
        button.line_width=1
    def _enabledButton(self,button,color):
        button.disabled = False
        button.md_bg_color = color
        button.line_width=2
        
    def _disabledAllActionButton(self,session):
        if not self._auth_session(session):
            return False
        
        for id_btn,button in self.root.ids.home.ids.items():
            if id_btn.startswith("abtn"):
                self._disabledButton(button)
        return True
    
    def sidebar_abtn_pressed(self,action):
        self._disabledAllActionButton(session=self.user)

        try:
            match action:
                case "init":
                    response = requests.post("http://127.0.0.1:5005/")
                case "start":   
                    response = requests.post("http://127.0.0.1:5005/start")
                case "stop":   
                    response = requests.post("http://127.0.0.1:5005/stop")
      
                case "performance":   
                    response = requests.post("http://127.0.0.1:5005/performance")
         
            response=response.json()
                
        except Exception as e:
            response = {
                "status_code":0,
                "message":"Something went wrong",
                "detail":{
                    "message":e
                }
            }
            
        self.filter_response(response,action)
        self._enabledWithStatus(session=self.user)
        return response
    
    
    def filter_response(self, response,action):

        if response["status_code"] == 0:
            self.snackbarManager.show_snackBar("warning",response,True)
        elif response["status_code"] == 404:
            self.snackbarManager.show_snackBar("failed",response,True)
        elif response["status_code"] ==200:
            self.snackbarManager.show_snackBar("success",response)
            self.user["status"] = response["status"]
            
            match action:
                case "init":
                    rtsp = self.user["detail"]["rtsp"]
                    is_ok = self._init_camera(rtsp)
                case "start":
                    self.root.ids.home.ids.camera.add_widget(self.my_camera)
                case "stop":
                    self.root.ids.home.ids.camera.remove_widget(self.my_camera)
                    self.capture.release()
                    
                    
if __name__ == '__main__':
    MainApp().run()