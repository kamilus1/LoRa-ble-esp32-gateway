# APP DEPENDENCIES
To compile the app on your side you need to install few dependencies:
1.  Install `python 3.8` https://www.python.org/downloads/
2.  Install `pip` https://phoenixnap.com/kb/install-pip-windows
3.  Install few `python` dependencies with `pip install`:
	- install kivy https://kivy.org/doc/stable/gettingstarted/installation.html
	- install kivy garden with pip via command line: `pip install kivy-garden`
	- install kivy mapview with pip via command line: `pip install mapview`
	- install python-for-android with pip via command line: `pip install python-for-android`

# ESP32 DEPENDENCIES

You can flash both node and gateway via platformio or ArduinoIDE version of project.
Before you do that, you need to install few ESP32 libraries:
- Both:
	- ArduinoJson
	- LoRa
	
- Node:
	- TinyGPS++

# APP BUILD
To build app first you should go to app directory where main.py is (via command line) and  you should use `buildozer` tool. Tutorial and documentation for installing and building app with `buildozer` can be found here https://buildozer.readthedocs.io/en/latest/installation.html#. 
`buildozer` can only run on Linux or MacOS device. If you are running Windows i suggest to create a Virtual Machine with Ubuntu for that process. 
In **Quickstart** section of tutorial after passing `buildozer init` command you should edit *buildozer.spec* file which you have created with previous command. 
Lines to add/edit:
- `requirements = python3,kivy,android,able_recipe,requests,concurrent.futures,openssl`
- `android.permissions = BLUETOOTH, BLUETOOTH_ADMIN, ACCESS_FINE_LOCATION`
- `p4a.local_recipes = /path/to/ble app/recipes/`
- `garden_requirements = mapview`
 - You should also edit `package.name =` line and
`package.domain =`line. If you want to change other  *buildozer.spec* settings refer to https://buildozer.readthedocs.io/en/latest/specifications.html site. 

After changing the *buildozer.spec* file follow rest of tutorial in **Quickstart** section. App now has pretty simple view(i didnt have any graphics to use). You can connect to gateway via it and read data from gateway/node, track node on map and also send new timer to it. To add tracking of few nodes the source code of node needs to change more from previous version. Every node should have hardcoded or configured via other way unique ID which will send in message. Possible change in further app versions. 

# Starting ESP32

After flashing code to both node and gateway, connecting hardware modules/cables and starting them, gateway should automatically get data from node. After getting data from node gateway set this data in BLE characteristics. Gateway can be found and connected via created mobile app or you can use external android app for testing like f.e: *BLE Scanner*.
Gateway name is set for: **ESP32 LoRa Gateway**. You can change that name and other settings (UUID of value charcteristics/service) by changing 
```c
#define SERVICE_UUID "4fafc201-1fb5-459e-8fcc-c5c9c331914b"
#define DEVICE_NAME "ESP32 LoRa Gateway"
```
in `main.hpp` and 
```c
#define GT_CHARACTERISTIC_UUID "beb5483e-36e1-4688-b7f5-ea07361b26a8"
#define NODE_CHARACTERISTIC_UUID "beb5483f-36e1-4688-b7f5-ea07361b26a8"
#define TIME_CHARACTERISTIC_UUID "beb54840-36e1-4688-b7f5-ea07361b26a8"
#define NEW_TIME_CHARACTERISTIC_UUID "beb54841-36e1-4688-b7f5-ea07361b26a8"
#define GPS_CHARACTERISTIC_UUID "beb54842-36e1-4688-b7f5-ea07361b26a8"
#define BATTERY_CHARACTERISTIC_UUID "beb54843-36e1-4688-b7f5-ea07361b26a8"
```
in `ble_callbacks.hpp` files.  
For debugging possible errors and listening to devices you can look in Serial monitor of gateway and/or node. Every message get from LoRa etc is printed to Serial port. 


