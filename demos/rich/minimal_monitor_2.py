import time
from datetime import datetime

from rich.console import Console
from rich.live import Live
from rich.text import Text


def create_simple_status(message="", progress=0):
    """创建简约状态栏"""
    now = datetime.now().strftime("%H:%M:%S")

    # 创建进度条
    bar_length = 20
    filled = int(bar_length * progress / 100)
    bar = "█" * filled + "░" * (bar_length - filled)

    status = Text()
    status.append("│ ", style="dim")
    status.append(message.ljust(30), style="cyan")
    status.append("│ ", style="dim")
    status.append(f"{bar} {progress:3d}%", style="green")
    status.append(" │ ", style="dim")
    status.append(now, style="yellow")
    status.append(" │", style="dim")

    return status


def main():
    """主函数入口"""
    console = Console()

    # 实时更新状态
    with Live(create_simple_status(), refresh_per_second=4) as live:
        for i in range(101):
            time.sleep(0.05)
            messages = [
                "正在初始化...",
                "加载配置文件...",
                "处理数据...",
                "保存结果...",
                "清理资源..."
            ]
            message = messages[(i // 25) % len(messages)]
            live.update(create_simple_status(message, i))

if __name__ == "__main__":
    main()
