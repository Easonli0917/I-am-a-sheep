import requests


class WeatherAPI:
    def __init__(self, api_key, lang="zh_tw"):
        self.api_key = api_key
        self.units = "metric"
        self.lang = lang
        self.base_url = "https://api.openweathermap.org/data/2.5/weather?"
        self.icon_url = "http://openweathermap.org/img/wn/"

    def get_current_weather(self, city_name):
        send_url = f"{self.base_url}appid={self.api_key}&q={city_name}&units={self.units}&lang={self.lang}"
        response = requests.get(send_url)
        return response.json()

    def get_weather_summary(self, icon_code):
        info = self.get_current_weather(icon_code)

        if "weather" in info and "main" in info:
            return {
                "city_name": info.get("name", "city_name"),
                "temperature_celsius": round(info["main"]["temp"], 2),
                "description": info["weather"][0]["description"],
                "icon code": info["weather"][0]["icon"],
            }

        return None

    def get_icon_url(self, icon_code):
        return f"{self.icon_base_url}{icon_code}.@2x.png"

    def get_weather_icon(self, icon_code):
        icon_url = self.get_icon_url(icon_code)
        response = requests.get(icon_url)
        if response.content:
            return response.content
        return None
