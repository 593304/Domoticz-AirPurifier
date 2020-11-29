from miio import AirPurifier


class MyAirPurifier:
    def __init__(self, ip, token):
        self.ap = AirPurifier(ip=ip, token=token)

    def get_status(self):
        status = self.ap.status()
        print("Status received:", status)
        return {
            "temperature": status.temperature,
            "humidity": status.humidity,
            "aqi": status.aqi,
            "life": status.filter_life_remaining,
            "hours": status.filter_hours_used,
        }
