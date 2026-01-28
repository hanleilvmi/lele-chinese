# -*- coding: utf-8 -*-
"""
语音预生成脚本
使用Edge TTS生成所有汉字和表扬/鼓励语的mp3文件
生成的文件将打包进APK，让平板也能使用汪汪队风格语音
"""
import os
import asyncio
import edge_tts

# 语音配置
VOICE = "zh-CN-XiaoyiNeural"  # 小艺 - 温柔女声

# 输出目录
OUTPUT_DIR = "audio/generated"

# 汉字列表（从汉字表.txt解析）
def load_characters():
    """从汉字表.txt加载汉字"""
    chars = []
    try:
        with open("汉字表.txt", "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                parts = line.split(",")
                if len(parts) >= 3:
                    char = parts[0].strip()
                    pinyin = parts[1].strip()
                    word = parts[2].strip()
                    chars.append({
                        "char": char,
                        "pinyin": pinyin,
                        "word": word
                    })
    except Exception as e:
        print(f"加载汉字表失败: {e}")
    return chars

# 表扬语列表
PRAISES = [
    "汪汪队，出动！答对啦！",
    "没有困难的工作，只有勇敢的狗狗！",
    "太棒了，乐乐是最勇敢的狗狗！",
    "耶！任务完成！",
    "狗狗们，做得好！",
    "莱德队长为你骄傲！",
    "汪汪汪，你真棒！",
    "阿奇说，乐乐真厉害！",
    "汪汪队需要你这样的小英雄！",
    "阿奇为你点赞！",
    "毛毛说，太酷了！",
    "消防狗狗毛毛为你鼓掌！",
    "毛毛觉得你超级棒！",
    "小砾说，挖掘机都为你欢呼！",
    "工程狗狗小砾给你点赞！",
    "小砾说你是最棒的！",
    "路马说，你像海浪一样厉害！",
    "水上救援成功！路马为你骄傲！",
    "路马说你真是太聪明了！",
    "天天说，你飞得比我还高！",
    "飞行狗狗天天为你欢呼！",
    "天天说你是小天才！",
    "灰灰说，这个问题难不倒你！",
    "环保狗狗灰灰为你点赞！",
    "灰灰说你超级聪明！",
    "乐乐真厉害，给你一个大大的赞！",
    "狗狗们都为你欢呼！",
    "你是汪汪队的荣誉成员！",
    "莱德说，乐乐做得太好了！",
    "汪汪队为你感到骄傲！",
    "你是最棒的小狗狗！",
    "任务完成得太漂亮了！",
    "汪汪队给你颁发勇气勋章！",
]

# 鼓励语列表
ENCOURAGES = [
    "没关系，汪汪队永不放弃！",
    "加油，勇敢的狗狗不怕困难！",
    "再试一次，你一定行！",
    "别担心，汪汪队来帮你！",
    "狗狗们，我们再来一次！",
    "莱德说，失败是成功之母！",
    "阿奇说，再试一次吧！",
    "毛毛说，别灰心，你可以的！",
    "小砾说，我们一起加油！",
    "路马说，大海也有风浪，没关系！",
    "天天说，跌倒了再爬起来！",
    "灰灰说，动动脑筋再想想！",
    "汪汪队相信你！",
    "勇敢的狗狗不怕失败！",
    "没事的，我们再来一次！",
    "加油加油，乐乐最棒！",
]

# 简短表扬语（用于打地鼠等快节奏游戏）
SHORT_PRAISES = ['真棒！', '好！', '对了！', '厉害！', '棒！', '耶！']
SHORT_ENCOURAGES = ['再试！', '加油！', '没事！']

async def generate_audio(text, filename):
    """生成单个音频文件"""
    filepath = os.path.join(OUTPUT_DIR, filename)
    if os.path.exists(filepath):
        print(f"  跳过（已存在）: {filename}")
        return True
    
    try:
        communicate = edge_tts.Communicate(text, VOICE)
        await communicate.save(filepath)
        print(f"  生成: {filename}")
        return True
    except Exception as e:
        print(f"  失败: {filename} - {e}")
        return False

async def main():
    """主函数"""
    # 创建输出目录
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    print("=" * 50)
    print("语音预生成脚本")
    print(f"语音: {VOICE}")
    print(f"输出目录: {OUTPUT_DIR}")
    print("=" * 50)
    
    # 加载汉字
    characters = load_characters()
    print(f"\n加载了 {len(characters)} 个汉字")
    
    # 生成汉字语音
    print("\n[1/4] 生成汉字语音...")
    for item in characters:
        char = item["char"]
        await generate_audio(char, f"char_{char}.mp3")
    
    # 生成拼音语音
    print("\n[2/4] 生成拼音语音...")
    for item in characters:
        char = item["char"]
        pinyin = item["pinyin"]
        await generate_audio(pinyin, f"pinyin_{char}.mp3")
    
    # 生成词组语音
    print("\n[3/4] 生成词组语音...")
    for item in characters:
        char = item["char"]
        word = item["word"]
        await generate_audio(word, f"word_{char}.mp3")
    
    # 生成表扬语
    print("\n[4/4] 生成表扬语和鼓励语...")
    for i, text in enumerate(PRAISES):
        await generate_audio(text, f"praise_{i:02d}.mp3")
    
    for i, text in enumerate(ENCOURAGES):
        await generate_audio(text, f"encourage_{i:02d}.mp3")
    
    # 生成简短表扬语
    print("\n[5/5] 生成简短表扬语和鼓励语...")
    for i, text in enumerate(SHORT_PRAISES):
        await generate_audio(text, f"short_praise_{i:02d}.mp3")
    
    for i, text in enumerate(SHORT_ENCOURAGES):
        await generate_audio(text, f"short_encourage_{i:02d}.mp3")
    
    # 统计
    files = [f for f in os.listdir(OUTPUT_DIR) if f.endswith(".mp3")]
    print("\n" + "=" * 50)
    print(f"完成！共生成 {len(files)} 个音频文件")
    print(f"目录: {os.path.abspath(OUTPUT_DIR)}")
    print("=" * 50)

if __name__ == "__main__":
    asyncio.run(main())
