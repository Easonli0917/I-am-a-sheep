import tkinter as tk
from PIL import Image, ImageDraw, ImageTk


# =========================
# 建立平滑圓形圖片
# =========================
def create_circle_image(color, size=40):

    scale = 8

    img = Image.new("RGBA", (size * scale, size * scale), (255, 255, 255, 0))

    draw = ImageDraw.Draw(img)

    draw.ellipse(
        (0, 0, size * scale - 1, size * scale - 1),
        fill=color,
        outline="black",
        width=scale,
    )

    img = img.resize((size, size), Image.LANCZOS)

    return ImageTk.PhotoImage(img)


# =========================
# 主視窗
# =========================
root = tk.Tk()
root.title("圓形切換器")
root.geometry("1400x650")
root.configure(bg="white")


# =========================
# 建立圖片
# =========================
images = {
    "black": create_circle_image("black"),
    "white": create_circle_image("white"),
    "gray": create_circle_image("gray"),
}


# =========================
# 儲存所有圓形
# =========================
circles = []


# =========================
# 點擊切換顏色
# =========================
def toggle_circle(label):

    if label.current_color == "gray":
        label.current_color = label.original_color
    else:
        label.current_color = "gray"

    label.config(image=images[label.current_color])


# =========================
# 建立圓形
# =========================
def make_circle(parent, color):

    label = tk.Label(parent, image=images[color], bd=0, bg="white")

    label.original_color = color
    label.current_color = color

    label.bind("<Button-1>", lambda event, l=label: toggle_circle(l))

    circles.append(label)

    return label


# =========================
# 恢復原狀
# =========================
def reset_all():

    for circle in circles:

        circle.current_color = circle.original_color

        circle.config(image=images[circle.original_color])


# =========================
# 中央容器
# =========================
main_frame = tk.Frame(root, bg="white")

main_frame.place(relx=0.5, rely=0.5, anchor="center")


# =========================
# 第一排 18 個黑色圓形
# =========================
row1 = tk.Frame(main_frame, bg="white")
row1.pack(pady=15)

for i in range(18):

    make_circle(row1, "black").pack(side="left", padx=4)


# =========================
# 第二排 26 個白色圓形
# =========================
row2 = tk.Frame(main_frame, bg="white")
row2.pack(pady=15)

for i in range(26):

    make_circle(row2, "white").pack(side="left", padx=4)


# =========================
# 恢復原狀按鈕
# =========================
reset_button = tk.Button(
    main_frame,
    text="恢復原狀",
    font=("微軟正黑體", 16, "bold"),
    width=12,
    height=2,
    command=reset_all,
)

reset_button.pack(pady=25)


# =========================
# 執行程式
# =========================
root.mainloop()
