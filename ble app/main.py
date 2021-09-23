from kivy_garden.mapview import MapView, MapMarker
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.app import App
from kivy.properties import ObjectProperty
from threading import Thread
from time import time
from ble import BLE


#classes for changing styles of elements
class RoundedButton(Button):
    pass


class RoundedLabel(Label):
    pass


class WhiteScreen(Screen):
    pass


class ConnectWindow(WhiteScreen):
    connecting_label = ObjectProperty(None)
    connecting_button = ObjectProperty(None)
    splitter = ObjectProperty(None)
    connected = 0

    def btn(self):
        if self.connected == 0:
            print("Started connecting")
            self.splitter.visible = False
            self.connecting_label.height = "45dp"
            self.connecting_label.text = "Connecting"
            Thread(target=self.connect, args={}).start()
        elif self.connected == 1:
            print("Menu screen")

    def connect(self):
        i = 0
        t = time()
        max_retries = 10
        while self.connected == 2 or self.connected == 0:
            self.connected = 2
            if time() - t > 1:
                self.connecting_label.text = f"{self.connecting_label.text}."
                t = time()
                i += 1
            if i == max_retries:
                self.connected = 1
        if self.connected:
            self.connecting_label.text = "Connected!"
            self.connecting_button.text = "Menu"


class MenuWindow(WhiteScreen):
    pass


class MapWindow(WhiteScreen):
    pass


class DeployTimeWindow(WhiteScreen):
    time_label = ObjectProperty(None)
    hour = 0
    minutes = 0
    seconds = 0

    def update_time_label(self):
        time_text = ""
        if self.hour < 10:
            time_text += "0"
        time_text += str(self.hour)
        time_text += ":"
        if self.minutes < 10:
            time_text += "0"
        time_text += str(self.minutes)
        time_text += ":"
        if self.seconds < 10:
            time_text += "0"
        time_text += str(self.seconds)
        self.time_label.text = time_text

    def hour_inc(self):
        self.hour += 1
        self.update_time_label()

    def hour_dec(self):
        if self.hour > 0:
            self.hour -= 1
            self.update_time_label()
            return True
        return False

    def min_inc(self):
        if self.minutes == 59:
            self.minutes = 0
            self.hour_inc()
        else:
            self.minutes += 1
        self.update_time_label()

    def min_dec(self):
        if self.minutes > 0:
            self.minutes -= 1
            self.update_time_label()
            return True
        elif self.hour_dec():
            self.minutes = 59
            self.update_time_label()
            return True
        return False

    def sec_inc(self):
        if self.seconds == 59:
            self.seconds = 0
            self.min_inc()
        else:
            self.seconds += 1
        self.update_time_label()

    def sec_dec(self):
        if self.seconds > 0:
            self.seconds -= 1
        elif self.min_dec():
            self.seconds = 59
        self.update_time_label()


    

class WindowManager(ScreenManager):
    pass


kv = Builder.load_file("main.kv")


class MapViewApp(App):
    def build(self):
        return kv


if __name__ == '__main__':
    MapViewApp().run()