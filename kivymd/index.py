from kivy.uix.actionbar import BoxLayout
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.navigationbar import MDNavigationBar, MDNavigationItem
from kivymd.uix.screen import MDScreen
from kivymd.uix.label import MDLabel

KV = '''
MDScreen:
    MDNavigationLayout:
        MDNavigationDrawer:
            id: nav_drawer
            radius: 0, dp(16), dp(16), 0
            MDNavigationDrawerMenu:
                MDNavigationDrawerLabel:
                    text: "Mail"
                MDNavigationDrawerItem:
                    MDNavigationDrawerItemLeadingIcon:
                        icon: "account"
                    MDNavigationDrawerItemText:
                        text: "Inbox"
                    MDNavigationDrawerItemTrailingText:
                        text: "24"
                MDNavigationDrawerDivider:
                
        MDScreenManager:
            id: screen_manager
            md_bg_color: self.theme_cls.backgroundColor
            MDScreen:
                name: "home"
                MDLabel:
                    text: "Hello Screen 1"
                    halign: "center"  # Centrer le texte
            MDScreen:
                name: "search"
                MDLabel:
                    text: "Hello Screen 2"
                    halign: "center"
            MDScreen:
                name: "settings"
                MDLabel:
                    text: "Hello Screen 3"
                    halign: "center"
                    
    MDNavigationBar:
        on_switch_tabs: app.on_switch_tabs(*args)
        MDNavigationItem:
            active: True
            MDNavigationItemIcon:
                icon: "menu"
             
            MDNavigationItemLabel:
                text: "home"
        MDNavigationItem:
            MDNavigationItemIcon:
                icon: "magnify"
            MDNavigationItemLabel:
                text: "search"
        MDNavigationItem:
            MDNavigationItemIcon:
                icon: "cog"
            MDNavigationItemLabel:
                text: "settings"
'''
class Example(MDApp):
    def on_switch_tabs(
        self,
        bar: MDNavigationBar,
        item: MDNavigationItem,
        item_icon: str,
        item_text: str,
    ):
        self.root.ids.screen_manager.current = item_text
            

    def build(self):
        return Builder.load_string(KV)


Example().run()

