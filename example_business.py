#!/usr/bin/env python3
"""
示例插件业务逻辑

该文件包含示例插件的业务逻辑，演示了如何使用FastX-Tui插件接口实现业务功能。
"""
import time
from typing import Any
from core.menu_system import MenuSystem, ActionItem, CommandType

class ExampleBusiness:
    """示例插件业务逻辑类
    
    该类包含示例插件的业务逻辑，包括：
    - 初始化业务逻辑
    - 注册插件命令到菜单系统
    - 实现Hello World命令
    - 实现配置演示命令
    - 清理业务逻辑资源
    """
    
    def __init__(self, plugin):
        """初始化业务逻辑
        
        Args:
            plugin: 插件实例，用于访问插件的配置、日志等功能
        """
        self.plugin = plugin
        self.logger = plugin.logger
        
        # 初始化配置
        self.greeting_message = "Hello from Example Plugin!"
        self.show_timestamp = True
        self.log_level = "INFO"
    
    def initialize(self):
        """初始化业务逻辑
        
        从配置中获取初始化参数，并记录初始化日志。
        """
        # 从配置中获取初始化参数
        self.greeting_message = self.plugin.get_config("greeting_message", "Hello from Example Plugin!")
        self.show_timestamp = self.plugin.get_config("show_timestamp", True)
        self.log_level = self.plugin.get_config("log_level", "INFO")
        
        self.plugin.log_info(f"示例插件初始化完成，问候语: {self.greeting_message}")
        self.plugin.log_info(f"显示时间戳: {self.show_timestamp}")
        self.plugin.log_info(f"日志级别: {self.log_level}")
    
    def register_commands(self, menu_system: MenuSystem):
        """注册插件命令到菜单系统
        
        将插件的命令和菜单注册到菜单系统中。
        
        Args:
            menu_system: 菜单系统实例，用于注册插件的命令和菜单
        """
        # 创建主菜单
        main_menu = menu_system.create_submenu(
            menu_id="example_plugin_menu",
            name="示例插件",
            description="演示插件的功能"
        )
        
        # 注册Hello World命令
        menu_system.register_item(ActionItem(
            id="example_hello",
            name="Hello World",
            description="演示基本命令执行",
            command_type=CommandType.PYTHON,
            python_func=self.hello_world,
            category="示例"
        ))
        
        # 注册配置演示命令
        menu_system.register_item(ActionItem(
            id="example_config",
            name="配置演示",
            description="演示如何使用插件配置",
            command_type=CommandType.PYTHON,
            python_func=self.config_demo,
            category="示例"
        ))
        
        # 将命令添加到菜单
        main_menu.add_item("example_hello")
        main_menu.add_item("example_config")
        
        # 将菜单添加到主菜单
        main_menu_id = "main_menu"
        main_menu_item = menu_system.get_item_by_id(main_menu_id)
        if main_menu_item and hasattr(main_menu_item, "add_item"):
            main_menu_item.add_item("example_plugin_menu")
    
    def hello_world(self) -> str:
        """演示基本命令执行
        
        返回一个包含问候信息、时间戳和插件版本的字符串。
        
        Returns:
            str: 包含问候信息、时间戳和插件版本的字符串
        """
        # 获取配置
        greeting = self.plugin.get_config("greeting_message", "Hello World!")
        show_timestamp = self.plugin.get_config("show_timestamp", True)
        
        # 构建响应
        result = f"{greeting}\n"
        if show_timestamp:
            result += f"当前时间: {time.strftime('%Y-%m-%d %H:%M:%S')}\n"
        result += f"插件版本: {self.plugin.get_info().version}\n"
        result += "命令执行成功!"
        
        return result
    
    def config_demo(self) -> str:
        """演示如何使用插件配置
        
        返回一个包含当前配置信息的字符串。
        
        Returns:
            str: 包含当前配置信息的字符串
        """
        # 获取所有配置
        greeting = self.plugin.get_config("greeting_message", "Default Greeting")
        show_timestamp = self.plugin.get_config("show_timestamp", True)
        log_level = self.plugin.get_config("log_level", "INFO")
        enabled = self.plugin.get_config("enabled", True)
        
        # 构建响应
        result = "配置演示\n\n"
        result += "当前配置:\n"
        result += f"- 问候信息: {greeting}\n"
        result += f"- 显示时间戳: {'是' if show_timestamp else '否'}\n"
        result += f"- 日志级别: {log_level}\n"
        result += f"- 插件启用: {'是' if enabled else '否'}\n"
        result += "\n配置读取成功!"
        
        return result
    
    def cleanup(self):
        """清理业务逻辑资源
        
        清理业务逻辑使用的资源，并记录清理日志。
        """
        self.plugin.log_info("示例插件业务逻辑清理完成")