import kivy
import random
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty, StringProperty, NumericProperty, BooleanProperty
from kivy.core.window import Window
from kivy.core.image import Image as CoreImage
from kivy.clock import Clock

Window.size = (360, 640)

class Coin(Widget):
    coin_texture = ObjectProperty(None)
    mode = StringProperty("Kopf/Zahl")
    tilt_angle = NumericProperty(0) 
    current_side = StringProperty("Kopf")
    is_flipping = BooleanProperty(False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.textures = {}
        self.load_textures()
        self.update_texture("Kopf")

    def load_textures(self):
        files = {
            "Kopf": "coin_kopf.png", "Zahl": "coin_zahl.png",
            "Ja": "coin_ja.png", "Nein": "coin_nein.png",
            "Kopf_Spin": "coin_kopf_spin.png", "Zahl_Spin": "coin_zahl_spin.png",
            "Air": "coin_air.png"
        }
        for key, filename in files.items():
            try:
                texture = CoreImage(filename).texture
                texture.mag_filter = 'nearest'
                texture.min_filter = 'nearest'
                self.textures[key] = texture
            except:
                print(f"Datei {filename} fehlt!")

    def update_texture(self, texture_key):
        if texture_key in self.textures:
            self.coin_texture = self.textures[texture_key]

    def on_touch_move(self, touch):
        if self.collide_point(*touch.pos) and not self.is_flipping:
            total_dx = touch.x - touch.ox
            self.tilt_angle = max(min(total_dx / 10, 20), -20)
            return True

    def on_touch_up(self, touch):
        if self.collide_point(*touch.pos) and not self.is_flipping:
            dy = touch.y - touch.oy 
            self.tilt_angle = 0 
            if dy > 30: # Up-Swipe Trigger
                self.start_flip_animation()
            return True

    def start_flip_animation(self):
        self.is_flipping = True
        # 50/50 Entscheidung
        if self.mode == "Kopf/Zahl":
            self.final_result = random.choice(["Kopf", "Zahl"])
        else:
            self.final_result = random.choice(["Ja", "Nein"])

        def stretch(frames):
            return [f for f in frames for _ in range(2)]

        h_k = stretch(["Kopf_Spin", "Air", "Zahl_Spin"])
        h_z = stretch(["Zahl_Spin", "Air", "Kopf_Spin"])

        self.anim_frames = []
        num_half_spins = random.randint(4, 6)
        temp_side = self.current_side
        
        for _ in range(num_half_spins):
            if temp_side in ["Kopf", "Ja"]:
                self.anim_frames.extend(h_k)
                temp_side = "Zahl"
            else:
                self.anim_frames.extend(h_z)
                temp_side = "Kopf"

        if temp_side != self.final_result:
            self.anim_frames.extend(h_k if temp_side in ["Kopf", "Ja"] else h_z)

        self.current_frame_idx = 0
        Clock.schedule_interval(self.next_frame, 0.05)

    def next_frame(self, dt):
        if self.current_frame_idx >= len(self.anim_frames):
            Clock.unschedule(self.next_frame)
            self.is_flipping = False
            self.current_side = self.final_result
            self.update_texture(self.final_result)
            return
        self.update_texture(self.anim_frames[self.current_frame_idx])
        self.current_frame_idx += 1

class CyberCoinRoot(FloatLayout):
    def toggle_mode(self):
        c = self.ids.coin
        if not c.is_flipping:
            if c.mode == "Kopf/Zahl":
                c.mode, c.current_side = "Ja/Nein", "Ja"
            else:
                c.mode, c.current_side = "Kopf/Zahl", "Kopf"
            c.update_texture(c.current_side)

class CyberCoinApp(App):
    def build(self): return CyberCoinRoot()

if __name__ == '__main__':
    CyberCoinApp().run()