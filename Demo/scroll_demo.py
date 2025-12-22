#!/usr/bin/env python3
"""
带滚动条的帮助系统实现
"""

import sys
from typing import List
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.layout import Layout
from rich.live import Live
from rich import box

if sys.platform == 'win32':
    import msvcrt
else:
    import termios
    import tty


class ScrollablePanel:
    """可滚动面板"""

    def __init__(self, content: str, height: int = 20):
        self.content_lines = content.split('\n')
        self.height = height
        self.scroll_offset = 0
        self.total_lines = len(self.content_lines)

    def scroll_up(self, lines: int = 1):
        """向上滚动"""
        self.scroll_offset = max(0, self.scroll_offset - lines)

    def scroll_down(self, lines: int = 1):
        """向下滚动"""
        self.scroll_offset = min(
            self.total_lines - self.height,
            self.scroll_offset + lines
        )

    def scroll_to_top(self):
        """滚动到顶部"""
        self.scroll_offset = 0

    def scroll_to_bottom(self):
        """滚动到底部"""
        self.scroll_offset = max(0, self.total_lines - self.height)

    def get_visible_content(self) -> str:
        """获取可见内容"""
        start = self.scroll_offset
        end = min(start + self.height, self.total_lines)
        visible_lines = self.content_lines[start:end]

        # 如果没有滚动，不显示滚动条
        if self.total_lines <= self.height:
            return '\n'.join(visible_lines)

        # 添加滚动条
        return self._add_scrollbar('\n'.join(visible_lines))

    def _add_scrollbar(self, content: str) -> str:
        """添加ASCII滚动条"""
        lines = content.split('\n')
        content_height = len(lines)

        # 计算滚动条位置
        scrollbar_height = max(1, int((content_height / self.total_lines) * content_height))
        scrollbar_pos = int(
            (self.scroll_offset / max(1, (self.total_lines - self.height))) * (content_height - scrollbar_height))

        # 构建带滚动条的内容
        result = []
        for i in range(content_height):
            line = lines[i]
            if i >= scrollbar_pos and i < scrollbar_pos + scrollbar_height:
                result.append(f"{line} █")  # 滚动条位置
            else:
                result.append(f"{line} │")  # 滚动条轨道

        return '\n'.join(result)

    def get_scroll_info(self) -> str:
        """获取滚动信息"""
        if self.total_lines <= self.height:
            return ""
        return f" 行 {self.scroll_offset + 1}-{min(self.scroll_offset + self.height, self.total_lines)}/{self.total_lines}"


