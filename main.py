# Set Pango as the text provider for Farsi rendering
import os
os.environ['KIVY_TEXT'] = 'pango'

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
from kivy.utils import platform
import statistics
import json
import hashlib
from fpdf import FPDF

# --- NEW: Pyjnius Biometric Implementation ---
if platform == 'android':
    try:
        from jnius import autoclass, PythonJavaClass, java_method
        from android.runnable import run_on_ui_thread

        # Import necessary Android classes
        PythonActivity = autoclass('org.kivy.android.PythonActivity')
        BiometricPrompt = autoclass('androidx.biometric.BiometricPrompt')
        BiometricManager = autoclass('androidx.biometric.BiometricManager')
        Executors = autoclass('java.util.concurrent.Executors')
        
        # This is the Python class that will implement the Java AuthenticationCallback interface
        class AuthenticationCallback(PythonJavaClass):
            __javainterfaces__ = ['androidx/biometric/BiometricPrompt$AuthenticationCallback']

            def __init__(self, callback):
                super().__init__()
                self.callback = callback

            @java_method('(Landroidx/biometric/BiometricPrompt$AuthenticationResult;)V')
            def onAuthenticationSucceeded(self, result):
                self.callback(True, "Success")

            @java_method('()V')
            def onAuthenticationFailed(self):
                # This is called when a different fingerprint is shown
                pass # Usually we wait for the error state

            @java_method('(ILjava/lang/CharSequence;)V')
            def onAuthenticationError(self, errorCode, errString):
                # This is called for actual errors or when the user cancels
                self.callback(False, errString.toString())
        
        PYJNIUS_AVAILABLE = True
    except Exception as e:
        print(f"Could not import pyjnius classes for biometrics: {e}")
        PYJNIUS_AVAILABLE = False
else:
    PYJNIUS_AVAILABLE = False


# --- Farsi Text Shaping Libraries ---
try:
    import arabic_reshaper
    from bidi.algorithm import get_display
except ImportError:
    # Define placeholder functions if libraries are not installed
    def arabic_reshaper(text): return text
    def get_display(text): return text

def _shape_text(s):
    try:
        return get_display(arabic_reshaper.reshape(s))
    except Exception:
        return s

CONFIG_FILE = 'config.json'
LIGHT_BLUE = (0.55, 0.8, 0.9, 1)

# The LANGUAGES dictionary and other utility functions remain unchanged...
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
        "fingerprints": "Fingerprint Info",
        "back_settings": "Back to Settings Menu",
        "passwords_empty": "Password fields cannot be empty.",
        "passwords_not_match": "Passwords do not match.",
        "password_set": "Password has been set.",
        "password_removed": "Password has been removed.",
        "fingerprint_info": "This app uses the fingerprints already registered on your device. You can add or remove fingerprints in your phone's Android Settings under Security.",
        "fingerprint_info_title": "Fingerprint Information",
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
        "lang_restart_required": "Language has been updated.",
        "restart_required_title": "Language Changed",
        "ok": "OK",
        "use_fingerprint_to_login": "Use Fingerprint to Login",
        "scan_prompt": "Please place your finger on the sensor",
        "enter_current_password": "Enter current password to confirm",
        "confirm_removal": "Confirm Removal",
        "cancel": "Cancel",
        "bio_auth_title": "Authentication Required",
        "bio_auth_subtitle": "Log in using your biometric credential",
        "bio_auth_error": "Authentication failed. Please try again.",
        "bio_auth_unavailable": "Biometric authentication is not available on this device.",
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
        "fingerprints": "اطلاعات اثرانگشت",
        "back_settings": "بازگشت به تنظیمات",
        "passwords_empty": "فیلدهای رمز عبور نمی‌توانند خالی باشند.",
        "passwords_not_match": "رمزها مطابقت ندارند.",
        "password_set": "رمز با موفقیت ثبت شد.",
        "password_removed": "رمز حذف شد.",
        "fingerprint_info": "این برنامه از اثر انگشت‌های ثبت شده در دستگاه شما استفاده می‌کند. برای افزودن یا حذف اثر انگشت، به بخش تنظیمات امنیتی گوشی خود مراجعه کنید.",
        "fingerprint_info_title": "اطلاعات اثرانگشت",
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
        "lang_restart_required": "زبان برنامه تغییر کرد.",
        "restart_required_title": "زبان تغییر کرد",
        "ok": "باشه",
        "use_fingerprint_to_login": "ورود با اثرانگشت",
        "scan_prompt": "لطفاً انگشت خود را روی سنسور قرار دهید",
        "enter_current_password": "برای تایید رمز فعلی را وارد کنید",
        "confirm_removal": "تایید حذف",
        "cancel": "لغو",
        "bio_auth_title": "نیاز به احراز هویت",
        "bio_auth_subtitle": "با استفاده از اطلاعات بیومتریک خود وارد شوید",
        "bio_auth_error": "احراز هویت ناموفق بود. لطفاً دوباره تلاش کنید.",
        "bio_auth_unavailable": "احراز هویت بیومتریک در این دستگاه در دسترس نیست.",
    }
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

