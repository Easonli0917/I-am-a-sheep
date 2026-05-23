##################匯入模組###############
# 用來發送HTTP請求獲取API數據
import requests
# 用來處理作業系統相關操作
import os
# 用來獲取系統路徑
import sys

#################定義常數#################
# OpenWeatherMap API的密鑰
API_KEY = "892da2f13edf3c7f382637760e72d224"
# 天氣查詢的基礎URL
BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"
# 溫度單位設為攝氏度
UNITS = "metric"
# 語言設定為繁體中文
LANGU = "zh_tw"
# 天氣圖示的基礎URL
ICON_BASE_URL = "https://openweathermap.org/img/wn/"

#################設定工作目錄###############
# 將工作目錄更改為腳本所在的目錄
os.chdir(sys.path[0])

#################主程式#####################
# 提示使用者輸入城市名稱
city_name = input("請輸入城市名稱：")

# 組合完整的API請求URL
send_url = f"{BASE_URL}q={city_name}&appid={API_KEY}&units={UNITS}&lang={LANGU}"
# 顯示發送的URL用於調試
print(f"發送的 URL:{send_url}")
# 發送HTTP GET請求到API
request = requests.get(send_url)
# 將JSON格式的回應轉換為Python字典
info = request.json()

########################## 處理天氣資訊 ##########################
# 檢查回應中是否包含天氣和溫度資訊
if "weather" in info and "main" in info:
    # 獲取當前氣溫（攝氏度）
    current_temperature = info["main"]["temp"]
    # 獲取天氣描述
    weather_description = info["weather"][0]["description"]
    # 獲取天氣圖示的代碼
    icon_code = info["weather"][0]["icon"]
    
    # 顯示查詢的城市名稱
    print(f"城市：{city_name}")
    # 顯示當前溫度
    print(f"溫度：{current_temperature}°C")
    # 顯示天氣狀況描述
    print(f"描述：{weather_description}")
    
    ######################## 下載天氣圖示 ########################
    # 根據圖示代碼組合完整的圖示URL
    icon_url = f"{ICON_BASE_URL}{icon_code}@2x.png"
    # 顯示圖示URL
    print(f"天氣圖示 URL: {icon_url}")
    # 下載天氣圖示
    icon_response = requests.get(icon_url)
    # 檢查下載是否成功（HTTP狀態碼200表示成功）
    if icon_response.status_code == 200:
        # 以二進制模式打開檔案並保存圖示
        with open("weather_icon.png", "wb") as icon_file:
            icon_file.write(icon_response.content)
        # 顯示下載成功訊息
        print(f"天氣圖示已下載並保存為 weather.png")
    else:
        # 若下載失敗，顯示錯誤訊息
        print("無法下載天氣圖示")
else:
    # 若查詢失敗，顯示錯誤訊息
    print("找不到該城市或無法獲取天氣資訊")
