# -*- coding: utf-8 -*-
"""
UI 配置模块 v1.0
统一管理界面配置，方便适配不同平台（桌面/平板）

使用方法：
    from ui_config import UI, get_font, get_path
    
    # 获取字体
    font = get_font("title")  # 返回 ("微软雅黑", 28, "bold")
    
    # 获取按钮大小
    btn_size = UI.BTN_LARGE  # 返回 (width, height)
    
    # 获取跨平台路径
    path = get_path("audio/praise")
"""

import os
import sys
import platform

# =====================================================
# 平台检测
# =====================================================
def get_platform():
    """检测当前运行平台"""
    system = platform.system().lower()
    
    # 检测安卓（Pydroid/Kivy环境）
    if 'android' in sys.platform or os.environ.get('ANDROID_ROOT'):
        return 'android'
    elif system == 'windows':
        return 'windows'
    elif system == 'darwin':
        return 'macos'
    elif system == 'linux':
        return 'linux'
    else:
        return 'unknown'

PLATFORM = get_platform()
IS_MOBILE = PLATFORM == 'android'

# =====================================================
# 屏幕和缩放配置
# =====================================================
class ScreenConfig:
    """屏幕配置"""
    
    # 默认设计尺寸（桌面）
    DESIGN_WIDTH = 1050
    DESIGN_HEIGHT = 800
    
    # 缩放因子（平板上可能需要调整）
    SCALE = 1.0 if not IS_MOBILE else 1.2
    
    @classmethod
    def get_window_size(cls):
        """获取窗口大小"""
        if IS_MOBILE:
            # 移动端全屏
            return None, None
        return cls.DESIGN_WIDTH, cls.DESIGN_HEIGHT
    
    @classmethod
    def scale(cls, value):
        """缩放数值"""
        if isinstance(value, (int, float)):
            return int(value * cls.SCALE)
        return value

# =====================================================
# 字体配置
# =====================================================
class FontConfig:
    """字体配置"""
    
    # 中文字体（按优先级）
    CN_FONTS = ["微软雅黑", "PingFang SC", "Noto Sans CJK SC", "SimHei", "Arial Unicode MS"]
    
    # 楷体（用于汉字显示）
    KAI_FONTS = ["楷体", "KaiTi", "STKaiti", "Noto Serif CJK SC"]
    
    # Emoji 字体
    EMOJI_FONTS = ["Segoe UI Emoji", "Apple Color Emoji", "Noto Color Emoji"]
    
    # 英文字体
    EN_FONTS = ["Arial", "Helvetica", "sans-serif"]
    
    @classmethod
    def get_cn_font(cls):
        """获取可用的中文字体"""
        # TODO: 实际检测系统字体
        return cls.CN_FONTS[0]
    
    @classmethod
    def get_kai_font(cls):
        """获取楷体字体"""
        return cls.KAI_FONTS[0]
    
    @classmethod
    def get_emoji_font(cls):
        """获取 Emoji 字体"""
        return cls.EMOJI_FONTS[0]

# 字体大小配置（基础大小，会根据 SCALE 缩放）
FONT_SIZES = {
    # 标题
    "title_large": 32,
    "title": 26,
    "title_small": 20,
    
    # 正文
    "body_large": 18,
    "body": 14,
    "body_small": 12,
    
    # 汉字显示
    "char_huge": 140,    # 认字卡片
    "char_large": 80,    # 故事模式
    "char_medium": 50,   # 选项按钮
    "char_small": 36,    # 小卡片
    
    # 按钮
    "btn_large": 16,
    "btn": 14,
    "btn_small": 11,
    
    # Emoji
    "emoji_huge": 100,
    "emoji_large": 60,
    "emoji_medium": 40,
    "emoji_small": 24,
}

def get_font(style, bold=False, scale=True):
    """获取字体配置
    
    Args:
        style: 字体样式名称
        bold: 是否加粗
        scale: 是否应用缩放
    
    Returns:
        (font_family, size, weight) 元组
    """
    # 确定字体族
    if style.startswith("char"):
        family = FontConfig.get_kai_font()
    elif style.startswith("emoji"):
        family = FontConfig.get_emoji_font()
    else:
        family = FontConfig.get_cn_font()
    
    # 获取大小
    size = FONT_SIZES.get(style, 14)
    if scale:
        size = ScreenConfig.scale(size)
    
    # 确定粗细
    weight = "bold" if bold or "title" in style else "normal"
    
    return (family, size, weight)

def get_font_tuple(family, size, bold=False, scale=True):
    """直接获取字体元组
    
    Args:
        family: "cn" / "kai" / "emoji" / "en"
        size: 字体大小
        bold: 是否加粗
        scale: 是否应用缩放
    """
    families = {
        "cn": FontConfig.get_cn_font(),
        "kai": FontConfig.get_kai_font(),
        "emoji": FontConfig.get_emoji_font(),
        "en": "Arial"
    }
    
    font_family = families.get(family, FontConfig.get_cn_font())
    if scale:
        size = ScreenConfig.scale(size)
    weight = "bold" if bold else "normal"
    
    return (font_family, size, weight)

