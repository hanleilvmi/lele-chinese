# -*- coding: utf-8 -*-
"""
一键打包脚本
将乐乐学习乐园打包成EXE可执行文件
"""

import os
import subprocess
import shutil

def build():
    print("=" * 50)
    print("乐乐学习乐园 - 打包工具")
    print("=" * 50)
    
    # 检查 PyInstaller
    try:
        import PyInstaller
        print("✓ PyInstaller 已安装")
    except ImportError:
        print("✗ PyInstaller 未安装，正在安装...")
        subprocess.run(["pip", "install", "pyinstaller"], check=True)
        print("✓ PyInstaller 安装完成")
    
    # 打包命令
    cmd = [
        "pyinstaller",
        "--onefile",           # 单文件
        "--windowed",          # 无控制台窗口
        "--name", "乐乐学习乐园",
        "--add-data", "voice_config_shared.py;.",
        "--add-data", "learning_data.py;.",
        "--add-data", "learning_base.py;.",
        "--add-data", "word_database.py;.",
        "--add-data", "drawing_utils.py;.",
        "--add-data", "kids_game_v3.py;.",
        "--add-data", "kids_pinyin.py;.",
        "--add-data", "kids_math.py;.",
        "--add-data", "kids_english.py;.",
        "--add-data", "kids_thinking.py;.",
        "--add-data", "kids_vehicles.py;.",
        "--hidden-import", "edge_tts",
        "--hidden-import", "pygame",
        "--hidden-import", "pypinyin",
        "--clean",
        "kids_learning_main.py"
    ]
    
    print("\n正在打包，请稍候...")
    print("（首次打包可能需要几分钟）\n")
    
    try:
        subprocess.run(cmd, check=True)
        print("\n" + "=" * 50)
        print("✓ 打包成功！")
        print("=" * 50)
        print(f"\n输出文件: dist/乐乐学习乐园.exe")
        
        # 复制音频文件夹
        if os.path.exists("audio"):
            dest_audio = os.path.join("dist", "audio")
            if os.path.exists(dest_audio):
                shutil.rmtree(dest_audio)
            shutil.copytree("audio", dest_audio)
            print("✓ 已复制 audio 文件夹到 dist/")
        
        # 复制配置文件
        for f in ["voice_config.json", "字库模板.txt"]:
            if os.path.exists(f):
                shutil.copy(f, "dist/")
                print(f"✓ 已复制 {f} 到 dist/")
        
        print("\n分发时请将 dist/ 文件夹整体打包给用户")
        print("用户双击 乐乐学习乐园.exe 即可运行")
        
    except subprocess.CalledProcessError as e:
        print(f"\n✗ 打包失败: {e}")
        print("请检查是否安装了所有依赖库")

if __name__ == "__main__":
    build()
