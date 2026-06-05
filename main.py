import datetime
from kivy.config import Config
# ڕێگریکردن لە کێشەی گرافیک پێش هێنانە ناوەوەی کیڤی
Config.set('graphics', 'multisamples', '0')

from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton, MDIconButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.selectioncontrol import MDCheckbox
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.core.audio import SoundLoader
import os

# پێناسەکردنی زمانەکان
TRANSLATIONS = {
    "ku": {
        "title": "Smart Watch Pro",
        "alarm_status": "زەنگ: چالاک نەکراوە",
        "alarm_set": "زەنگ بۆ شەممە کاژمێر ١٠:٠٠ جێگیرکرا!",
        "alarm_fired": "🚨 کاتی ئاگادارکردنەوەیە!",
        "set_btn": "دانانی زەنگ (شەممە ١٠:٠٠)",
        "bg_btn": "باگراوندی داهاتوو",
        "sound_btn": "دەنگی داهاتوو"
    },
    "ar": {
        "title": "Smart Watch Pro",
        "alarm_status": "المنبه: غير نشط",
        "alarm_set": "تم ضبط المنبه ليوم السبت الساعة ١٠:٠٠!",
        "alarm_fired": "🚨 حان الوقت!",
        "set_btn": "ضبط المنبه (السبت ١٠:٠٠)",
        "bg_btn": "الخلفية التالية",
        "sound_btn": "الصوت التالي"
    },
    "en": {
        "title": "Smart Watch Pro",
        "alarm_status": "Alarm: Not Set",
        "alarm_set": "Alarm set for Saturday at 10:00!",
        "alarm_fired": "🚨 Alarm Ringing!",
        "set_btn": "Set Alarm (Sat 10:00)",
        "bg_btn": "Next Background",
        "sound_btn": "Next Sound"
    }
}

DAYS_KU = ["دووشەممە", "سێشەممە", "چوارشەممە", "پێنجشەممە", "هەینی", "شەممە", "یەکشەممە"]
DAYS_AR = ["الإثنين", "الثلاثاء", "الأربعاء", "الخميس", "الجمعة", "السبت", "الأحد"]
DAYS_EN = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

MONTHS_KU = ["کانوونی دووەم", "شوبات", "ئادار", "نیسان", "ئایار", "حوزەیران", "تەممووز", "ئاب", "ئەیلوول", "تشرینی یەکەم", "تشرینی دووەم", "کانوونی یەکەم"]
MONTHS_AR = ["كانون الثاني", "شباط", "آذار", "نيسان", "أيار", "حزيران", "تموز", "آب", "أيلول", "تشرين الأول", "تشرين الثاني", "كانون الأول"]

class SmartWatchProApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "DeepPurple"
        
        # ڕێکخستنی سەرەتایی گۆڕاوەکان
        self.current_lang = "ku"
        self.bg_index = 1
        self.sound_index = 1
        self.alarm_time = None
        self.alarm_day_idx = 5  # شەممە
        self.current_sound = None
        
        screen = MDScreen()
        
        # ١. وێنەی باگراوندی شاهانە (توانای گۆڕینی هەیە بۆ ٢٠ دانە)
        self.bg_image = Image(
            source=f"assets/images/bg{self.bg_index}.jpg",
            allow_stretch=True,
            keep_ratio=False,
            opacity=0.3
        )
        screen.add_widget(self.bg_image)
        
        # ٢. تێکستی جوڵاوی سەرنجڕاکێش لە باگراوند (ibrahim. M)
        self.bg_text = MDLabel(
            text="ibrahim. M",
            font_style="H2",
            halign="center",
            theme_text_color="Custom",
            text_color=[0.6, 0.2, 0.8, 0.15],
            font_size="60sp"
        )
        screen.add_widget(self.bg_text)
        
        # لایوتی سەرەکی بۆ ڕێکخستنی توخمەکان
        main_layout = MDBoxLayout(orientation='vertical', padding="20dp", spacing="15dp")
        
        # بەشی سەرەوە: دوگمەکانی گۆڕینی زمان
        lang_layout = MDBoxLayout(orientation='horizontal', size_hint_y=None, height="50dp", spacing="10dp", pos_hint={"center_x": 0.5})
        lang_layout.add_widget(MDRaisedButton(text="کوردی", on_release=lambda x: self.change_language("ku")))
        lang_layout.add_widget(MDRaisedButton(text="العربية", on_release=lambda x: self.change_language("ar")))
        lang_layout.add_widget(MDRaisedButton(text="English", on_release=lambda x: self.change_language("en")))
        main_layout.add_widget(lang_layout)
        
        # ٣. لایبڵی کاتی دیجیتاڵی (زۆر ورد لە چرکە بچووکتر)
        self.time_label = MDLabel(
            text="00:00:00",
            font_style="H3",
            halign="center",
            size_hint_y=None,
            height="70dp",
            theme_text_color="Primary"
        )
        main_layout.add_widget(self.time_label)
        
        # ٤. لایبڵی ڕێکەوتی سێ زمانی پێکەوە
        self.date_label = MDLabel(
            text="",
            font_style="Body1",
            halign="center",
            theme_text_color="Secondary",
            size_hint_y=None,
            height="90dp"
        )
        main_layout.add_widget(self.date_label)
        
        # ٥. لایبڵی دۆخی زەنگ
        self.alarm_status_label = MDLabel(
            text=TRANSLATIONS[self.current_lang]["alarm_status"],
            font_style="Body2",
            halign="center",
            theme_text_color="Hint",
            size_hint_y=None,
            height="40dp"
        )
        main_layout.add_widget(self.alarm_status_label)
        
        # بەشی کۆنتڕۆڵ و دوگمەکان (گۆڕینی باگراوند، دەنگ، دانانی زەنگ)
        controls_layout = MDGridLayout(cols=1, spacing="10dp", size_hint_y=None, height="180dp")
        
        self.btn_set_alarm = MDRaisedButton(
            text=TRANSLATIONS[self.current_lang]["set_btn"],
            pos_hint={"center_x": 0.5},
            on_release=self.set_alarm_clock
        )
        controls_layout.add_widget(self.btn_set_alarm)
        
        self.btn_change_bg = MDRaisedButton(
            text=f"{TRANSLATIONS[self.current_lang]['bg_btn']} ({self.bg_index}/20)",
            pos_hint={"center_x": 0.5},
            on_release=self.next_background
        )
        controls_layout.add_widget(self.btn_change_bg)
        
        self.btn_change_sound = MDRaisedButton(
            text=f"{TRANSLATIONS[self.current_lang]['sound_btn']} ({self.sound_index}/20)",
            pos_hint={"center_x": 0.5},
            on_release=self.next_sound
        )
        controls_layout.add_widget(self.btn_change_sound)
        
        main_layout.add_widget(controls_layout)
        screen.add_widget(main_layout)
        
        # نوێکردنەوەی بەردەوامی کاتژمێر (هەموو 0.05 چرکەیەک بۆ ئەوپەڕی وردی)
        Clock.schedule_interval(self.update_clock, 0.05)
        self.start_text_animation()
        
        return screen

    def update_clock(self, dt):
        now = datetime.datetime.now()
        # پیشاندانی کات بە چرکەوە
        self.time_label.text = now.strftime("%H:%M:%S")
        
        # دروستکردنی دەقی ڕێکەوتی سێ زمانی پێکەوە
        day_idx = now.weekday()
        month_idx = now.month - 1
        
        ku_date = f"کوردی: {DAYS_KU[day_idx]}، {now.day}ی {MONTHS_KU[month_idx]} {now.year}"
        ar_date = f"العربية: {DAYS_AR[day_idx]}، {now.day} {MONTHS_AR[month_idx]} {now.year}"
        en_date = f"English: {DAYS_EN[day_idx]}, {now.strftime('%B %d, %Y')}"
        
        self.date_label.text = f"{ku_date}\n{ar_date}\n{en_date}"
        
        # پشکنینی کاتی زەنگەکە
        if self.alarm_time:
            if day_idx == self.alarm_day_idx and now.strftime("%H:%M:%S") == self.alarm_time:
                self.fire_alarm()

    def change_language(self, lang):
        self.current_lang = lang
        self.btn_set_alarm.text = TRANSLATIONS[lang]["set_btn"]
        self.btn_change_bg.text = f"{TRANSLATIONS[lang]['bg_btn']} ({self.bg_index}/20)"
        self.btn_change_sound.text = f"{TRANSLATIONS[lang]['sound_btn']} ({self.sound_index}/20)"
        if not self.alarm_time:
            self.alarm_status_label.text = TRANSLATIONS[lang]["alarm_status"]

    def next_background(self, instance):
        # گۆڕینی باگراوند لە نێوان ١ بۆ ٢٠
        self.bg_index = (self.bg_index % 20) + 1
        self.bg_image.source = f"assets/images/bg{self.bg_index}.jpg"
        self.btn_change_bg.text = f"{TRANSLATIONS[self.current_lang]['bg_btn']} ({self.bg_index}/20)"

    def next_sound(self, instance):
        # گۆڕینی دەنگی زەنگەکە لە نێوان ١ بۆ ٢٠
        self.sound_index = (self.sound_index % 20) + 1
        self.btn_change_sound.text = f"{TRANSLATIONS[self.current_lang]['sound_btn']} ({self.sound_index}/20)"
        # تاقیکردنەوەی دەنگە نوێیەکە بۆ چەند چرکەیەک
        sound_path = f"assets/sounds/alarm{self.sound_index}.mp3"
        if os.path.exists(sound_path):
            test_sound = SoundLoader.load(sound_path)
            if test_sound:
                test_sound.play()

    def set_alarm_clock(self, instance):
        self.alarm_time = "10:00:00"
        self.alarm_status_label.text = TRANSLATIONS[self.current_lang]["alarm_set"]
        self.alarm_status_label.theme_text_color = "Primary"

    def fire_alarm(self):
        self.alarm_status_label.text = TRANSLATIONS[self.current_lang]["alarm_fired"]
        sound_path = f"assets/sounds/alarm{self.sound_index}.mp3"
        if os.path.exists(sound_path):
            self.current_sound = SoundLoader.load(sound_path)
            if self.current_sound:
                self.current_sound.play()

    def start_text_animation(self):
        # جوڵەی دەقی سەرنجڕاکێشی باگراوند (ibrahim. M) بۆ ناوەڕاست و گەورەبوون
        anim = Animation(font_size="75sp", text_color=[0.5, 0, 0.7, 0.35], duration=3, t="in_out_sin") + \
               Animation(font_size="55sp", text_color=[0.6, 0.2, 0.8, 0.12], duration=3, t="in_out_sin")
        anim.repeat = True
        anim.start(self.bg_text)

if __name__ == "__main__":
    SmartWatchProApp().run()

