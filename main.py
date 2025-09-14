import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.slider import Slider
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from kivy_garden.graph import Graph, LinePlot
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock
from kivy.core.text import LabelBase
from kivy.uix.behaviors import ButtonBehavior
from kivy.graphics import Color, Rectangle
import statistics
import json
import os
import hashlib
from fpdf import FPDF
from kivy.utils import platform

# --- Android Permissions Handling ---
if platform == 'android':
    from android.permissions import request_permissions, Permission

CONFIG_FILE = 'config.json'
LIGHT_BLUE = (0.55, 0.8, 0.9, 1)

LANGUAGES = {
    "English": {
        "main_menu": "Main Menu",
        "login": "Login",
        "settings": "Settings",
        "exit": "Exit",
        "password_prompt": "Please enter your password:",
        "error": "Error",
        "incorrect_password": "Incorrect password.",
        "pressure_vs_time": "Pressure vs. Time",
        "error_data": "Error: data.txt not found or is empty.",
        "max": "Max",
        "min": "Min",
        "avg": "Avg",
        "save_png_word": "Save",
        "save_png_ext": "PNG",
        "save_jpg_word": "Save",
        "save_jpg_ext": "JPG",
        "save_pdf_word": "Save",
        "save_pdf_ext": "PDF",
        "back_menu": "Back to Menu",
        "settings_title": "Settings",
        "appearance": "Appearance",
        "security": "Security",
        "back_main": "Back to Main Menu",
        "security_options": "Security Options",
        "change_password": "Create/Change Password",
        "back_settings": "Back to Settings Menu",
        "passwords_empty": "Password fields cannot be empty.",
        "passwords_not_match": "Passwords do not match.",
        "password_set": "Password has been set.",
        "password_removed": "Password has been removed.",
        "time": "Time",
        "pressure_pa": "Pressure (Pa)",
        "theme": "Theme",
        "graph_color": "Graph Color",
        "title_font_size": "Title Font Size",
        "save_and_back": "Save and Back",
        "light": "Light",
        "dark": "Dark",
        "toggle_theme": "Toggle Theme",
        "new_password": "Enter new password",
        "confirm_password": "Confirm password",
        "set_change": "Set/Change",
        "remove": "Remove",
        "back_to_settings": "Back to Settings Menu",
        "color_orange": "Orange",
        "color_blue": "Blue",
        "color_green": "Green",
        "ok": "OK",
        "enter_current_password": "Enter current password to confirm",
        "confirm_removal": "Confirm Removal",
        "cancel": "Cancel",
    },
}

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            try: return json.load(f)
            except Exception: return {}
    return {}

def save_config(config):
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=4, ensure_ascii=False)

def hash_password(password, salt):
    return hashlib.sha256((password + salt).encode()).hexdigest()

class DualLabelButton(ButtonBehavior, BoxLayout):
    def __init__(self, main_key, ext_key, on_press_callback=None, app=None, **kwargs):
        super().__init__(orientation='horizontal', spacing=10, padding=10, **kwargs)
        self.app = app; self.main_key = main_key; self.ext_key = ext_key
        with self.canvas.before:
            Color(0.9, 0.9, 0.9, 1); self._rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self._update_rect, size=self._update_rect)
        self.label_main = Label(halign='center', valign='middle')
        self.label_ext = Label(halign='center', valign='middle')
        self._on_press_callback = on_press_callback; self.update()
    def _update_rect(self, *a): self._rect.pos = self.pos; self._rect.size = self.size
    def on_press(self):
        if self._on_press_callback:
            try: self._on_press_callback(self)
            except Exception: pass
    def update(self):
        self.clear_widgets()
        main_raw = self.app.t(self.main_key); ext_raw = self.app.t(self.ext_key)
        self.label_main.text = main_raw; self.label_main.font_name = 'Roboto'
        self.label_ext.text = ext_raw; self.label_ext.font_name = 'Roboto'
        self.add_widget(self.label_main); self.add_widget(self.label_ext)

