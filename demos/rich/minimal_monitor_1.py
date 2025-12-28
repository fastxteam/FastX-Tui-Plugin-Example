import time

from rich.console import Console
from rich.status import Status


def main():
    """主函数入口"""
    console = Console()

    # 创建状态栏
    with Status("[bold blue]处理中...", spinner="dots") as status:
        # 更新状态信息
        time.sleep(1)
        status.update("[bold green]加载数据...")
        time.sleep(1)
        status.update("[bold yellow]处理数据...")
        time.sleep(1)
        status.update("[bold red]保存结果...")
        time.sleep(1)

    console.print("[bold green]✓ 任务完成！")

if __name__ == "__main__":
    main()
