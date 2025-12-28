#!/usr/bin/env python3
"""
Layout路由实现示例
展示如何用Layout实现真正的页面切换
支持上下键切换章节
"""

from rich.console import Console
from rich.panel import Panel
from rich.layout import Layout
from rich.table import Table
from rich.tree import Tree
from rich.text import Text
from rich import box
import sys
import os


class RouterApp:
    """基于Layout的简单路由应用"""

    def __init__(self):
        self.console = Console()
        self.current_page = "home"  # 当前页面
        self.current_section = 0  # 当前章节索引
        self.pages = ["home", "scripts", "settings", "help"]
        self.sections = {
            "home": ["仪表板", "统计信息", "使用指南"],
            "scripts": ["脚本列表", "运行历史", "新建脚本"],
            "settings": ["界面设置", "执行设置", "高级选项"],
            "help": ["快捷键", "快速开始", "常见问题"]
        }
        self.layout = self.create_layout()

    def create_layout(self):
        """创建基础布局"""
        layout = Layout()
        layout.split_column(
            Layout(name="header", size=3),
            Layout(name="main"),
            Layout(name="navigation", size=3),
            Layout(name="footer", size=2)
        )

        layout["main"].split_row(
            Layout(name="sidebar", ratio=1),
            Layout(name="content", ratio=3)
        )

        return layout

    def clear_screen(self):
        """清屏"""
        os.system('cls' if os.name == 'nt' else 'clear')

    def update_header(self):
        """更新头部"""
        page_names = {
            "home": "首页",
            "scripts": "脚本管理",
            "settings": "设置",
            "help": "帮助"
        }

        sections = self.sections[self.current_page]
        current_section_name = sections[self.current_section]

        title = f"脚本管理器 - {page_names[self.current_page]} > {current_section_name}"

        self.layout["header"].update(
            Panel(title,
                  style="bold white on blue",
                  subtitle=f"第 {self.current_section + 1}/{len(sections)} 节")
        )

    def update_sidebar(self):
        """更新侧边栏导航"""
        # 页面导航
        pages_items = [
            ("首页", "1", "home"),
            ("脚本管理", "2", "scripts"),
            ("设置", "3", "settings"),
            ("帮助", "4", "help"),
        ]

        # 当前页面的章节
        sections = self.sections[self.current_page]

        nav_text = "[bold]页面导航:[/bold]\n"
        for name, shortcut, page in pages_items:
            if page == self.current_page:
                nav_text += f"[reverse]▶ {name}[/reverse] [yellow]({shortcut})[/yellow]\n"
            else:
                nav_text += f"  {name} [dim]({shortcut})[/dim]\n"

        nav_text += "\n[bold]章节切换:[/bold]\n"
        for i, section in enumerate(sections):
            if i == self.current_section:
                nav_text += f"[reverse]• {section}[/reverse] [yellow](↑↓选择)[/yellow]\n"
            else:
                nav_text += f"  {section}\n"

        nav_text += "\n[dim]操作提示:[/dim]\n"
        nav_text += "  [yellow]Q[/yellow] 退出程序\n"
        nav_text += "  [yellow]↑↓[/yellow] 切换章节\n"

        self.layout["sidebar"].update(
            Panel(nav_text.strip(),
                  title="导航控制",
                  border_style="green",
                  padding=(1, 2))
        )

    def update_content(self):
        """根据当前页面和章节更新内容"""
        section_key = self.current_page
        section_index = self.current_section

        if self.current_page == "home":
            self.show_home_section(section_index)
        elif self.current_page == "scripts":
            self.show_scripts_section(section_index)
        elif self.current_page == "settings":
            self.show_settings_section(section_index)
        elif self.current_page == "help":
            self.show_help_section(section_index)

    def update_navigation(self):
        """更新导航栏"""
        nav_info = f"""
当前页面: [bold green]{self.current_page}[/bold green] | 
当前章节: [bold yellow]{self.sections[self.current_page][self.current_section]}[/bold yellow] |
总章节数: [bold cyan]{len(self.sections[self.current_page])}[/bold cyan]
        """.strip()

        self.layout["navigation"].update(
            Panel(nav_info,
                  style="dim",
                  border_style="yellow")
        )

    def update_footer(self):
        """更新底部状态栏"""
        status = f"使用数字键切换页面 (1-4) | 方向键↑↓切换章节 | Q键退出"
        self.layout["footer"].update(
            Panel(status,
                  style="white on blue")
        )

    def show_home_section(self, section_index):
        """首页各章节内容"""
        sections_content = [
            """[bold]仪表板概览[/bold]

欢迎使用脚本管理器！这是一个强大的脚本管理工具，可以帮助您：
• 管理和组织各种脚本文件
• 快速执行常用命令
• 监控脚本执行状态
• 查看历史执行记录

[cyan]今日状态:[/cyan]
• 系统状态: 正常
• 脚本总数: 15个
• 今日执行: 3次
• 可用空间: 85%
            """,

            """[bold]统计信息[/bold]

[cyan]执行统计:[/cyan]
月份    执行次数  成功率  平均耗时
--------------------------------
01月    45       98%     2.3s
02月    38       96%     3.1s  
03月    52       99%     1.8s

[cyan]脚本类型分布:[/cyan]
Shell脚本:    8个 (53%)
Python脚本:   5个 (33%)
Batch脚本:    2个 (14%)

[dim]数据更新: 2024-01-15 14:30[/dim]
            """,

            """[bold]使用指南[/bold]

[cyan]基础操作:[/cyan]
1. 使用数字键 1-4 切换主页面
2. 在侧边栏使用方向键选择章节
3. 按 Enter 键确认选择
4. 按 Q 键退出程序

[cyan]脚本管理:[/cyan]
• 脚本管理页面可以查看所有脚本
• 支持运行、编辑、删除操作
• 可以查看脚本执行历史

[cyan]设置选项:[/cyan]
• 界面主题设置
• 执行参数配置
• 编辑器偏好设置
            """
        ]

        self.layout["content"].update(
            Panel(sections_content[section_index],
                  title="首页",
                  border_style="yellow",
                  padding=(1, 2))
        )

    def show_scripts_section(self, section_index):
        """脚本管理各章节内容"""
        if section_index == 0:
            # 脚本列表表格
            table = Table(title="脚本列表", box=box.ROUNDED)
            table.add_column("ID", style="cyan", width=8)
            table.add_column("脚本名称", style="magenta", width=20)
            table.add_column("类型", style="green", width=10)
            table.add_column("最后修改", style="dim", width=12)
            table.add_column("状态", style="bold", width=10)

            scripts = [
                ("001", "系统备份.sh", "Shell", "2024-01-15", "正常"),
                ("002", "日志分析.py", "Python", "2024-01-14", "正常"),
                ("003", "数据库备份", "Shell", "2024-01-13", "待测试"),
                ("004", "文件同步", "Python", "2024-01-12", "正常"),
                ("005", "监控警报", "Shell", "2024-01-11", "已禁用"),
            ]

            for script in scripts:
                table.add_row(*script)

            content = str(table)

        elif section_index == 1:
            # 运行历史
            content = """[bold]脚本执行历史[/bold]

[cyan]最近执行记录:[/cyan]
时间                脚本名称        状态    耗时
----------------------------------------------
2024-01-15 14:30   系统备份.sh     成功    1m23s
2024-01-15 11:20   日志分析.py     成功    45s
2024-01-15 09:15   文件同步        失败    15s
2024-01-14 16:40   数据库备份      成功    2m10s
2024-01-14 14:25   系统备份.sh     成功    1m18s

[cyan]执行统计:[/cyan]
• 今日执行: 3次
• 本周执行: 12次
• 成功率: 92%
• 平均耗时: 1分15秒
            """

        else:  # section_index == 2
            # 新建脚本
            content = """[bold]新建脚本向导[/bold]

[cyan]脚本信息:[/cyan]
• 脚本名称: [请输入]
• 脚本类型: ○ Shell  ○ Python  ○ Batch
• 保存位置: ./scripts/
• 描述信息: [可选]

[cyan]模板选择:[/cyan]
[ ] 基础模板 - 简单的脚本框架
[ ] 备份模板 - 包含备份逻辑
[ ] 监控模板 - 监控脚本框架
[ ] 自定义模板

[cyan]高级选项:[/cyan]
[ ] 添加执行权限
[ ] 添加到收藏夹
[ ] 设置定时执行

[dim]按 Enter 开始创建新脚本[/dim]
            """

        self.layout["content"].update(
            Panel(content,
                  title="脚本管理",
                  border_style="blue",
                  padding=(1, 2))
        )

    def show_settings_section(self, section_index):
        """设置各章节内容"""
        sections_content = [
            """[bold]界面设置[/bold]

[cyan]主题设置:[/cyan]
[●] 深色主题
[ ] 浅色主题
[ ] 自动切换

[cyan]布局设置:[/cyan]
[✓] 显示侧边栏
[✓] 显示状态栏
[ ] 全屏模式
[ ] 紧凑模式

[cyan]字体设置:[/cyan]
字体大小: [12px] [14px] [16px]
字体样式: [等宽] [衬线] [无衬线]

[cyan]颜色方案:[/cyan]
[ ] 默认配色
[ ] 高对比度
[ ] 自定义配色
            """,

            """[bold]执行设置[/bold]

[cyan]执行参数:[/cyan]
[✓] 执行前确认
[ ] 后台执行
[✓] 保存输出日志
[ ] 显示详细输出

[cyan]超时设置:[/cyan]
默认超时: [60] 秒
最大超时: [300] 秒
超时动作: [中断执行] [继续执行]

[cyan]安全设置:[/cyan]
[✓] 检查脚本权限
[✓] 验证脚本签名
[ ] 沙盒模式执行
[ ] 禁止外部调用

[cyan]通知设置:[/cyan]
[✓] 执行完成通知
[ ] 执行失败通知
[ ] 长时间运行警告
            """,

            """[bold]高级选项[/bold]

[cyan]性能设置:[/cyan]
最大并发数: [5] 个脚本
缓存大小: [100] MB
历史记录: 保留 [30] 天

[cyan]网络设置:[/cyan]
代理服务器: [无]
连接超时: [30] 秒
重试次数: [3] 次

[cyan]日志设置:[/cyan]
日志级别: [INFO] [DEBUG] [WARNING]
日志保存: [7] 天
日志路径: ./logs/

[cyan]数据管理:[/cyan]
[ ] 自动备份配置
[ ] 清理临时文件
[ ] 压缩历史数据

[dim]注意: 部分设置需要重启生效[/dim]
            """
        ]

        self.layout["content"].update(
            Panel(sections_content[section_index],
                  title="设置",
                  border_style="magenta",
                  padding=(1, 2))
        )

    def show_help_section(self, section_index):
        """帮助各章节内容"""
        sections_content = [
            """[bold]快捷键说明[/bold]

[cyan]页面导航:[/cyan]
数字键 1  - 切换到首页
数字键 2  - 切换到脚本管理
数字键 3  - 切换到设置页面
数字键 4  - 切换到帮助页面
Q 键      - 退出程序

[cyan]章节切换:[/cyan]
方向键 ↑  - 切换到上一章节
方向键 ↓  - 切换到下一章节
Home键    - 切换到第一个章节
End键     - 切换到最后一个章节

[cyan]内容操作:[/cyan]
Enter键   - 确认/执行选择
Esc键     - 取消/返回
Tab键     - 切换焦点
空格键    - 切换选项状态

[cyan]编辑操作:[/cyan]
Ctrl+S    - 保存
Ctrl+Z    - 撤销
Ctrl+C    - 复制
Ctrl+V    - 粘贴
            """,

            """[bold]快速开始[/bold]

[cyan]第一步: 了解界面布局[/cyan]
1. 顶部显示当前页面和章节信息
2. 左侧是导航控制面板
3. 中间是主要内容区域
4. 下方是导航栏和状态栏

[cyan]第二步: 基本操作流程[/cyan]
1. 使用数字键选择要进入的页面
2. 使用方向键浏览页面的不同章节
3. 查看或修改相关内容
4. 按需要执行相应操作

[cyan]第三步: 脚本管理示例[/cyan]
1. 按数字键 2 进入脚本管理页面
2. 在"脚本列表"章节查看所有脚本
3. 选择要操作的脚本
4. 执行运行、编辑或删除操作

[cyan]第四步: 个性化设置[/cyan]
1. 按数字键 3 进入设置页面
2. 调整界面主题、布局等选项
3. 配置执行参数和安全设置
4. 保存设置并应用
            """,

            """[bold]常见问题解答[/bold]

[cyan]Q: 如何添加新的脚本？[/cyan]
A: 进入脚本管理页面，选择"新建脚本"章节，填写脚本信息后创建。

[cyan]Q: 脚本执行失败怎么办？[/cyan]
A: 1. 检查脚本是否有执行权限
   2. 查看执行日志获取错误信息
   3. 确认依赖环境是否正确配置
   4. 尝试在设置中调整超时时间

[cyan]Q: 如何备份配置？[/cyan]
A: 设置页面中提供配置导出功能，也可以手动备份配置文件。

[cyan]Q: 支持哪些脚本类型？[/cyan]
A: 目前支持Shell脚本(.sh)、Python脚本(.py)、Batch脚本(.bat)等。

[cyan]Q: 如何查看详细的执行日志？[/cyan]
A: 在脚本管理页面的"运行历史"章节可以查看详细执行记录。

[cyan]Q: 遇到程序崩溃如何处理？[/cyan]
A: 1. 检查错误日志文件
   2. 尝试清理缓存数据
   3. 重置用户配置文件
   4. 联系技术支持
            """
        ]

        self.layout["content"].update(
            Panel(sections_content[section_index],
                  title="帮助",
                  border_style="green",
                  padding=(1, 2))
        )

    def render(self):
        """渲染整个界面"""
        self.update_header()
        self.update_sidebar()
        self.update_content()
        self.update_navigation()
        self.update_footer()
        self.console.print(self.layout)

    def handle_input(self):
        """处理用户输入"""
        try:
            import tty
            import termios
            import select

            # 保存原始终端设置
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)

            try:
                # 设置为非阻塞模式
                tty.setraw(sys.stdin.fileno())

                while True:
                    self.clear_screen()
                    self.render()

                    # 等待用户输入
                    if select.select([sys.stdin], [], [], 1)[0]:
                        key = sys.stdin.read(1)

                        # 处理退出
                        if key.lower() == 'q':
                            break

                        # 处理页面切换 (数字键1-4)
                        elif key in ['1', '2', '3', '4']:
                            page_index = int(key) - 1
                            if page_index < len(self.pages):
                                self.current_page = self.pages[page_index]
                                self.current_section = 0  # 切换到新页面时重置章节

                        # 处理方向键（需要读取转义序列）
                        elif key == '\x1b':  # ESC字符
                            next1, next2 = sys.stdin.read(2)  # 读取两个字符
                            if next1 == '[':
                                if next2 == 'A':  # 上箭头
                                    # 切换到上一章节
                                    if self.current_section > 0:
                                        self.current_section -= 1
                                elif next2 == 'B':  # 下箭头
                                    # 切换到下一章节
                                    sections = self.sections[self.current_page]
                                    if self.current_section < len(sections) - 1:
                                        self.current_section += 1
                                elif next2 == 'H':  # Home键
                                    self.current_section = 0
                                elif next2 == 'F':  # End键
                                    sections = self.sections[self.current_page]
                                    self.current_section = len(sections) - 1

                        # 处理Enter键
                        elif key == '\r' or key == '\n':
                            # 可以在这里添加具体章节的确认操作
                            self.console.print(
                                f"\n[green]确认选择: {self.sections[self.current_page][self.current_section]}[/green]")
                            sys.stdin.read(1)  # 等待用户按任意键继续

            finally:
                # 恢复原始终端设置
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

        except ImportError:
            # 如果tty模块不可用（如Windows），使用简单输入方式
            from rich.prompt import Prompt

            while True:
                self.clear_screen()
                self.render()

                try:
                    choice = Prompt.ask(
                        "\n输入操作 (1-4切换页面, ↑↓切换章节, Q退出)",
                        choices=["1", "2", "3", "4", "up", "down", "q", "Q"],
                        show_choices=False
                    ).lower()

                    if choice == "q":
                        break
                    elif choice in ["1", "2", "3", "4"]:
                        page_index = int(choice) - 1
                        if page_index < len(self.pages):
                            self.current_page = self.pages[page_index]
                            self.current_section = 0
                    elif choice == "up":
                        if self.current_section > 0:
                            self.current_section -= 1
                    elif choice == "down":
                        sections = self.sections[self.current_page]
                        if self.current_section < len(sections) - 1:
                            self.current_section += 1

                except KeyboardInterrupt:
                    break

    def run(self):
        """运行应用"""
        self.console.clear()
        print("正在启动脚本管理器...")
        self.handle_input()
        self.console.print("\n[yellow]感谢使用脚本管理器！[/yellow]")


def main():
    """主函数入口"""
    app = RouterApp()
    app.run()

if __name__ == "__main__":
    main()