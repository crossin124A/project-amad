from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.clock import Clock
from datetime import datetime
import time
import pygame  # Importing pygame for audio playback


class AlarmApp(App):
    def build(self):
        self.alarm_time = None
        self.stopwatch_running = False
        self.start_time = time.time()
        self.stopwatch_time = 0

        self.layout = BoxLayout(orientation='vertical')

        # Saat Label
        self.time_label = Label(text='Saat: ', font_size='20sp')
        self.layout.add_widget(self.time_label)

        # Kronometre Label
        self.stopwatch_label = Label(text='Kronometre: 00:00:00', font_size='20sp')
        self.layout.add_widget(self.stopwatch_label)

        # Alarm Zamanı Input
        self.alarm_input = TextInput(hint_text='Alarm saati (HH:MM:SS)', multiline=False, font_size='20sp')
        self.layout.add_widget(self.alarm_input)

        # Alarm Ayarla Butonu
        self.set_alarm_button = Button(text='Alarmı Ayarla', on_press=self.set_alarm)
        self.layout.add_widget(self.set_alarm_button)

        # Kronometre Kontrol Butonları
        self.start_button = Button(text='Başlat', on_press=self.start_stopwatch)
        self.layout.add_widget(self.start_button)

        self.stop_button = Button(text='Durdur', on_press=self.stop_stopwatch)
        self.layout.add_widget(self.stop_button)

        self.reset_button = Button(text='Sıfırla', on_press=self.reset_stopwatch)
        self.layout.add_widget(self.reset_button)

        # Çıkış Butonu
        self.exit_button = Button(text='Çıkış', on_press=self.stop)
        self.layout.add_widget(self.exit_button)

        # Pygame için başlangıç
        pygame.mixer.init()

        Clock.schedule_interval(self.update_time, 1)
        Clock.schedule_interval(self.update_stopwatch, 1)

        return self.layout

    def update_time(self, dt):
        now = datetime.now().strftime('%H:%M:%S')
        self.time_label.text = f'Saat: {now}'
        if self.alarm_time == now:
            self.trigger_alarm()

    def update_stopwatch(self, dt):
        if self.stopwatch_running:
            elapsed = int(time.time() - self.start_time + self.stopwatch_time)
            hours, remainder = divmod(elapsed, 3600)
            minutes, seconds = divmod(remainder, 60)
            self.stopwatch_label.text = f'Kronometre: {hours:02}:{minutes:02}:{seconds:02}'

    def set_alarm(self, instance):
        self.alarm_time = self.alarm_input.text
        print(f'Alarm saati ayarlandı: {self.alarm_time}')

    def trigger_alarm(self):
        # Ses dosyasını çal
        pygame.mixer.music.load('alarm.wav')  # Ses dosyasını yükle
        pygame.mixer.music.play()  # Ses dosyasını çal
        # Mesaj
        print('Alarm! Zaman geldi!')

    def start_stopwatch(self, instance):
        if not self.stopwatch_running:
            self.start_time = time.time() - self.stopwatch_time
            self.stopwatch_running = True

    def stop_stopwatch(self, instance):
        if self.stopwatch_running:
            self.stopwatch_time = int(time.time() - self.start_time)
            self.stopwatch_running = False

    def reset_stopwatch(self, instance):
        self.start_time = time.time()
        self.stopwatch_time = 0
        self.stopwatch_label.text = 'Kronometre: 00:00:00'


if __name__ == '__main__':
    AlarmApp().run()