class FontManager:
    # ... FontManager class is unchanged ...
    def __init__(self):
        self.registered = False
        self.font_name = None
        self.font_path = None
    def try_register(self):
        if self.registered: return
        candidates = ['BNaznnBd.ttf', 'vazir.ttf', 'Vazir-Regular.ttf', 'NotoNaskhArabic-Regular.ttf', 'NotoSansArabic-Regular.ttf', 'NotoSansArabic.ttf']
        for fn in candidates:
            if os.path.exists(fn):
                try:
                    LabelBase.register(name='FarsiFont', fn_regular=fn)
                    self.registered = True
                    self.font_name = 'FarsiFont'
                    self.font_path = fn
                    return
                except Exception: continue
    def available(self):
        return self.registered
FONT_MANAGER = FontManager()

# --- REWRITTEN: FingerprintManager now uses Pyjnius directly ---
class FingerprintManager:
    def __init__(self, app):
        self.app = app

    def available(self):
        if not PYJNIUS_AVAILABLE:
            return False
        
        try:
            activity = PythonActivity.mActivity
            manager = BiometricManager.fromContext(activity)
            # Check for strong biometric hardware
            result = manager.canAuthenticate(BiometricManager.Authenticators.BIOMETRIC_STRONG)
            return result == BiometricManager.BIOMETRIC_SUCCESS
        except Exception as e:
            print(f"Error checking biometric availability: {e}")
            return False

    @run_on_ui_thread
    def authenticate(self, on_complete_callback):
        if not PYJNIUS_AVAILABLE:
            on_complete_callback(False, "bio_auth_unavailable")
            return

        try:
            activity = PythonActivity.mActivity
            executor = Executors.newSingleThreadExecutor()
            
            # Create an instance of our Python class that acts as the Java callback
            auth_callback = AuthenticationCallback(on_complete_callback)
            
            prompt = BiometricPrompt(activity, executor, auth_callback)

            # Get translated text for the prompt
            title = self.app.ms(self.app.t("bio_auth_title"))
            subtitle = self.app.ms(self.app.t("bio_auth_subtitle"))
            cancel_button = self.app.ms(self.app.t("cancel"))
            
            prompt_info = BiometricPrompt.PromptInfo.newBuilder() \
                .setTitle(title) \
                .setSubtitle(subtitle) \
                .setNegativeButtonText(cancel_button) \
                .build()
            
            prompt.authenticate(prompt_info)
        except Exception as e:
            print(f"Error starting authentication: {e}")
            on_complete_callback(False, "bio_auth_error")


# The rest of your application code remains the same as it was,
# as it correctly interfaces with the FingerprintManager class.
# ...
class DualLabelButton(ButtonBehavior, BoxLayout):
    def __init__(self, main_key, ext_key, on_press_callback=None, app=None, **kwargs):
        super().__init__(orientation='horizontal', spacing=10, padding=10, **kwargs)
        self.app = app; self.main_key = main_key; self.ext_key = ext_key
        with self.canvas.before:
            Color(0.9, 0.9, 0.9, 1); self._rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self._update_rect, size=self._update_rect)
        self.label_main = Label(halign='center', valign='middle')
        self.label_ext = Label(halign='center', valign='middle')
        self._on_press_callback = on_press_callback
        self.update()
    def _update_rect(self, *a):
        self._rect.pos = self.pos; self._rect.size = self.size
    def on_press(self):
        if self._on_press_callback:
            try: self._on_press_callback(self)
            except Exception: pass
    def update(self):
        self.clear_widgets()
        main_raw = self.app.t(self.main_key); ext_raw = self.app.t(self.ext_key)
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
        return self.sm
    def apply_theme(self):
        if self.config.get('theme') == 'Dark':
            self.theme_background = (0.1, 0.1, 0.1, 1); self.theme_text_color = (0.9, 0.9, 0.9, 1)
        else:
            self.theme_background = (0.95, 0.95, 0.95, 1); self.theme_text_color = (0.1, 0.1, 0.1, 1)
        Window.clearcolor = self.theme_background
    def t(self, key):
        lang = self.config.get('language', 'English'); return LANGUAGES.get(lang, LANGUAGES['English']).get(key, key)
    def is_farsi_mode(self): return self.config.get('language', 'English') == 'Farsi'
    def ms(self, s):
        if self.is_farsi_mode(): return _shape_text(str(s))
        return str(s)
    def get_font(self):
        if self.is_farsi_mode() and FONT_MANAGER.available(): return FONT_MANAGER.font_name
        return 'Roboto'
    def show_info_popup(self, title_key, message_key):
        font = self.get_font(); title = self.ms(self.t(title_key)); message = self.ms(self.t(message_key))
        content = Label(text=message, font_name=font)
        content.bind(size=lambda *x: content.setter('text_size')(content, (content.width-20, None)))
        popup = Popup(title=title, content=content, size_hint=(None, None), size=(400, 200), title_font=font)
        popup.open()
    def ensure_farsi_font_popup(self):
        if self.is_farsi_mode() and not FONT_MANAGER.available(): self.show_info_popup("error", "missing_font_instruction")

