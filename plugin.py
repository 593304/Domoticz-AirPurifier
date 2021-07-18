# Xiaomi Airpurifier 2H Plugin
#
# Author: 593304
#
"""
<plugin key="XiaomiAirpurifier2HPlugin" name="Xiaomi Airpurifier 2H Plugin" author="593304" version="0.5" externallink="https://github.com/593304/Domoticz-AirPurifier">
    <description>
        <h2>Xiaomi Airpurifier 2H Plugin</h2><br/>
        <p>The plugin will connect to a Xiaomi Airpurifier device with the given IP address and token.</p>
        <p>Before using this plugin, you have to install the<a href="https://github.com/rytilahti/python-miio" style="margin-left: 5px">python-miio module</a></p>
        <br />
        <br />
    </description>
    <params>
        <param field="Mode1" label="IP address" width="250px" required="true"/>
        <param field="Password" label="Token" width="250px" required="true" password="true"/>
        <param field="Mode2" label="Debug" width="50px">
            <options>
                <option label="On" value="on"/>
                <option label="Off" value="off" default="off"/>
            </options>
        </param>
        <param field="Mode3" label="Refresh interval" width="100px">
            <options>
                <option label="5" value="5" default="5"/>
                <option label="10" value="10"/>
                <option label="20" value="20"/>
                <option label="30" value="30"/>
                <option label="45" value="45"/>
                <option label="60" value="60"/>
                <option label="90" value="90"/>
                <option label="120" value="120"/>
                <option label="150" value="150"/>
                <option label="180" value="180"/>
            </options>
        </param>
    </params>
</plugin>
"""
import Domoticz
from miio import AirPurifier
from miio.airpurifier import OperationMode
from miio.airpurifier import LedBrightness


# Simple heartbeat with 5-180 secs interval
class Heartbeat():
    def __init__(self, interval):
        self.callback = None
        self.interval = interval
        self.heartbeatRate = 15
        self.heartbeatRoundCounter = 0
        self.heartbeatRound = self.interval / self.heartbeatRate

    def setHeartbeat(self, callback):
        if self.interval > 30:
            Domoticz.Heartbeat(self.heartbeatRate)
        else:
            Domoticz.Heartbeat(self.interval)
        Domoticz.Log("Heartbeat interval is %s seconds" % (str(self.interval)))
        self.callback = callback
            
    def beatHeartbeat(self):
        callbackEnabled = False
        if self.interval > 30:
            self.heartbeatRoundCounter += 1
            if self.heartbeatRoundCounter == int(self.heartbeatRound):
                callbackEnabled = True
                self.heartbeatRoundCounter = 0
        else:
            callbackEnabled = True

        if callbackEnabled:
            self.callback()


