#######################匯入模組#######################
from ttkbootstrap import *
import sys
import os

#######################設定工作目錄####################
os.chdir(sys.path[0])


#######################定義函數########################
def show_result():
    entey_text = entry.get()
    try:
        result = eval(entey_text)
    except:
        result = "輸入錯誤"
    label.config(text=result)


#######################建立視窗########################
window = Tk()
window.title("I-am-a-sheep")
#######################設定字形###########################
font_size = 20
window.option_add("*Font", ("Halvetica", font_size))
#######################設定主題###############################
style = Style(theme="cyborg")
style.configure("yaya.TButton", font=("Halvetica", font_size))
######################建立標籤################################ˇ
label = Label(window, text="計算結果")
label.grid(row=2, column=0, columnspan=2, padx=10, pady=10)
########################建立按鈕##########################
button = Button(window, text="顯示計算結果", command=show_result, style="yaya.TButton")
button.grid(row=1, column=0, columnspan=2, padx=10, pady=10)
########################建立Entry物件####################
entry = Entry(window, width=30)
entry.grid(row=0, column=0, columnspan=2, padx=10, pady=10)
#######################運行應用程式########################
window.mainloop()