class ScrollableHelpFeature:
    """带滚动功能的帮助系统"""

    def __init__(self, console: Console):
        self.console = console
        self.current_page = "basic"
        self.scroll_panels = {}
        self._init_scroll_panels()
        self.running = True

    def _init_scroll_panels(self):
        """初始化滚动面板"""
        # 插件开发长内容
        plugin_dev_content = self._create_plugin_dev_content()
        self.scroll_panels["plug"] = ScrollablePanel(plugin_dev_content, height=20)

        # 插件API长内容
        plugin_api_content = self._create_plugin_api_content()
        self.scroll_panels["plapi"] = ScrollablePanel(plugin_api_content, height=20)

    def _create_plugin_dev_content(self) -> str:
        """创建插件开发长内容"""
        content = []

        # 标题
        content.append("📚 FastX-Tui 插件开发指南")
        content.append("=" * 60)

        # 1. 概述
        content.append("\n📖 概述")
        content.append("-" * 40)
        content.append("FastX-Tui 插件系统支持多文件结构、二进制文件和在线安装，为开发者提供了强大的扩展能力。")
        content.append("本文档将指导您如何开发 FastX-Tui 插件。")

        # 2. 插件结构
        content.append("\n📁 插件结构")
        content.append("-" * 40)
        content.append("插件仓库必须使用以下命名格式：")
        content.append("FastX-Tui-Plugin-{PluginName}")
        content.append("")
        content.append("其中 PluginName 是插件的名称，建议使用驼峰命名法。")

        # 3. 目录结构
        content.append("\n🗂️ 目录结构")
        content.append("-" * 40)
        content.append("一个完整的插件应该包含以下结构：")
        content.append("FastX-Tui-Plugin-{PluginName}/")
        content.append("├── fastx_plugin.py          # 插件入口文件（必须，固定命名）")
        content.append("├── pyproject.toml           # 插件元数据和依赖声明")
        content.append("├── README.md                # 插件说明文档")
        content.append("├── LICENSE                  # 许可证文件")
        content.append("├── resources/               # 插件资源文件目录（可选）")
        content.append("└── bin/                     # 二进制文件目录（可选）")

        # 4. 核心文件说明
        content.append("\n📄 核心文件说明")
        content.append("-" * 40)
        content.append("fastx_plugin.py（必须）：")
        content.append("  这是插件的入口文件，必须包含一个继承自 Plugin 类的插件类。")
        content.append("  该文件包含插件的配置信息和基本结构，业务逻辑应该分离到其他文件中。")
        content.append("")
        content.append("pyproject.toml：")
        content.append("  用于声明插件的元数据、依赖项和其他配置信息。")
        content.append("")
        content.append("README.md：")
        content.append("  插件的说明文档，包含插件的功能、安装方法和使用说明。")

        # 5. 插件开发步骤
        content.append("\n🛠️ 插件开发步骤")
        content.append("-" * 40)
        content.append("1. 创建插件目录结构")
        content.append("2. 实现插件类，继承自 Plugin 基类")
        content.append("3. 实现必要的方法")
        content.append("4. 在 register() 方法中注册菜单和命令")
        content.append("5. 将插件放置到 plugins/ 目录")

        # 6. 代码示例
        content.append("\n💻 代码示例")
        content.append("-" * 40)
        content.append("from core.plugin_manager import Plugin, PluginInfo")
        content.append("from core.menu_system import MenuSystem")
        content.append("")
        content.append("class {PluginName}Plugin(Plugin):")
        content.append("    \"\"\"{PluginName} 插件\"\"\"")
        content.append("    ")
        content.append("    def get_info(self) -> PluginInfo:")
        content.append("        \"\"\"获取插件信息\"\"\"")
        content.append("        return PluginInfo(")
        content.append("            name=\"{PluginName}\",")
        content.append("            version=\"1.0.0\",")
        content.append("            author=\"Your Name\",")
        content.append("            description=\"插件描述\",")
        content.append("            category=\"插件分类\",")
        content.append("            tags=[\"标签1\", \"标签2\"]")
        content.append("        )")
        content.append("    ")
        content.append("    def initialize(self):")
        content.append("        \"\"\"初始化插件\"\"\"")
        content.append("        pass")
        content.append("    ")
        content.append("    def cleanup(self):")
        content.append("        \"\"\"清理插件资源\"\"\"")
        content.append("        pass")
        content.append("    ")
        content.append("    def register(self, menu_system: MenuSystem):")
        content.append("        \"\"\"注册插件命令到菜单系统\"\"\"")
        content.append("        pass")

        # 7. 必须实现的方法
        content.append("\n🔧 必须实现的方法")
        content.append("-" * 40)
        content.append("get_info()    - 返回插件信息，包括名称、版本、作者等")
        content.append("initialize()  - 初始化插件资源，如连接数据库、加载配置等")
        content.append("cleanup()     - 清理插件资源，如关闭连接、释放内存等")
        content.append("register()    - 将插件命令注册到菜单系统")

        # 8. 注册菜单和命令
        content.append("\n📋 注册菜单和命令")
        content.append("-" * 40)
        content.append("插件可以通过 menu_system 对象注册菜单和命令。")
        content.append("")
        content.append("创建子菜单：")
        content.append("submenu = menu_system.create_submenu(")
        content.append("    menu_id=\"plugin_submenu\",")
        content.append("    name=\"插件菜单\",")
        content.append("    description=\"插件的专属菜单\",")
        content.append("    icon=\"🔌\"")
        content.append(")")
        content.append("")
        content.append("注册命令：")
        content.append("menu_system.register_item(ActionItem(")
        content.append("    id=\"plugin_command\",")
        content.append("    name=\"命令名称\",")
        content.append("    description=\"命令描述\",")
        content.append("    command_type=CommandType.PYTHON,")
        content.append("    python_func=lambda: \"命令执行结果\"")
        content.append("))")

        # 9. PluginInfo 字段
        content.append("\n📋 PluginInfo 字段说明")
        content.append("-" * 40)
        content.append("name: str                    - 插件名称 (必填)")
        content.append("version: str                 - 插件版本 (必填)")
        content.append("author: str                  - 插件作者 (必填)")
        content.append("description: str             - 插件描述 (必填)")
        content.append("enabled: bool = True         - 是否启用")
        content.append("category: str = \"其他\"      - 插件分类")
        content.append("tags: List[str] = []         - 插件标签")
        content.append("compatibility: Dict[str, str] = {} - 兼容性信息")
        content.append("dependencies: List[str] = [] - 依赖项")

        # 10. 依赖管理
        content.append("\n📦 依赖管理")
        content.append("-" * 40)
        content.append("插件的依赖项应该在 pyproject.toml 文件中声明：")
        content.append("")
        content.append("[project]")
        content.append("dependencies = [")
        content.append("    \"requests>=2.31.0\",")
        content.append("    \"numpy>=1.21.0\",")
        content.append("]")

        return '\n'.join(content)

    def _create_plugin_api_content(self) -> str:
        """创建插件API长内容"""
        content = []

        # 标题
        content.append("📚 FastX-Tui 插件API接口")
        content.append("=" * 60)

        # 1. 概述
        content.append("\n📖 API概述")
        content.append("-" * 40)
        content.append("FastX-Tui 插件API提供完整的接口，支持插件开发、菜单注册、资源管理等功能。")

        # 2. 核心接口
        content.append("\n🔧 核心接口")
        content.append("-" * 40)
        content.append("Plugin 基类 - 所有插件的基类")
        content.append("  ├── get_info() -> PluginInfo")
        content.append("  ├── initialize() -> None")
        content.append("  ├── cleanup() -> None")
        content.append("  └── register(menu_system) -> None")
        content.append("")
        content.append("PluginInfo 类 - 插件信息容器")
        content.append("MenuSystem 类 - 菜单系统接口")

        # 3. 详细方法说明
        content.append("\n📋 方法详细说明")
        content.append("-" * 40)
        content.append("get_info()")
        content.append("  返回：PluginInfo 对象")
        content.append("  说明：返回插件的基本信息，包括名称、版本、作者、描述等")
        content.append("  示例：return PluginInfo(name=\"MyPlugin\", version=\"1.0.0\", ...)")
        content.append("")
        content.append("initialize()")
        content.append("  返回：None")
        content.append("  说明：初始化插件，加载配置、准备资源等")
        content.append("  示例：self.config = self.load_config()")
        content.append("")
        content.append("cleanup()")
        content.append("  返回：None")
        content.append("  说明：清理插件资源，释放内存、关闭连接等")
        content.append("  示例：self.connection.close()")
        content.append("")
        content.append("register(menu_system)")
        content.append("  参数：menu_system - MenuSystem 对象")
        content.append("  返回：None")
        content.append("  说明：注册菜单项到菜单系统")
        content.append("  示例：menu_system.add_menu(\"插件菜单\", \"菜单描述\")")

        # 4. 完整代码示例
        content.append("\n💻 完整代码示例")
        content.append("-" * 40)
        content.append("from core.plugin_manager import Plugin, PluginInfo")
        content.append("from core.menu_system import MenuSystem")
        content.append("from typing import Dict, Any")
        content.append("")
        content.append("class CompletePlugin(Plugin):")
        content.append("    \"\"\"完整的插件示例\"\"\"")
        content.append("    ")
        content.append("    def __init__(self):")
        content.append("        self.config = {}")
        content.append("        self.logger = None")
        content.append("    ")
        content.append("    def get_info(self) -> PluginInfo:")
        content.append("        \"\"\"返回插件信息\"\"\"")
        content.append("        return PluginInfo(")
        content.append("            name=\"完整示例插件\",")
        content.append("            version=\"1.0.0\",")
        content.append("            author=\"开发者\",")
        content.append("            description=\"一个完整的插件示例\",")
        content.append("            category=\"示例\",")
        content.append("            tags=[\"example\", \"demo\", \"complete\"],")
        content.append("            enabled=True,")
        content.append("            dependencies=[\"requests>=2.31.0\"],")
        content.append("            license=\"MIT\",")
        content.append("            homepage=\"https://github.com/fastxteam/FastX-Tui\",")
        content.append("            compatibility={\"fastx-tui\": \">=1.0.0\"}")
        content.append("        )")
        content.append("    ")
        content.append("    def initialize(self) -> None:")
        content.append("        \"\"\"初始化插件\"\"\"")
        content.append("        self.logger = self.get_logger()")
        content.append("        self.config = self.load_config()")
        content.append("        self.logger.info(\"插件初始化完成\")")
        content.append("    ")
        content.append("    def cleanup(self) -> None:")
        content.append("        \"\"\"清理插件\"\"\"")
        content.append("        self.config.clear()")
        content.append("        if self.logger:")
        content.append("            self.logger.info(\"插件清理完成\")")
        content.append("    ")
        content.append("    def register(self, menu_system: MenuSystem) -> None:")
        content.append("        \"\"\"注册菜单\"\"\"")
        content.append("        main_menu = menu_system.add_menu(")
        content.append("            name=\"示例插件\",")
        content.append("            description=\"完整示例的功能菜单\",")
        content.append("            icon=\"🔧\"")
        content.append("        )")
        content.append("        ")
        content.append("        main_menu.add_item(")
        content.append("            name=\"运行示例\",")
        content.append("            description=\"运行示例功能\",")
        content.append("            action=self.run_example")
        content.append("        )")
        content.append("        ")
        content.append("        main_menu.add_item(")
        content.append("            name=\"查看配置\",")
        content.append("            description=\"查看插件配置\",")
        content.append("            action=self.show_config")
        content.append("        )")
        content.append("    ")
        content.append("    def run_example(self) -> Dict[str, Any]:")
        content.append("        return {\"status\": \"success\", \"message\": \"示例运行成功\"}")
        content.append("    ")
        content.append("    def show_config(self) -> str:")
        content.append("        return f\"当前配置: {self.config}\"")
        content.append("    ")
        content.append("    def load_config(self) -> Dict[str, Any]:")
        content.append("        return {\"setting1\": \"value1\", \"setting2\": \"value2\"}")
        content.append("    ")
        content.append("    def get_logger(self):")
        content.append("        import logging")
        content.append("        return logging.getLogger(__name__)")

        # 5. 使用说明
        content.append("\n📖 使用说明")
        content.append("-" * 40)
        content.append("1. 继承 Plugin 基类")
        content.append("2. 实现所有必需方法")
        content.append("3. 在 initialize() 中准备资源")
        content.append("4. 在 register() 中注册菜单项")
        content.append("5. 在 cleanup() 中清理资源")

        return '\n'.join(content)

    def create_layout(self) -> Layout:
        """创建布局"""
        layout = Layout()
        layout.split_column(
            Layout(name="header", size=3),
            Layout(name="content"),
            Layout(name="footer", size=3)
        )
        return layout

    def get_current_scroll_panel(self):
        """获取当前滚动面板"""
        return self.scroll_panels.get(self.current_page)

    def create_full_display(self) -> Layout:
        """创建完整显示"""
        layout = self.create_layout()

        # 头部
        title = f"FastX-Tui 帮助系统 - {self.current_page}"
        layout["header"].update(Panel(title, style="bold blue"))

        # 内容
        if self.current_page in self.scroll_panels:
            scroll_panel = self.scroll_panels[self.current_page]
            content = scroll_panel.get_visible_content()
            scroll_info = scroll_panel.get_scroll_info()

            panel = Panel(
                content,
                title=f"帮助内容{scroll_info}",
                border_style="green",
                box=box.ROUNDED,
                padding=(1, 2)
            )
        else:
            panel = Panel("该页面不支持滚动", border_style="red")

        layout["content"].update(panel)

        # 底部
        footer_text = "导航: 1-6 切换页面 | ↑↓ 滚动 | Home/End 顶部/底部 | Q 退出"
        layout["footer"].update(Panel(footer_text, style="dim"))

        return layout

    def _getch(self) -> str:
        """获取按键"""
        if sys.platform == 'win32':
            ch = msvcrt.getch()
            if ch == b'\x03':  # Ctrl+C
                raise KeyboardInterrupt
            if ch == b'\xe0':  # 方向键
                ch2 = msvcrt.getch()
                if ch2 == b'H':
                    return 'up'
                elif ch2 == b'P':
                    return 'down'
                elif ch2 == b'G':
                    return 'home'
                elif ch2 == b'O':
                    return 'end'
            return ch.decode('latin-1', errors='ignore')
        else:
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                tty.setraw(fd)
                ch = sys.stdin.read(1)
                if ch == '\x1b':  # ESC
                    ch2 = sys.stdin.read(1)
                    if ch2 == '[':  # CSI
                        ch3 = sys.stdin.read(1)
                        if ch3 == 'A':
                            return 'up'
                        elif ch3 == 'B':
                            return 'down'
                        elif ch3 == 'H':
                            return 'home'
                        elif ch3 == 'F':
                            return 'end'
                return ch
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

    def handle_input(self):
        """处理输入"""
        with Live(self.create_full_display(), console=self.console, refresh_per_second=10, screen=True) as live:
            while self.running:
                live.update(self.create_full_display())
                ch = self._getch()

                if ch in ['q', 'Q', '\x03']:
                    self.running = False
                    break

                # 数字键切换页面
                if ch.isdigit():
                    page_num = int(ch)
                    pages = ['basic', 'short', 'navi', 'feat', 'plug', 'plapi']
                    if 1 <= page_num <= len(pages):
                        self.current_page = pages[page_num - 1]

                # 滚动控制
                elif ch == 'up':
                    if self.current_page in self.scroll_panels:
                        self.scroll_panels[self.current_page].scroll_up()

                elif ch == 'down':
                    if self.current_page in self.scroll_panels:
                        self.scroll_panels[self.current_page].scroll_down()

                elif ch == 'home':
                    if self.current_page in self.scroll_panels:
                        self.scroll_panels[self.current_page].scroll_to_top()

                elif ch == 'end':
                    if self.current_page in self.scroll_panels:
                        self.scroll_panels[self.current_page].scroll_to_bottom()

    def show_help(self):
        """显示帮助"""
        self.console.clear()
        self.handle_input()
        self.console.clear()


# 使用示例
if __name__ == "__main__":
    console = Console()
    help_system = ScrollableHelpFeature(console)
    help_system.show_help()