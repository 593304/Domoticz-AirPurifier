# Domoticz-AirPurifier
The Xiaomi Air Purifier devices are providing multiple useful values such as
   - temperature and humidity
   - air quality index
   - filter usage (life passed and hours used)
   - power state, speed, etc.
   
Based on these values it is possible to create multiple devices in Domoticz to monitor your device's and room's status

## Prerequisites
### miio library
This module is using [rytilahti's python-miio library](https://github.com/rytilahti/python-miio). Please follow their guide on how to install the miio library and get the IP address and token of an air purifier device.  
If you are done with the installation, then get the IP address and token of your device and write them down.

### Domoticz setup
First, you have to create a new Dummy hardware, of course you can use an existing one. To create a new Dummy hardware open your Domoticz homepage and go to SETUP > HARDWARE.  
Give it a name and from Type dropdown choose the Dummy one, then add it.

Second step is to create the necessary virtual devices. At this point only 4 different virtual devices are supported:
   - Temperute + humidity sensor (Domoticz sensor type: Temp+Hum)
   - Custom sensor for the air quality index in mcg/m3 (Domoticz sensor type: Custom Sensor)
   - Custom sensor for filter's life passed value in percentage (Domoticz sensor type: Custom Sensor)
   - Custom sensor for filter usage in hours (Domoticz sensor type: Custom Sensor)

If you don't need one or more of these, then skip the creation of them. E.g.: If you only interested in the air quality index, then create only the custom sensor for it.  
On the Domoticz webpage go to SETUP > HARDWARE and find the newly created or the already existing Dummy hardware and click on the CREATE VIRTUAL SENSORS link.  
Add a name for your virtual sensor and select the correct sensor type for it, please check the list above for the correct sensor type. For the custom sensors you have to set the axis label, it can be anything, e.g. the unit of the value.

If you added every virtual device, then go to the Devices page under SETUP > DEVICES and write down the IDX values for each virtual sensor.

Now you should have at least one IP address with a token and one or more IDX value for the virtual device(s).

## Installation
Connect to your Domoticz server via SSH and go to domoticz's plugins directory. Clone this repository into the plugins directory:  
`git clone https://github.com/593304/Domoticz-AirPurifier.git`

## Configuration
Now you have to edit the domoticz_air-purifier-2h.py script file. You will find everything in the first few lines.  
If you are using authentication, then add the username and password for the `DOMOTICZ_USER` and `DOMOTICZ_USER` variables.  
At the `AIR_PURIFIERS` array you need to set the IP address, token and the IDX values.  
   - IDX_TH: None or the IDX of you Temp+Hum virtual sensor
   - IDX_CS_AQI: None or the IDX of your air quality index virtual sensor
   - IDX_CS_Life: None or the IDX of your filter's life passed virtual sensor
   - IDX_CS_Hours: None or the IDX of your filter usage in hours virtual sensor

You can have multiple air purifier device by adding new dictionary objects to the array.

## Scheduling
You can run this script in every minute to get up-to-date values on your Domoticz dashboard.  
Connect to your server via SSH and type this command:  
`sudo crontab -e`  
Add a new line at the bottom of the file:  
`* * * * * /usr/bin/python3 /home/pi/domoticz/plugins/Domoticz-AirPurifier/domoticz_air-purifier-2h.py >/dev/null 2>&1`  
Change the path of you Domoticz' plugins directory if necessary.
