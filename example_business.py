#!/usr/bin/env python3
"""
示例插件业务逻辑

该文件包含示例插件的业务逻辑，演示了如何使用FastX-Tui插件接口实现业务功能。
"""
import os
import sys
import time

from core.menu_system import ActionItem, CommandType, MenuSystem

# 添加demo目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))  # 添加项目根目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), 'FastX-Tui-Plugin-Example'))  # 添加插件目录到路径

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

        # 创建Rich Demo子菜单
        rich_demo_menu = menu_system.create_submenu(
            menu_id="rich_demo_menu",
            name="Rich演示",
            description="演示Rich库的各种功能"
        )

        # 注册Rich Demo命令
        rich_demos = [
            ("rich_code_execution_monitor", "代码执行监控", "演示实时代码执行监控界面", self.rich_code_execution_monitor),
            ("rich_components_view", "Rich组件演示", "演示Rich库的各种组件", self.rich_components_view),
            ("rich_layout_nav", "布局导航", "演示带路由功能的布局导航系统", self.rich_layout_nav),
            ("rich_log_execution_monitor", "日志执行监控", "演示实时日志监控系统", self.rich_log_execution_monitor),
            ("rich_minimal_monitor_1", "简约监控1", "使用Status组件创建简约任务监控", self.rich_minimal_monitor_1),
            ("rich_minimal_monitor_2", "简约监控2", "使用Live组件创建实时更新状态栏", self.rich_minimal_monitor_2),
            ("rich_monitor_dashboard", "监控仪表板", "创建多面板系统监控仪表板", self.rich_monitor_dashboard),
            ("rich_panel_table", "面板表格", "演示Panel和Table组件创建脚本管理器", self.rich_panel_table),
            ("rich_parallel_progress", "并行进度条", "创建多任务并行进度条系统", self.rich_parallel_progress)
        ]

        for demo_id, demo_name, demo_desc, demo_func in rich_demos:
            menu_system.register_item(ActionItem(
                id=demo_id,
                name=demo_name,
                description=demo_desc,
                command_type=CommandType.PYTHON,
                python_func=demo_func,
                category="Rich演示"
            ))
            rich_demo_menu.add_item(demo_id)

        # 将命令添加到菜单
        main_menu.add_item("example_hello")
        main_menu.add_item("example_config")
        main_menu.add_item("rich_demo_menu")

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

    # Rich Demo 函数接口
    def rich_code_execution_monitor(self) -> str:
        """代码执行监控演示
        
        演示如何使用Rich库创建实时代码执行监控界面，包括代码高亮、日志输出和状态监控。
        
        Returns:
            str: 命令执行结果
        """
        try:
            from demos.rich.code_execution_monitor import main
            main()
            return "代码执行监控演示完成"
        except Exception as e:
            return f"演示失败: {str(e)}"

    def rich_components_view(self) -> str:
        """Rich组件演示
        
        演示Rich库的各种组件，包括面板、表格、树状结构、布局管理等。
        
        Returns:
            str: 命令执行结果
        """
        try:
            from demos.rich.components_view import main
            main()
            return "Rich组件演示完成"
        except Exception as e:
            return f"演示失败: {str(e)}"

    def rich_layout_nav(self) -> str:
        """布局导航演示
        
        演示如何使用Rich库创建带路由功能的布局导航系统。
        
        Returns:
            str: 命令执行结果
        """
        try:
            from demos.rich.layout_nav import main
            main()
            return "布局导航演示完成"
        except Exception as e:
            return f"演示失败: {str(e)}"

    def rich_log_execution_monitor(self) -> str:
        """日志执行监控
        
        演示如何使用Rich库创建实时日志监控系统。
        
        Returns:
            str: 命令执行结果
        """
        try:
            from demos.rich.log_execution_monitor import main
            main()
            return "日志执行监控演示完成"
        except Exception as e:
            return f"演示失败: {str(e)}"

    def rich_minimal_monitor_1(self) -> str:
        """简约监控1
        
        演示使用Rich库的Status组件创建简约的任务监控。
        
        Returns:
            str: 命令执行结果
        """
        try:
            from demos.rich.minimal_monitor_1 import main
            main()
            return "简约监控1演示完成"
        except Exception as e:
            return f"演示失败: {str(e)}"

    def rich_minimal_monitor_2(self) -> str:
        """简约监控2
        
        演示使用Rich库的Live组件创建实时更新的简约状态栏。
        
        Returns:
            str: 命令执行结果
        """
        try:
            from demos.rich.minimal_monitor_2 import main
            main()
            return "简约监控2演示完成"
        except Exception as e:
            return f"演示失败: {str(e)}"

    def rich_monitor_dashboard(self) -> str:
        """监控仪表板
        
        演示使用Rich库创建多面板的系统监控仪表板。
        
        Returns:
            str: 命令执行结果
        """
        try:
            from demos.rich.monitor_dashboard import main
            main()
            return "监控仪表板演示完成"
        except Exception as e:
            return f"演示失败: {str(e)}"

    def rich_panel_table(self) -> str:
        """面板表格示例
        
        演示使用Rich库的Panel和Table组件创建脚本管理器界面。
        
        Returns:
            str: 命令执行结果
        """
        try:
            from demos.rich.panel_table import main
            main()
            return "面板表格示例演示完成"
        except Exception as e:
            return f"演示失败: {str(e)}"

    def rich_parallel_progress(self) -> str:
        """并行进度条
        
        演示使用Rich库创建多任务并行进度条系统。
        
        Returns:
            str: 命令执行结果
        """
        try:
            from demos.rich.parallel_progress import main
            main()
            return "并行进度条演示完成"
        except Exception as e:
            return f"演示失败: {str(e)}"

    def cleanup(self):
        """清理业务逻辑资源
        
        清理业务逻辑使用的资源，并记录清理日志。
        """
        self.plugin.log_info("示例插件业务逻辑清理完成")
