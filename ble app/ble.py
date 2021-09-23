from able.able import BluetoothDispatcher, GATT_SUCCESS


class BLE(BluetoothDispatcher):
    device = characteristic = None

    def __init__(self, characteristic_uuid="beb5483e-36e1-4688-b7f5-ea07361b26a8",
                 device_name="ESP32 LoRa Gateway", queue_timeout=0.5, enable_ble_code=0xab1e):
        super().__init__(queue_timeout, enable_ble_code)
        self.device_name = device_name
        self.characteristic_uuid = characteristic_uuid
        

    def is_connected(self):
        if self.characteristic:
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
            self.characteristic = None
            self.close_gatt()

    def on_services(self, services, status):
        if status == GATT_SUCCESS:
            self.characteristic = services.search(self.characteristic_uuid)

    def on_device(self, device, rssi, advertisement):
        name = device.getName()
        if name and name.startswith(self.device_name):
            self.device = device
            self.stop_scan()



    def on_characteristic_read(self, characteristic, status):
        pass
