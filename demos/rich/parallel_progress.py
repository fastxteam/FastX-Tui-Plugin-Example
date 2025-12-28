import time

from rich.console import Console
from rich.layout import Layout
from rich.live import Live
from rich.panel import Panel
from rich.progress import (
    BarColumn,
    Progress,
    SpinnerColumn,
    TaskProgressColumn,
    TextColumn,
    TimeElapsedColumn,
    TimeRemainingColumn,
)


def main():
    """主函数入口"""
    console = Console()

    # 创建多个进度条
    progress = Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        TimeRemainingColumn(),
        TimeElapsedColumn(),
        expand=True
    )

    # 创建布局
    layout = Layout()
    layout.split(
        Layout(name="header", size=3),
        Layout(name="main"),
        Layout(name="footer", size=3)
    )

    # 创建任务
    task1 = progress.add_task("[red]下载...", total=100)
    task2 = progress.add_task("[green]处理...", total=100)
    task3 = progress.add_task("[blue]上传...", total=100)

    # 实时更新
    with Live(layout, refresh_per_second=10):
        # 更新头部
        layout["header"].update(
            Panel("[bold cyan]多任务处理系统[/bold cyan]",
                  border_style="yellow")
        )

        # 更新主内容区
        layout["main"].update(progress)

        # 更新底部状态栏
        for i in range(100):
            time.sleep(0.05)
            progress.update(task1, advance=1)
            if i % 2 == 0:
                progress.update(task2, advance=1)
            if i % 3 == 0:
                progress.update(task3, advance=1)

            # 动态更新底部状态
            layout["footer"].update(
                Panel(f"[bold]统计:[/bold] "
                      f"已完成: {i + 1}% | "
                      f"速度: {i * 2} KB/s | "
                      f"内存: {70 + i % 30}%",
                      border_style="green")
            )

if __name__ == "__main__":
    main()
