# -*- coding: utf-8 -*-
import tkinter as tk
import random

try:
    from theme_drawings import ThemeDrawings
    from theme_config import THEME, ThemeHelper
    DRAWINGS_AVAILABLE = True
except ImportError:
    DRAWINGS_AVAILABLE = False

def show_theme_selector(parent, callback=None):
    dialog = tk.Toplevel(parent)
    dialog.title("汪汪队主题")
    dialog.geometry("700x550")
    dialog.configure(bg="#E3F2FD")
    tk.Label(dialog, text="汪汪队主题风格", font=("微软雅黑", 20, "bold"), bg="#E3F2FD", fg="#1565C0").pack(pady=15)
    if DRAWINGS_AVAILABLE:
        canvas = tk.Canvas(dialog, width=650, height=280, bg="#87CEEB")
        canvas.pack(pady=10)
        canvas.create_rectangle(0, 200, 650, 280, fill="#81C784", outline="")
        ThemeDrawings.draw_puppy_chase(canvas, 100, 160, 0.7)
        ThemeDrawings.draw_puppy_marshall(canvas, 220, 160, 0.7)
        ThemeDrawings.draw_puppy_skye(canvas, 340, 160, 0.7)
        ThemeDrawings.draw_puppy_rubble(canvas, 460, 160, 0.7)
        ThemeDrawings.draw_puppy_rocky(canvas, 580, 160, 0.7)
    tk.Button(dialog, text="太棒了！", font=("微软雅黑", 12), bg="#4CAF50", fg="white", command=dialog.destroy).pack(pady=20)

def show_character_picker(parent, callback=None):
    dialog = tk.Toplevel(parent)
    dialog.title("选择角色")
    dialog.geometry("800x500")
    dialog.configure(bg="#E3F2FD")
    tk.Label(dialog, text="选择你喜欢的狗狗", font=("微软雅黑", 18, "bold"), bg="#E3F2FD", fg="#1565C0").pack(pady=15)
    tk.Button(dialog, text="关闭", command=dialog.destroy).pack(pady=20)

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("400x300")
    tk.Button(root, text="显示主题", command=lambda: show_theme_selector(root)).pack(pady=20)
    root.mainloop()