class Helper():
    def __init__(self, ip, token):
        self.ap = AirPurifier(ip=ip, token=token)
        self.status = self.ap.status()
        self.units = {}
        self.selectorData = {}
        return
    
    def createDomoticzDevices(self):
        Domoticz.Log("Creating devices in Domoticz")
        name = "Airpurifier"

        unit = 1
        if unit not in Devices:
            Domoticz.Debug("Creating power switch")
            Domoticz.Device(Name="Power", Unit=unit, Image=7, TypeName="Switch").Create()
        else:
            Domoticz.Debug("Power switch already exists with unit ID: %d" % (unit))
        self.units[unit] = {
            "type": "switch",
            "command": self.powerSwitch,
            "currentValue": self.powerSwitchCurrentValue,
            "dependantSwitch": {
                "unit": 2,
                "ifValue": "off",
                "setValue": 10
            }
        }

        unit = 2
        if unit not in Devices:
            Domoticz.Debug("Creating operation selector switch")
            Options = {"LevelActions" : "||||",
                    "LevelNames" : "|Idle|Auto|Silent|Favorite",
                    "LevelOffHidden" : "true",
                    "SelectorStyle" : "1"}
            Domoticz.Device(Name="Operation selector", Unit=unit, Image=7, TypeName="Selector Switch", Options=Options).Create()
        else:
            Domoticz.Debug("Operation selector switch already exists with unit ID: %d" % (unit))
        self.units[unit] = {
            "type": "selector",
            "command": self.operationSelectorSwitch,
            "currentValue": self.operationSelectorSwitchCurrentValue,
            "dependantSwitch": {
                "unit": 1,
                "ifValue": "10",
                "setValue": "off"
            }
        }
        self.selectorData[unit] = {
            "idle": 10,   "auto": 20,   "silent": 30,   "favorite": 40,
            "10": "idle", "20": "auto", "30": "silent", "40": "favorite"
        }

        unit = 3
        if unit not in Devices:
            Domoticz.Debug("Creating led brightness selector switch")
            Options = {"LevelActions" : "|||",
                    "LevelNames" : "|Off|Dim|Bright",
                    "LevelOffHidden" : "true",
                    "SelectorStyle" : "1"}
            Domoticz.Device(Name="Led brightness", Unit=unit, Image=7, TypeName="Selector Switch", Options=Options).Create()
        else:
            Domoticz.Debug("Led brightness switch already exists with unit ID: %d" % (unit))
        self.units[unit] = {
            "type": "selector",
            "command": self.ledBrightnessSwitch,
            "currentValue": self.ledBrightnessSwitchCurrentValue
        }
        self.selectorData[unit] = {
            "2": 10,   "1": 20,   "0": 30,
            "10": 2, "20": 1, "30": 0
        }

        unit = 4
        if unit not in Devices:
            Domoticz.Debug("Creating favorite level selector switch")
            Options = {"LevelActions" : "||||||||||||||||",
                    "LevelNames" : "|1|2|3|4|5|6|7|8|9|10|11|12|13|14|15|16",
                    "LevelOffHidden" : "true",
                    "SelectorStyle" : "1"}
            Domoticz.Device(Name="Favorite level", Unit=unit, Image=7, TypeName="Selector Switch", Options=Options).Create()
        else:
            Domoticz.Debug("Favorite level switch already exists with unit ID: %d" % (unit))
        self.units[unit] = {
            "type": "selector",
            "command": self.favoriteLevelSwitch,
            "currentValue": self.favoriteLevelSwitchCurrentValue
        }
        self.selectorData[unit] = {
            "1": 10,   "2": 20,   "3": 30,   "4": 40,
            "5": 50,   "6": 60,   "7": 70,   "8": 80,
            "9": 90,   "10": 100, "11": 110, "12": 120,
            "13": 130, "14": 140, "15": 150, "16": 160,
            "10": 1,   "20": 2,   "30": 3,   "40": 4,
            "50": 5,   "60": 6,   "70": 7,   "80": 8,
            "90": 9,   "100": 10, "110": 11, "120": 12,
            "130": 13, "140": 14, "150": 15, "160": 16
        }

        unit = 5
        if unit not in Devices:
            Domoticz.Debug("Creating air quality device")
            Options = { "Custom": "1;μg/m³" }
            Domoticz.Device(Name="Air quality", Unit=unit, Type=243, Subtype=31, Image=7, Options=Options).Create()
        else:
            Domoticz.Debug("Air quality device already exists with unit ID: %d" % (unit))
        self.units[unit] = {
            "type": "sensor",
            "currentValue": self.airQualityDeviceCurrentValue
        }
        
        unit = 6
        if unit not in Devices:
            Domoticz.Debug("Creating temperature + humidity device")
            Domoticz.Device(Name="Temperature + humidity", Unit=unit, Type=82, Image=7).Create()
        else:
            Domoticz.Debug("Temperature + humidity device already exists with unit ID: %d" % (unit))
        self.units[unit] = {
            "type": "sensor",
            "currentValue": self.temperatureHumidityDeviceCurrentValue
        }
        
        unit = 7
        if unit not in Devices:
            Domoticz.Debug("Creating filter life remaining device")
            Domoticz.Device(Name="Filter life remaining", Unit=unit, Type=243, Subtype=6, Image=7).Create()
        else:
            Domoticz.Debug("Filter life remaining device already exists with unit ID: %d" % (unit))
        self.units[unit] = {
            "type": "sensor",
            "currentValue": self.filterLifeRemainingDeviceCurrentValue
        }
        
        unit = 8
        if unit not in Devices:
            Domoticz.Debug("Creating filter hours used device")
            Options = { "Custom": "1;hours" }
            Domoticz.Device(Name="Filter hours used", Unit=unit, Type=243, Subtype=31, Image=7, Options=Options).Create()
        else:
            Domoticz.Debug("Filter hours used device already exists with unit ID: %d" % (unit))
        self.units[unit] = {
            "type": "sensor",
            "currentValue": self.filterHoursUsedDeviceCurrentValue
        }

        return

    def runCommand(self, unit, command, level):
        updateValues = self.units[unit]["command"](unit, command, str(level))
        self.updateDomoticzDevice(unit, updateValues["nValue"], updateValues["sValue"])
        if "dependantSwitch" in self.units[unit] and self.units[unit]["dependantSwitch"]["ifValue"] == updateValues["sValue"].lower():
            self.updateDomoticzDevice(self.units[unit]["dependantSwitch"]["unit"], updateValues["nValue"], self.units[unit]["dependantSwitch"]["setValue"])
        return
    
    def powerSwitchCurrentValue(self):
        return self.status.power

    def powerSwitch(self, unit, command, level):
        nValue = 0
        sValue = "Off"
        if command.lower() == "on":
            self.ap.on()
            nValue = 1
            sValue = "On"
        else:
            self.ap.off()
        return {
            "nValue": nValue,
            "sValue": sValue
        }
    
    def operationSelectorSwitchCurrentValue(self):
        return self.status.mode.value
    
    def operationSelectorSwitch(self, unit, command, level):
        nValue = 0
        sValue = OperationMode(self.selectorData[unit][level])
        if sValue != "idle":
            nValue = 1
        self.ap.set_mode(sValue)
        return {
            "nValue": nValue,
            "sValue": level
        }
    
    def ledBrightnessSwitchCurrentValue(self):
        return self.status.led_brightness.value
    
    def ledBrightnessSwitch(self, unit, command, level):
        ps = self.powerSwitchCurrentValue()
        nValue = 0 if ps.lower() == "off" else 1
        sValue = LedBrightness(self.selectorData[unit][level])
        self.ap.set_led_brightness(sValue)
        return {
            "nValue": nValue,
            "sValue": level
        }
    
    def favoriteLevelSwitchCurrentValue(self):
        return self.status.favorite_level
    
    def favoriteLevelSwitch(self, unit, command, level):
        ps = self.powerSwitchCurrentValue()
        nValue = 0 if ps.lower() == "off" else 1
        sValue = self.selectorData[unit][level]
        self.ap.set_favorite_level(sValue)
        return {
            "nValue": nValue,
            "sValue": level
        }
    
    def airQualityDeviceCurrentValue(self):
        return self.status.aqi
    
    def temperatureHumidityDeviceCurrentValue(self):
        temp = self.status.temperature
        hum = self.status.humidity
        humStatus = 3
        if hum < 25:
            humStatus = 2
        elif hum < 40:
            humStatus = 1
        elif hum < 60:
            humStatus = 0
        return "%f;%f;%d"%(temp, hum, humStatus)

    def filterLifeRemainingDeviceCurrentValue(self):
        return self.status.filter_life_remaining

    def filterHoursUsedDeviceCurrentValue(self):
        return self.status.filter_hours_used

    def updateAirPurifierStatus(self):
        self.status = self.ap.status()
    
    def updateDomoticzDevice(self, unit, nValue, sValue):
        Domoticz.Debug("Updating Domoticz device %d: (%d,%s)" % (unit, nValue, sValue))
        Devices[unit].Update(nValue = nValue, sValue = str(sValue))
    
    def updateDomoticzDevices(self):
        self.updateAirPurifierStatus()
        for unit in self.units:
            unitType = self.units[unit]["type"]
            value = self.units[unit]["currentValue"]()
            ps = self.powerSwitchCurrentValue()
            
            nValue = 0 if ps.lower() == "off" else 1
            sValue = value
            if unitType == "switch":
                nValue = 0 if value.lower() == "off" else 1
                sValue = "On" if sValue else "Off"
            elif unitType == "sensor":
                nValue = 0
            if unit in self.selectorData and (str(sValue)).lower() in self.selectorData[unit]:
                sValue = self.selectorData[unit][(str(sValue)).lower()]

            self.updateDomoticzDevice(unit, nValue, sValue)
        return


