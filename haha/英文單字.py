import tkinter as tk
from tkinter import ttk, messagebox
import random

words = []
questions = []
current_word = None
correct_count = 0
wrong_count = 0
editing_index = None


def add_chat(msg):
    chat.config(state="normal")
    chat.insert(tk.END, msg + "\n")
    chat.config(state="disabled")
    chat.see(tk.END)


def update_stats():
    total = correct_count + wrong_count
    rate = 0 if total == 0 else round(correct_count / total * 100)
    stats_label.config(
        text=f"題庫：{len(words)} 個單字   答對：{correct_count}   答錯：{wrong_count}   正確率：{rate}%"
    )


def add_word():
    chinese = chinese_entry.get().strip()
    english = english_entry.get().strip()

    if not chinese or not english:
        return

    words.append((chinese, english))
    word_listbox.insert(tk.END, f"{chinese} → {english}")

    add_chat(f"📚 已加入單字：{chinese}")

    chinese_entry.delete(0, tk.END)
    english_entry.delete(0, tk.END)

    update_stats()


def load_selected():
    global editing_index

    selected = word_listbox.curselection()
    if not selected:
        return

    editing_index = selected[0]

    chinese_entry.delete(0, tk.END)
    english_entry.delete(0, tk.END)

    chinese_entry.insert(0, words[editing_index][0])
    english_entry.insert(0, words[editing_index][1])


def save_edit():
    global editing_index

    if editing_index is None:
        return

    chinese = chinese_entry.get().strip()
    english = english_entry.get().strip()

    words[editing_index] = (chinese, english)

    word_listbox.delete(editing_index)
    word_listbox.insert(editing_index, f"{chinese} → {english}")

    add_chat(f"✏️ 已修改：{chinese}")

    chinese_entry.delete(0, tk.END)
    english_entry.delete(0, tk.END)

    editing_index = None


def delete_word():
    selected = word_listbox.curselection()
    if not selected:
        return

    index = selected[0]
    word = words[index][0]

    del words[index]
    word_listbox.delete(index)

    add_chat(f"🗑️ 已刪除：{word}")
    update_stats()


def start_quiz():
    global questions

    if not words:
        messagebox.showwarning("提醒", "請先加入單字")
        return

    questions = words.copy()
    random.shuffle(questions)

    add_chat("🚀 測驗開始！")
    next_question()


def next_question():
    global current_word

    if not questions:
        finish_round()
        return

    current_word = questions.pop(0)

    add_chat("🤖 單字老師：")
    add_chat(f"請輸入英文：{current_word[0]}")


def check_answer():
    global correct_count, wrong_count

    if current_word is None:
        return

    answer = answer_entry.get().strip()

    if answer.lower() == current_word[1].lower():
        correct_count += 1
        add_chat("✅ 恭喜答對！")
    else:
        wrong_count += 1
        add_chat(f"❌ 再加油喔！正確答案：{current_word[1]}")

    answer_entry.delete(0, tk.END)

    update_stats()
    root.after(600, next_question)


def finish_round():
    total = correct_count + wrong_count
    rate = 0 if total == 0 else round(correct_count / total * 100)

    result = messagebox.askyesno(
        "完成",
        f"本輪完成！\n\n答對：{correct_count}\n答錯：{wrong_count}\n正確率：{rate}%\n\n按『是』繼續複習\n按『否』重新開始",
    )

    if result:
        continue_review()
    else:
        restart_all()


def continue_review():
    global questions

    questions = words.copy()
    random.shuffle(questions)

    add_chat("🔄 開始新一輪複習")
    next_question()


def restart_all():
    global words, questions, current_word
    global correct_count, wrong_count

    words = []
    questions = []
    current_word = None
    correct_count = 0
    wrong_count = 0

    word_listbox.delete(0, tk.END)

    chat.config(state="normal")
    chat.delete("1.0", tk.END)
    chat.config(state="disabled")

    update_stats()


root = tk.Tk()
root.title("🚀 單字冒險王 🚀")
root.geometry("900x700")
root.configure(bg="#E3F2FD")
root.resizable(False, False)

title = tk.Label(
    root,
    text="🚀 單字冒險王 🚀",
    font=("微軟正黑體", 24, "bold"),
    bg="#E3F2FD",
    fg="#1565C0",
)
title.pack(pady=10)

stats_label = tk.Label(root, text="", font=("微軟正黑體", 11), bg="#E3F2FD")
stats_label.pack()

frame = ttk.LabelFrame(root, text="新增 / 修改單字")
frame.pack(fill="x", padx=10, pady=10)

ttk.Label(frame, text="中文").grid(row=0, column=0, padx=5, pady=5)
chinese_entry = ttk.Entry(frame, width=18)
chinese_entry.grid(row=0, column=1)

ttk.Label(frame, text="英文").grid(row=0, column=2, padx=5)
english_entry = ttk.Entry(frame, width=18)
english_entry.grid(row=0, column=3)

ttk.Button(frame, text="加入單字", command=add_word).grid(row=0, column=4, padx=5)
ttk.Button(frame, text="載入修改", command=load_selected).grid(row=0, column=5, padx=5)
ttk.Button(frame, text="儲存修改", command=save_edit).grid(row=0, column=6, padx=5)
ttk.Button(frame, text="刪除單字", command=delete_word).grid(row=0, column=7, padx=5)

word_listbox = tk.Listbox(root, height=8, font=("微軟正黑體", 11))
word_listbox.pack(fill="x", padx=10)

ttk.Button(root, text="開始測驗", command=start_quiz).pack(pady=8)

chat = tk.Text(root, height=15, font=("微軟正黑體", 12), bg="white")
chat.pack(fill="both", expand=True, padx=10, pady=10)
chat.config(state="disabled")

answer_frame = ttk.Frame(root)
answer_frame.pack(pady=10)

answer_entry = ttk.Entry(answer_frame, width=35)
answer_entry.grid(row=0, column=0, padx=5)

ttk.Button(answer_frame, text="送出答案", command=check_answer).grid(row=0, column=1)

answer_entry.bind("<Return>", lambda event: check_answer())

update_stats()
root.mainloop()
