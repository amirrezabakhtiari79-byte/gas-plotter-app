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
# import sys  <- REMOVED: No longer needed after removing os.execl
import hashlib
from fpdf import FPDF

# --- MODIFIED ERROR HANDLING ---
try:
    import arabic_reshaper
    from bidi.algorithm import get_display
    print("Successfully imported Farsi shaping libraries.")
except Exception as e:
    print(f"CRITICAL ERROR: Could not import Farsi libraries. PDF will not work. Error: {e}")
    # Define a placeholder function so the app doesn't crash
    def _shape_text(s):
        return s

# --- MODIFIED ERROR HANDLING ---
def _shape_text(s):
    try:
        reshaped_text = arabic_reshaper.reshape(s)
        return get_display(reshaped_text)
    except Exception as e:
        print(f"ERROR: Failed to shape Farsi text. Text: '{s}'. Error: {e}")
        return s # Return the original string on failure

# --- FIX START: Removed pyfingerprint ---
# The pyfingerprint library is incompatible with Android and was causing the
# "aidl not found" build error. It has been completely removed.
# The app will now use the software-based PIN as the only "fingerprint" option.
HAS_PYF = False
# --- FIX END ---

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
        "language": "Language",
        "back_main": "Back to Main Menu",
        "security_options": "Security Options",
        "change_password": "Create/Change Password",
        "fingerprints": "Add PIN Code", # Text changed to reflect functionality
        "back_settings": "Back to Settings Menu",
        "passwords_empty": "Password fields cannot be empty.",
        "passwords_not_match": "Passwords do not match.",
        "password_set": "Password has been set.",
        "password_removed": "Password has been removed.",
        "fingerprint_coming": "Enter a PIN for quick access.", # Text changed
        "missing_font_instruction": "Put a Persian TTF (e.g. Vazir.ttf) in the app folder and restart.",
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
        "lang_choose": "Choose Language",
        "lang_english": "English",
        "lang_farsi": "Farsi",
        "lang_restart_required": "Language has been updated.", # Text changed
        "restart_required_title": "Language Changed", # Text changed
        "theme_restart_required": "Theme has been updated. Please restart the app for the changes to fully apply.",
        "theme_restart_title": "Restart Recommended",
        "ok": "OK",
        "enroll_fingerprint": "Enroll PIN", # Text changed
        "use_fingerprint_to_login": "Use PIN to Login", # Text changed
        "enter_pin": "Enter PIN",
        "scan_prompt": "Please place your finger on the sensor", # This will no longer be seen
        "enter_current_password": "Enter current password to confirm",
        "confirm_removal": "Confirm Removal",
        "cancel": "Cancel",
        "report_title": "Report Title",
        "date": "Date",
        "inspector_name": "Inspector Name",
        "inspector_code": "Inspector Code",
        "location": "Location",
        "signature_title": "Inspector Signature and Approval",
        "company_name": "National Gas Company"
    },
    "Farsi": {
        "main_menu": "منو اصلی",
        "login": "ورود",
        "settings": "تنظیمات",
        "exit": "خروج",
        "password_prompt": "لطفاً رمز عبور خود را وارد کنید:",
        "error": "خطا",
        "incorrect_password": "رمز اشتباه است.",
        "pressure_vs_time": "فشار در برابر زمان",
        "error_data": "خطا: فایل داده یافت نشد یا خالی است.",
        "max": "بیشینه",
        "min": "کمینه",
        "avg": "میانگین",
        "save_png_word": "ذخیره",
        "save_png_ext": "PNG",
        "save_jpg_word": "ذخیره",
        "save_jpg_ext": "JPG",
        "save_pdf_word": "ذخیره",
        "save_pdf_ext": "PDF",
        "back_menu": "بازگشت به منو",
        "settings_title": "تنظیمات",
        "appearance": "ظاهر",
        "security": "امنیت",
        "language": "زبان",
        "back_main": "بازگشت به منو اصلی",
        "security_options": "گزینه‌های امنیتی",
        "change_password": "ایجاد/تغییر رمز",
        "fingerprints": "افزودن کد PIN", # Text changed
        "back_settings": "بازگشت به تنظیمات",
        "passwords_empty": "فیلدهای رمز عبور نمی‌توانند خالی باشند.",
        "passwords_not_match": "رمزها مطابقت ندارند.",
        "password_set": "رمز با موفقیت ثبت شد.",
        "password_removed": "رمز حذف شد.",
        "fingerprint_coming": "برای دسترسی سریع، یک کد PIN وارد کنید.", # Text changed
        "missing_font_instruction": "یک فونت فارسی (مثلاً Vazir.ttf) در پوشه برنامه قرار دهید و برنامه را دوباره اجرا کنید.",
        "time": "زمان",
        "pressure_pa": "فشار",
        "theme": "قالب",
        "graph_color": "رنگ نمودار",
        "title_font_size": "اندازه فونت عنوان",
        "save_and_back": "ذخیره و بازگشت",
        "light": "روشن",
        "dark": "تیره",
        "toggle_theme": "تغییر قالب",
        "new_password": "رمز جدید را وارد کنید",
        "confirm_password": "تأیید رمز",
        "set_change": "ثبت/تغییر",
        "remove": "حذف",
        "back_to_settings": "بازگشت به تنظیمات",
        "color_orange": "نارنجی",
        "color_blue": "آبی",
        "color_green": "سبز",
        "lang_choose": "انتخاب زبان",
        "lang_english": "انگلیسی",
        "lang_farsi": "فارسی",
        "lang_restart_required": "زبان برنامه تغییر کرد.", # Text changed
        "restart_required_title": "زبان تغییر کرد", # Text changed
        "theme_restart_required": "قالب به روز شد. لطفاً برای اعمال کامل تغییرات، برنامه را مجدداً راه اندازی کنید.",
        "theme_restart_title": "راه اندازی مجدد توصیه می شود",
        "ok": "باشه",
        "enroll_fingerprint": "ثبت کد PIN", # Text changed
        "use_fingerprint_to_login": "ورود با کد PIN", # Text changed
        "enter_pin": "کد PIN را وارد کنید",
        "scan_prompt": "لطفاً انگشت خود را روی سنسور قرار دهید", # This will no longer be seen
        "enter_current_password": "برای تایید رمز فعلی را وارد کنید",
        "confirm_removal": "تایید حذف",
        "cancel": "لغو",
        "report_title": "عنوان گزارش",
        "date": "تاریخ",
        "inspector_name": "نام بازرس",
        "inspector_code": "کد بازرس",
        "location": "آدرس محل",
        "signature_title": "محل امضا و تایید بازرس",
        "company_name": "شرکت ملی گاز ایران"
    }
}

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            try:
                return json.load(f)
            except Exception:
                return {}
    return {}

