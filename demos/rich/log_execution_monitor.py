import random
import time
from datetime import datetime

from rich.console import Console
from rich.layout import Layout
from rich.live import Live
from rich.panel import Panel
from rich.text import Text


class StatusBar:
    def __init__(self):
        self.console = Console()
        self.layout = Layout()

        # 分割布局：日志区 + 状态栏
        self.layout.split(
            Layout(name="logs", ratio=5),  # 日志区域
            Layout(name="status", size=3)  # 状态栏
        )

        # 初始化日志
        self.log_content = Text()
        self.layout["logs"].update(
            Panel(
                self.log_content,
                title="[bold]系统日志[/bold]",
                border_style="green",
                padding=(1, 1)
            )
        )

        # 初始化状态栏
        self.update_status_bar()

    def _create_status_bar(self,
                           status="准备中",
                           progress=0,
                           errors=0,
                           warnings=0):
        """创建状态栏内容"""
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # 创建进度条
        bar_length = 30
        filled = int(bar_length * progress / 100)
        progress_bar = "█" * filled + "░" * (bar_length - filled)

        status_text = Text()
        status_text.append("状态: ", style="bold")

        # 动态状态样式
        if status == "准备中":
            status_text.append(f"{status}", style="cyan")
        elif status == "运行中":
            status_text.append(f"{status}", style="green")
        elif status == "警告":
            status_text.append(f"{status}", style="yellow")
        elif status == "错误":
            status_text.append(f"{status}", style="red")
        else:
            status_text.append(f"{status}", style="white")

        status_text.append(" | ", style="dim")
        status_text.append("进度: ", style="bold")
        status_text.append(f"{progress_bar} {progress:3d}%", style="cyan")
        status_text.append(" | ", style="dim")
        status_text.append("任务: ", style="bold")
        status_text.append(f"{progress}", style="magenta")
        status_text.append(" | ", style="dim")
        status_text.append("错误: ", style="bold red")
        status_text.append(f"{errors}", style="red")
        status_text.append(" | ", style="dim")
        status_text.append("警告: ", style="bold yellow")
        status_text.append(f"{warnings}", style="yellow")
        status_text.append(" | ", style="dim")
        status_text.append(now, style="blue")

        return Panel(
            status_text,
            border_style="cyan",
            title="[bold]状态监控[/bold]",
            padding=(0, 1)
        )

    def update_status_bar(self, **kwargs):
        """更新状态栏"""
        self.layout["status"].update(self._create_status_bar(**kwargs))

    def add_log(self, message, level="INFO"):
        """添加日志消息"""
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]

        # 根据日志级别设置样式
        if level == "INFO":
            style = "green"
            prefix = "ℹ"
        elif level == "WARNING":
            style = "yellow"
            prefix = "⚠"
        elif level == "ERROR":
            style = "red"
            prefix = "✗"
        elif level == "SUCCESS":
            style = "bold green"
            prefix = "✓"
        else:
            style = "white"
            prefix = "·"

        # 添加新日志（显示最新的在最下面）
        log_line = Text()
        log_line.append(f"[{timestamp}] ", style="dim cyan")
        log_line.append(f"{prefix} ", style=style)
        log_line.append(f"{message}\n", style=style)

        self.log_content.append(log_line)

        # 限制日志行数，防止内存过大
        lines = str(self.log_content).split('\n')
        if len(lines) > 30:  # 保留最近30行
            self.log_content = Text("\n".join(lines[-30:]) + "\n")

        # 更新日志面板
        self.layout["logs"].update(
            Panel(
                self.log_content,
                title="[bold]系统日志[/bold]",
                border_style="green",
                padding=(1, 1)
            )
        )

    def run(self):
        """运行状态栏示例"""
        # 模拟任务处理
        tasks = [
            ("初始化系统...", "INFO"),
            ("加载配置文件 config.yaml", "INFO"),
            ("连接数据库...", "INFO"),
            ("数据库连接成功", "SUCCESS"),
            ("开始处理用户数据", "INFO"),
            ("处理第1批数据 (100条记录)", "INFO"),
            ("检测到异常数据格式", "WARNING"),
            ("数据验证通过", "SUCCESS"),
            ("处理第2批数据 (200条记录)", "INFO"),
            ("内存使用率超过80%", "WARNING"),
            ("清理临时文件...", "INFO"),
            ("生成统计报告", "INFO"),
            ("写入输出文件 output.csv", "INFO"),
            ("文件保存成功", "SUCCESS"),
            ("发送邮件通知...", "INFO"),
            ("邮件发送失败，重试中...", "ERROR"),
            ("邮件发送成功", "SUCCESS"),
            ("任务执行完成", "INFO"),
        ]

        # 实时更新状态栏和日志
        with Live(self.layout, refresh_per_second=10, screen=True):
            errors = 0
            warnings = 0
            task_index = 0

            for progress in range(1, 101):
                time.sleep(0.15)  # 稍微慢一点，方便观察

                # 根据进度触发日志
                if task_index < len(tasks) and progress >= (task_index + 1) * (100 // len(tasks)):
                    message, level = tasks[task_index]
                    self.add_log(message, level)

                    # 更新错误/警告计数
                    if level == "ERROR":
                        errors += 1
                    elif level == "WARNING":
                        warnings += 1

                    task_index += 1

                # 随机状态变化
                if progress < 30:
                    status = "准备中"
                elif progress < 80:
                    status = "运行中"
                elif progress < 95:
                    status = "警告"
                else:
                    status = "完成"

                # 随机添加一些额外的日志
                if random.random() < 0.1 and progress < 95:
                    extra_messages = [
                        f"处理进度: {progress}%",
                        f"内存使用: {60 + progress // 3}%",
                        f"CPU负载: {40 + progress // 2}%",
                        f"处理速度: {progress * 2} 条/秒",
                    ]
                    self.add_log(random.choice(extra_messages), "INFO")

                # 更新状态栏
                self.update_status_bar(
                    status=status,
                    progress=progress,
                    errors=errors,
                    warnings=warnings
                )

            # 最后一条完成日志
            self.add_log("所有任务执行完成！", "SUCCESS")
            time.sleep(2)


def main():
    """主函数入口"""
    print("[bold cyan]开始运行实时日志监控系统...[/bold cyan]\n")
    status_bar = StatusBar()
    status_bar.run()
    print("\n[bold green]程序执行完毕！[/bold green]")

if __name__ == "__main__":
    main()
