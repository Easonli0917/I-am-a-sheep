##################匯入模組###############
import requests
import os
import sys

#################定義常數#################
API_KEY = "892da2f13edf3c7f382637760e72d224"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"
UNITS = "metric"
LANGU = "zh_tw"
ICON_BASE_URL = "https://openweathermap.org/img/wn/"
#################主程式#####################
city_name = input("請輸入城市名稱：")

send_url = f"{BASE_URL}q={city_name}&appid={API_KEY}&units={UNITS}&lang={LANGU}"
print(f"發送的 URL:{send_url}")
request = requests.get(send_url)
info = request.json()
# 解析 JSON

########################## 主程式 ##########################
os.chdir(sys.path[0])
# 處理和顯示天氣資訊
if "weather" in info and "main" in info:
    current_temperature = info["main"]["temp"]
    weather_description = info["weather"][0]["description"]
    icon_code = info["weather"][0]["icon"]
    print(f"城市：{city_name}")
    print(f"溫度：{current_temperature}°C")
    print(f"描述：{weather_description}")
    icon_url = f"{ICON_BASE_URL}{icon_code}@2x.png"
    print(f"天氣圖示 URL: {icon_url}")
    icon_response = requests.get(icon_url)
    if icon_response.status_code == 200:
        with open("weather_icon.png", "wb") as icon_file:
            icon_file.write(icon_response.content)
        print(f"天氣圖示已下載並保存為 weather.png")
    else:
        print("無法下載天氣圖示")
else:
    print("找不到該城市或無法獲取天氣資訊")
