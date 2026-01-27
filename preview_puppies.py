"""预览所有汪汪队狗狗"""
import tkinter as tk
from theme_drawings import ThemeDrawings

def create_preview():
    root = tk.Tk()
    root.title("汪汪队狗狗预览")
    root.configure(bg="#87CEEB")
    
    # 创建画布
    canvas = tk.Canvas(root, width=1200, height=800, bg="#87CEEB", highlightthickness=0)
    canvas.pack(padx=10, pady=10)
    
    # 标题
    canvas.create_text(600, 30, text="🐾 汪汪队狗狗预览 🐾", font=("微软雅黑", 24, "bold"), fill="#1565C0")
    
    # 狗狗列表和绘制函数
    puppies = [
        ("阿奇 Chase", ThemeDrawings.draw_puppy_chase),
        ("毛毛 Marshall", ThemeDrawings.draw_puppy_marshall),
        ("天天 Skye", ThemeDrawings.draw_puppy_skye),
        ("小砾 Rubble", ThemeDrawings.draw_puppy_rubble),
        ("灰灰 Rocky", ThemeDrawings.draw_puppy_rocky),
        ("路马 Zuma", ThemeDrawings.draw_puppy_zuma),
        ("珠珠 Everest", ThemeDrawings.draw_puppy_everest),
        ("阿克 Tracker", ThemeDrawings.draw_puppy_tracker),
        ("小克 Rex", ThemeDrawings.draw_puppy_rex),
        ("乐乐 Liberty", ThemeDrawings.draw_puppy_liberty),
    ]
    
    # 绘制每只狗狗 (2行5列)
    for i, (name, draw_func) in enumerate(puppies):
        row = i // 5
        col = i % 5
        x = 120 + col * 240
        y = 180 + row * 350
        
        # 背景圆
        canvas.create_oval(x-80, y-90, x+80, y+90, fill="white", outline="#E0E0E0", width=2)
        
        # 绘制狗狗
        draw_func(canvas, x, y, scale=1.2)
        
        # 名字
        canvas.create_text(x, y+120, text=name, font=("微软雅黑", 12, "bold"), fill="#333")
    
    # 保存为图片
    root.update()
    
    # 使用PIL保存
    try:
        from PIL import ImageGrab
        import time
        
        # 获取窗口位置
        root.update_idletasks()
        x = root.winfo_rootx()
        y = root.winfo_rooty()
        w = root.winfo_width()
        h = root.winfo_height()
        
        time.sleep(0.5)
        
        # 截图保存
        img = ImageGrab.grab(bbox=(x, y, x+w, y+h))
        img.save("puppies_preview.png")
        print("✅ 图片已保存为 puppies_preview.png")
    except ImportError:
        print("⚠️ 需要安装 Pillow 来保存图片: pip install Pillow")
        print("窗口将保持打开，您可以手动截图")
    
    root.mainloop()

if __name__ == "__main__":
    create_preview()