class DataPlotterApp(App):
    def build(self):
        if platform == 'android':
            permissions = [Permission.WRITE_EXTERNAL_STORAGE, Permission.READ_EXTERNAL_STORAGE]
            request_permissions(permissions)
        
        self.config = load_config()
        self.config.setdefault('graph_color', [1, 0.4, 0, 0.9])
        self.config.setdefault('title_font_size', '20sp')
        self.config.setdefault('theme', 'Light')
        self.config.setdefault('language', 'English')

        self.apply_theme()
        
        self.sm = ScreenManager()
        self.sm.add_widget(EntryScreen(name='entry', app=self))
        self.sm.add_widget(PasswordScreen(name='password', app=self))
        self.sm.add_widget(PlotScreen(name='plot', app=self))
        self.sm.add_widget(SettingsMenuScreen(name='settings_menu', app=self))
        self.sm.add_widget(AppearanceSettingsScreen(name='appearance_settings', app=self))
        self.sm.add_widget(PasswordSettingsScreen(name='password_settings', app=self))
        self.sm.add_widget(SecurityScreen(name='security_screen', app=self))
        self.sm.current = 'entry'
        return self.sm
        
    def apply_theme(self):
        if self.config.get('theme') == 'Dark':
            self.theme_background = (0.1, 0.1, 0.1, 1); self.theme_text_color = (0.9, 0.9, 0.9, 1)
        else:
            self.theme_background = (0.95, 0.95, 0.95, 1); self.theme_text_color = (0.1, 0.1, 0.1, 1)
        Window.clearcolor = self.theme_background
        
    def t(self, key):
        return LANGUAGES['English'].get(key, key)
        
    def ms(self, s):
        return str(s)
        
    def get_font(self):
        return 'Roboto'
        
    def show_info_popup(self, title_key, message_key):
        title = self.t(title_key); message = self.t(message_key)
        content = Label(text=message)
        content.bind(size=lambda *x: content.setter('text_size')(content, (content.width-20, None)))
        popup = Popup(title=title, content=content, size_hint=(None, None), size=(400, 200))
        popup.open()

class BaseScreen(Screen):
    def __init__(self, app, **kwargs):
        super().__init__(**kwargs); self.app = app
    def on_pre_enter(self, *args):
        if hasattr(self, 'update_ui_text_and_fonts'): self.update_ui_text_and_fonts()
    def update_ui_text_and_fonts(self): self._update_font_recursive(self)
    def _update_font_recursive(self, widget):
        if isinstance(widget, (Label, Button, TextInput)):
            widget.font_name = 'Roboto'
        if isinstance(widget, DualLabelButton): widget.update()
        if hasattr(widget, 'children'):
            for child in list(widget.children):
                if not isinstance(child, DualLabelButton): self._update_font_recursive(child)

class EntryScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', spacing=20, padding=50)
        logo_image = Image(source='gas.png', size_hint_y=None, height=250)
        self.title = Label(font_size='30sp', bold=True, size_hint_y=None, height=60)
        self.login_button = Button(font_size='20sp', on_press=self.go_to_login)
        self.settings_button = Button(font_size='20sp', on_press=self.go_to_settings)
        self.exit_button = Button(font_size='20sp', on_press=App.get_running_app().stop)
        layout.add_widget(logo_image); layout.add_widget(self.title); layout.add_widget(self.login_button)
        layout.add_widget(self.settings_button); layout.add_widget(self.exit_button)
        self.add_widget(layout)
    def update_ui_text_and_fonts(self):
        self.title.text = self.app.t("main_menu"); self.title.color = self.app.theme_text_color
        self.login_button.text = self.app.t("login")
        self.settings_button.text = self.app.t("settings")
        self.exit_button.text = self.app.t("exit")
        super().update_ui_text_and_fonts()
    def go_to_login(self, instance):
        if 'password_hash' in self.app.config: self.manager.current = 'password'
        else: self.manager.current = 'plot'
    def go_to_settings(self, instance): self.manager.current = 'settings_menu'

class PasswordScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', spacing=10, padding=40)
        self.info_label = Label(font_size='18sp')
        self.password_input = TextInput(password=True, multiline=False, font_size='20sp', size_hint_y=None, height=40)
        self.submit_button = Button(font_size='20sp', size_hint_y=None, height=50, on_press=self.check_password)
        self.back_button = Button(font_size='18sp', size_hint_y=None, height=40, on_press=self.go_back)
        self.layout.add_widget(self.info_label)
        self.layout.add_widget(self.password_input)
        self.layout.add_widget(self.submit_button)
        self.layout.add_widget(self.back_button)
        self.add_widget(self.layout)
    def go_back(self, instance): self.manager.current = 'entry'
    def update_ui_text_and_fonts(self):
        self.info_label.text = self.app.t("password_prompt"); self.info_label.color = self.app.theme_text_color
        self.submit_button.text = self.app.t("login")
        self.back_button.text = self.app.t("back_menu")
        self.password_input.text = ""
        super().update_ui_text_and_fonts()
    def check_password(self, instance):
        password = self.password_input.text; salt = self.app.config.get('password_salt', '')
        password_hash = self.app.config.get('password_hash', '')
        if hash_password(password, salt) == password_hash: self.manager.current = 'plot'
        else: self.app.show_info_popup("error", "incorrect_password")

class PlotScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        self.add_widget(self.layout)
    def on_enter(self):
        self.layout.clear_widgets()
        loading_label = Label(text=self.app.t("pressure_vs_time"), font_size='24sp', color=self.app.theme_text_color)
        self.layout.add_widget(loading_label)
        Clock.schedule_once(self.build_plot, 0.1)
    def build_plot(self, dt):
        self.layout.clear_widgets()
        self.title_label = Label(size_hint_y=None, height=40, bold=True, font_size=self.app.config['title_font_size'], color=self.app.theme_text_color)
        self.layout.add_widget(self.title_label)
        data_points, time_values, pressure_values = self.load_data()
        if not data_points:
            error_label = Label(text=self.app.t("error_data"), color=self.app.theme_text_color)
            self.layout.add_widget(error_label)
            return
        self.layout.add_widget(self.create_stats_layout(pressure_values))
        self.graph_widget = self.create_graph(data_points, time_values, pressure_values)
        self.layout.add_widget(self.graph_widget)
        self.layout.add_widget(self.create_export_layout())
        back_button = Button(size_hint_y=None, height=40, on_press=lambda x: setattr(self.manager, 'current', 'entry'))
        self.layout.add_widget(back_button)
        self.title_label.text = self.app.t("pressure_vs_time")
        back_button.text = self.app.t("back_menu")
        self.update_ui_text_and_fonts()
        
    def load_data(self):
        data_points, time_values, pressure_values = [], [], []
        try:
            with open('data.txt', 'r', encoding='utf-8') as f:
                next(f) # Skip header
                for line in f:
                    parts = line.strip().split()
                    if len(parts) == 2:
                        time, pressure = float(parts[0]), float(parts[1])
                        data_points.append((time, pressure))
                        time_values.append(time)
                        pressure_values.append(pressure)
        except Exception as e:
            # --- FIX: Added error logging to find the root cause ---
            print(f"CRITICAL: Failed to load or parse data.txt. Error: {e}")
            # This will print the exact error (e.g., FileNotFoundError, PermissionError, ValueError) to the logcat.
        
        return data_points, time_values, pressure_values
        
    def create_stats_layout(self, pressure_values):
        stats_layout = BoxLayout(size_hint_y=None, height=30)
        max_p = Label(color=self.app.theme_text_color); min_p = Label(color=self.app.theme_text_color); avg_p = Label(color=self.app.theme_text_color)
        stats_layout.add_widget(min_p); stats_layout.add_widget(avg_p); stats_layout.add_widget(max_p)
        max_val = max(pressure_values); min_val = min(pressure_values); avg_val = statistics.mean(pressure_values)
        max_p.text = f"{self.app.t('max')}: {max_val:.2f}"
        min_p.text = f"{self.app.t('min')}: {min_val:.2f}"
        avg_p.text = f"{self.app.t('avg')}: {avg_val:.2f}"
        return stats_layout
        
    def create_graph(self, data_points, time_values, pressure_values):
        xlabel = self.app.t("time"); ylabel = self.app.t("pressure_pa")
        xmaj = (max(time_values) - min(time_values)) / 10 if time_values and max(time_values) != min(time_values) else 1
        ymin = min(pressure_values) if pressure_values else 0; ymax = max(pressure_values) if pressure_values else 1
        label_opts = {'color': self.app.theme_text_color, 'bold': True}
        graph = Graph(xlabel=xlabel, ylabel=ylabel, x_ticks_major=xmaj, y_ticks_major=(ymax - ymin) / 5 if ymax > ymin else 1,
            y_grid_label=True, x_grid_label=True, padding=10, x_grid=True, y_grid=True,
            xmin=min(time_values) if time_values else 0, xmax=max(time_values) if time_values else 1,
            ymin=ymin, ymax=ymax if ymax > ymin else ymin + 1, font_size='12sp', label_options=label_opts,
            background_color=(*self.app.theme_background[:3], 0), border_color=self.app.theme_text_color)
        plot = LinePlot(color=self.app.config['graph_color'], line_width=2); plot.points = data_points
        graph.add_plot(plot)
        return graph
        
    def create_export_layout(self):
        export_layout = BoxLayout(size_hint_y=None, height=50, spacing=10)
        btn_png = DualLabelButton("save_png_word", "save_png_ext", on_press_callback=lambda x: self.export_graph('png'), app=self.app)
        btn_jpg = DualLabelButton("save_jpg_word", "save_jpg_ext", on_press_callback=lambda x: self.export_graph('jpg'), app=self.app)
        btn_pdf = DualLabelButton("save_pdf_word", "save_pdf_ext", on_press_callback=lambda x: self.export_graph('pdf'), app=self.app)
        export_layout.add_widget(btn_png); export_layout.add_widget(btn_jpg); export_layout.add_widget(btn_pdf)
        return export_layout
        
    def export_graph(self, file_format):
        # NOTE: fpdf export is complex. This is a placeholder. A full implementation would go here.
        print(f"Exporting to {file_format} is not fully implemented yet.")
        pass

class SettingsMenuScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', spacing=20, padding=50)
        self.title = Label(font_size='30sp', bold=True)
        self.appearance_btn = Button(font_size='20sp', on_press=lambda x: setattr(self.manager, 'current', 'appearance_settings'))
        self.security_btn = Button(font_size='20sp', on_press=lambda x: setattr(self.manager, 'current', 'security_screen'))
        self.back_btn = Button(font_size='20sp', on_press=lambda x: setattr(self.manager, 'current', 'entry'))
        layout.add_widget(self.title); layout.add_widget(self.appearance_btn); layout.add_widget(self.security_btn)
        layout.add_widget(self.back_btn)
        self.add_widget(layout)
    def update_ui_text_and_fonts(self):
        self.title.text = self.app.t("settings_title"); self.title.color = self.app.theme_text_color
        self.appearance_btn.text = self.app.t("appearance")
        self.security_btn.text = self.app.t("security")
        self.back_btn.text = self.app.t("back_main")
        super().update_ui_text_and_fonts()

class SecurityScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', spacing=20, padding=50)
        self.title = Label(font_size='30sp', bold=True)
        self.change_pass_btn = Button(font_size='20sp', on_press=lambda x: setattr(self.manager, 'current', 'password_settings'))
        self.back_btn = Button(font_size='20sp', on_press=lambda x: setattr(self.manager, 'current', 'settings_menu'))
        layout.add_widget(self.title); layout.add_widget(self.change_pass_btn)
        layout.add_widget(self.back_btn)
        self.add_widget(layout)
    def update_ui_text_and_fonts(self):
        self.title.text = self.app.t("security_options"); self.title.color = self.app.theme_text_color
        self.change_pass_btn.text = self.app.t("change_password")
        self.back_btn.text = self.app.t("back_settings")
        super().update_ui_text_and_fonts()

class AppearanceSettingsScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', spacing=10, padding=30)
        self.color_label = Label(font_size='18sp')
        color_layout = BoxLayout(spacing=10, size_hint_y=None, height=40)
        self.btn_orange = Button(on_press=lambda x: self.set_graph_color([1, 0.4, 0, 0.9]))
        self.btn_blue = Button(on_press=lambda x: self.set_graph_color([0.1, 0.6, 0.9, 1]))
        self.btn_green = Button(on_press=lambda x: self.set_graph_color([0, 0.7, 0.3, 1]))
        color_layout.add_widget(self.btn_orange); color_layout.add_widget(self.btn_blue); color_layout.add_widget(self.btn_green)
        self.font_label = Label(font_size='18sp')
        self.font_slider = Slider(min=10, max=40); self.font_slider.bind(value=self.on_font_slider_value)
        self.current_font_label = Label(text="")
        self.theme_label = Label(font_size='18sp')
        theme_layout = BoxLayout(spacing=10, size_hint_y=None, height=40)
        self.light_btn = Button(on_press=lambda x: self.set_theme('Light'))
        self.dark_btn = Button(on_press=lambda x: self.set_theme('Dark'))
        theme_layout.add_widget(self.light_btn); theme_layout.add_widget(self.dark_btn)
        self.back_button = Button(size_hint_y=None, height=50, on_press=self.save_and_exit)
        layout.add_widget(self.color_label); layout.add_widget(color_layout); layout.add_widget(self.font_label)
        layout.add_widget(self.font_slider); layout.add_widget(self.current_font_label); layout.add_widget(self.theme_label)
        layout.add_widget(theme_layout); layout.add_widget(BoxLayout()); layout.add_widget(self.back_button)
        self.add_widget(layout)
    def update_ui_text_and_fonts(self):
        self.color_label.text = self.app.t("graph_color")
        self.font_label.text = self.app.t("title_font_size")
        self.theme_label.text = self.app.t("theme")
        self.back_button.text = self.app.t("save_and_back")
        self.btn_orange.text = self.app.t("color_orange"); self.btn_blue.text = self.app.t("color_blue")
        self.btn_green.text = self.app.t("color_green"); self.light_btn.text = self.app.t("light")
        self.dark_btn.text = self.app.t("dark")
        self.color_label.color = self.app.theme_text_color; self.font_label.color = self.app.theme_text_color
        self.current_font_label.color = self.app.theme_text_color; self.theme_label.color = self.app.theme_text_color
        try: self.font_slider.value = int(self.app.config['title_font_size'][:-2])
        except Exception: self.font_slider.value = 20
        self.current_font_label.text = f"{int(self.font_slider.value)}sp"
        super().update_ui_text_and_fonts()
    def set_graph_color(self, color): self.app.config['graph_color'] = color
    def on_font_slider_value(self, instance, value):
        self.app.config['title_font_size'] = f"{int(value)}sp"; self.current_font_label.text = f"{int(value)}sp"
    def set_theme(self, theme_name):
        self.app.config['theme'] = theme_name; self.app.apply_theme(); self.update_ui_text_and_fonts()
    def save_and_exit(self, instance):
        save_config(self.app.config); self.manager.current = 'settings_menu'

class PasswordSettingsScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', spacing=10, padding=30)
        self.password_label = Label(font_size='18sp')
        self.pass_input1 = TextInput(multiline=False, size_hint_y=None, height=40, password=True)
        self.pass_input2 = TextInput(multiline=False, size_hint_y=None, height=40, password=True)
        password_buttons = BoxLayout(size_hint_y=None, height=40, spacing=10)
        self.set_pass_btn = Button(on_press=self.set_password)
        self.remove_pass_btn = Button(on_press=self.remove_password)
        password_buttons.add_widget(self.set_pass_btn); password_buttons.add_widget(self.remove_pass_btn)
        self.back_button = Button(size_hint_y=None, height=50, on_press=lambda x: setattr(self.manager, 'current', 'security_screen'))
        layout.add_widget(self.password_label); layout.add_widget(self.pass_input1); layout.add_widget(self.pass_input2)
        layout.add_widget(password_buttons); layout.add_widget(BoxLayout()); layout.add_widget(self.back_button)
        self.add_widget(layout)
    def update_ui_text_and_fonts(self):
        self.password_label.text = self.app.t("change_password")
        self.set_pass_btn.text = self.app.t("set_change")
        self.remove_pass_btn.text = self.app.t("remove")
        self.back_button.text = self.app.t("back_to_settings")
        self.pass_input1.hint_text = self.app.t("new_password")
        self.pass_input2.hint_text = self.app.t("confirm_password")
        self.password_label.color = self.app.theme_text_color
        self.pass_input1.text = ""; self.pass_input2.text = ""
        super().update_ui_text_and_fonts()
    def set_password(self, instance):
        p1 = self.pass_input1.text; p2 = self.pass_input2.text
        if not p1 or not p2: self.app.show_info_popup("error", "passwords_empty"); return
        if p1 != p2: self.app.show_info_popup("error", "passwords_not_match"); return
        salt = os.urandom(16).hex()
        self.app.config['password_salt'] = salt
        self.app.config['password_hash'] = hash_password(p1, salt)
        save_config(self.app.config)
        self.pass_input1.text = ""; self.pass_input2.text = ""
        self.app.show_info_popup("main_menu", "password_set")
    def remove_password(self, instance):
        pass

if __name__ == '__main__':
    DataPlotterApp().run()