def save_config(config):
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=4, ensure_ascii=False)

def hash_password(password, salt):
    return hashlib.sha256((password + salt).encode()).hexdigest()

def make_all_buttons_light_blue(widget):
    if isinstance(widget, Button):
        widget.background_color = LIGHT_BLUE
    if hasattr(widget, 'children'):
        for child in widget.children:
            make_all_buttons_light_blue(child)

class FontManager:
    def __init__(self):
        self.registered = False
        self.font_name = None
        self.font_path = None

    def try_register(self):
        if self.registered:
            return
        candidates = [
            'BNaznnBd.ttf', 'vazir.ttf', 'Vazir-Regular.ttf',
            'NotoNaskhArabic-Regular.ttf', 'NotoSansArabic-Regular.ttf', 'NotoSansArabic.ttf'
        ]
        for fn in candidates:
            if os.path.exists(fn):
                try:
                    LabelBase.register(name='FarsiFont', fn_regular=fn)
                    self.registered = True
                    self.font_name = 'FarsiFont'
                    self.font_path = fn
                    print(f"Registered Farsi font: {fn}")
                    return
                except Exception as e:
                    print(f"Failed to register font {fn}: {e}")
                    continue

    def available(self):
        return self.registered

FONT_MANAGER = FontManager()

class FingerprintManager:
    def __init__(self, app):
        self.app = app

    def available(self):
        # --- FIX: Hardware fingerprint is not available on Android this way ---
        return False

    # --- FIX: All hardware-specific methods removed ---
    # try_connect, enroll_with_sensor, verify_with_sensor were deleted
    # as they relied on the incompatible pyfingerprint library.

    def enroll_software(self, pin):
        salt = os.urandom(16).hex()
        self.app.config['fingerprint_soft'] = hash_password(pin, salt)
        self.app.config['fingerprint_soft_salt'] = salt
        save_config(self.app.config)

    def verify_software(self, pin):
        salt = self.app.config.get('fingerprint_soft_salt', '')
        stored = self.app.config.get('fingerprint_soft', '')
        return stored and hash_password(pin, salt) == stored