class XiaomiAirpurifier2HPlugin:
    def __init__(self):
        self.devices = {}
        self.lastState = None
        self.heartbeat = None
        self.helper = None
        return

    def onStart(self):
        Domoticz.Log("onStart called")
        
        # Setting up debug mode
        if (Parameters["Mode2"] != "off"):
            Domoticz.Debugging(1)
            Domoticz.Debug("Debug mode enabled")

        # Setting up heartbeat
        self.heartbeat = Heartbeat(int(Parameters["Mode3"]))
        self.heartbeat.setHeartbeat(self.update)

        # Setting up helper
        self.helper = Helper(Parameters["Mode1"], Parameters["Password"])

        # Creating Domoticz devices
        self.helper.createDomoticzDevices()

        #Updating Domoticz devices
        self.update()

        DumpConfigToLog()

        return

    def onStop(self):
        Domoticz.Log("onStop called")
        return

    def onConnect(self, Connection, Status, Description):
        Domoticz.Log("onConnect called; connection: %s, status: %s, description: %s" % (str(Connection), str(Status), str(Description)))
        return

    def onMessage(self, Connection, Data):
        Domoticz.Log("onMessage called; connection: %s, data: %s" % (str(Connection), str(Data)))
        return

    def onCommand(self, Unit, Command, Level, Hue):
        Domoticz.Log("onCommand called for Unit: %d, Parameter: '%s', Level: '%s'" % (Unit, str(Command), str(Level)))
        self.helper.runCommand(Unit, Command, Level)
        return

    def onNotification(self, Name, Subject, Text, Status, Priority, Sound, ImageFile):
        Domoticz.Log("Notification: " + Name + "," + Subject + "," + Text + "," + Status + "," + str(Priority) + "," + Sound + "," + ImageFile)
        return

    def onDisconnect(self, Connection):
        Domoticz.Log("onDisconnect called")
        return

    def onHeartbeat(self):
        Domoticz.Debug("onHeartbeat called")
        self.heartbeat.beatHeartbeat()
        return

    def update(self):
        Domoticz.Debug("update called")
        self.helper.updateDomoticzDevices()
        return


