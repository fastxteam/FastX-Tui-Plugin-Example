import random
import time

from rich.columns import Columns
from rich.console import Console
from rich.live import Live
from rich.panel import Panel


def generate_dynamic_status(counter):
    """生成动态状态栏内容"""
    # 动态数据
    cpu_usage = 30 + (counter * 5) % 70
    memory_usage = 60 + random.randint(-5, 10)

    # 创建状态面板 - 固定高度内容
    status_content = (
        f"[bold cyan]系统状态[/bold cyan]\n"
        f"[green]✓ 运行中[/green] | 时间: {time.strftime('%H:%M:%S')}\n"
        f"CPU使用率: {cpu_usage:02d}%\n"
        f"内存使用: {memory_usage:02d}% {'[yellow]⚠[/yellow]' if memory_usage > 80 else '[green]✓[/green]'}\n"
        f"任务数量: {counter}\n"
        f"网络状态: 正常\n"
        f"磁盘空间: 65%"
    )

    status_panel = Panel(
        status_content,
        title="监控面板",
        border_style="blue",
        padding=(1, 2),
        height=10  # 固定高度
    )

    # 动态进度
    file_progress = min(100, 10 + counter * 15)
    data_progress = min(100, 20 + counter * 12)
    export_progress = min(100, 5 + counter * 8)

    # 进度条字符
    file_bar = '█' * (file_progress // 10) + '░' * (10 - file_progress // 10)
    data_bar = '█' * (data_progress // 10) + '░' * (10 - data_progress // 10)
    export_bar = '█' * (export_progress // 10) + '░' * (10 - export_progress // 10)

    # 创建进度面板 - 固定高度内容
    progress_content = (
        "[bold magenta]处理进度[/bold magenta]\n\n"
        f"文件处理: {file_bar} {file_progress}%\n"
        f"数据分析: {data_bar} {data_progress}%\n"
        f"导出结果: {export_bar} {export_progress}%\n"
        f"\n[dim]整体进度: {(file_progress + data_progress + export_progress) // 3}%[/dim]\n"
        f"[dim]迭代次数: {counter}[/dim]"
    )

    progress_panel = Panel(
        progress_content,
        title="进度",
        border_style="green",
        padding=(1, 2),
        height=10  # 固定高度
    )

    # 添加第三个面板 - 日志面板
    log_msgs = [
        f"[dim]{time.strftime('%H:%M:%S')}[/dim] 系统启动",
        f"[dim]{time.strftime('%H:%M:%S')}[/dim] 加载配置文件",
        f"[dim]{time.strftime('%H:%M:%S')}[/dim] 开始处理任务 {counter}",
        f"[dim]{time.strftime('%H:%M:%S')}[/dim] 内存使用: {memory_usage}%",
        f"[dim]{time.strftime('%H:%M:%S')}[/dim] CPU负载: {cpu_usage}%"
    ]

    if counter > 5:
        log_msgs.append(f"[green]{time.strftime('%H:%M:%S')}[/green] 完成前5个任务")
    if counter > 10:
        log_msgs.append(f"[green]{time.strftime('%H:%M:%S')}[/green] 达到10个任务")
    if counter > 15:
        log_msgs.append(f"[green]{time.strftime('%H:%M:%S')}[/green] 即将完成")

    # 确保日志面板也有足够内容填满高度
    while len(log_msgs) < 7:  # 确保至少7行
        log_msgs.append(f"[dim]{time.strftime('%H:%M:%S')}[/dim] 系统运行正常")

    log_content = "[bold yellow]系统日志[/bold yellow]\n\n" + "\n".join(log_msgs[-7:])  # 显示最近7条

    log_panel = Panel(
        log_content,
        title="日志",
        border_style="yellow",
        padding=(1, 2),
        height=10  # 固定高度
    )

    return Columns([status_panel, progress_panel, log_panel], expand=True)


def main():
    """主函数入口"""
    console = Console()

    # 使用 Live 实时更新
    console.print("[bold]开始实时监控系统状态...[/bold]\n")
    console.print("按 Ctrl+C 停止监控\n")

    try:
        with Live(generate_dynamic_status(0), refresh_per_second=4, screen=True) as live:
            for i in range(1, 21):  # 运行20次迭代
                time.sleep(0.5)
                # 更新状态
                live.update(generate_dynamic_status(i))

            # 最后显示完成状态
            live.update(generate_dynamic_status(20))
            time.sleep(1)

    except KeyboardInterrupt:
        console.print("\n[yellow]监控已手动停止[/yellow]")

    # 最终状态汇总
    console.print("\n[bold cyan]最终状态汇总：[/bold cyan]")
    console.print("✓ 文件处理: 100% 完成")
    console.print("✓ 数据分析: 100% 完成")
    console.print("✓ 导出结果: 100% 完成")
    console.print("✓ 系统运行正常")

if __name__ == "__main__":
    main()
