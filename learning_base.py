# -*- coding: utf-8 -*-
"""
学习乐园基础模块 v1.0
提供所有学习模块共用的功能：
- 异常处理
- 临时文件清理
- 定时器管理
- 休息提醒
- 退出确认
"""

import os
import tempfile
import glob
import atexit
import threading
import time
from datetime import datetime

# =====================================================
# 临时文件清理管理
# =====================================================

class TempFileManager:
    """临时文件管理器 - 确保TTS音频文件被正确清理"""
    
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        self.temp_dir = tempfile.gettempdir()
        self.created_files = set()
        self._cleanup_lock = threading.Lock()
        
        # 注册退出时清理
        atexit.register(self.cleanup_all)
        
        # 启动定期清理线程
        self._start_periodic_cleanup()
    
    def register_file(self, filepath):
        """注册一个临时文件"""
        with self._cleanup_lock:
            self.created_files.add(filepath)
    
    def unregister_file(self, filepath):
        """取消注册一个临时文件"""
        with self._cleanup_lock:
            self.created_files.discard(filepath)
    
    def cleanup_file(self, filepath):
        """清理单个文件"""
        try:
            if os.path.exists(filepath):
                os.remove(filepath)
            self.unregister_file(filepath)
        except Exception as e:
            print(f"清理文件失败 {filepath}: {e}")
    
    def cleanup_all(self):
        """清理所有注册的临时文件"""
        with self._cleanup_lock:
            files_to_clean = list(self.created_files)
        
        for filepath in files_to_clean:
            self.cleanup_file(filepath)
        
        # 额外清理可能遗留的tts文件
        self._cleanup_orphan_tts_files()
    
    def _cleanup_orphan_tts_files(self):
        """清理可能遗留的TTS临时文件"""
        try:
            pattern = os.path.join(self.temp_dir, "tts_*.mp3")
            for filepath in glob.glob(pattern):
                try:
                    # 只清理超过10分钟的文件
                    if os.path.exists(filepath):
                        file_age = time.time() - os.path.getmtime(filepath)
                        if file_age > 600:  # 10分钟
                            os.remove(filepath)
                except:
                    pass
        except Exception as e:
            print(f"清理遗留TTS文件失败: {e}")
    
    def _start_periodic_cleanup(self):
        """启动定期清理线程"""
        def cleanup_thread():
            while True:
                time.sleep(300)  # 每5分钟清理一次
                self._cleanup_orphan_tts_files()
        
        t = threading.Thread(target=cleanup_thread, daemon=True)
        t.start()


# 全局临时文件管理器实例
temp_file_manager = TempFileManager()


# =====================================================
# 定时器管理
# =====================================================

class TimerManager:
    """定时器管理器 - 确保所有after定时器被正确取消"""
    
    def __init__(self, window):
        self.window = window
        self.timers = set()
        self._lock = threading.Lock()
    
    def after(self, delay, callback):
        """创建一个受管理的定时器"""
        def wrapped_callback():
            with self._lock:
                self.timers.discard(timer_id)
            try:
                callback()
            except Exception as e:
                print(f"定时器回调错误: {e}")
        
        timer_id = self.window.after(delay, wrapped_callback)
        with self._lock:
            self.timers.add(timer_id)
        return timer_id
    
    def cancel(self, timer_id):
        """取消单个定时器"""
        try:
            self.window.after_cancel(timer_id)
            with self._lock:
                self.timers.discard(timer_id)
        except:
            pass
    
    def cancel_all(self):
        """取消所有定时器"""
        with self._lock:
            timers_to_cancel = list(self.timers)
            self.timers.clear()
        
        for timer_id in timers_to_cancel:
            try:
                self.window.after_cancel(timer_id)
            except:
                pass


# =====================================================
# 休息提醒
# =====================================================

class RestReminder:
    """休息提醒管理器"""
    
    def __init__(self, window, interval_minutes=15):
        self.window = window
        self.interval_minutes = interval_minutes
        self.start_time = datetime.now()
        self.last_reminder_time = None
        self.enabled = True
        self._check_timer = None
    
    def start(self):
        """开始休息提醒检查"""
        self._schedule_check()
    
    def stop(self):
        """停止休息提醒检查"""
        if self._check_timer:
            try:
                self.window.after_cancel(self._check_timer)
            except:
                pass
            self._check_timer = None
    
    def _schedule_check(self):
        """安排下一次检查"""
        if self.enabled:
            self._check_timer = self.window.after(60000, self._check_and_remind)  # 每分钟检查
    
    def _check_and_remind(self):
        """检查是否需要提醒休息"""
        if not self.enabled:
            return
        
        elapsed = (datetime.now() - self.start_time).seconds // 60
        
        if elapsed > 0 and elapsed % self.interval_minutes == 0:
            # 检查是否已经提醒过这个时间点
            current_reminder_key = elapsed // self.interval_minutes
            if self.last_reminder_time != current_reminder_key:
                self.last_reminder_time = current_reminder_key
                self._show_reminder(elapsed)
        
        self._schedule_check()
    
    def _show_reminder(self, minutes):
        """显示休息提醒"""
        try:
            from tkinter import messagebox
            messagebox.showinfo(
                "😊 休息一下",
                f"乐乐已经学习了 {minutes} 分钟啦！\n\n"
                "👀 让眼睛休息一下\n"
                "🚶 站起来活动活动\n"
                "💧 喝点水吧！\n\n"
                "休息好了再继续学习哦！"
            )
        except:
            pass
    
    def reset(self):
        """重置计时"""
        self.start_time = datetime.now()
        self.last_reminder_time = None


