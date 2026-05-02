#######################匯入模組#######################
from ttkbootstrap import *
import sys
import os
from PIL import Image, ImageTk

#######################設定工作目錄####################
os.chdir(sys.path[0])


#######################定義函數########################
def on_switch_change():
    check_label.config(text=str(check_type.get()))


#######################建立視窗########################
window = Tk()
window.title("I-am-a-sheep")
######################設定字形######################
font_size = 20
window.option_add("*font", ("Halvetica", font_size))
######################設定主題######################
style = Style(theme="cyborg")
style.configure("yaya.TButton", font=("Halvetica", font_size))
style.configure("yaya.TCheckbutton", font=("Halvetica", font_size))
######################建立變數#########################
check_type = BooleanVar()
check_type.set(True)
######################建立標籤########################
check_label = Label(window, text="True")
check_label.grid(row=1, column=2, padx=10, pady=10)
image = Image.open("weather.png")
img = ImageTk.PhotoImage(image)
img_label = Label(window, image=img)
img_label.grid(row=2, column=1, columnspan=2, padx=10, pady=10)
img_label.image = img
######################建立checkbutton########################
check = Checkbutton(
    window,
    variable=check_type,
    onvalue=True,
    offvalue=False,
    command=on_switch_change,
    style="yaya.TCheckbutton",
)
check.grid(row=1, column=1, padx=10, pady=10)
######################運行應用程式#########################
window.mainloop()
