#######################匯入模組#######################
# 匯入tkinter模組
from tkinter import *
import sys
import os

# pip install pillow
from PIL import Image, ImageTk

#######################設定工作目錄####################
# 設定工作目錄
os.chdir(sys.path[0])


# 顯示目前工作目錄
#######################定義函數#########################


# 定義一個函數，用來處理按下時要做出的事情
def move_circle(event):
    # 取得按下的案件
    key = event.keysym
    print(key)  # 判斷按下的哪一個按鍵，並根據不同的案件來移動不同的圖形
    if key == "Up":
        canvas.move(circle, 0, -10)  # 向上移動
    elif key == "Down":
        canvas.move(circle, 0, 10)  # 向下移動
    elif key == "Left":
        canvas.move(circle, -10, 0)  # 向左移動
    elif key == "Right":
        canvas.move(circle, 10, 0)  # 向右移動
    elif key == "w":  # 向上移動
        canvas.move(rect, 0, -10)
    elif key == "s":  # 向下移動
        canvas.move(rect, 0, 10)
    elif key == "a":  # 向左移動
        canvas.move(rect, -10, 0)
    elif key == "d":  # 向右移動
        canvas.move(rect, 10, 0)


#######################建立視窗########################
# 建立視窗
windows = Tk()
# 設置視窗名稱
windows.title("I-am-a-sheep")

#######################創建畫布############################
# 創建畫布
canvas = Canvas(windows, width=600, height=600, bg="white")
canvas.pack()

#########################設定視窗圖片####################
# 設定視窗圖片
windows.iconbitmap("crocodile2.ico")
########################載入圖片###########################
# tkinter內建photoimang.只支援 png pgm ppm 格式(不支援jpg bmp等)

# img = PhotoImage(file="crocodile2.png")

image = Image.open("images.png")

img = ImageTk.PhotoImage(image)
#########################顯示圖片#####################
# 在畫布上顯示圖,設定的圖片中心點座標為300,300
my_img = canvas.create_image(300, 300, image=img)
#######################畫圖形#############################
#  在畫布上畫一個圖形，起始位置為(250，150)，結束位置為(300，200)，填充顏色為紅色
circle = canvas.create_oval(250, 150, 300, 200, fill="red")
# 在畫布上畫一個矩形，起始位置為(220,400)，結束位置為(350,500)，填充顏色為藍色
rect = canvas.create_rectangle(220, 400, 340, 430, fill="blue")
# 在畫布上顯示一段文字，位置為(300,100)，文字為dog，顏色為黑色，字型為Arial，大小為30
msg = canvas.create_text(300, 100, text="dog", fill="black", font="Arial 30")
########################綁定案件指令##################################
# 將案件事件綁定在畫布上，當按下指定的案件時，移動對應的物件
canvas.bind_all("<Key>", move_circle)
#######################運行應用程式########################
# 開始執行主迴圈等待用戶操
windows.mainloop()
