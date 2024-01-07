# Importing necessary modules and classes
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.screen import MDScreen
from datetime import datetime
import os
import random

# Importing custom modules and components
from log_manager import LogManager
from detail_manager import DetailManager
from devices_manager import DevicesManager
from register_manager import RegisterManager
from components import *

# Main Application Class
class MainApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def build(self):
        # Setting theme style and primary palette
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Orange"
        return Builder.load_file('kv/main.kv')
    
    def on_start(self):
        # Adjusting the header button height and scheduling data initialization
        self.devices_backdrop = self.root.ids.devices_backdrop
        self.devices_manager = self.root.ids.devices_manager
        self.log_manager = self.root.ids.log_manager
        self.devices_backdrop.ids.header_button.height = "30dp"
        from kivy.clock import Clock
        Clock.schedule_once(lambda x: self._init_data())

    def _init_data(self):
        # Initializing data for cameras
        names = [f"Camera {i}" for i in range(4)]
        rtsp = [f"rtsp://localhost {i}" for i in range(4)]
        desc = [f'Con meo '*random.randint(1, 6) for i in range(4)]
        avatar = [os.path.join("assets/images", os.listdir("assets/images")[i]) for i in range(4)]
        created_at = [datetime.now().strftime(r'%Y-%m-%d %H:%M:%S') for i in range(4)]

        # Adding camera items to DevicesManager
        for i in range(4):
            info = {
                "content":{
                    "name": names[i],
                    "desc": desc[i],
                    "rtsp": rtsp[i],
                    "avatar": avatar[i],
                    "status": "Pending",
                    "date": {
                        "created_at": created_at[i],
                        "last_stopped": created_at[i]
                    }
                }
            }
            self.devices_manager.add_camera_item(info)

        # Adding chat data to LogManager
        num=len(os.listdir("assets/images"))
        text = [f"Image {i} "*random.randint(1, 2) for i in range(num)]
        avatar = [os.path.join("assets/images", os.listdir("assets/images")[i]) for i in range(num)]
        data_list=[]
        for i in range(num):
            data = {
                "text": text[i],    
                "detail": {
                    "source_image": avatar[i]
                },
                "created_at": datetime.now().strftime(r'%H:%M:%S'),
            }
            data_list.append(data)
            self.log_manager.ids.log_screen.add_message(data)
            


    def check_devices_backdrop(self):
        # Checking and adding a header button to the backdrop
        # This function temporarily resoletes the issues somtimes occurs when header_button is Weak Inferenced widget
        try:
            self.devices_backdrop.ids.header_button
        except:
            self.devices_backdrop.ids.header_button = MDBoxLayout()
            self.devices_backdrop.ids.header_button.height = "30dp"
        self.devices_backdrop.open()

# Running the application
if __name__ == "__main__":
    MainApp().run()
