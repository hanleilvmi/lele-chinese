# -*- coding: utf-8 -*-
"""
打包识字乐园项目用于Android编译
运行: python pack_for_android.py
"""
import zipfile
import os

def pack_project():
    """打包项目文件"""
    zip_name = 'lele_chinese.zip'
    
    # 需要打包的文件
    files_to_pack = [
        # 主程序
        'ui_kivy/chinese_app.py',
        'ui_kivy/font_config.py',
        'ui_kivy/audio_kivy.py',
        'ui_kivy/__init__.py',
        
        # 核心模块
        'core/data_chinese.py',
        'core/game_logic.py',
        'core/audio_interface.py',
        'core/__init__.py',
        
        # 语音配置
        'voice_config_shared.py',
        
        # 编译配置
        'buildozer_chinese.spec',
    ]
    
    # 创建__init__.py如果不存在
    for init_file in ['ui_kivy/__init__.py', 'core/__init__.py']:
        if not os.path.exists(init_file):
            os.makedirs(os.path.dirname(init_file), exist_ok=True)
            with open(init_file, 'w') as f:
                f.write('# -*- coding: utf-8 -*-\n')
    
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zf:
        for file_path in files_to_pack:
            if os.path.exists(file_path):
                # 保持目录结构
                zf.write(file_path, file_path)
                print(f'已添加: {file_path}')
            else:
                print(f'警告: 文件不存在 {file_path}')
        
        # 重命名buildozer配置
        if os.path.exists('buildozer_chinese.spec'):
            zf.write('buildozer_chinese.spec', 'buildozer.spec')
            print('已添加: buildozer.spec (从 buildozer_chinese.spec)')
    
    print(f'\n打包完成: {zip_name}')
    print(f'文件大小: {os.path.getsize(zip_name) / 1024:.1f} KB')
    print('\n下一步:')
    print('1. 上传 lele_chinese.zip 到 Google Colab')
    print('2. 运行 build_android_colab.ipynb 中的代码')
    print('3. 下载生成的 APK 文件')

if __name__ == '__main__':
    pack_project()
