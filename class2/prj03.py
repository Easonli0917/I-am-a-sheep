#######################匯入模組#######################
# 匯入tkinter模組
from tkinter import *
import random


#######################定義函數########################
change = False


def 換顏色():
    fg_color = "#" + "".join([random.choice("0123456789ABCDEF") for j in range(6)])
    bg_color = "#" + "".join([random.choice("0123456789ABCDEF") for j in range(6)])
    文字.config(text="color", fg=fg_color, bg=bg_color)


#######################建立視窗########################
# 建立視窗
windows = Tk()
# 設置視窗名稱
windows.title("I-am-a-sheep")
########################建立按鈕########################
# 建立按鈕

Click = Button(windows, text="Chick me", command=換顏色)

# 設置按鈕位置
Click.pack()

########################建立標籤########################
# 建立標籤
# Label(樹窗名稱,文字內容,前景顏色,背景顏色)
文字 = Label(windows, text="")
# 將標籤家入主視窗
文字.pack()
#######################運行應用程式########################
# 開始執行主迴圈等待用戶操作
windows.mainloop()
