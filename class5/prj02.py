#######################匯入模組#######################
from ttkbootstrap import *
import sys
import os
from tkinter import filedialog
from PIL import Image, ImageTk


#######################定義函數########################
def open_file():
    global file_path
    file_path = filedialog.askopenfilename(initialdir=sys.path[0])
    label2.config(text=file_path)


def show_image():
    global file_path
    image = Image.open(file_path)
    image2 = image.resize((canvas.winfo_width(), canvas.winfo_height()), Image.LANCZOS)
    Photo = ImageTk.PhotoImage(image2)
    canvas.create_image(0, 0, image=Photo, anchor="nw")
    canvas.image = Photo


#######################建立視窗########################
Window = Tk()
Window.title("I-am-a-sheep")
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
label = Label(Window, text="選擇檔案")
label.grid(row=0, column=0, sticky="E")
label2 = Label(Window, text="無")
label2.grid(row=0, column=1, sticky="E")
########################建立按鈕##########################
button = Button(Window, text="瀏覽", command=open_file, style="yaya.TButton")
button.grid(row=0, column=2, sticky="W")
button2 = Button(Window, text="顯示", command=show_image, style="yaya.TButton")
button2.grid(row=1, column=0, columnspan=3, sticky="EW")
canvas = Canvas(Window, width=600, height=600)
canvas.grid(row=2, column=0, columnspan=3)
#########################運行應用程式###################
Window.mainloop()
