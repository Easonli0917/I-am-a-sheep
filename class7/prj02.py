#######################匯入模組#######################
# 導入ttkbootstrap用於美化Tkinter視窗
from ttkbootstrap import *
# 導入sys用於獲取系統路徑
import sys
# 導入os用於處理作業系統相關操作
import os
# 導入PIL圖片模組用於載入圖片
from PIL import Image, ImageTk

#######################設定工作目錄####################
# 將工作目錄更改為指令碼所在的目錄
os.chdir(sys.path[0])


#######################定義函數########################
# 定義勾選狀態改變時的回調函數
def on_switch_change():
    # 根據勾選狀態更新標籤顯示的文字
    check_label.config(text=str(check_type.get()))


#######################建立視窗########################
# 建立主視窗
window = Tk()
# 設置視窗標題
window.title("I-am-a-sheep")

######################設定字形######################
# 設定字體大小為20
font_size = 20
# 為所有元件設定預設字體
window.option_add("*font", ("Halvetica", font_size))

######################設定主題######################
# 建立樣式物件並設定主題為cyborg（暗色主題）
style = Style(theme="cyborg")
# 設定按鈕的字體大小
style.configure("yaya.TButton", font=("Halvetica", font_size))
# 設定勾選框的字體大小
style.configure("yaya.TCheckbutton", font=("Halvetica", font_size))

######################建立變數#########################
# 建立布林變數用於記錄勾選狀態
check_type = BooleanVar()
# 初始化勾選狀態為True（已勾選）
check_type.set(True)

######################建立標籤########################
# 建立標籤用於顯示勾選狀態，初始值為"True"
check_label = Label(window, text="True")
# 放置標籤在第1列第2行
check_label.grid(row=1, column=2, padx=10, pady=10)

# 載入並開啟天氣圖片
image = Image.open("weather.png")
# 將PIL圖片轉換為Tkinter可使用的格式
img = ImageTk.PhotoImage(image)
# 建立標籤用於顯示圖片
img_label = Label(window, image=img)
# 放置圖片標籤在第2行，跨越1-2列
img_label.grid(row=2, column=1, columnspan=2, padx=10, pady=10)
# 保存圖片引用，防止被垃圾回收而消失
img_label.image = img

######################建立勾選框########################
# 建立勾選框用於切換勾選狀態
check = Checkbutton(
    window,
    # 綁定到check_type布林變數
    variable=check_type,
    # 勾選時的值為True
    onvalue=True,
    # 未勾選時的值為False
    offvalue=False,
    # 勾選狀態改變時執行on_switch_change函數
    command=on_switch_change,
    # 應用自訂樣式
    style="yaya.TCheckbutton",
)
# 放置勾選框在第1行第1列
check.grid(row=1, column=1, padx=10, pady=10)

######################運行應用程式#########################
# 啟動主視窗的主迴圈，等待使用者操作
window.mainloop()
