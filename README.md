# Domoticz-AirPurifier
Xiaomi Airpurifier 2H Plugin for Domoticz.

## Prerequisites
### python-miio library
This module is using [rytilahti's python-miio library](https://github.com/rytilahti/python-miio). Install this module by running this command: `pip3 install python-miio`.  
### Airpurifier token
If you do not have token for your airpurifier device, then please follow the [Getting started documentation](https://python-miio.readthedocs.io/en/latest/discovery.html) of the python-miio library to obtain the token.

## Installation
Connect to your Domoticz server via SSH and go to Domoticz's plugins directory. Clone this repository into the plugins directory:  
`git clone https://github.com/593304/Domoticz-AirPurifier.git`  
If necessary modify the access permissions for the plugin. For example:  
`chmod -R 777 Domoticz-AirPurifier/`  
Then restart Domoticz service to add the Xiaomi Airpurifier 2H plugin to the hardware list in Domoticz.
```
sudo /etc/init.d/domoticz.sh stop
sudo /etc/init.d/domoticz.sh start
```
OR  
```
sudo service domoticz.sh stop
sudo service domoticz.sh start
```

## Configuration
If Domoticz started, then go to the Hardware page on your Domoticz website and add a new one. You should find the Xiaomi Airpurifier 2H Plugin in the Type list. Select it and set the following values:
   - IP (IP address of your airpurifier device)
   - Token (token for the airpurifier device)
   - Debug (you can turn on or off debug messages)
   - Refresh interval
