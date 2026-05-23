##################匯入模組###############
# 用來發送HTTP請求獲取API數據
import requests

#################定義常數#################
# OpenWeatherMap API的密鑰
API_KEY = "892da2f13edf3c7f382637760e72d224"
# 天氣查詢的基礎URL
BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"
# 溫度單位設為攝氏度
UNITS = "metric"
# 語言設定為繁體中文
LANGU = "zh_tw"

#################主程式#####################
# 提示使用者輸入城市名稱
city_name = input("請輸入城市名稱：")

# 組合完整的API請求URL
send_url = f"{BASE_URL}q={city_name}&appid={API_KEY}&units={UNITS}&lang={LANGU}"
# 顯示發送的URL用於調試
print(f"發送的 URL:{send_url}")
# 發送HTTP GET請求到API
requests = requests.get(send_url)
# 將JSON格式的回應轉換為Python字典
info = requests.json()

########################## 處理天氣資訊 ##########################
# 檢查回應中是否包含天氣和溫度資訊
if "weather" in info and "main" in info:
    # 獲取當前氣溫（攝氏度）
    current_temperature = info["main"]["temp"]
    # 獲取天氣描述
    weather_description = info["weather"][0]["description"]

    # 顯示查詢的城市名稱
    print(f"城市：{city_name}")
    # 顯示當前溫度
    print(f"溫度：{current_temperature}°C")
    # 顯示天氣狀況描述
    print(f"描述：{weather_description}")
else:
    # 若查詢失敗，顯示錯誤訊息
    print("找不到該城市或無法獲取天氣資訊")
