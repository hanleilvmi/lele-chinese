# -*- coding: utf-8 -*-
"""
配置管理模块 v1.0
统一管理所有配置文件
"""

import os
import json
import threading
from typing import Any, Dict, Optional

try:
    from ui_config import get_data_path, get_path
    UI_CONFIG_AVAILABLE = True
except ImportError:
    UI_CONFIG_AVAILABLE = False


class ConfigManager:
    """统一配置管理器 - 线程安全的单例"""
    
    _instance = None
    _lock = threading.Lock()
    
    # 配置文件定义
    CONFIG_FILES = {
        "voice": "voice_config.json",
        "theme": "theme_settings.json",
        "sound": "sound_settings.json",
        "mastery": "char_mastery.json",
        "progress": "learning_progress.json",
    }
    
    # 默认配置
    DEFAULT_CONFIGS = {
        "voice": {"style": "汪汪队风格"},
        "theme": {"current_theme": "paw_patrol"},
        "sound": {"sound_enabled": True, "music_enabled": False, "volume": 0.8},
        "mastery": {},
    }
    
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
        self._configs: Dict[str, Dict] = {}
        self._dirty: Dict[str, bool] = {}
        self._config_lock = threading.Lock()
        
        # 确定配置目录
        if UI_CONFIG_AVAILABLE:
            self._config_dir = get_path()
        else:
            self._config_dir = os.path.dirname(os.path.abspath(__file__))
    
    def _get_config_path(self, config_name: str) -> str:
        """获取配置文件路径"""
        filename = self.CONFIG_FILES.get(config_name, f"{config_name}.json")
        return os.path.join(self._config_dir, filename)
    
    def load(self, config_name: str) -> Dict:
        """加载配置
        
        Args:
            config_name: 配置名称 (voice, theme, sound, mastery, progress)
        
        Returns:
            配置字典
        """
        with self._config_lock:
            # 如果已加载，直接返回
            if config_name in self._configs:
                return self._configs[config_name].copy()
            
            # 从文件加载
            config_path = self._get_config_path(config_name)
            config = self._load_from_file(config_path)
            
            # 合并默认值
            if config_name in self.DEFAULT_CONFIGS:
                default = self.DEFAULT_CONFIGS[config_name].copy()
                default.update(config)
                config = default
            
            self._configs[config_name] = config
            self._dirty[config_name] = False
            
            return config.copy()
    
    def _load_from_file(self, filepath: str) -> Dict:
        """从文件加载配置"""
        try:
            if os.path.exists(filepath):
                with open(filepath, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except json.JSONDecodeError as e:
            print(f"配置文件格式错误: {filepath}, {e}")
            # 尝试从备份恢复
            backup_path = filepath + ".bak"
            if os.path.exists(backup_path):
                try:
                    with open(backup_path, 'r', encoding='utf-8') as f:
                        return json.load(f)
                except:
                    pass
        except Exception as e:
            print(f"加载配置失败: {filepath}, {e}")
        
        return {}
    
    def save(self, config_name: str, config: Optional[Dict] = None) -> bool:
        """保存配置
        
        Args:
            config_name: 配置名称
            config: 要保存的配置（如果为None，保存缓存的配置）
        
        Returns:
            是否保存成功
        """
        with self._config_lock:
            if config is not None:
                self._configs[config_name] = config.copy()
            
            if config_name not in self._configs:
                return False
            
            config_path = self._get_config_path(config_name)
            return self._save_to_file(config_path, self._configs[config_name])
    
    def _save_to_file(self, filepath: str, config: Dict) -> bool:
        """保存配置到文件（带备份）"""
        try:
            # 创建备份
            if os.path.exists(filepath):
                backup_path = filepath + ".bak"
                try:
                    import shutil
                    shutil.copy2(filepath, backup_path)
                except:
                    pass
            
            # 写入临时文件
            temp_path = filepath + ".tmp"
            with open(temp_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
            
            # 验证
            with open(temp_path, 'r', encoding='utf-8') as f:
                json.load(f)
            
            # 替换原文件
            if os.path.exists(filepath):
                os.remove(filepath)
            os.rename(temp_path, filepath)
            
            return True
        except Exception as e:
            print(f"保存配置失败: {filepath}, {e}")
            return False
    
    def get(self, config_name: str, key: str, default: Any = None) -> Any:
        """获取配置项
        
        Args:
            config_name: 配置名称
            key: 配置键
            default: 默认值
        
        Returns:
            配置值
        """
        config = self.load(config_name)
        return config.get(key, default)
    
    def set(self, config_name: str, key: str, value: Any, auto_save: bool = True) -> None:
        """设置配置项
        
        Args:
            config_name: 配置名称
            key: 配置键
            value: 配置值
            auto_save: 是否自动保存
        """
        with self._config_lock:
            if config_name not in self._configs:
                self.load(config_name)
            
            self._configs[config_name][key] = value
            self._dirty[config_name] = True
        
        if auto_save:
            self.save(config_name)
    
    def save_all(self) -> None:
        """保存所有已修改的配置"""
        with self._config_lock:
            dirty_configs = [name for name, is_dirty in self._dirty.items() if is_dirty]
        
        for config_name in dirty_configs:
            self.save(config_name)
    
    def reload(self, config_name: str) -> Dict:
        """重新加载配置"""
        with self._config_lock:
            if config_name in self._configs:
                del self._configs[config_name]
            if config_name in self._dirty:
                del self._dirty[config_name]
        
        return self.load(config_name)


# 全局配置管理器实例
config_manager = ConfigManager()


# 便捷函数
def get_config(config_name: str) -> Dict:
    """获取配置"""
    return config_manager.load(config_name)

def save_config(config_name: str, config: Dict) -> bool:
    """保存配置"""
    return config_manager.save(config_name, config)

def get_setting(config_name: str, key: str, default: Any = None) -> Any:
    """获取配置项"""
    return config_manager.get(config_name, key, default)

def set_setting(config_name: str, key: str, value: Any) -> None:
    """设置配置项"""
    config_manager.set(config_name, key, value)


# 导出
__all__ = [
    'ConfigManager',
    'config_manager',
    'get_config',
    'save_config',
    'get_setting',
    'set_setting',
]