global _plugin
_plugin = XiaomiAirpurifier2HPlugin()

def onStart():
    global _plugin
    _plugin.onStart()

def onStop():
    global _plugin
    _plugin.onStop()

def onConnect(Connection, Status, Description):
    global _plugin
    _plugin.onConnect(Connection, Status, Description)

def onMessage(Connection, Data):
    global _plugin
    _plugin.onMessage(Connection, Data)

def onCommand(Unit, Command, Level, Hue):
    global _plugin
    _plugin.onCommand(Unit, Command, Level, Hue)

def onNotification(Name, Subject, Text, Status, Priority, Sound, ImageFile):
    global _plugin
    _plugin.onNotification(Name, Subject, Text, Status, Priority, Sound, ImageFile)

def onDisconnect(Connection):
    global _plugin
    _plugin.onDisconnect(Connection)

def onHeartbeat():
    global _plugin
    _plugin.onHeartbeat()

def DumpConfigToLog():
    for x in Parameters:
        if Parameters[x] != "":
            Domoticz.Debug( "'" + x + "':'" + str(Parameters[x]) + "'")
    Domoticz.Debug("Device count: " + str(len(Devices)))
    for x in Devices:
        Domoticz.Debug("Device:           " + str(x) + " - " + str(Devices[x]))
        Domoticz.Debug("Device ID:       '" + str(Devices[x].ID) + "'")
        Domoticz.Debug("Device Name:     '" + Devices[x].Name + "'")
        Domoticz.Debug("Device nValue:    " + str(Devices[x].nValue))
        Domoticz.Debug("Device sValue:   '" + Devices[x].sValue + "'")
        Domoticz.Debug("Device LastLevel: " + str(Devices[x].LastLevel))
    return
