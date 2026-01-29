# -*- coding: utf-8 -*-
"""
下载汉字笔顺数据
数据来源: hanzi-writer-data (基于 Make Me a Hanzi 项目)
"""
import os
import json
import urllib.request
import urllib.parse

# 需要下载的汉字列表 (52个精选汉字)
CHARS = [
    # 初级 (16个)
    '日', '天', '月', '风', '爸', '妈', '宝', '姐',
    '开', '关', '地', '里', '他', '工', '儿', '老',
    # 中级 (16个)
    '好', '饭', '看', '玩', '叔', '自', '姑', '娘',
    '火', '土', '水', '电', '木', '比', '图', '树',
    # 高级 (20个)
    '一', '三', '四', '五', '羊', '白', '牛', '鼠',
    '心', '可', '说', '两', '男', '你', '不', '子',
    '在', '头', '我', '房'
]

# 输出目录
OUTPUT_DIR = "stroke_data"

def download_char_data(char):
    """下载单个汉字的笔顺数据"""
    # URL编码汉字
    encoded = urllib.parse.quote(char)
    url = f"https://raw.githubusercontent.com/chanind/hanzi-writer-data/master/data/{encoded}.json"
    
    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            data = json.loads(response.read().decode('utf-8'))
            return data
    except Exception as e:
        print(f"  下载失败 {char}: {e}")
        return None

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    print("下载汉字笔顺数据...")
    print(f"共 {len(CHARS)} 个汉字")
    print()
    
    all_data = {}
    
    for i, char in enumerate(CHARS):
        print(f"[{i+1}/{len(CHARS)}] 下载: {char}")
        data = download_char_data(char)
        if data:
            all_data[char] = data
            print(f"  成功! {len(data.get('medians', []))} 笔")
        else:
            print(f"  失败!")
    
    # 保存为单个JSON文件
    output_file = os.path.join(OUTPUT_DIR, "all_strokes.json")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_data, f, ensure_ascii=False, indent=2)
    
    print()
    print(f"完成! 成功下载 {len(all_data)} 个汉字")
    print(f"数据保存到: {output_file}")

if __name__ == "__main__":
    main()
