#!/usr/bin/env python3
"""
FastX-Tui Example Plugin - 入口文件
这个文件是插件的入口，包含插件的配置信息和基本结构
业务逻辑请参考 example_business.py
"""
import os
import json
import toml
from typing import Dict, Any
from core.plugin_manager import Plugin, PluginInfo
from core.menu_system import MenuSystem
from example_business import ExampleBusiness


class ExamplePlugin(Plugin):
    """示例插件，演示如何使用FastX-Tui插件接口

    这是FastX-Tui插件的入口类，所有插件必须继承自Plugin类并实现所有抽象方法。

    必须实现的方法：
    - get_info(): 返回插件信息
    - initialize(): 初始化插件
    - cleanup(): 清理插件资源
    - register(): 注册插件命令到菜单系统

    可选实现的方法：
    - get_binary_path(): 获取插件二进制文件路径
    - get_resource_path(): 获取插件资源文件路径
    """

    def __init__(self):
        """初始化插件"""
        super().__init__()
        self.business = None
    
    @classmethod
    def get_version(cls) -> str:
        """从pyproject.toml获取当前版本号"""
        try:
            # 获取当前文件所在目录
            current_dir = os.path.dirname(os.path.abspath(__file__))
            # 构建pyproject.toml的路径
            pyproject_path = os.path.join(current_dir, "pyproject.toml")
            # 读取文件
            with open(pyproject_path, "r", encoding="utf-8") as f:
                data = toml.load(f)
            # 返回版本号
            return data["project"]["version"]
        except Exception as e:
            # 如果读取失败，返回默认版本
            return "1.0.0"

    def get_info(self) -> PluginInfo:
        """获取插件信息

        必须实现此方法，返回插件的详细信息
        """
        return PluginInfo(
            name="示例插件",
            version=self.get_version(),
            author="FastX Team",
            description="演示如何使用FastX-Tui插件接口，包括插件手册、配置管理和业务逻辑分离",
            category="工具",  # 插件分类
            tags=["示例", "演示", "教程"],  # 插件标签
            compatibility={"fastx-tui": ">=0.1.31"},  # 兼容性要求
            dependencies=[],  # 依赖项
            repository="https://github.com/fastxteam/FastX-Tui-Plugin-Example",  # 插件仓库
            homepage="https://github.com/fastxteam/FastX-Tui-Plugin-Example",  # 插件主页
            license="MIT",  # 许可证
            last_updated="2025-12-27",  # 最后更新时间
            rating=5.0,  # 评分
            downloads=0  # 下载次数
        )

    def initialize(self):
        """初始化插件

        必须实现此方法，用于初始化插件的资源、连接数据库等
        """
        # 初始化业务逻辑
        self.business = ExampleBusiness(self)
        self.business.initialize()
        self.log_info("示例插件初始化完成")

    def cleanup(self):
        """清理插件资源

        必须实现此方法，用于清理插件使用的资源，如关闭连接、释放内存等
        """
        self.log_info("示例插件清理完成")
        # 清理业务逻辑资源
        if self.business:
            self.business.cleanup()
            self.business = None

    def register(self, menu_system: MenuSystem):
        """注册插件命令到菜单系统

        必须实现此方法，用于将插件命令注册到菜单系统中

        参数：
        - menu_system: 菜单系统实例，用于注册命令和菜单
        """
        # 调用业务逻辑注册命令
        self.business.register_commands(menu_system)
        
        # 更新主菜单计数
        self.main_menus_registered += 1
        self.main_menu_id = "example_plugin_menu"

    def get_manual(self) -> str:
        """获取插件手册，返回Markdown格式的帮助内容
        
        Returns:
            str: Markdown格式的插件手册，从manual.md文件中读取
        """
        try:
            # 获取插件目录路径
            if self.plugin_path:
                manual_path = os.path.join(self.plugin_path, "manual.md")
                if os.path.exists(manual_path):
                    with open(manual_path, "r", encoding="utf-8") as f:
                        return f.read()
            # 如果文件不存在或plugin_path未设置，返回默认内容
            return "# 插件手册\n\n该插件未提供帮助文档。"
        except Exception as e:
            self.log_error(f"读取插件手册失败: {e}")
            return "# 插件手册\n\n读取帮助文档失败。"

    def get_config_schema(self) -> Dict[str, Any]:
        """获取插件配置模式，从config_schema.json文件中读取
        
        Returns:
            Dict[str, Any]: 配置项模式，包含配置名、类型、默认值、说明、可选值等
        """
        try:
            # 获取插件目录路径
            if self.plugin_path:
                config_schema_path = os.path.join(self.plugin_path, "config_schema.json")
                if os.path.exists(config_schema_path):
                    with open(config_schema_path, "r", encoding="utf-8") as f:
                        return json.load(f)
            # 如果文件不存在或plugin_path未设置，返回默认配置
            return {
                "enabled": {
                    "type": "boolean",
                    "default": True,
                    "description": "是否启用该插件",
                    "required": True
                }
            }
        except Exception as e:
            self.log_error(f"读取配置模式失败: {e}")
            # 返回默认配置
            return {
                "enabled": {
                    "type": "boolean",
                    "default": True,
                    "description": "是否启用该插件",
                    "required": True
                }
            }

    def get_binary_path(self) -> str:
        """获取插件二进制文件路径

        可选实现此方法，用于返回插件二进制文件的路径
        """
        # 示例：返回bin目录下的example_binary文件
        return self.get_resource_path("../bin/example_binary")