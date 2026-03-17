import kivy
import random
import os
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty, StringProperty, NumericProperty, BooleanProperty
from kivy.core.image import Image as CoreImage
from kivy.clock import Clock
from kivy.utils import platform
from kivy.animation import Animation
from kivy.storage.jsonstore import JsonStore

class Coin(Widget):
    coin_texture = ObjectProperty(None)
    mode = StringProperty("Kopf/Zahl")
    tilt_scale_x = NumericProperty(1.0) 
    tilt_scale_y = NumericProperty(1.0) 
    current_side = StringProperty("0")
    is_flipping = BooleanProperty(False)

    def __init__(self, **kwargs):
        self._touch_start_pos = None
        super().__init__(**kwargs)
        self.textures = {}
        self.load_textures()
        Clock.schedule_once(self.late_init, 0.1)

    def late_init(self, dt):
        self.update_texture("0")
        if self.parent:
            self.center_x = self.parent.center_x + 3
            self.center_y = self.parent.center_y

    def load_textures(self):
        files = {
            "0": "pixil-frame-0-startkopf.png", "1": "pixil-frame-1.png",
            "2": "pixil-frame-2.png", "3": "pixil-frame-3-liegend.png",
            "4": "pixil-frame-4.png", "5": "pixil-frame-5.png",
            "6": "pixil-frame-6-startzahl.png", "7": "pixil-frame-7-startja.png",
            "8": "pixil-frame-8.png", "9": "pixil-frame-9.png",
            "10": "pixil-frame-3-liegend.png", "11": "pixil-frame-11.png",
            "12": "pixil-frame-12.png", "13": "pixil-frame-13-startnein.png"
        }
        for key, filename in files.items():
            try:
                if os.path.exists(filename):
                    tex = CoreImage(filename).texture
                    tex.mag_filter = 'nearest'
                    tex.min_filter = 'nearest'
                    self.textures[key] = tex
            except Exception as e:
                print(f"PYTHON_LOG: Failed to load {filename}: {e}")

    def update_texture(self, key):
        if key in self.textures:
            self.coin_texture = self.textures[key]
            self.current_side = key

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos) and not self.is_flipping:
            self._touch_start_pos = touch.pos
            return True
        return super().on_touch_down(touch)

    def on_touch_up(self, touch):
        if self._touch_start_pos and not self.is_flipping:
            dy = touch.y - self._touch_start_pos[1]
            if dy > 100: self.flip()
            self._touch_start_pos = None
            return True
        return super().on_touch_up(touch)

    def flip(self):
        if self.is_flipping: return
        self.is_flipping = True
        if self.mode == "Kopf/Zahl":
            target = random.choice(["0", "6"])
            path = ["0", "1", "2", "3", "4", "5", "6", "5", "4", "3", "2", "1"]
        else:
            target = random.choice(["7", "13"])
            path = ["7", "8", "9", "10", "11", "12", "13", "12", "11", "10", "9", "8"]
        
        start_idx = path.index(self.current_side) if self.current_side in path else 0
        long_p = path[start_idx:] + (path * 3)
        self.anim_frames = []
        for f in long_p:
            self.anim_frames.append(f)
            if len(self.anim_frames) > 15 and f == target: break
        self.current_frame_idx = 0
        Clock.schedule_interval(self.next_frame, 0.05)

    def next_frame(self, dt):
        if self.current_frame_idx >= len(self.anim_frames):
            self.is_flipping = False
            Clock.unschedule(self.next_frame)
            return
        self.update_texture(self.anim_frames[self.current_frame_idx])
        self.current_frame_idx += 1

class CyberCoinRoot(FloatLayout):
    bg_texture = ObjectProperty(None)
    btn_bg_tex = ObjectProperty(None)
    btn_mode_tex = ObjectProperty(None)
    logo_tex = ObjectProperty(None)
    sign_tex = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.all_bg_textures = {}
        for i in range(1, 5):
            fname = f"bg{i}.png"
            try:
                if os.path.exists(fname):
                    t = CoreImage(fname).texture
                    t.mag_filter = 'nearest'
                    self.all_bg_textures[f"bg{i}"] = t
            except: pass
        
        if "bg1" in self.all_bg_textures:
            self.bg_texture = self.all_bg_textures["bg1"]

        assets = {"btn": "bg-button.png", "mode": "mode.png", "logo": "flip-it.png", "sign": "sign.png"}
        for key, f in assets.items():
            try:
                if os.path.exists(f):
                    t = CoreImage(f).texture
                    if key == "btn": self.btn_bg_tex = t
                    elif key == "mode": self.btn_mode_tex = t
                    elif key == "logo": self.logo_tex = t
                    elif key == "sign": self.sign_tex = t
            except: pass

    def next_background(self):
        # Einfacher BG-Wechsel ohne Speichern für Testzwecke
        pass

    def toggle_mode(self):
        c = self.ids.coin
        if not c.is_flipping:
            if c.mode == "Kopf/Zahl":
                c.mode = "Ja/Nein"
                c.update_texture("7")
            else:
                c.mode = "Kopf/Zahl"
                c.update_texture("0")

class CyberCoinApp(App):
    def build(self):
        return CyberCoinRoot()

if __name__ == "__main__":
    CyberCoinApp().run()
