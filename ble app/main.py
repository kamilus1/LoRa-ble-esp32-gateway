from kivy_garden.mapview import MapMarker
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.app import App
from kivy.properties import ObjectProperty
from threading import Thread
from time import time
from ble import BLE
from kivy.clock import mainthread
from time import sleep
__version__ = "1.0.3"

android_device = True
new_time = 0
connected = 0
gateway_data = {"name": "No data", "rssi": "No data", "connected": "False", "gateway timer": "No data"}
node_data = {"gps": "No data", "battery": "No data", "node timer": "No data"}


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
    connected = False

    def btn(self):
        global connected
        if connected == 0 or connected == 3:
            print("Started connecting")
            self.splitter.visible = False
            self.connecting_label.height = "45dp"
            self.connecting_label.text = "Connecting"
            Thread(target=self.connect, args={}).start()
        elif connected == 1:
            print("Menu screen")

    @mainthread
    def change_connect_label(self, text):
        self.connecting_label.text = text
    @mainthread
    def change_connect_button(self, text):
        self.connecting_button.text = text

    def connect(self):
        i = 0
        t = time()
        global connected
        while connected == 2 or connected == 0:

            self.change_connect_label("%s." % self.connecting_label.text)
            i += 1
            sleep(1.5)
        if connected == 1:
            self.connected = True
            self.change_connect_label("Connected")
            self.change_connect_button("Menu")
        else:
            self.change_connect_label("Cant connect")
            self.change_connect_button("Connect again")


class MenuWindow(WhiteScreen):
    pass


class MapWindow(WhiteScreen):
    map_view = ObjectProperty(None)
    data_update = False

    def start_data_update(self):
        print("map update")
        self.data_update = True
        Thread(target=self.start_data_update_thread, args={}).start()

    @mainthread
    def map_update(self, marker):
        self.map_view.add_marker(marker)

    def start_data_update_thread(self):
        t = 0
        while self.data_update:
                coords = node_data["gps"].split(";")
                print(coords)
                if len(coords) >=2:
                    try:
                        m1 = MapMarker(lat=float(coords[0]), lon=float(coords[1]))
                        self.map_update(m1)
                    except Exception as e:
                        print(type(e), e)
                sleep(10)

    def stop_data_update(self):
        self.data_update = False


class GatewayWindow(WhiteScreen):
    gt_lab = ObjectProperty(None)
    rssi_lab = ObjectProperty(None)
    con_lab = ObjectProperty(None)
    timer_lab = ObjectProperty(None)
    data_update = False

    def start_data_update(self):
        print("gateway update")
        self.data_update = True
        Thread(target=self.start_data_update_thread, args={}).start()

    @mainthread
    def change_labels_text(self, data):
        self.gt_lab.text = data["name"]
        self.rssi_lab.text = data["rssi"]
        self.con_lab.text = data["connected"]
        self.timer_lab.text = data["gateway timer"]

    def start_data_update_thread(self):
        t = 0
        global gateway_data
        while self.data_update:
            self.change_labels_text(gateway_data)
            sleep(5)

    def stop_data_update(self):
        self.data_update = False


class NodeWindow(WhiteScreen):
    gps_lab = ObjectProperty(None)
    node_ts_lab = ObjectProperty(None)
    btr_lab = ObjectProperty(None)
    data_update = False

    def start_data_update(self):
        print("node update")
        self.data_update = True
        Thread(target=self.start_data_update_thread, args={}).start()

    @mainthread
    def change_labels_text(self, data):
        self.node_ts_lab.text = data["node timer"]
        self.gps_lab.text = data["gps"]
        self.btr_lab.text = data["battery"]

    def start_data_update_thread(self):
        t = 0
        global node_data
        while self.data_update:
            self.change_labels_text(node_data)
            sleep(5)

    def stop_data_update(self):
        self.data_update = False


class DeployTimeWindow(WhiteScreen):
    time_label = ObjectProperty(None)
    hour = 0
    minutes = 0
    seconds = 0

    def zero_values(self):
        self.hour = 0
        self.minutes = 0
        self.seconds = 0
        self.update_time_label()

    def update_time_label(self):
        global new_time
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
        new_time = self.hour * 60 * 60 * 1000 + self.minutes * 60 * 1000 + self.seconds * 1000

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
    ble = None
    gateway_screen = node_screen = False

    def build(self):
        if android_device:
            self.ble = BLE()
            print(self.ble)
        return kv

    def btn_connect(self):
        if self.ble:
            Thread(target=self.ble_connection, args={}).start()
        else:
            Thread(target=self.no_ble_connection, args={}).start()

    def no_ble_connection(self):
        i = 0
        t = 0
        global connected
        while i < 5:
            i += 1
            sleep(1)
        connected = 1

    def start_gateway_screen(self):
        if self.ble:
            self.gateway_screen = True
            Thread(target=self.ble_gateway_screen, args={}).start()

    def ble_gateway_screen(self):
        global gateway_data
        while self.gateway_screen:
            gateway_data = self.ble.get_gateway_data()
            sleep(5)

    def start_node_screen(self):
        if self.ble:
            self.node_screen = True
            Thread(target=self.ble_node_screen, args={}).start()


    def ble_node_screen(self):
        global node_data
        while self.node_screen:
            node_data = self.ble.get_node_data()
            sleep(5)

    def stop_gateway_screen(self):
        self.gateway_screen = False

    def stop_node_screen(self):
        self.node_screen = False

    def ble_connection(self):
        t = 0
        i = 0
        global connected
        while not self.ble.is_connected() and i < 10:
            self.ble.stop_scan()
            self.ble.start_scan()
            t = time()
            i += 1
            sleep(5)
        if self.ble.is_connected():
            connected = 1
        else:
            connected = 3

    def send_new_timer(self):
        global new_time
        print(new_time)
        if self.ble:
            Thread(target=self.send_new_timer_thread, args={}).start()

    def send_new_timer_thread(self):
        global new_time
        if self.ble.get_characteristic("NEW_TIME"):
            self.ble.set_characteristic_value(str(new_time))



if __name__ == '__main__':
    MapViewApp().run()