from typing import Any
from kivy.properties import StringProperty, ObjectProperty
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.screen import MDScreen
from components.chatBubble import ChatBubble
from components.log_screen import LogScreen

KV = '''
#:import FadeTransition kivy.uix.screenmanager.FadeTransition

<LogManager>:
    orientation: "horizontal"

    MDNavigationRail:
        md_bg_color: "#66CCFF"
        size_hint_x: 0.22
        selected_color_background: "#3399FF"
        ripple_color_item: "#0099FF"
        on_item_release: root.switch_log_screen(*args)

        MDNavigationRailItem:
            name: "log"
            text: "Log"
            icon: "dots-hexagon"
            badge_icon:"numeric-10"
            badge_font_size:dp(20)
        MDNavigationRailItem:
            name: "search"
            text: "Search"
            icon: "archive-search"
            badge_icon:""
            badge_font_size:dp(20)
    ScreenManager:
        id: screen_manager
        transition: FadeTransition(duration=0.2, clearcolor=app.theme_cls.bg_dark)

        LogScreen:
            id: log_screen
            md_bg_color: "#CCFFCC"

                    

        SearchScreen:
'''

Builder.load_string(KV)



class SearchScreen(MDScreen):
    name = StringProperty("search_screen")

class LogManager(MDBoxLayout):
    switch_screen = ObjectProperty(int)

    def __init__(self, *args: Any, **kwds: Any) -> Any:
        super(LogManager, self).__init__(**kwds)

    def switch_log_screen(self, instance_navigation_rail, instance_navigation_rail_item):
        try:
            self.ids.screen_manager.current = instance_navigation_rail_item.name + "_screen"
        except Exception as e:
            pass
