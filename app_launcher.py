
import os
import lcd

import image

from framework import BaseApp
from app_camera import CameraApp
from app_explorer import ExplorerApp

class LauncherApp(BaseApp):
    def __init__(self, system_singleton):
        super(LauncherApp, self).__init__(system_singleton)
        print("LauncherApp: super.__init__() called")
        self.app_list = [
            {"id": "camera", "icon": "/sd/icons/camera.jpg"},
            {"id": "explorer", "icon": "/sd/icons/memory_card.jpg"},
            {"id": "settings", "icon": "/sd/icons/settings.jpg"},
            {"id": "music", "icon": "/sd/icons/music.jpg"},
            {"id": "tools", "icon": "/sd/icons/tools.jpg"},
        ]
        self.app_count = len(self.app_list)
        self.cursor_index = 0

    def on_draw(self):
        print("LauncherApp.on_draw()")
        icon_width = icon_height = 64
        icon_padding = 6
        screen_canvas = image.Image()

        # closure: an inner function inside a method
        def draw_icon(icon_path, center_x, center_y):
            icon = image.Image(icon_path)
            screen_canvas.draw_image(icon, center_x - icon.width() // 2,
                                     center_y - icon.height() // 2)
            del icon

        icons_count = screen_canvas.width() // (icon_width + icon_padding)
        if icons_count % 2 == 0:
            icons_count += 1
        else:
            icons_count += 2
        # icons_count must be an odd integer
        icons_half_count = icons_count // 2
        for i in range(-icons_half_count, icons_half_count + 1):
            icon_center_x = screen_canvas.width() // 2 + i * (icon_width + icon_padding)
            icon_center_y = screen_canvas.height() // 2 - 5
            index = (self.cursor_index + i) % self.app_count
            draw_icon(self.app_list[index]["icon"], icon_center_x, icon_center_y)
        # draw center small arrow icon below
        draw_icon('/sd/icons/arrow_top_24.jpg', screen_canvas.width() // 2,
                  screen_canvas.height() // 2 + icon_height // 2 + icon_padding + 5)
        lcd.display(screen_canvas)
        del screen_canvas

    def navigate(self, app):
        self.system_singleton.navigate(app)
        print("navigate from", self, "to", app)

    def on_home_button_changed(self, state):
        app_id = self.app_list[self.cursor_index]["id"]
        if app_id == "camera":
            self.navigate(CameraApp(self.system_singleton))
        elif app_id == "explorer":
            self.navigate(ExplorerApp(self.system_singleton))
        return True

    def on_top_button_changed(self, state):
        if state == "pressed":
            self.cursor_index += 1
            print(self.cursor_index, len(self.app_list))
            if self.cursor_index >= self.app_count:
                self.cursor_index = 0
            self.invalidate_drawing()
            print(self.cursor_index, len(self.app_list))
        return True

    def on_back_pressed(self):
        # handled by launcher app
        self.cursor_index = 0
        self.invalidate_drawing()
        return True