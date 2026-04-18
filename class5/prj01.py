#######################匯入模組#######################
from ttkbootstrap import *
import sys
import os


#######################定義函數########################
def test():
    print("test")


#######################建立視窗########################
Window = Tk()
Window.title("I-am-a-sheep")
#######################運行應用程式########################
#######################設定字形###########################
font_size = 20
Window.option_add("*Font", ("Halvetica", font_size))
#######################設定主題###############################
style = Style(theme="cyborg")  # 設定主題
# "my.TButton"的命名邏輯:
# 就像貼標籤一樣,分成兩個部分用.隔開
# 前面是自訂的名稱,後面是要套用的元件類型
style.configure("yaya.TButton", font=("Halvetica", font_size))
######################建立標籤################################ˇ
label = Label(Window, text="I-am-a-sheep")
label.grid(row=0, column=0, sticky="E")
########################建立按鈕##########################
button = Button(Window, text="瀏覽", command=test, style="yaya.TButton")
button.grid(row=0, column=1, sticky="W")
button2 = Button(Window, text="顯示", command=test, style="yaya.TButton")
button2.grid(row=1, column=0, columnspan=2, sticky="EW")
#########################運行應用程式###################
Window.mainloop()
