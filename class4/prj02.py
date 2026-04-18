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

keys_pressed = set()  # 用來記錄目前按下的案件


def key_press(event):
    keys_pressed.add(event.keysym)  # 將按下的案件加入集合中


def key_release(event):
    keys_pressed.discard(event.keysym)  # 將按下的案件從集合中移除


# 定義一個函數，用來處理按下時要做出的事情
def game_loop():
    if "Up" in keys_pressed:
        canvas.move(circle, 0, -5)  # 向上移動
    if "Down" in keys_pressed:
        canvas.move(circle, 0, 5)  # 向下移動
    if "Left" in keys_pressed:
        canvas.move(circle, -5, 0)  # 向左移動
    if "Right" in keys_pressed:
        canvas.move(circle, 5, 0)  # 向右移動
    if "w" in keys_pressed:  # 向上移動
        canvas.move(rect, 0, -5)
    if "s" in keys_pressed:  # 向下移動
        canvas.move(rect, 0, 5)
    if "a" in keys_pressed:  # 向左移動
        canvas.move(rect, -5, 0)
    if "d" in keys_pressed:  # 向右移動
        canvas.move(rect, 5, 0)
    windows.after(16, game_loop)  # 每50毫秒呼叫一次game_loop函數，形成一個遊戲循環


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
canvas.bind_all("<KeyPress>", key_press)
canvas.bind_all("<KeyRelease>", key_release)
###########################啟動遊戲迴圈##################################
game_loop()
#######################運行應用程式########################
# 開始執行主迴圈等待用戶操
windows.mainloop()
