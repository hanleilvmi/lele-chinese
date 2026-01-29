# -*- coding: utf-8 -*-
"""
下载汉字笔顺数据
数据来源: hanzi-writer-data (基于 Make Me a Hanzi 项目)
"""
import os
import json
import urllib.request
import urllib.parse

# 需要下载的汉字列表
CHARS = [
    '人', '口', '手', '足', '日', '月', '水', '火', '山', '石', '田', '土',
    '大', '小', '上', '下', '左', '右', '天', '地', '花', '草', '树', '鸟',
    '爸', '妈', '爷', '奶', '哥', '姐', '弟', '妹', '吃', '喝', '看', '听'
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
