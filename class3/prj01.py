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

image = Image.open("crocodile2.png")

img = ImageTk.PhotoImage(image)
#########################顯示圖片#####################
# 在畫布上顯示圖,設定的圖片中心點座標為300,300
my_img = canvas.create_image(300, 300, image=img)
#######################運行應用程式########################
# 開始執行主迴圈等待用戶操
windows.mainloop()
