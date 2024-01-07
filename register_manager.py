from typing import Any
from kivy.properties import StringProperty, ObjectProperty
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.utils import get_color_from_hex
from datetime import datetime
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton, MDRaisedButton
from components.snackbar import Snackbar
from kivymd.uix.textfield import MDTextField

# KV Language string for the UI layout
KV = '''
#:import get_color_from_hex kivy.utils.get_color_from_hex

<RegisterManager>:
    name: "register_form"
    MDBoxLayout:
        radius: [0, 25, 0, 0]
        padding:16
        md_bg_color: root.md_bg_color 
        MDScrollView:
            MDBoxLayout:
                orientation: "vertical"
                spacing:dp(10)
                size_hint_y:None
                height:self.minimum_height
                MDBoxLayout:
                    orientation: "horizontal"
                    size_hint_y:None
                    height:self.minimum_height
                    InputTextField:
                        id: name
                        hint_text: "Name"
                        helper_text: "Camera Name"
                        icon_right: ""
                        pos_hint: {"left": 0, "center_y": 0.5}

                    Widget:
                        size_hint_x: 0.5

                    MDFlatButton:
                        size_hint: None, None
                        padding: [dp(25), dp(18), dp(25), dp(18)]
                        text: 'Submit'
                        md_bg_color: "#3399FF"
                        font_size: dp(12)
                        font_style: "H6"
                        text_color: "black"
                        pos_hint: {"right": 0, "center_y": 0.5}
                        on_press: root.check_valid()
                MDBoxLayout:
                    orientation: "vertical"
                    spacing: 10
                    size_hint_y:None
                    height:self.minimum_height
                    InputTextField:
                        id: rtsp
                        hint_text: "URL"
                        helper_text: 'rtsp://{user}:{password}@{ip}:554/cam/realmonitor?channel=1&subtype=0'
                        icon_right: "key-variant"
                        size_hint_x: 1
                        pos_hint: {"left": 0}

                    InputTextField:
                        id: desc
                        hint_text: "Description"
                        icon_right: "pencil"
                        size_hint_x: 1
                        pos_hint: {"left": 0}


<InputTextField>:
    size_hint_x: root.size_hint_x
    hint_text: root.hint_text
    helper_text: root.helper_text
    helper_text_mode: "persistent"
    mode: "line"
    pos_hint: {"center_x": .5, "center_y": .5}
    icon_right: root.icon_right
    font_size: "18dp"
    text_color_focus: "#333333"
    text_color_normal: "#777777"

    icon_right_color_focus: "#33CCFF"
    icon_right_color_normal: "#DDDDDD"

    line_color_normal: "#999999"
    line_color_focus: "#EEEEEE"

    error_color: "red"

    hint_text_color_normal: "#FFFFFF"
    hint_text_color_focus: "#333333"

    helper_text_color_focus: "#3333FF"
    helper_text_color_normal: "#0066FF" 

    radius: [15, 15, 0, 0]
'''

# Load the KV layout string
Builder.load_string(KV)

# Custom MDTextField for better styling
class InputTextField(MDTextField):
    pass

# Main class representing the registration manager
class RegisterManager(MDBoxLayout):
    md_bg_color="#66CCCC"
    def __init__(self, *args: Any, **kwds: Any) -> Any:
        super(RegisterManager, self).__init__(**kwds)
        self.snackbar = Snackbar()
        self.confirm_form = None

    def check_valid(self):
        # Check if the entered data is valid
        name_text = self.ids.name.text
        rtsp_text = self.ids.rtsp.text
        desc = self.ids.desc.text
        if len(name_text) > 0 and len(desc) > 0:
            self.show_confirm()  # If valid, show confirmation dialog
            return True
        return False

    def show_confirm(self):
        # Show a confirmation dialog
        self.confirm_form = MDDialog(
            title="ADD CAMERA",
            text="Are you sure to add the camera?",
            buttons=[
                MDFlatButton(
                    text="CANCEL",
                    theme_text_color="Custom",
                    text_color="blue",
                    on_release=lambda x: self.confirm_form.dismiss()
                ),
                MDRaisedButton(
                    text="ACCEPT",
                    theme_text_color="Custom",
                    text_color="black",
                    on_release=lambda x: self.submit_success()
                ),
            ],
        )
        self.confirm_form.open()

    def submit_success(self):
        # Submit the entered data after confirmation
        name_text = self.ids.name.text
        rtsp_text = self.ids.rtsp.text
        desc = self.ids.desc.text
        try:
            message = [
                "success",
                {
                    "message": "Add camera successfully !!!",
                    "detail": {
                        "message": "Successfully"
                    }
                }
            ]

            self.confirm_form.dismiss()
            devices_backdrop = MDApp.get_running_app().root.ids.devices_backdrop
            devices_manager = MDApp.get_running_app().root.ids.devices_manager
            info = {
                "content":{
                    "name": name_text,
                    "desc": desc,
                    "rtsp": rtsp_text,
                    "avatar": "",
                    "status": "Pending",
                    "date": {
                        "created_at": datetime.now().strftime(r'%Y-%m-%d %H:%M:%S'),
                        "last_stopped": "No data"
                    }
                }
            }
            devices_manager.add_camera_item(info)
            devices_backdrop.left_action_items[0][1](devices_backdrop)

        except Exception as e:
            message = [
                "failed",
                {
                    "message": "Add camera failed !!!",
                    "detail": {
                        "message": "Failed"
                    }
                }
            ]

        self.ids.name.text = ''
        self.ids.rtsp.text = ''
        self.ids.desc.text = ''
        self.snackbar.show_snackBar(*message)
