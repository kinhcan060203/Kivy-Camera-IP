from typing import Any
from kivy.properties import StringProperty, NumericProperty, ColorProperty, ListProperty, ObjectProperty
from kivy.animation import Animation
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.utils import get_color_from_hex
from kivymd.uix.boxlayout import MDBoxLayout
from datetime import datetime
from kivymd.uix.button import MDFlatButton, MDRaisedButton
from components.camera_item import CameraItem
from components.snackbar import Snackbar
from kivymd.uix.dialog import MDDialog
from kivy.core.window import Window

# Kivy Language String
KV = '''
#:import get_color_from_hex kivy.utils.get_color_from_hex
#:import Gradient kivy_gradient.Gradient

<DevicesManager>:
    radius: [0, 16, 16, 0]
    orientation: 'vertical'
    size_hint: 1, 1
    spacing: dp(20)
    padding: dp(10)
    canvas.before:
        RoundedRectangle:
            size: self.size
            pos: self.pos
            texture: Gradient.horizontal(get_color_from_hex("#ec60ff"), get_color_from_hex("#eeb9ff"))
            radius: [0, 16, 16, 0]

    MDScrollView:
        id: camera_manager
        size_hint: (1, 1)
        do_scroll_y: True
        do_scroll_x: False
        bar_width: 5
        bar_color: "#00CCFF"   
        bar_inactive_color: "#AAAAAA"  
        effect_cls: "ScrollEffect"
        scroll_type: ['bars']
        MDSelectionList:
            id: camera_list
            spacing: "10dp"
            overlay_color: root.overlay_color[:-1] + [.3]
            icon_bg_color: root.overlay_color
            on_selected: root.on_selected(*args)
            on_unselected: root.on_unselected(*args)
            on_selected_mode: root.set_selection_mode(*args)
            size_hint_y: None
            height: self.minimum_height
            padding: [0, 5, 15, 0]
            icon_pos: [self.width * 0.8, 45]
'''

Builder.load_string(KV)

class DevicesManager(MDBoxLayout):
    # Class for managing camera devices
    overlay_color = get_color_from_hex("#6633FF")

    def __init__(self, **kwds: Any) -> Any:
        # Initializing DevicesManager
        super(DevicesManager, self).__init__(**kwds)
        self.confirmForm = None
        self.snackbar = Snackbar()
        self.selected_device = None

    def add_camera_item(self, info):
        # Adding a CameraItem to the DevicesManager
        camera_item = CameraItem(**info)
        instance_selection_list = self.ids.camera_list
        instance_selection_list.add_widget(camera_item, index=len(instance_selection_list.children))
        camera_item.select()
        self._update_selected_device(camera_item)
        return camera_item

    def set_selection_mode(self, instance_selection_list, mode):
        # Setting selection mode based on the mode parameter
        devices_backdrop = MDApp.get_running_app().root.ids.devices_backdrop
        if mode:
            md_bg_color = self.overlay_color
            left_action_items = [["close", lambda x: instance_selection_list.unselected_all()]]
            right_action_items = [["trash-can", lambda x: self.show_confirm_remove(instance_selection_list)], ["dots-vertical"]]
        else:
            md_bg_color = get_color_from_hex("#00CCFF")
            devices_backdrop.title = "Devices"
            left_action_items = [['plus', lambda x: MDApp.get_running_app().check_devices_backdrop()]]
            right_action_items = []

        Animation(back_layer_color=md_bg_color, d=0.2).start(devices_backdrop)
        devices_backdrop.left_action_items = left_action_items
        devices_backdrop.right_action_items = right_action_items

    def on_selected(self, instance_selection_list, instance_selection_item):
        # Handling the selection event
        self._update_selection_item(instance_selection_item, check=True)
        self._update_devices_backdrop_title(instance_selection_list)

    def on_unselected(self, instance_selection_list, instance_selection_item):
        # Handling the unselection event
        self._update_selection_item(instance_selection_item, check=False)
        self._update_devices_backdrop_title(instance_selection_list)

    def show_confirm_remove(self, instance_selection_list):
        # Showing a confirmation dialog for removing selected cameras
        selected_list_item = instance_selection_list.get_selected_list_items()
        self.confirmForm = MDDialog(
            title="REMOVE CAMERA", 
            text=f"Are you sure to remove {len(selected_list_item)} camera?", 
            
            buttons=[
                MDRaisedButton(
                    text="ACCEPT",
                    theme_text_color="Custom",
                    text_color="black",
                    on_release=lambda x: self.remove_all_selected(selected_list_item)
                ),
                MDFlatButton(
                    text="CANCEL",
                    theme_text_color="Custom",
                    text_color="white",
                    md_bg_color=[1,1,1,0.3],
                    on_release=lambda x: self.confirmForm.dismiss()
                ),
            ],
        )
        self.confirmForm.open()

    def remove_all_selected(self, selected_list_item):
        # Removing all selected cameras
        instance_selection_list = self.ids.camera_list
        self.confirmForm.dismiss()
        
        for selected_instance in selected_list_item:
            instance_selection_list.remove_widget(selected_instance)

        instance_selection_list.unselected_all()
        self.snackbar.show_snackBar("success", {"message": "Removed successfully !!!", "detail": {"message": "Successfully"}})

        for instance in instance_selection_list.children:
            if instance.children[1].selected:
                instance.children[1].select()
                return

        detail_manager = MDApp.get_running_app().root.ids.detail_manager
        detail_manager.parent.dispatch("on_tab_press")
        detail_manager.update_item({})

    def _update_selected_device(self, camera_item):
        # Updating the selected device
        if self.selected_device:
            self.selected_device.unselect()
        self.selected_device = camera_item

    def _update_selection_item(self, instance_selection_item, check):
        # Updating the selection item (check or uncheck)
        instance_selection_item.children[1].check() if check else instance_selection_item.children[1].uncheck()

    def _update_devices_backdrop_title(self, instance_selection_list):
        # Updating the title of the devices backdrop based on the number of selected items
        devices_backdrop = MDApp.get_running_app().root.ids.devices_backdrop
        devices_backdrop.title = str(len(instance_selection_list.get_selected_list_items()))
