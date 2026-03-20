import kivy
import random
import os
import os
from kivy.resources import resource_add_path
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty, StringProperty, NumericProperty, BooleanProperty
from kivy.core.image import Image as CoreImage
from kivy.clock import Clock
from kivy.utils import platform
from kivy.animation import Animation
from kivy.storage.jsonstore import JsonStore

if platform != 'android':
    from kivy.core.window import Window
    Window.size = (360, 640)
    Window.title = "FLIP IT"

# Fügt den assets-Ordner zum Suchpfad für Bilder/Sounds hinzu
if os.path.exists('assets'):
    resource_add_path(os.path.abspath('assets'))

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
        # Pfade angepasst auf assets/
        files = {
            "0": "assets/pixil-frame-0-startkopf.png", "1": "assets/pixil-frame-1.png",
            "2": "assets/pixil-frame-2.png", "3": "assets/pixil-frame-3-liegend.png",
            "4": "assets/pixil-frame-4.png", "5": "assets/pixil-frame-5.png",
            "6": "assets/pixil-frame-6-startzahl.png", "7": "assets/pixil-frame-7-startja.png",
            "8": "assets/pixil-frame-8.png", "9": "assets/pixil-frame-9.png",
            "10": "assets/pixil-frame-3-liegend.png", "11": "assets/pixil-frame-11.png",
            "12": "assets/pixil-frame-12.png", "13": "assets/pixil-frame-13-startnein.png"
        }
        for key, filename in files.items():
            try:
                tex = CoreImage(filename).texture
                tex.mag_filter = 'nearest'
                tex.min_filter = 'nearest'
                self.textures[key] = tex
            except Exception as e:
                print(f"Fehler beim Laden der Textur '{filename}': {e}")

    def update_texture(self, key):
        if key in self.textures:
            self.coin_texture = self.textures[key]
            self.current_side = key

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos) and not self.is_flipping:
            self._touch_start_pos = touch.pos
            Animation.stop_all(self, 'tilt_scale_x')
            Animation.stop_all(self, 'tilt_scale_y')
            return True
        return super().on_touch_down(touch)

    def on_touch_move(self, touch):
        if self._touch_start_pos and not self.is_flipping:
            dx = (touch.x - self._touch_start_pos[0]) * 0.0015
            dy = (touch.y - self._touch_start_pos[1]) * 0.0015
            self.tilt_scale_x = max(0.7, 1.0 - abs(dx))
            self.tilt_scale_y = max(0.7, 1.0 - abs(dy))
            return True
        return super().on_touch_move(touch)

    def on_touch_up(self, touch):
        if self._touch_start_pos and not self.is_flipping:
            dy = touch.y - self._touch_start_pos[1]
            if dy > 100: self.flip()
            else: Animation(tilt_scale_x=1.0, tilt_scale_y=1.0, duration=0.5, t='out_elastic').start(self)
            self._touch_start_pos = None
            return True
        return super().on_touch_up(touch)

    def flip(self):
        if self.is_flipping: return
        self.is_flipping = True
        Animation(tilt_scale_x=1.0, tilt_scale_y=1.0, duration=0.2).start(self)
        if self.mode == "Kopf/Zahl":
            target = random.choice(["0", "6"])
            path = ["0", "1", "2", "3", "4", "5", "6", "5", "4", "3", "2", "1"]
        else:
            target = random.choice(["7", "13"])
            path = ["7", "8", "9", "10", "11", "12", "13", "12", "11", "10", "9", "8"]
        try: start_idx = path.index(self.current_side)
        except: start_idx = 0
        long_p = path[start_idx:] + (path * 3)
        self.anim_frames = []
        for f in long_p:
            self.anim_frames.append(f)
            if len(self.anim_frames) > 20 and f == target: break
        self.current_frame_idx = 0
        Clock.schedule_interval(self.next_frame, 0.055)

    def next_frame(self, dt):
        if self.current_frame_idx >= len(self.anim_frames):
            self.is_flipping = False
            self.update_texture(self.anim_frames[-1])
            Clock.unschedule(self.next_frame)
            return
        self.update_texture(self.anim_frames[self.current_frame_idx])
        self.current_frame_idx += 1

class CyberCoinRoot(FloatLayout):
    bg_index = NumericProperty(1)
    bg_texture = ObjectProperty(None)
    btn_bg_tex = ObjectProperty(None)
    btn_mode_tex = ObjectProperty(None)
    logo_tex = ObjectProperty(None)
    sign_tex = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.store = None
        self.bg_index = 1
        try:
            if platform == 'android':
                from android.storage import app_storage_path # type: ignore
                store_path = os.path.join(app_storage_path(), 'settings.json')
            else:
                store_path = 'settings.json'
                
            self.store = JsonStore(store_path)
            
            if self.store.exists('background'):
                self.bg_index = self.store.get('background')['index']
        except Exception as e:
            print(f"Warnung: Store konnte nicht geladen werden - {e}")

        # Lade Hintergründe aus assets/
        self.all_bg_textures = {}
        for i in range(1, 5):
            path = f"assets/bg{i}.png"
            try:
                t = CoreImage(path).texture
                t.mag_filter = 'nearest'
                t.min_filter = 'nearest'
                self.all_bg_textures[f"bg{i}"] = t
            except Exception as e:
                print(f"Fehler beim Laden von {path}: {e}")
        
        if f"bg{self.bg_index}" in self.all_bg_textures:
            self.bg_texture = self.all_bg_textures[f"bg{self.bg_index}"]

        # Lade UI Assets aus assets/
        ui_assets = {
            "btn": "assets/bg-button.png", "mode": "assets/mode.png", 
            "logo": "assets/flip-it.png", "sign": "assets/sign.png"
        }
        for key, f in ui_assets.items():
            try:
                t = CoreImage(f).texture
                t.mag_filter = 'nearest'
                t.min_filter = 'nearest'
                if key == "btn": self.btn_bg_tex = t
                elif key == "mode": self.btn_mode_tex = t
                elif key == "logo": self.logo_tex = t
                elif key == "sign": self.sign_tex = t
            except Exception as e:
                print(f"Fehler beim Laden von {f}: {e}")

    def next_background(self):
        self.bg_index = self.bg_index + 1 if self.bg_index < 4 else 1
        if f"bg{self.bg_index}" in self.all_bg_textures:
            self.bg_texture = self.all_bg_textures[f"bg{self.bg_index}"]
        
        if self.store is not None:
            try:
                self.store.put('background', index=self.bg_index)
            except Exception as e:
                print(f"Warnung: Hintergrund konnte nicht gespeichert werden - {e}")

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
        # Icon-Pfad ebenfalls angepasst
        self.icon = "assets/pixil-frame-0-startkopf.png"
        return CyberCoinRoot()

if __name__ == "__main__":
    CyberCoinApp().run()