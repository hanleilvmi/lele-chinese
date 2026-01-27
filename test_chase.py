# -*- coding: utf-8 -*-
"""测试新版阿奇绘图效果"""
import tkinter as tk
from theme_drawings import ThemeDrawings

root = tk.Tk()
root.title("阿奇预览 - 超精细版")
root.geometry("600x500")
root.configure(bg="#87CEEB")

canvas = tk.Canvas(root, width=550, height=450, bg="#E3F2FD", highlightthickness=2)
canvas.pack(pady=20)

# 画背景
canvas.create_rectangle(0, 350, 550, 450, fill="#228B22", outline="")

# 画不同大小的阿奇
canvas.create_text(100, 30, text="小", font=("微软雅黑", 12))
ThemeDrawings.draw_puppy_chase(canvas, 100, 200, 0.6)

canvas.create_text(280, 30, text="中", font=("微软雅黑", 12))
ThemeDrawings.draw_puppy_chase(canvas, 280, 200, 1.0)

canvas.create_text(450, 30, text="大", font=("微软雅黑", 12))
ThemeDrawings.draw_puppy_chase(canvas, 450, 200, 1.3)

tk.Label(root, text="🐾 阿奇 - 超精细版 🐾", font=("微软雅黑", 16, "bold"), 
         bg="#87CEEB", fg="#1976D2").pack()

root.mainloop()
