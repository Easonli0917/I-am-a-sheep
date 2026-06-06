import tkinter as tk  # 做視窗用
from tkinter import ttk  # 做勾選框用
from PIL import Image, ImageTk  # 顯示圖片用
import requests  # 去網路抓資料用
from io import BytesIO  # 把圖片變成Python可讀格式用

API_KEY = "892da2f13edf3c7f382637760e72d224"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"
UNITS = "metric"
LANGU = "zh_tw"
ICON_BASE_URL = "https://openweathermap.org/img/wn/"  # OpenWeather的密碼

current_temp_c = 0  # 存目前的攝氏溫度（之後轉華氏用）


# ===== 查天氣的函式 =====
def get_weather():

    global current_temp_c  # 讓函式可以改外面的溫度

    city = city_entry.get()  # 讀取使用者輸入的城市

    if city == "":  # 如果沒輸入
        temp_label.config(text="請輸入城市")  # 提示使用者
        return  # 停止程式

    # 去 OpenWeather 拿資料
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric&lang=zh_tw"

    data = requests.get(url).json()  # 把資料變成Python字典

    if data["cod"] == 200:  # 如果成功找到城市

        current_temp_c = data["main"]["temp"]  # 取得攝氏溫度
        desc = data["weather"][0]["description"]  # 天氣描述

        icon_code = data["weather"][0]["icon"]  # 天氣圖標代碼

        icon_url = f"https://openweathermap.org/img/wn/{icon_code}@2x.png"  # 圖片網址

        response = requests.get(icon_url)  # 下載圖片

        image_data = Image.open(BytesIO(response.content))  # 轉圖片格式

        photo = ImageTk.PhotoImage(image_data)  # 轉成Tkinter能用的圖片

        icon_label.config(image=photo)  # 顯示圖片
        icon_label.image = photo  # 防止圖片消失

        update_temperature()  # 更新溫度顯示

        desc_label.config(text=f"描述: {desc}")  # 顯示天氣描述

    else:  # 如果找不到城市
        temp_label.config(text="找不到城市")  # 顯示錯誤
        desc_label.config(text="")  # 清空描述
        icon_label.config(image="")  # 清空圖片


# ===== 更新溫度（攝氏/華氏切換）=====
def update_temperature():

    if temp_var.get():  # 如果勾選（華氏）

        f = (current_temp_c * 9 / 5) + 32  # 攝氏轉華氏
        temp_label.config(text=f"溫度: {f:.1f}°F")  # 顯示華氏

    else:  # 沒勾選（攝氏）

        temp_label.config(text=f"溫度: {current_temp_c:.1f}°C")  # 顯示攝氏


# ===== 建立視窗 =====
root = tk.Tk()  # 建立主視窗
root.title("Weather App")  # 標題
root.geometry("1200x600")  # 視窗大小
root.configure(bg="white")  # 背景白色

# ===== 上方區塊 =====
top_frame = tk.Frame(root, bg="white")  # 建立上方區塊
top_frame.pack(pady=30)  # 放上去並留空間

city_label = tk.Label(  # 文字提示
    top_frame, text="請輸入想搜尋的城市：", font=("微軟正黑體", 24), bg="white"
)
city_label.pack(side="left")  # 靠左

city_entry = tk.Entry(top_frame, font=("微軟正黑體", 24), width=20)  # 輸入框
city_entry.pack(side="left", padx=10)  # 放中間

search_button = tk.Button(  # 按鈕
    top_frame,
    text="獲得天氣資訊",
    font=("微軟正黑體", 22),
    bg="#9ED9C8",
    fg="white",
    relief="flat",
    command=get_weather,  # 按下去就查天氣
)
search_button.pack(side="left")

# ===== 中間顯示區 =====
middle_frame = tk.Frame(root, bg="white")  # 中間區塊
middle_frame.pack(pady=20)

icon_label = tk.Label(middle_frame, bg="white")  # 天氣圖標
icon_label.grid(row=0, column=0, padx=80)

temp_label = tk.Label(  # 溫度
    middle_frame, text="溫度: ?°C", font=("微軟正黑體", 24), bg="white"
)
temp_label.grid(row=0, column=1, padx=80)

desc_label = tk.Label(  # 天氣描述
    middle_frame, text="描述: ?", font=("微軟正黑體", 24), bg="white"
)
desc_label.grid(row=0, column=2, padx=80)

# ===== 下方勾選 =====
bottom_frame = tk.Frame(root, bg="white")  # 下方區塊
bottom_frame.pack()

temp_var = tk.BooleanVar()  # 記錄有沒有勾選

style = ttk.Style()  # 設定樣式
style.configure("TCheckbutton", font=("微軟正黑體", 18))

check = ttk.Checkbutton(  # 勾選框
    bottom_frame,
    text="切換成華氏溫度 °F",
    variable=temp_var,
    command=update_temperature,  # 一改就更新溫度
)
check.pack()

root.mainloop()  # 讓視窗一直運作