class BaseScreen(Screen):
    def __init__(self, app, **kwargs):
        super().__init__(**kwargs); self.app = app
    def on_pre_enter(self, *args):
        if hasattr(self, 'update_ui_text_and_fonts'): self.update_ui_text_and_fonts()
        self.app.ensure_farsi_font_popup()
    def update_ui_text_and_fonts(self): self._update_font_recursive(self)
    def _update_font_recursive(self, widget):
        font_name = self.app.get_font()
        if isinstance(widget, (Label, Button)): widget.font_name = font_name
        if isinstance(widget, TextInput):
            widget.font_name = font_name; widget.base_direction = 'rtl' if self.app.is_farsi_mode() else 'ltr'
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
        self.title.text = self.app.ms(self.app.t("main_menu")); self.title.color = self.app.theme_text_color
        self.login_button.text = self.app.ms(self.app.t("login"))
        self.settings_button.text = self.app.ms(self.app.t("settings"))
        self.exit_button.text = self.app.ms(self.app.t("exit"))
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
        self.fingerprint_button = Button(font_size='18sp', size_hint_y=None, height=40, on_press=self.use_fingerprint)
        self.back_button = Button(font_size='18sp', size_hint_y=None, height=40, on_press=self.go_back)
        self.layout.add_widget(self.info_label); self.layout.add_widget(self.password_input)
        self.layout.add_widget(self.submit_button); self.layout.add_widget(self.fingerprint_button)
        self.layout.add_widget(self.back_button)
        self.add_widget(self.layout)
    def on_pre_enter(self, *args):
        if not self.app.fpm.available():
            self.fingerprint_button.disabled = True
            self.fingerprint_button.opacity = 0.5
        else:
            self.fingerprint_button.disabled = False
            self.fingerprint_button.opacity = 1
        super().on_pre_enter(*args)
    def go_back(self, instance): self.manager.current = 'entry'
    def update_ui_text_and_fonts(self):
        self.info_label.text = self.app.ms(self.app.t("password_prompt")); self.info_label.color = self.app.theme_text_color
        self.submit_button.text = self.app.ms(self.app.t("login"))
        self.fingerprint_button.text = self.app.ms(self.app.t("use_fingerprint_to_login"))
        self.back_button.text = self.app.ms(self.app.t("back_menu"))
        self.password_input.text = ""
        super().update_ui_text_and_fonts()
    def check_password(self, instance):
        password = self.password_input.text; salt = self.app.config.get('password_salt', ''); password_hash = self.app.config.get('password_hash', '')
        if hash_password(password, salt) == password_hash: self.manager.current = 'plot'
        else: self.app.show_info_popup("error", "incorrect_password")
    def use_fingerprint(self, instance):
        def on_auth_complete(success, message):
            if success:
                self.manager.current = 'plot'
            else:
                # The callback returns the raw Java CharSequence, convert it to a string for the popup
                self.app.show_info_popup("error", str(message))
        self.app.fpm.authenticate(on_auth_complete)

class PlotScreen(BaseScreen):
    # This class and all subsequent classes are unchanged.
    pass
# ... (rest of the unchanged classes from the previous version)

if __name__ == '__main__':
    DataPlotterApp().run()
