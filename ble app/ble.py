from able import BluetoothDispatcher, GATT_SUCCESS
from time import time, sleep


class BLE(BluetoothDispatcher):
    device = characteristic = None
    rssi = 0

    def __init__(self, characteristics_uuid=None,
                 device_name="ESP32 LoRa Gateway", queue_timeout=0.5, enable_ble_code=0xab1e):
        super().__init__(queue_timeout, enable_ble_code)
        self.device_name = device_name
        self.curr_uid = "GPS"
        if not characteristics_uuid:
            self.characteristic_uuid = {"GT": "483e",
                                        "NODE": "483f",
                                        "TIME": "4840",
                                        "NEW_TIME": "4841",
                                        "GPS": "4842",
                                        "BATTERY": "4843"
                                        }

    def get_gateway_data(self):
        rssi = self.get_rssi()
        connected = "False"
        if self.is_connected():
            connected = "True"
        gt_ts = "No data"
        if self.get_characteristic("GT"):
            i = 0
            value = None
            while i < 10:
                value = self.get_characteristic_value()
                if value:
                    break
                i += 1
                sleep(1)
            if value:
                gt_ts = value
        return {"name": self.device_name, "rssi": rssi, "connected": connected, "gateway timer": gt_ts}

    def get_node_data(self):
        node_data = {"gps": "No data", "battery": "No data", "node timer": "No data"}
        if self.get_characteristic("GPS"):
            i = 0
            value = None
            while i < 10:
                    value = self.get_characteristic_value()
                    if value:
                        break
                    i += 1
                    sleep(1)
            if value:
                node_data["gps"] = value
        if self.get_characteristic("BATTERY"):
            i = 0
            value = None
            while i < 10:
                    value = self.get_characteristic_value()
                    if value:
                        break
                    i += 1
                    sleep(1)
            if value:
                node_data["battery"] = value
        if self.get_characteristic("NODE"):
            i = 0
            value = None
            while i < 10:
                    value = self.get_characteristic_value()
                    if value:
                        break
                    i += 1
                    sleep(1)
            if value:
                node_data["node timer"] = value
        return node_data

    def on_rssi_updated(self, rssi, status):
        if status == GATT_SUCCESS:
            self.rssi = rssi

    def get_rssi(self):
        return self.rssi

    def is_connected(self):
        if self.device:
            return True
        else:
            return False

    def on_scan_completed(self):
        if self.device:
            self.connect_gatt(self.device)

    def on_connection_state_change(self, status, state):
        if status == GATT_SUCCESS and state:
            self.discover_services()
        else:
            self.device = None
            self.characteristic = None
            self.close_gatt()

    def on_services(self, services, status):
        if status == GATT_SUCCESS:
            self.characteristic = services.search(self.characteristic_uuid[self.curr_uid])
            self.read_characteristic(self.characteristic)

    def on_device(self, device, rssi, advertisement):
        name = device.getName()
        if name and name.startswith(self.device_name):
            self.device = device
            self.stop_scan()

    def get_characteristic(self, curr_uid):
        self.curr_uid = curr_uid
        self.characteristic = None
        t = 0
        i = 0
        while not self.device and i < 10:
                self.stop_scan()
                self.start_scan()
                i += 1
                sleep(3)
        if not self.device:
            return False
        i = 0
        t = 0
        while not self.characteristic and i < 10:
                i += 1
                self.discover_services()
                sleep(3)
        if self.characteristic:
            return True
        else:
            return False

    def on_characteristic_read(self, characteristic, status):
        if status == GATT_SUCCESS:
            print(self.characteristic.getStringValue(0))

    def get_characteristic_value(self):
        if self.characteristic:
            self.read_characteristic(self.characteristic)
            print(self.characteristic.getStringValue(0))
            return self.characteristic.getStringValue(0)
        else:
            return None

    def set_characteristic_value(self, value):
        t = 0
        i = 0
        while not self.device and i < 10:
            if time() - t > 5:
                t = time()
                self.stop_scan()
                self.start_scan()
                i += 1
        if not self.device:
            return False
        i = 0
        while not self.characteristic and i < 10:
                i += 1
                self.discover_services()
                sleep(3)

        if self.characteristic:
            s = str(value)
            s_array = []
            for i in s:
                s_array.append(i)
            self.write_characteristic(self.characteristic, s_array)
            return True

        return False