# =====================================================
# 安全退出
# =====================================================

def confirm_exit(window, on_exit_callback=None):
    """显示退出确认对话框
    
    Args:
        window: Tk窗口
        on_exit_callback: 退出前的回调函数（如保存数据）
    
    Returns:
        bool: 是否确认退出
    """
    from tkinter import messagebox
    
    result = messagebox.askyesno(
        "👋 确认退出",
        "确定要退出学习乐园吗？\n\n学习进度会自动保存哦！",
        icon='question',
        default='yes'
    )
    
    if result:
        if on_exit_callback:
            try:
                on_exit_callback()
            except Exception as e:
                print(f"退出回调错误: {e}")
        
        # 清理临时文件
        temp_file_manager.cleanup_all()
        
        window.quit()
    
    return result


def setup_window_close_handler(window, on_exit_callback=None):
    """设置窗口关闭处理器
    
    Args:
        window: Tk窗口
        on_exit_callback: 退出前的回调函数
    """
    def on_closing():
        confirm_exit(window, on_exit_callback)
    
    window.protocol("WM_DELETE_WINDOW", on_closing)


# =====================================================
# 安全执行包装器
# =====================================================

def safe_execute(func, default=None, error_msg="操作失败"):
    """安全执行函数，捕获异常
    
    Args:
        func: 要执行的函数
        default: 异常时返回的默认值
        error_msg: 错误消息前缀
    
    Returns:
        函数返回值或默认值
    """
    try:
        return func()
    except Exception as e:
        print(f"{error_msg}: {e}")
        return default


def safe_import(module_name, fallback=None):
    """安全导入模块
    
    Args:
        module_name: 模块名
        fallback: 导入失败时的回退值
    
    Returns:
        模块或回退值
    """
    try:
        import importlib
        return importlib.import_module(module_name)
    except ImportError as e:
        print(f"导入模块 {module_name} 失败: {e}")
        return fallback


# =====================================================
# 数据保存优化
# =====================================================

class BatchSaver:
    """批量保存管理器 - 减少频繁IO"""
    
    def __init__(self, save_func, interval_seconds=30):
        """
        Args:
            save_func: 保存函数
            interval_seconds: 保存间隔（秒）
        """
        self.save_func = save_func
        self.interval = interval_seconds
        self.pending_save = False
        self._lock = threading.Lock()
        self._timer = None
        self._last_save = time.time()
        
        # 注册退出时保存
        atexit.register(self.force_save)
    
    def mark_dirty(self):
        """标记数据已修改，需要保存"""
        with self._lock:
            self.pending_save = True
            
            # 如果距离上次保存超过间隔，立即保存
            if time.time() - self._last_save >= self.interval:
                self._do_save()
            elif self._timer is None:
                # 否则安排延迟保存
                self._schedule_save()
    
    def _schedule_save(self):
        """安排延迟保存"""
        def delayed_save():
            with self._lock:
                self._timer = None
                if self.pending_save:
                    self._do_save()
        
        self._timer = threading.Timer(self.interval, delayed_save)
        self._timer.daemon = True
        self._timer.start()
    
    def _do_save(self):
        """执行保存"""
        try:
            self.save_func()
            self.pending_save = False
            self._last_save = time.time()
        except Exception as e:
            print(f"保存数据失败: {e}")
    
    def force_save(self):
        """强制立即保存"""
        with self._lock:
            if self._timer:
                self._timer.cancel()
                self._timer = None
            if self.pending_save:
                self._do_save()


# =====================================================
# 游戏状态管理
# =====================================================

class GameStateManager:
    """游戏状态管理器"""
    
    def __init__(self):
        self.current_game = None
        self.game_running = False
        self.game_data = {}
        self._lock = threading.Lock()
    
    def start_game(self, game_name):
        """开始游戏"""
        with self._lock:
            self.stop_game()  # 先停止当前游戏
            self.current_game = game_name
            self.game_running = True
            self.game_data = {}
    
    def stop_game(self):
        """停止游戏"""
        with self._lock:
            self.game_running = False
            self.current_game = None
            self.game_data = {}
    
    def is_running(self, game_name=None):
        """检查游戏是否在运行"""
        with self._lock:
            if game_name:
                return self.game_running and self.current_game == game_name
            return self.game_running
    
    def set_data(self, key, value):
        """设置游戏数据"""
        with self._lock:
            self.game_data[key] = value
    
    def get_data(self, key, default=None):
        """获取游戏数据"""
        with self._lock:
            return self.game_data.get(key, default)
