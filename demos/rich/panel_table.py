#!/usr/bin/env python3
"""
脚本管理器中的Panel+Table组合
"""


from rich import box
from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel
from rich.table import Table

console = Console()

def create_script_manager():
    """创建脚本管理器界面"""

    # 脚本列表表格
    script_table = Table(title="脚本列表", box=box.ROUNDED, show_lines=True)
    script_table.add_column("选择", style="cyan", width=8, justify="center")
    script_table.add_column("名称", style="magenta")
    script_table.add_column("类型", style="green", width=10)
    script_table.add_column("大小", justify="right", style="dim")
    script_table.add_column("最后修改", style="dim")
    script_table.add_column("操作", style="bold", width=20)

    scripts = [
        ("[✓]", "system_backup.sh", "Shell", "4.2KB", "2024-01-15", "[green]▶ 运行[/green] [blue]✏ 编辑[/blue]"),
        ("[ ]", "log_analyzer.py", "Python", "8.7KB", "2024-01-14", "[green]▶ 运行[/green] [blue]✏ 编辑[/blue]"),
        ("[ ]", "database_sync.sh", "Shell", "3.8KB", "2024-01-13", "[green]▶ 运行[/green] [blue]✏ 编辑[/blue]"),
        ("[ ]", "monitor_alert.py", "Python", "12.1KB", "2024-01-12", "[green]▶ 运行[/green] [blue]✏ 编辑[/blue]"),
        ("[ ]", "file_cleaner.sh", "Shell", "2.3KB", "2024-01-11", "[green]▶ 运行[/green] [blue]✏ 编辑[/blue]"),
    ]

    for script in scripts:
        script_table.add_row(*script)

    # 执行历史表格
    history_table = Table(title="执行历史", box=box.SIMPLE)
    history_table.add_column("时间", style="dim", width=16)
    history_table.add_column("脚本", style="cyan")
    history_table.add_column("状态", style="bold")
    history_table.add_column("耗时", justify="right")
    history_table.add_column("输出", style="dim")

    history = [
        ("2024-01-15 10:30", "system_backup.sh", "[green]成功[/green]", "45s", "2.4GB"),
        ("2024-01-15 09:15", "log_analyzer.py", "[green]成功[/green]", "3s", "128KB"),
        ("2024-01-14 16:20", "database_sync.sh", "[red]失败[/red]", "12s", "错误: 连接超时"),
        ("2024-01-14 14:10", "monitor_alert.py", "[green]成功[/green]", "8s", "警报已发送"),
        ("2024-01-13 11:45", "file_cleaner.sh", "[green]成功[/green]", "25s", "清理了2.1GB"),
    ]

    for record in history:
        history_table.add_row(*record)

    # 创建布局
    layout = Layout()
    layout.split_column(
        Layout(name="top"),
        Layout(name="bottom", size=12)
    )

    # 顶部Panel：脚本列表
    script_panel = Panel(
        script_table,
        title="📁 脚本管理",
        border_style="blue",
        subtitle="Space: 选择 | Enter: 运行 | E: 编辑 | D: 删除"
    )
    layout["top"].update(script_panel)

    # 底部Panel：执行历史
    history_panel = Panel(
        history_table,
        title="📜 执行历史",
        border_style="green",
        subtitle="R: 重新运行 | C: 清除历史 | F: 过滤"
    )
    layout["bottom"].update(history_panel)

    return layout

def main():
    console.clear()

    # 创建标题
    title = Panel(
        "[bold cyan]🚀 脚本管理器 v1.0[/bold cyan]\n"
        "[dim]一个基于Rich的终端脚本管理工具[/dim]",
        border_style="cyan",
        box=box.DOUBLE
    )
    console.print(title)

    # 创建主界面
    layout = create_script_manager()
    console.print(layout)

    # 状态栏
    status = Panel(
        "就绪 | 选中: 1个脚本 | 总计: 5个脚本 | 按 Q 退出",
        border_style="dim",
        box=box.SIMPLE
    )
    console.print(status)

if __name__ == "__main__":
    main()