# =====================================================
# 按钮和控件尺寸
# =====================================================
class UI:
    """UI 尺寸配置"""
    
    # 最小触控区域（适配触屏）
    MIN_TOUCH_SIZE = 48 if IS_MOBILE else 32
    
    # 按钮尺寸 (width, height) - 字符单位
    BTN_HUGE = (10, 4)      # 超大按钮
    BTN_LARGE = (8, 3)      # 大按钮
    BTN_MEDIUM = (6, 2)     # 中等按钮
    BTN_SMALL = (4, 1)      # 小按钮
    
    # 按钮内边距
    BTN_PADX = 15 if IS_MOBILE else 10
    BTN_PADY = 10 if IS_MOBILE else 6
    
    # 间距
    SPACING_LARGE = 20
    SPACING_MEDIUM = 12
    SPACING_SMALL = 6
    
    # 边框
    BORDER_WIDTH = 4 if IS_MOBILE else 3
    
    # 圆角（Tkinter 不支持，但 Kivy 需要）
    BORDER_RADIUS = 10
    
    # 汉字选项按钮（答题用）
    CHAR_BTN_WIDTH = 4 if IS_MOBILE else 3
    CHAR_BTN_HEIGHT = 2 if IS_MOBILE else 1
    CHAR_BTN_FONT_SIZE = 45 if IS_MOBILE else 50
    
    # 游戏模式卡片
    MODE_CARD_WIDTH = 8 if IS_MOBILE else 7
    MODE_CARD_HEIGHT = 4 if IS_MOBILE else 3
    
    @classmethod
    def get_btn_size(cls, size="medium"):
        """获取按钮尺寸"""
        sizes = {
            "huge": cls.BTN_HUGE,
            "large": cls.BTN_LARGE,
            "medium": cls.BTN_MEDIUM,
            "small": cls.BTN_SMALL
        }
        return sizes.get(size, cls.BTN_MEDIUM)

# =====================================================
# 颜色配置
# =====================================================
class Colors:
    """颜色配置"""
    
    # 主题色
    PRIMARY = "#FF6B6B"      # 主色（红色）
    SECONDARY = "#4ECDC4"    # 次色（青色）
    ACCENT = "#FFD93D"       # 强调色（黄色）
    
    # 功能色
    SUCCESS = "#4CAF50"      # 成功（绿色）
    WARNING = "#FF9800"      # 警告（橙色）
    ERROR = "#F44336"        # 错误（红色）
    INFO = "#2196F3"         # 信息（蓝色）
    
    # 背景色
    BG_PRIMARY = "#FFF8E1"   # 主背景（米黄）
    BG_SECONDARY = "#FFFFFF" # 次背景（白色）
    BG_CARD = "#FFFFFF"      # 卡片背景
    
    # 文字色
    TEXT_PRIMARY = "#333333"
    TEXT_SECONDARY = "#666666"
    TEXT_HINT = "#999999"
    TEXT_WHITE = "#FFFFFF"
    
    # 掌握度颜色
    MASTERY_NEW = "#FF6B6B"      # 生疏
    MASTERY_LEARNING = "#FF9800" # 学习中
    MASTERY_FAMILIAR = "#FFD700" # 熟悉
    MASTERY_MASTERED = "#4CAF50" # 掌握
    
    # 游戏模式颜色
    MODE_COLORS = [
        "#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4",
        "#DDA0DD", "#FFD93D", "#FF9800", "#8BC34A", "#E91E63"
    ]
    
    # 选项按钮颜色
    OPTION_COLORS = ["#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4"]

# =====================================================
# 路径管理
# =====================================================
# 应用根目录
if getattr(sys, 'frozen', False):
    # 打包后的路径
    APP_ROOT = os.path.dirname(sys.executable)
else:
    # 开发环境路径
    APP_ROOT = os.path.dirname(os.path.abspath(__file__))

def get_path(*parts):
    """获取跨平台路径
    
    Args:
        *parts: 路径部分，如 "audio", "praise"
    
    Returns:
        完整的绝对路径
    
    Example:
        get_path("audio", "praise")  # 返回 /path/to/app/audio/praise
    """
    return os.path.join(APP_ROOT, *parts)

def get_data_path(filename):
    """获取数据文件路径（用于保存用户数据）
    
    在安卓上会使用应用数据目录
    """
    if IS_MOBILE:
        # 安卓数据目录
        data_dir = os.environ.get('ANDROID_DATA', APP_ROOT)
        return os.path.join(data_dir, filename)
    else:
        return os.path.join(APP_ROOT, filename)

def ensure_dir(path):
    """确保目录存在"""
    dir_path = os.path.dirname(path) if os.path.splitext(path)[1] else path
    if dir_path and not os.path.exists(dir_path):
        os.makedirs(dir_path, exist_ok=True)

# =====================================================
# 便捷函数
# =====================================================
def create_button_style(color, size="medium"):
    """创建按钮样式配置
    
    Returns:
        dict: 可以直接传给 tk.Button 的配置
    """
    w, h = UI.get_btn_size(size)
    return {
        "bg": color,
        "fg": Colors.TEXT_WHITE,
        "font": get_font("btn_large" if size == "large" else "btn", bold=True),
        "width": w,
        "height": h,
        "relief": "raised",
        "bd": UI.BORDER_WIDTH,
        "cursor": "hand2",
        "activebackground": color,
    }

def create_label_style(style="body", color=None, bg=None):
    """创建标签样式配置"""
    return {
        "font": get_font(style),
        "fg": color or Colors.TEXT_PRIMARY,
        "bg": bg or Colors.BG_PRIMARY,
    }

# =====================================================
# 调试信息
# =====================================================
def print_config():
    """打印当前配置（调试用）"""
    print(f"平台: {PLATFORM}")
    print(f"移动端: {IS_MOBILE}")
    print(f"缩放: {ScreenConfig.SCALE}")
    print(f"应用目录: {APP_ROOT}")
    print(f"中文字体: {FontConfig.get_cn_font()}")
    print(f"楷体: {FontConfig.get_kai_font()}")

if __name__ == "__main__":
    print_config()
