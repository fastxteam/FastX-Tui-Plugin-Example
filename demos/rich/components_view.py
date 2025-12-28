#!/usr/bin/env python3
"""
Rich组件演示器 - 菜单驱动版
用户可以选择要查看的组件
"""

import sys
import time
import os
from typing import Dict, List, Callable
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.tree import Tree
from rich.layout import Layout
from rich.text import Text
from rich.syntax import Syntax
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn
from rich.columns import Columns
from rich.prompt import Prompt
from rich import box
from rich.style import Style


class RichDemoMenu:
    def __init__(self):
        self.console = Console()
        self.components = self._setup_components()
        self.current_page = 0
        self.items_per_page = 8

    def _setup_components(self) -> Dict[str, Dict]:
        """设置可演示的组件"""
        return {
            "console": {
                "name": "Console - 基础输出",
                "description": "Rich的基础输出控制，支持样式、颜色",
                "demo_func": self._demo_console,
                "icon": ">"
            },
            "panel": {
                "name": "Panel - 面板容器",
                "description": "创建带边框的容器区域",
                "demo_func": self._demo_panel,
                "icon": "+"
            },
            "table": {
                "name": "Table - 表格",
                "description": "展示结构化数据，支持多种边框样式",
                "demo_func": self._demo_table,
                "icon": "#"
            },
            "tree": {
                "name": "Tree - 树状结构",
                "description": "展示层级结构，如文件系统",
                "demo_func": self._demo_tree,
                "icon": "*"
            },
            "layout": {
                "name": "Layout - 布局管理",
                "description": "创建复杂的多面板布局",
                "demo_func": self._demo_layout,
                "icon": "@"
            },
            "text": {
                "name": "Text - 高级文本",
                "description": "高级文本处理，精确控制样式",
                "demo_func": self._demo_text,
                "icon": "T"
            },
            "syntax": {
                "name": "Syntax - 语法高亮",
                "description": "代码语法高亮显示",
                "demo_func": self._demo_syntax,
                "icon": "$"
            },
            "progress": {
                "name": "Progress - 进度条",
                "description": "显示长时间任务的进度",
                "demo_func": self._demo_progress,
                "icon": "%"
            },
            "columns": {
                "name": "Columns - 列布局",
                "description": "创建并排布局，自动调整宽度",
                "demo_func": self._demo_columns,
                "icon": "|"
            },
            "prompt": {
                "name": "Prompt - 交互提示",
                "description": "用户交互输入，支持多种类型",
                "demo_func": self._demo_prompt,
                "icon": "?"
            },
            "box": {
                "name": "Box - 边框样式",
                "description": "各种边框样式定义",
                "demo_func": self._demo_box,
                "icon": "[]"
            },
            "style": {
                "name": "Style - 样式管理",
                "description": "创建和组合样式对象",
                "demo_func": self._demo_style,
                "icon": "{}"
            },
            "all": {
                "name": "全部演示",
                "description": "按顺序演示所有组件",
                "demo_func": self._demo_all,
                "icon": "A"
            },
            "quit": {
                "name": "退出程序",
                "description": "结束演示",
                "demo_func": None,
                "icon": "X"
            }
        }

    def clear_screen(self):
        """清屏 - 跨平台兼容"""
        os.system('cls' if os.name == 'nt' else 'clear')

    def show_header(self):
        """显示程序标题"""
        title = """
        ====================================================
                Rich组件演示器 - 菜单版
              选择要查看的组件，按序号选择
        ====================================================
        """
        self.console.print(title, style="bold cyan")

    def show_menu(self, page: int = 0) -> List[str]:
        """显示菜单页面"""
        self.clear_screen()
        self.show_header()

        # 分页逻辑
        keys = list(self.components.keys())
        start_idx = page * self.items_per_page
        end_idx = start_idx + self.items_per_page
        page_keys = keys[start_idx:end_idx]

        # 创建菜单表格
        menu_table = Table(
            title=f"组件菜单 (第 {page + 1}/{((len(keys) - 1) // self.items_per_page) + 1} 页)",
            box=box.ROUNDED,
            show_header=True,
            header_style="bold magenta"
        )
        menu_table.add_column("选择", style="cyan", width=6, justify="center")  # 改为"选择"
        menu_table.add_column("图标", style="yellow", width=4, justify="center")
        menu_table.add_column("组件名称", style="green", width=20)
        menu_table.add_column("描述", style="white", width=50)

        # 显示页面相对序号（1,2,3,...）
        for i, key in enumerate(page_keys, start=1):
            comp = self.components[key]
            menu_table.add_row(
                str(i),  # 显示1,2,3,...而不是全局序号
                comp["icon"],
                comp["name"],
                comp["description"]
            )

        self.console.print(menu_table)
        self.console.print("\n")

        # 显示导航提示
        nav_panel = Panel(
            f"[bold]导航:[/bold]\n"
            f"* 输入 1-{len(page_keys)} 选择组件\n"  # 明确范围
            f"* [P]上一页 | [N]下一页\n"
            f"* [R]返回菜单 | [Q]退出",
            border_style="yellow",
            width=60
        )
        self.console.print(nav_panel)

        return page_keys

    def get_user_choice(self, page_keys: List[str]) -> str:
        """获取用户选择 - 修复选择限制问题"""
        while True:
            try:
                # 创建可用的选择列表
                available_choices = [str(i) for i in range(1, len(page_keys) + 1)]

                # 显示提示
                self.console.print("\n[bold cyan]请输入选择:[/bold cyan] ", end="")
                choice = sys.stdin.readline().strip().lower()

                if choice in ['q']:
                    return 'quit'
                elif choice in ['p']:
                    return 'prev'
                elif choice in ['n']:
                    return 'next'
                elif choice in ['r']:
                    return 'menu'
                elif choice in available_choices:
                    idx = int(choice) - 1
                    return page_keys[idx]
                else:
                    self.console.print(f"[red]无效选择，请输入 1-{len(page_keys)} 的数字或 P/N/Q/R[/red]")
            except ValueError:
                self.console.print("[red]请输入有效的数字[/red]")
            except KeyboardInterrupt:
                self.console.print("\n[yellow]检测到中断信号，正在退出...[/yellow]")
                return 'quit'

    def wait_for_continue(self):
        """等待用户继续"""
        self.console.print("\n[dim]按 Enter 继续...[/dim]", end="")
        sys.stdin.readline()

    # ===== 各组件演示函数 =====

    def _demo_console(self):
        """演示Console组件"""
        self.clear_screen()
        self.console.print(Panel("Console - 基础输出控制", border_style="cyan"))

        self.console.print("\n[bold]基础样式:[/bold]")
        self.console.print("普通文本")
        self.console.print("[bold]粗体文本[/bold]")
        self.console.print("[italic]斜体文本[/italic]")
        self.console.print("[underline]下划线文本[/underline]")

        self.console.print("\n[bold]颜色输出:[/bold]")
        self.console.print("[red]红色文本[/red]")
        self.console.print("[green]绿色文本[/green]")
        self.console.print("[blue]蓝色文本[/blue]")
        self.console.print("[yellow]黄色文本[/yellow]")
        self.console.print("[magenta]洋红色文本[/magenta]")

        self.console.print("\n[bold]组合样式:[/bold]")
        self.console.print("[bold red on yellow]粗体红色文本黄色背景[/bold red on yellow]")
        self.console.print("[italic green on black]斜体绿色文本黑色背景[/italic green on black]")

        self.wait_for_continue()

    def _demo_panel(self):
        """演示Panel组件"""
        self.clear_screen()
        self.console.print(Panel("Panel - 面板容器", border_style="cyan"))

        self.console.print("\n[bold]不同边框样式:[/bold]")

        panels = [
            Panel("简单面板内容", title="简单面板"),
            Panel("带绿色边框的面板", title="绿色边框", border_style="green"),
            Panel("圆角边框面板", title="圆角边框", box=box.ROUNDED, border_style="blue"),
            Panel("双线边框面板", title="双线边框", box=box.DOUBLE, border_style="red"),
        ]

        for panel in panels:
            self.console.print(panel)
            time.sleep(0.5)

        self.wait_for_continue()

    def _demo_table(self):
        """演示Table组件"""
        self.clear_screen()
        self.console.print(Panel("Table - 表格", border_style="cyan"))

        self.console.print("\n[bold]员工信息表:[/bold]")
        table1 = Table(title="员工信息", box=box.ROUNDED)
        table1.add_column("ID", style="cyan")
        table1.add_column("姓名", style="magenta")
        table1.add_column("部门", style="green")
        table1.add_column("工资", justify="right", style="yellow")
        table1.add_column("状态", style="bold")

        table1.add_row("001", "张三", "技术部", "15,000", "[green]在职[/green]")
        table1.add_row("002", "李四", "市场部", "12,000", "[green]在职[/green]")
        table1.add_row("003", "王五", "财务部", "13,500", "[yellow]休假[/yellow]")
        table1.add_row("004", "赵六", "人事部", "11,000", "[red]离职[/red]")

        self.console.print(table1)
        time.sleep(1)

        self.console.print("\n[bold]产品库存表:[/bold]")
        table2 = Table(title="产品库存", box=box.SIMPLE, show_lines=True)
        table2.add_column("产品")
        table2.add_column("库存", justify="right")
        table2.add_column("价格", justify="right")
        table2.add_column("状态", style="bold")

        table2.add_row("笔记本电脑", "45", "6,999", "[green]充足[/green]")
        table2.add_row("智能手机", "12", "3,299", "[yellow]紧张[/yellow]")
        table2.add_row("平板电脑", "3", "2,499", "[red]缺货[/red]")

        self.console.print(table2)

        self.wait_for_continue()

    def _demo_tree(self):
        """演示Tree组件"""
        self.clear_screen()
        self.console.print(Panel("Tree - 树状结构", border_style="cyan"))

        self.console.print("\n[bold]项目结构:[/bold]")
        tree = Tree("我的项目", guide_style="bright_cyan")

        src = tree.add("src")
        src.add("api")
        src.add("components")
        src.add("utils")

        docs = tree.add("docs")
        docs.add("README.md")
        docs.add("API.md")
        docs.add("CHANGELOG.md")

        tests = tree.add("tests")
        tests.add("test_api.py")
        tests.add("test_components.py")

        self.console.print(tree)
        time.sleep(1)

        self.console.print("\n[bold]文件系统:[/bold]")
        file_tree = Tree("文件系统", guide_style="green")
        home = file_tree.add("/home/user")
        home.add("Documents")
        home.add("Downloads")
        home.add("Pictures")

        projects = home.add("Projects")
        web_app = projects.add("web-app")
        web_app.add("frontend")
        web_app.add("backend")

        self.console.print(file_tree)

        self.wait_for_continue()

    def _demo_layout(self):
        """演示Layout组件"""
        self.clear_screen()
        self.console.print(Panel("Layout - 布局管理", border_style="cyan"))

        self.console.print("\n[bold]创建复杂布局:[/bold]")

        layout = Layout()
        layout.split_column(
            Layout(name="header", size=3),
            Layout(name="main"),
            Layout(name="footer", size=3)
        )

        layout["main"].split_row(
            Layout(name="sidebar", ratio=1),
            Layout(name="content", ratio=3)
        )

        layout["header"].update(Panel("脚本管理器", style="bold blue"))
        layout["sidebar"].update(Panel("导航菜单\n\n* 首页\n* 脚本\n* 设置\n* 帮助", border_style="green"))
        layout["content"].update(Panel("主内容区域\n\n这里显示主要内容...", border_style="yellow"))
        layout["footer"].update(Panel("状态栏: 就绪", style="dim"))

        self.console.print(layout)

        self.wait_for_continue()

    def _demo_text(self):
        """演示Text组件"""
        self.clear_screen()
        self.console.print(Panel("Text - 高级文本处理", border_style="cyan"))

        self.console.print("\n[bold]精确控制文本样式:[/bold]")

        text1 = Text("带部分样式的文本")
        text1.stylize("bold red", 0, 3)  # 前3个字符
        text1.stylize("underline green", 3, 6)  # 第3-6个字符
        self.console.print(text1)

        self.console.print("\n[bold]动态构建文本:[/bold]")
        text2 = Text()
        text2.append("正常文本 ")
        text2.append("粗体文本", style="bold")
        text2.append(" 红色文本", style="red")
        text2.append(" 背景色文本", style="white on blue")
        self.console.print("结果:", text2)

        self.console.print("\n[bold]文本对齐:[/bold]")
        width = 40
        self.console.print(Text("左对齐文本").align("left", width=width))
        self.console.print(Text("居中对齐文本").align("center", width=width))
        self.console.print(Text("右对齐文本").align("right", width=width))

        self.wait_for_continue()

    def _demo_syntax(self):
        """演示Syntax组件"""
        self.clear_screen()
        self.console.print(Panel("Syntax - 语法高亮", border_style="cyan"))

        python_code = '''def hello_world():
    """打印Hello World"""
    print("Hello, World!")

if __name__ == "__main__":
    hello_world()'''

        self.console.print("\n[bold]Python代码高亮:[/bold]")
        syntax = Syntax(python_code, "python", theme="monokai", line_numbers=True)
        self.console.print(syntax)

        json_code = '''{
    "name": "张三",
    "age": 30,
    "skills": ["Python", "JavaScript"]
}'''

        self.console.print("\n[bold]JSON代码高亮:[/bold]")
        syntax = Syntax(json_code, "json", theme="vim", line_numbers=True)
        self.console.print(syntax)

        self.wait_for_continue()

    def _demo_progress(self):
        """演示Progress组件"""
        self.clear_screen()
        self.console.print(Panel("Progress - 进度条", border_style="cyan"))

        self.console.print("\n[bold]单个任务进度:[/bold]")
        with Progress(
                TextColumn("[progress.description]{task.description}"),
                BarColumn(),
                TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
                TimeElapsedColumn(),
        ) as progress:

            task = progress.add_task("[cyan]下载文件中...", total=100)
            for i in range(10):
                progress.update(task, advance=10)
                time.sleep(0.05)

        self.console.print("\n[bold]多任务进度:[/bold]")
        with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                BarColumn(),
                TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        ) as progress:

            tasks = [
                progress.add_task("[red]下载...", total=100),
                progress.add_task("[green]解压...", total=50),
                progress.add_task("[blue]安装...", total=30),
            ]

            for i in range(10):
                for task_id in tasks:
                    progress.update(task_id, advance=5)
                time.sleep(0.03)

        self.wait_for_continue()

    def _demo_columns(self):
        """演示Columns组件"""
        self.clear_screen()
        self.console.print(Panel("Columns - 列布局", border_style="cyan"))

        self.console.print("\n[bold]文本列布局:[/bold]")
        texts = [
            "第一列文本内容",
            "第二列文本，稍长一些",
            "第三列文本内容",
        ]
        columns = Columns(texts, equal=True, expand=True)
        self.console.print(columns)

        self.console.print("\n[bold]面板列布局:[/bold]")
        panels = [
            Panel("系统信息\n\nCPU: 25%\n内存: 45%", title="系统", border_style="green"),
            Panel("网络状态\n\n上传: 1.2MB/s\n下载: 5.1MB/s", title="网络", border_style="blue"),
            Panel("服务状态\n\nWeb: OK\nDB: OK", title="服务", border_style="yellow"),
        ]
        self.console.print(Columns(panels, expand=True))

        self.wait_for_continue()

    def _demo_prompt(self):
        """演示Prompt组件"""
        self.clear_screen()
        self.console.print(Panel("Prompt - 交互提示", border_style="cyan"))

        self.console.print("\n[bold]各种输入类型演示:[/bold]")

        self.console.print("\n1. 文本输入:")
        self.console.print("   请输入姓名 [张三]: 李四")
        self.console.print("   -> 输入: 李四")
        time.sleep(0.5)

        self.console.print("\n2. 确认提示:")
        self.console.print("   继续吗? (y/n) [y]: y")
        self.console.print("   -> 选择: 是")
        time.sleep(0.5)

        self.console.print("\n3. 数字输入:")
        self.console.print("   请输入年龄 [25]: 30")
        self.console.print("   -> 年龄: 30")
        time.sleep(0.5)

        self.console.print("\n4. 选择提示:")
        choices = ["Python", "JavaScript", "Go"]
        self.console.print(f"   请选择语言 {choices}: Python")
        self.console.print("   -> 选择: Python")

        self.wait_for_continue()

    def _demo_box(self):
        """演示Box组件"""
        self.clear_screen()
        self.console.print(Panel("Box - 边框样式", border_style="cyan"))

        self.console.print("\n[bold]不同边框样式:[/bold]")

        boxes = [
            ("ASCII", box.ASCII),
            ("SIMPLE", box.SIMPLE),
            ("ROUNDED", box.ROUNDED),
            ("DOUBLE", box.DOUBLE),
        ]

        for name, box_style in boxes:
            self.console.print(f"\n{name}:")
            table = Table(box=box_style, show_header=False, width=30)
            table.add_column("样式")
            table.add_row("示例边框")
            self.console.print(table)
            time.sleep(0.5)

        self.wait_for_continue()

    def _demo_style(self):
        """演示Style组件"""
        self.clear_screen()
        self.console.print(Panel("Style - 样式管理", border_style="cyan"))

        self.console.print("\n[bold]创建和使用样式:[/bold]")

        # 创建样式
        error_style = Style(color="red", bold=True)
        success_style = Style(color="green", bold=True, underline=True)
        warning_style = Style(color="yellow", italic=True)

        self.console.print("错误信息", style=error_style)
        self.console.print("成功信息", style=success_style)
        self.console.print("警告信息", style=warning_style)

        self.console.print("\n[bold]样式组合:[/bold]")
        combined = error_style + Style(bgcolor="white")
        self.console.print("组合样式: 红色粗体 + 白色背景", style=combined)

        self.wait_for_continue()

    def _demo_all(self):
        """演示所有组件"""
        self.clear_screen()
        self.console.print(Panel("快速演示所有组件", border_style="cyan"))

        components_to_demo = [
            ("console", "Console - 基础输出"),
            ("panel", "Panel - 面板容器"),
            ("table", "Table - 表格"),
            ("tree", "Tree - 树状结构"),
            ("layout", "Layout - 布局管理"),
            ("text", "Text - 高级文本"),
            ("syntax", "Syntax - 语法高亮"),
            ("progress", "Progress - 进度条"),
            ("columns", "Columns - 列布局"),
            ("prompt", "Prompt - 交互提示"),
            ("box", "Box - 边框样式"),
            ("style", "Style - 样式管理"),
        ]

        for key, name in components_to_demo:
            if key in self.components and key != "all":
                self.clear_screen()
                self.console.print(Panel(f"正在演示: {name}", border_style="yellow"))
                self.components[key]["demo_func"]()

        self.clear_screen()
        self.console.print(Panel("所有组件演示完成！", border_style="green"))
        self.wait_for_continue()

    def run_demo(self, component_key: str):
        """运行指定组件的演示"""
        if component_key == "quit":
            self.clear_screen()
            self.console.print(Panel("感谢使用Rich演示器！", border_style="cyan"))
            sys.exit(0)

        if component_key in self.components:
            comp = self.components[component_key]
            if comp["demo_func"]:
                comp["demo_func"]()
        else:
            self.console.print("[red]无效的组件选择[/red]")
            self.wait_for_continue()

    def main_loop(self):
        """主循环"""
        while True:
            page_keys = self.show_menu(self.current_page)
            choice = self.get_user_choice(page_keys)

            if choice == 'prev':
                if self.current_page > 0:
                    self.current_page -= 1
                continue
            elif choice == 'next':
                max_page = (len(self.components) - 1) // self.items_per_page
                if self.current_page < max_page:
                    self.current_page += 1
                continue
            elif choice == 'menu':
                self.current_page = 0
                continue
            else:
                self.run_demo(choice)


def main():
    """主函数"""
    demo = RichDemoMenu()
    demo.main_loop()


if __name__ == "__main__":
    main()