class DualLabelButton(ButtonBehavior, BoxLayout):
    def __init__(self, main_key, ext_key, on_press_callback=None, app=None, **kwargs):
        super().__init__(orientation='horizontal', spacing=10, padding=10, **kwargs)
        self.app = app
        self.main_key = main_key
        self.ext_key = ext_key
        with self.canvas.before:
            Color(0.9, 0.9, 0.9, 1)
            self._rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self._update_rect, size=self._update_rect)
        
        self.label_main = Label(halign='center', valign='middle')
        self.label_ext = Label(halign='center', valign='middle')
        
        self._on_press_callback = on_press_callback
        self.update()

    def _update_rect(self, *a):
        self._rect.pos = self.pos
        self._rect.size = self.size

    def on_press(self):
        if self._on_press_callback:
            try: self._on_press_callback(self)
            except Exception: pass

    def update(self):
        self.clear_widgets()
        
        main_raw = self.app.t(self.main_key)
        ext_raw = self.app.t(self.ext_key)

        if self.app.is_farsi_mode():
            self.label_main.text = self.app.ms(main_raw)
            self.label_main.font_name = self.app.get_font()
            self.label_ext.text = ext_raw
            self.label_ext.font_name = 'Roboto'
            self.add_widget(self.label_ext)
            self.add_widget(self.label_main)
        else:
            self.label_main.text = main_raw
            self.label_main.font_name = 'Roboto'
            self.label_ext.text = ext_raw
            self.label_ext.font_name = 'Roboto'
            self.add_widget(self.label_main)
            self.add_widget(self.label_ext)

class DataPlotterApp(App):
    def build(self):
        self.config = load_config()
        self.config.setdefault('graph_color', [1, 0.4, 0, 0.9])
        self.config.setdefault('title_font_size', '20sp')
        self.config.setdefault('theme', 'Light')
        self.config.setdefault('language', 'English')

        self.apply_theme()
        FONT_MANAGER.try_register()
        self.fpm = FingerprintManager(self)
        self.sm = ScreenManager()
        self.sm.add_widget(EntryScreen(name='entry', app=self))
        self.sm.add_widget(PasswordScreen(name='password', app=self))
        self.sm.add_widget(PlotScreen(name='plot', app=self))
        self.sm.add_widget(SettingsMenuScreen(name='settings_menu', app=self))
        self.sm.add_widget(AppearanceSettingsScreen(name='appearance_settings', app=self))
        self.sm.add_widget(PasswordSettingsScreen(name='password_settings', app=self))
        self.sm.add_widget(SecurityScreen(name='security_screen', app=self))
        self.sm.current = 'entry'
        Clock.schedule_once(lambda dt: make_all_buttons_light_blue(self.sm), 0.1)
        return self.sm

    def apply_theme(self):
        if self.config.get('theme') == 'Dark':
            self.theme_background = (0.1, 0.1, 0.1, 1)
            self.theme_text_color = (0.9, 0.9, 0.9, 1)
        else:
            self.theme_background = (0.95, 0.95, 0.95, 1)
            self.theme_text_color = (0.1, 0.1, 0.1, 1)
        Window.clearcolor = self.theme_background

    def t(self, key):
        lang = self.config.get('language', 'English')
        return LANGUAGES.get(lang, LANGUAGES['English']).get(key, key)

    def is_farsi_mode(self):
        return self.config.get('language', 'English') == 'Farsi'

    def ms(self, s):
        if self.is_farsi_mode():
            return _shape_text(str(s))
        return str(s)

    def get_font(self):
        if self.is_farsi_mode() and FONT_MANAGER.available():
            return FONT_MANAGER.font_name
        return 'Roboto'

    def show_info_popup(self, title_key, message_key, on_dismiss=None):
        font = self.get_font()
        title = self.ms(self.t(title_key))
        message = self.ms(self.t(message_key))

        content = Label(text=message, font_name=font)
        content.bind(size=lambda *x: content.setter('text_size')(content, (content.width-20, None)))

        popup = Popup(title=title,
                      content=content,
                      size_hint=(None, None),
                      size=(400, 200),
                      title_font=font)
        if on_dismiss:
            popup.bind(on_dismiss=on_dismiss)
        popup.open()


    def ensure_farsi_font_popup(self):
        if self.is_farsi_mode() and not FONT_MANAGER.available():
            self.show_info_popup("error", "missing_font_instruction")

    # --- FIX: Removed hard_restart ---
    # The os.execl function is incompatible with Android.
    # UI updates are now handled by screen transitions and popups.
    # def hard_restart(self):
    #     save_config(self.config)
    #     python = sys.executable
    #     os.execl(python, python, *sys.argv)

