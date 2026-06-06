import tkinter as tk
from PIL import Image, ImageDraw, ImageTk


# =========================
# 建立平滑圓形圖片
# =========================
def make_circle(color, size=40):
    scale = 6  # 放大倍率，越大越平滑

    img = Image.new("RGBA", (size * scale, size * scale), (255, 255, 255, 0))

    draw = ImageDraw.Draw(img)

    draw.ellipse(
        (0, 0, size * scale - 1, size * scale - 1),
        fill=color,
        outline="black",
    )

    img = img.resize((size, size), Image.LANCZOS)

    return ImageTk.PhotoImage(img)


# =========================
# 主視窗
# =========================
root = tk.Tk()
root.title("圓形切換器")
root.geometry("900x260")

# 儲存圖片避免被回收
images = {
    "black": make_circle("black"),
    "white": make_circle("white"),
    "gray": make_circle("gray"),
}

circle_labels = []


# =========================
# 點擊切換顏色
# =========================
def toggle(label):
    current = label.current_color

    if current == "gray":
        label.current_color = label.original_color
    else:
        label.current_color = "gray"

    label.config(image=images[label.current_color])


# =========================
# 建立一個圓形
# =========================
def create_circle(parent, color):
    lbl = tk.Label(parent, image=images[color], bd=0, highlightthickness=0)

    lbl.original_color = color
    lbl.current_color = color

    lbl.bind("<Button-1>", lambda e, l=lbl: toggle(l))

    circle_labels.append(lbl)

    return lbl


# =========================
# 第一排
# =========================
row1 = tk.Frame(root)
row1.pack(pady=15)

for i in range(10):
    create_circle(row1, "black").pack(side="left", padx=5)

# =========================
# 第二排
# =========================
row2 = tk.Frame(root)
row2.pack(pady=15)

for i in range(15):
    create_circle(row2, "white").pack(side="left", padx=5)


# =========================
# 恢復原狀
# =========================
def reset_all():
    for lbl in circle_labels:
        lbl.current_color = lbl.original_color
        lbl.config(image=images[lbl.original_color])


btn = tk.Button(root, text="恢復原狀", font=("微軟正黑體", 12), command=reset_all)

btn.pack(pady=10)

root.mainloop()
