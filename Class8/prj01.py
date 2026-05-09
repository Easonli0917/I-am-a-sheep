import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import requests
from io import BytesIO

# OpenWeather API KEY
API_KEY = "892da2f13edf3c7f382637760e72d224"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"
UNITS = "metric"
LANGU = "zh_tw"
ICON_BASE_URL = "https://openweathermap.org/img/wn/"

# 目前溫度（攝氏）
current_temp_c = 0


# ===== 查詢天氣 =====
def get_weather():

    global current_temp_c

    city = city_entry.get()

    if city == "":
        temp_label.config(text="請輸入城市")
        return

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric&lang=zh_tw"

    data = requests.get(url).json()

    if data["cod"] == 200:

        # 攝氏溫度
        current_temp_c = data["main"]["temp"]

        # 描述
        desc = data["weather"][0]["description"]

        # 圖標代碼
        icon_code = data["weather"][0]["icon"]

        # 圖標網址
        icon_url = f"https://openweathermap.org/img/wn/{icon_code}@2x.png"

        # 下載圖片
        response = requests.get(icon_url)

        # 轉圖片
        image_data = Image.open(BytesIO(response.content))

        # tkinter圖片格式
        photo = ImageTk.PhotoImage(image_data)

        # 顯示圖片
        icon_label.config(image=photo)
        icon_label.image = photo

        # 顯示溫度
        update_temperature()

        # 顯示描述
        desc_label.config(text=f"描述: {desc}")

    else:
        temp_label.config(text="找不到城市")
        desc_label.config(text="")
        icon_label.config(image="")


# ===== 更新溫度 =====
def update_temperature():

    # 如果勾選 -> 華氏
    if temp_var.get():

        f = (current_temp_c * 9 / 5) + 32
        temp_label.config(text=f"溫度: {f:.1f}°F")

    # 否則 -> 攝氏
    else:

        temp_label.config(text=f"溫度: {current_temp_c:.1f}°C")


# ===== 建立視窗 =====
root = tk.Tk()
root.title("Weather App")
root.geometry("")
root.configure(bg="white")

# ===== 上面 =====
top_frame = tk.Frame(root, bg="white")
top_frame.pack(pady=30)

city_label = tk.Label(
    top_frame, text="請輸入想搜尋的城市：", font=("微軟正黑體", 24), bg="white"
)
city_label.pack(side="left")

city_entry = tk.Entry(top_frame, font=("微軟正黑體", 24), width=20)
city_entry.pack(side="left", padx=10)

search_button = tk.Button(
    top_frame,
    text="獲得天氣資訊",
    font=("微軟正黑體", 22),
    bg="#9ED9C8",
    fg="white",
    relief="flat",
    command=get_weather,
)
search_button.pack(side="left")

# ===== 中間 =====
middle_frame = tk.Frame(root, bg="white")
middle_frame.pack(pady=20)

# 天氣圖片
icon_label = tk.Label(middle_frame, bg="white")
icon_label.grid(row=0, column=0, padx=80)

# 溫度
temp_label = tk.Label(
    middle_frame, text="溫度: ?°C", font=("微軟正黑體", 24), bg="white"
)
temp_label.grid(row=0, column=1, padx=80)

# 描述
desc_label = tk.Label(middle_frame, text="描述: ?", font=("微軟正黑體", 24), bg="white")
desc_label.grid(row=0, column=2, padx=80)

# ===== 下面 =====
bottom_frame = tk.Frame(root, bg="white")
bottom_frame.pack()

# 勾選變數
temp_var = tk.BooleanVar()

# 字體
style = ttk.Style()
style.configure("TCheckbutton", font=("微軟正黑體", 18))

# 勾選框
check = ttk.Checkbutton(
    bottom_frame,
    text="切換成華氏溫度 °F",
    variable=temp_var,
    command=update_temperature,
)
check.pack()

# 啟動
root.mainloop()
