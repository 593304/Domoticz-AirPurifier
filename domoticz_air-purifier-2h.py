from urllib.request import Request, urlopen
from base64 import encodebytes
from miio_devices.air_purifier import MyAirPurifier

DOMOTICZ_URL = "http://127.0.0.1:8080/json.htm"
DOMOTICZ_TH_QUERY = "?type=command&param=udevice&idx=%d&nvalue=0&svalue=%d;%d;%d&battery=%d"
DOMOTICZ_CS_QUERY = "?type=command&param=udevice&idx=%d&nvalue=0&svalue=%d"
DOMOTICZ_USER = ""
DOMOTICZ_PASS = ""
DOMOTICZ_AUTH = encodebytes((DOMOTICZ_USER + ":" + DOMOTICZ_PASS).encode()).decode().replace("\n", "")

AIR_PURIFIERS = [
    {"ip": "...",
     "token": "...",
     "IDX_TH": None,
     "IDX_CS_AQI": None,
     "IDX_CS_Life": None,
     "IDX_CS_Hours": None}
]


def send_request(url):
    print("Sending request to:", url)
    request = Request(url)
    request.add_header("Authorization", "Basic %s" % DOMOTICZ_AUTH)
    response = urlopen(request)
    print(response.read())


def get_comfort_value(humidity):
    if humidity < 40:
        return 2
    elif humidity <= 70:
        return 1
    else:
        return 3


def handle_th(idx, temperature, humidity):
    if idx:
        print("Sending temperature and humidity request to Domoticz ...")
        comfort = get_comfort_value(humidity)
        send_request(DOMOTICZ_URL + DOMOTICZ_TH_QUERY % (idx, temperature, humidity, comfort, 100))
    else:
        print("IDX not defined for temperature and humidity")


def handle_aqi(idx, aqi):
    if idx:
        print("Sending air quality index request to Domoticz ...")
        send_request(DOMOTICZ_URL + DOMOTICZ_CS_QUERY % (idx, aqi))
    else:
        print("IDX not defined for air quality index")


def handle_life(idx, life):
    if idx:
        print("Sending filter life usage request to Domoticz ...")
        send_request(DOMOTICZ_URL + DOMOTICZ_CS_QUERY % (idx, life))
    else:
        print("IDX not defined for filter life usage")


def handle_hours(idx, hours):
    if idx:
        print("Sending filter hours used request to Domoticz ...")
        send_request(DOMOTICZ_URL + DOMOTICZ_CS_QUERY % (idx, hours))
    else:
        print("IDX not defined for filter hours used")


for ap in AIR_PURIFIERS:
    my_ap = MyAirPurifier(ap["ip"], ap["token"])
    try:
        print("Getting status for", ap["ip"])
        status = my_ap.get_status()
        handle_th(ap["IDX_TH"], status["temperature"], status["humidity"])
        handle_aqi(ap["IDX_CS_AQI"], status["aqi"])
        handle_life(ap["IDX_CS_Life"], 100 - status["life"])
        handle_hours(ap["IDX_CS_Hours"], status["hours"])
    except Exception as e:
        print(e)