class BaseScreen(Screen):
    def __init__(self, app, **kwargs):
        super().__init__(**kwargs)
        self.app = app

    def on_pre_enter(self, *args):
        # This function is key for updating UI text when navigating
        if hasattr(self, 'update_ui_text_and_fonts'):
            self.update_ui_text_and_fonts()
        self.app.ensure_farsi_font_popup()

    def update_ui_text_and_fonts(self):
        self._update_font_recursive(self)

    def _update_font_recursive(self, widget):
        font_name = self.app.get_font()
        if isinstance(widget, (Label, Button)):
            widget.font_name = font_name
        if isinstance(widget, TextInput):
            widget.font_name = font_name
            widget.base_direction = 'rtl' if self.app.is_farsi_mode() else 'ltr'
        if isinstance(widget, DualLabelButton):
            widget.update()
        if hasattr(widget, 'children'):
            for child in list(widget.children):
                if not isinstance(child, DualLabelButton):
                    self._update_font_recursive(child)

# ... All other classes remain the same until SettingsMenuScreen and AppearanceSettingsScreen ...
# (The code for EntryScreen, PasswordScreen, PlotScreen is unchanged)
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
        self.title.text = self.app.ms(self.app.t("main_menu"))
        self.title.color = self.app.theme_text_color
        self.login_button.text = self.app.ms(self.app.t("login"))
        self.settings_button.text = self.app.ms(self.app.t("settings"))
        self.exit_button.text = self.app.ms(self.app.t("exit"))
        super().update_ui_text_and_fonts()
    def go_to_login(self, instance):
        if 'password_hash' in self.app.config: self.manager.current = 'password'
        else: self.manager.current = 'plot'
    def go_to_settings(self, instance):
        self.manager.current = 'settings_menu'

class PasswordScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', spacing=10, padding=40)
        self.info_label = Label(font_size='18sp')
        self.password_input = TextInput(password=True, multiline=False, font_size='20sp', size_hint_y=None, height=40)
        self.submit_button = Button(font_size='20sp', size_hint_y=None, height=50, on_press=self.check_password)
        self.fingerprint_button = Button(font_size='18sp', size_hint_y=None, height=40, on_press=self.use_fingerprint)
        
        self.back_button = Button(font_size='18sp', size_hint_y=None, height=40, on_press=self.go_back)

        self.layout.add_widget(self.info_label); self.layout.add_widget(self.password_input)
        self.layout.add_widget(self.submit_button); self.layout.add_widget(self.fingerprint_button)
        self.layout.add_widget(self.back_button) 
        
        self.add_widget(self.layout)

    def go_back(self, instance):
        self.manager.current = 'entry'

    def update_ui_text_and_fonts(self):
        self.info_label.text = self.app.ms(self.app.t("password_prompt"))
        self.info_label.color = self.app.theme_text_color
        self.submit_button.text = self.app.ms(self.app.t("login"))
        self.fingerprint_button.text = self.app.ms(self.app.t("use_fingerprint_to_login"))
        self.back_button.text = self.app.ms(self.app.t("back_menu")) 
        self.password_input.text = ""
        super().update_ui_text_and_fonts()
        
    def check_password(self, instance):
        password = self.password_input.text
        salt = self.app.config.get('password_salt', '')
        password_hash = self.app.config.get('password_hash', '')
        if hash_password(password, salt) == password_hash: self.manager.current = 'plot'
        else: self.app.show_info_popup("error", "incorrect_password")
        
    def use_fingerprint(self, instance):
        # This method now only triggers the software PIN check, as fpm.available() is always False
        font = self.app.get_font() # Corrected from self.get_font()
        def on_result(success, info):
            if success: self.manager.current = 'plot'
            else:
                msg = info if isinstance(info, str) else str(info)
                popup_content_text = self.app.ms(self.app.t(msg)) if msg in LANGUAGES[self.app.config['language']] else msg
                popup_content = Label(text=popup_content_text, font_name=font)
                popup = Popup(title=self.app.ms(self.app.t("error")), content=popup_content, size_hint=(None, None), size=(350, 200), title_font=font)
                popup.open()

        if self.app.fpm.available(): # This condition will be false
            # This block of code is now unreachable, which is correct.
            popup_content = Label(text=self.app.ms(self.app.t("scan_prompt")), font_name=font)
            popup = Popup(title=self.app.ms(self.app.t("scan_prompt")), content=popup_content, size_hint=(None, None), size=(350, 200), title_font=font)
            popup.open()
            # Clock.schedule_once(lambda dt: (popup.dismiss(), self.app.fpm.verify_with_sensor(on_result)), 0.5)
        else:
            # This is the only part that will run
            content = BoxLayout(orientation='vertical', spacing=10)
            pin_input = TextInput(password=True, multiline=False, hint_text=self.app.ms(self.app.t("enter_pin")), size_hint_y=None, height=40, font_name=font, base_direction='ltr')
            btn = Button(text=self.app.ms(self.app.t("login")), size_hint_y=None, height=40, font_name=font)
            content.add_widget(pin_input); content.add_widget(btn)
            popup = Popup(title=self.app.ms(self.app.t("enter_pin")), content=content, size_hint=(None, None), size=(350, 200), title_font=font)
            def check_pin(x):
                pin = pin_input.text
                popup.dismiss()
                if self.app.fpm.verify_software(pin): on_result(True, "ok")
                else: on_result(False, "incorrect_password")
            btn.bind(on_press=check_pin)
            popup.open()

class PlotScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        self.add_widget(self.layout)
    def on_enter(self):
        self.layout.clear_widgets()
        loading_label = Label(text=self.app.ms(self.app.t("pressure_vs_time")), font_size='24sp', color=self.app.theme_text_color, font_name=self.app.get_font())
        self.layout.add_widget(loading_label)
        Clock.schedule_once(self.build_plot, 0.1)
    def build_plot(self, dt):
        self.layout.clear_widgets()
        self.title_label = Label(size_hint_y=None, height=40, bold=True, font_size=self.app.config['title_font_size'], color=self.app.theme_text_color)
        self.layout.add_widget(self.title_label)
        data_points, time_values, pressure_values = self.load_data()
        if not data_points:
            error_label = Label(text=self.app.ms(self.app.t("error_data")), color=self.app.theme_text_color, font_name=self.app.get_font())
            self.layout.add_widget(error_label)
            # Add a back button even if data fails to load
            back_button = Button(text=self.app.ms(self.app.t("back_menu")), size_hint_y=None, height=40, on_press=lambda x: setattr(self.manager, 'current', 'entry'))
            self.layout.add_widget(back_button)
            self.update_ui_text_and_fonts()
            return
        self.layout.add_widget(self.create_stats_layout(pressure_values))
        self.graph_widget = self.create_graph(data_points, time_values, pressure_values)
        self.layout.add_widget(self.graph_widget)
        self.layout.add_widget(self.create_export_layout())
        back_button = Button(size_hint_y=None, height=40, on_press=lambda x: setattr(self.manager, 'current', 'entry'))
        self.layout.add_widget(back_button)
        self.title_label.text = self.app.ms(self.app.t("pressure_vs_time"))
        back_button.text = self.app.ms(self.app.t("back_menu"))
        self.update_ui_text_and_fonts()
    def load_data(self):
        data_points, time_values, pressure_values = [], [], []
        try:
            with open('data.txt', 'r', encoding='utf-8') as f:
                next(f)
                for line in f:
                    parts = line.strip().split()
                    if len(parts) == 2:
                        time, pressure = float(parts[0]), float(parts[1])
                        data_points.append((time, pressure)); time_values.append(time); pressure_values.append(pressure)
        except Exception as e:
            print(f"Error loading data.txt: {e}")
        return data_points, time_values, pressure_values
    def create_stats_layout(self, pressure_values):
        stats_layout = BoxLayout(size_hint_y=None, height=30)
        max_p = Label(color=self.app.theme_text_color); min_p = Label(color=self.app.theme_text_color); avg_p = Label(color=self.app.theme_text_color)
        stats_layout.add_widget(min_p); stats_layout.add_widget(avg_p); stats_layout.add_widget(max_p)
        max_val = max(pressure_values); min_val = min(pressure_values); avg_val = statistics.mean(pressure_values)
        max_p.text = self.app.ms(f"{self.app.t('max')}: {max_val:.2f}")
        min_p.text = self.app.ms(f"{self.app.t('min')}: {min_val:.2f}")
        avg_p.text = self.app.ms(f"{self.app.t('avg')}: {avg_val:.2f}")
        return stats_layout
    def create_graph(self, data_points, time_values, pressure_values):
        xlabel = self.app.ms(self.app.t("time")); ylabel = self.app.ms(self.app.t("pressure_pa"))
        xmaj = (max(time_values) - min(time_values)) / 10 if time_values and max(time_values) != min(time_values) else 1
        ymin = min(pressure_values) if pressure_values else 0; ymax = max(pressure_values) if pressure_values else 1
        label_opts = {'color': self.app.theme_text_color, 'bold': True, 'font_name': self.app.get_font()}
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
        if file_format in ['png', 'jpg']:
            tmp_name = "pressure_plot.png"
            try:
                self.graph_widget.export_to_png(tmp_name)
                if file_format == 'jpg':
                    if os.path.exists("pressure_plot.jpg"): os.remove("pressure_plot.jpg")
                    os.rename(tmp_name, "pressure_plot.jpg")
            except Exception as e:
                 print(f"Error exporting to {file_format}: {e}")
        elif file_format == 'pdf':
            try:
                self.graph_widget.export_to_png("temp_graph.png")
                _, _, pressure_values = self.load_data()

                pdf = FPDF(orientation='P', unit='mm', format='A4')
                pdf.add_page()
                
                if FONT_MANAGER.font_path:
                    pdf.add_font('Farsi', '', FONT_MANAGER.font_path, uni=True)
                    pdf.add_font('Farsi', 'B', FONT_MANAGER.font_path, uni=True)
                else:
                    print("Warning: Farsi font file not found. PDF will use default font.")

                if os.path.exists('gas_dim.png'):
                    pdf.image('gas_dim.png', x=0, y=0, w=210, h=297)
                pdf.set_line_width(0.5)
                pdf.rect(10, 10, 190, 277)
                if os.path.exists('gas.png'):
                    pdf.image('gas.png', x=150, y=15, w=40)
                
                pdf.set_font('Farsi', 'B', 18)
                pdf.set_xy(0, 20)
                pdf.cell(w=210, text=_shape_text("شرکت ملی گاز ایران"), align='C')
                
                pdf.set_font('Farsi', 'B', 22)
                pdf.set_xy(0, 40)
                pdf.cell(w=210, text=_shape_text("عنوان گزارش"), align='C')

                pdf.set_font('Farsi', 'B', 15)
                y_pos = 60
                pdf.set_xy(45, y_pos); pdf.multi_cell(w=90, h=8, text=_shape_text("تاریخ:"), align='L')
                y_pos = 60
                pdf.set_xy(90, y_pos); pdf.multi_cell(w=90, h=8, text=_shape_text("نام بازرس:"), align='R')
                y_pos += 10
                pdf.set_xy(90, y_pos); pdf.multi_cell(w=90, h=8, text=_shape_text("کد بازرس:"), align='R')
                y_pos += 10
                pdf.set_xy(90, y_pos); pdf.multi_cell(w=90, h=8, text=_shape_text("آدرس محل:"), align='R')
                
                pdf.image('temp_graph.png', x=30, y=100, w=150)
                
                pdf.set_font('Farsi', 'B', 14)
                pdf.set_xy(30, 220) # Position near bottom
                pdf.multi_cell(w=180, h=10, text=_shape_text("محل امضا و تایید بازرس"), align='L')

                pdf.output('pressure_plot.pdf')

                if os.path.exists("temp_graph.png"):
                    os.remove("temp_graph.png")

            except Exception as e: 
                print(f"Error generating PDF: {e}")

class SettingsMenuScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', spacing=20, padding=50)
        self.title = Label(font_size='30sp', bold=True)
        self.appearance_btn = Button(font_size='20sp', on_press=lambda x: setattr(self.manager, 'current', 'appearance_settings'))
        self.security_btn = Button(font_size='20sp', on_press=lambda x: setattr(self.manager, 'current', 'security_screen'))
        self.language_btn = Button(font_size='20sp', on_press=self.change_language)
        self.back_btn = Button(font_size='20sp', on_press=lambda x: setattr(self.manager, 'current', 'entry'))
        layout.add_widget(self.title); layout.add_widget(self.appearance_btn); layout.add_widget(self.security_btn)
        layout.add_widget(self.language_btn); layout.add_widget(self.back_btn)
        self.add_widget(layout)
    def update_ui_text_and_fonts(self):
        self.title.text = self.app.ms(self.app.t("settings_title"))
        self.title.color = self.app.theme_text_color
        self.appearance_btn.text = self.app.ms(self.app.t("appearance"))
        self.security_btn.text = self.app.ms(self.app.t("security"))
        self.language_btn.text = self.app.ms(self.app.t("language"))
        self.back_btn.text = self.app.ms(self.app.t("back_main"))
        super().update_ui_text_and_fonts()
        
    def change_language(self, instance):
        font = self.app.get_font()
        content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        btn_en = Button(text="English", font_name='Roboto')
        btn_fa = Button(text=_shape_text("فارسی"), font_name=FONT_MANAGER.font_name if FONT_MANAGER.available() else 'Roboto')
        
        popup = Popup(title=self.app.ms(self.app.t("lang_choose")), content=content, size_hint=(None, None), size=(300, 200), title_font=font)
        
        def set_lang(lang):
            popup.dismiss()
            if lang != self.app.config.get('language'):
                self.app.config['language'] = lang
                save_config(self.app.config)
                # --- FIX: Replaced hard_restart with a popup and UI update on navigation ---
                self.app.show_info_popup("restart_required_title", "lang_restart_required", on_dismiss=self.refresh_ui_text)

        btn_en.bind(on_press=lambda x: set_lang("English"))
        btn_fa.bind(on_press=lambda x: set_lang("Farsi"))
        content.add_widget(btn_en); content.add_widget(btn_fa)
        popup.open()

    def refresh_ui_text(self, instance):
        # This forces the current screen to update its text immediately after the popup closes.
        self.update_ui_text_and_fonts()


class SecurityScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', spacing=20, padding=50)
        self.title = Label(font_size='30sp', bold=True)
        self.change_pass_btn = Button(font_size='20sp', on_press=lambda x: setattr(self.manager, 'current', 'password_settings'))
        self.fingerprint_btn = Button(font_size='20sp', on_press=self.handle_fingerprint)
        self.back_btn = Button(font_size='20sp', on_press=lambda x: setattr(self.manager, 'current', 'settings_menu'))
        layout.add_widget(self.title); layout.add_widget(self.change_pass_btn)
        layout.add_widget(self.fingerprint_btn); layout.add_widget(self.back_btn)
        self.add_widget(layout)
    def update_ui_text_and_fonts(self):
        self.title.text = self.app.ms(self.app.t("security_options"))
        self.title.color = self.app.theme_text_color
        self.change_pass_btn.text = self.app.ms(self.app.t("change_password"))
        self.fingerprint_btn.text = self.app.ms(self.app.t("fingerprints"))
        self.back_btn.text = self.app.ms(self.app.t("back_settings"))
        super().update_ui_text_and_fonts()
    def handle_fingerprint(self, instance):
        font = self.app.get_font()
        if self.app.fpm.available():
            # This code is now unreachable, which is correct
            pass
        else:
            # This is the only part that will run
            content = BoxLayout(orientation='vertical', spacing=10)
            pin_input = TextInput(password=True, multiline=False, hint_text=self.app.ms(self.app.t("enter_pin")), size_hint_y=None, height=40, font_name=font)
            btn = Button(text=self.app.ms(self.app.t("enroll_fingerprint")), size_hint_y=None, height=40, font_name=font)
            content.add_widget(pin_input); content.add_widget(btn)
            popup = Popup(title=self.app.ms(self.app.t("enroll_fingerprint")), content=content, size_hint=(None, None), size=(400, 220), title_font=font)
            def on_set(x):
                pin = pin_input.text
                if not pin: self.app.show_info_popup("error", "passwords_empty"); return
                self.app.fpm.enroll_software(pin)
                popup.dismiss()
                self.app.show_info_popup("main_menu", "password_set")
            btn.bind(on_press=on_set)
            popup.open()
    def _enroll_result(self, success, info):
        # This callback is no longer used by the hardware flow but is kept for completeness
        if success: self.app.show_info_popup("enroll_fingerprint", "password_set")
        else: self.app.show_info_popup("error", "error")

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
        self.color_label.text = self.app.ms(self.app.t("graph_color"))
        self.font_label.text = self.app.ms(self.app.t("title_font_size"))
        self.theme_label.text = self.app.ms(self.app.t("theme"))
        self.back_button.text = self.app.ms(self.app.t("save_and_back"))
        self.btn_orange.text = self.app.ms(self.app.t("color_orange")); self.btn_blue.text = self.app.ms(self.app.t("color_blue"))
        self.btn_green.text = self.app.ms(self.app.t("color_green")); self.light_btn.text = self.app.ms(self.app.t("light"))
        self.dark_btn.text = self.app.ms(self.app.t("dark"))
        self.color_label.color = self.app.theme_text_color; self.font_label.color = self.app.theme_text_color
        self.current_font_label.color = self.app.theme_text_color; self.theme_label.color = self.app.theme_text_color
        try: self.font_slider.value = int(self.app.config['title_font_size'][:-2])
        except Exception: self.font_slider.value = 20
        self.current_font_label.text = f"{int(self.font_slider.value)}sp"
        super().update_ui_text_and_fonts()
    def set_graph_color(self, color): self.app.config['graph_color'] = color
    def on_font_slider_value(self, instance, value):
        self.app.config['title_font_size'] = f"{int(value)}sp"
        self.current_font_label.text = f"{int(value)}sp"
        
    def set_theme(self, theme_name):
        if self.app.config['theme'] != theme_name:
            self.app.config['theme'] = theme_name
            save_config(self.app.config)
            # --- FIX: Replaced hard_restart with a popup ---
            self.app.apply_theme() # Apply immediately
            # Inform the user to restart for full effect, which is a safe mobile pattern.
            self.app.show_info_popup("theme_restart_title", "theme_restart_required")
            self.update_ui_text_and_fonts() # Update current screen colors

    def save_and_exit(self, instance):
        save_config(self.app.config)
        self.manager.current = 'settings_menu'

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
        self.password_label.text = self.app.ms(self.app.t("change_password"))
        self.set_pass_btn.text = self.app.ms(self.app.t("set_change"))
        self.remove_pass_btn.text = self.app.ms(self.app.t("remove"))
        self.back_button.text = self.app.ms(self.app.t("back_to_settings"))
        self.pass_input1.hint_text = self.app.ms(self.app.t("new_password"))
        self.pass_input2.hint_text = self.app.ms(self.app.t("confirm_password"))
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
        if 'password_hash' not in self.app.config:
            self.app.show_info_popup("main_menu", "password_removed")
            return

        font = self.app.get_font()
        content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        info_label = Label(text=self.app.ms(self.app.t("enter_current_password")), font_name=font)
        content.add_widget(info_label)

        pass_input1 = TextInput(multiline=False, size_hint_y=None, height=40, password=True, font_name=font,
                                hint_text=self.app.ms(self.app.t("enter_current_password")),
                                base_direction='rtl' if self.app.is_farsi_mode() else 'ltr')
        pass_input2 = TextInput(multiline=False, size_hint_y=None, height=40, password=True, font_name=font,
                                hint_text=self.app.ms(self.app.t("confirm_password")),
                                base_direction='rtl' if self.app.is_farsi_mode() else 'ltr')
        content.add_widget(pass_input1); content.add_widget(pass_input2)

        buttons_layout = BoxLayout(size_hint_y=None, height=40, spacing=10)
        confirm_btn = Button(text=self.app.ms(self.app.t("confirm_removal")), font_name=font)
        cancel_btn = Button(text=self.app.ms(self.app.t("cancel")), font_name=font)
        buttons_layout.add_widget(confirm_btn); buttons_layout.add_widget(cancel_btn)
        content.add_widget(buttons_layout)

        popup = Popup(title=self.app.ms(self.app.t("remove")),
                      content=content,
                      size_hint=(None, None),
                      size=(450, 300),
                      title_font=font)

        def _confirm_action(instance):
            p1 = pass_input1.text; p2 = pass_input2.text
            popup.dismiss()
            if not p1 or not p2: self.app.show_info_popup("error", "passwords_empty"); return
            if p1 != p2: self.app.show_info_popup("error", "passwords_not_match"); return
            
            salt = self.app.config.get('password_salt', '')
            password_hash = self.app.config.get('password_hash', '')
            if hash_password(p1, salt) == password_hash:
                if 'password_hash' in self.app.config: del self.app.config['password_hash']
                if 'password_salt' in self.app.config: del self.app.config['password_salt']
                save_config(self.app.config)
                self.app.show_info_popup("main_menu", "password_removed")
            else:
                self.app.show_info_popup("error", "incorrect_password")

        confirm_btn.bind(on_press=_confirm_action)
        cancel_btn.bind(on_press=popup.dismiss)
        popup.open()


if __name__ == '__main__':
    DataPlotterApp().run()