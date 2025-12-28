from rich.console import Console
from rich.live import Live
from rich.layout import Layout
from rich.panel import Panel
from rich.text import Text
from rich.syntax import Syntax
from datetime import datetime
import time
import random


class CodeMonitor:
    def __init__(self):
        self.console = Console()
        self.layout = Layout()

        # 初始化状态变量
        self.progress = 0
        self.errors = 0
        self.warnings = 0
        self.current_line = 0  # 先初始化这个属性
        self.log_content = Text()

        # 创建三栏布局：代码 + 日志 + 状态
        self.layout.split_row(
            Layout(name="code", ratio=2),  # 代码显示区
            Layout(name="logs", ratio=1),  # 日志输出区
        )
        self.layout["logs"].split(
            Layout(name="log_content", ratio=3),
            Layout(name="status", size=6)  # 状态栏
        )

        # 初始化内容
        self.init_code_panel()
        self.init_log_panel()
        self.init_status_bar()

    def init_code_panel(self):
        """初始化代码显示面板"""
        self.code_content = '''def main():
    """主处理函数"""
    print("Starting data processing...")

    # 1. 加载数据
    data = load_data("input.csv")
    logger.info(f"Loaded {len(data)} records")

    # 2. 数据清洗
    cleaned_data = clean_data(data)
    if len(cleaned_data) < len(data):
        logger.warning(f"Removed {len(data)-len(cleaned_data)} invalid records")

    # 3. 数据分析
    try:
        analysis_result = analyze(cleaned_data)
    except Exception as e:
        logger.error(f"Analysis failed: {e}")
        return False

    # 4. 保存结果
    save_results(analysis_result, "output.json")
    logger.success("Processing completed successfully!")

    return True

# 辅助函数
def load_data(filename):
    """加载CSV数据"""
    # TODO: 实现数据加载
    pass

def clean_data(data):
    """数据清洗"""
    # TODO: 实现数据清洗
    return data

def analyze(data):
    """数据分析"""
    # TODO: 实现分析逻辑
    return {"summary": "Analysis complete"}

def save_results(results, filename):
    """保存结果到文件"""
    # TODO: 实现文件保存
    pass

if __name__ == "__main__":
    main()'''

        self.highlight_line = 0

        # 使用简单的Syntax初始化，避免调用未完全初始化的方法
        self.layout["code"].update(
            Panel(
                Syntax(self.code_content, "python", line_numbers=True),
                title="[bold blue]代码执行[/bold blue]",
                border_style="blue",
                padding=(0, 1)
            )
        )

    def get_highlighted_code(self):
        """获取高亮显示的代码"""
        lines = self.code_content.split('\n')
        highlighted = []

        for i, line in enumerate(lines, 1):
            if i == self.current_line:
                highlighted.append(f"[reverse blue]{line}[/reverse blue]")
            elif i in self.get_relevant_lines():
                highlighted.append(f"[cyan]{line}[/cyan]")
            else:
                highlighted.append(line)

        return Syntax('\n'.join(highlighted), "python", line_numbers=True)

    def get_relevant_lines(self):
        """获取当前相关的代码行"""
        # 基于当前进度返回相关行
        if self.progress < 20:
            return [1, 2, 3, 4]  # 函数开始
        elif self.progress < 40:
            return [5, 6, 7, 8]  # 数据加载
        elif self.progress < 60:
            return [9, 10, 11, 12]  # 数据清洗
        elif self.progress < 80:
            return [13, 14, 15, 16, 17]  # 数据分析
        else:
            return [18, 19, 20, 21, 22]  # 保存结果

    def init_log_panel(self):
        """初始化日志面板"""
        self.log_content.append("[dim]系统初始化完成，等待执行命令...\n[/dim]")

        self.layout["log_content"].update(
            Panel(
                self.log_content,
                title="[bold yellow]执行日志[/bold yellow]",
                border_style="yellow",
                padding=(1, 1)
            )
        )

    def init_status_bar(self):
        """初始化状态栏"""
        self.update_status_bar()

    def update_status_bar(self):
        """更新状态栏"""
        now = datetime.now().strftime("%H:%M:%S")

        # 创建进度条
        bar_length = 30
        filled = int(bar_length * self.progress / 100)
        progress_bar = "█" * filled + "░" * (bar_length - filled)

        # 创建状态文本
        status_text = Text()
        status_text.append("🚀 ", style="bold cyan")

        # 状态显示
        if self.progress < 20:
            status = "初始化"
            style = "cyan"
        elif self.progress < 60:
            status = "处理中"
            style = "green"
        elif self.progress < 90:
            status = "收尾中"
            style = "yellow"
        else:
            status = "完成"
            style = "bold green"

        status_text.append(f"{status}", style=style)
        status_text.append(" | ", style="dim")

        # 进度显示
        status_text.append("进度: ", style="bold")
        status_text.append(f"{progress_bar} {self.progress:3d}%", style="cyan")
        status_text.append(" | ", style="dim")

        # 代码位置
        status_text.append("行号: ", style="bold")
        status_text.append(f"{self.current_line:3d}", style="magenta")
        status_text.append(" | ", style="dim")

        # 错误/警告
        if self.errors > 0:
            status_text.append("错误: ", style="bold red")
            status_text.append(f"{self.errors}", style="red")
            status_text.append(" | ", style="dim")

        if self.warnings > 0:
            status_text.append("警告: ", style="bold yellow")
            status_text.append(f"{self.warnings}", style="yellow")
            status_text.append(" | ", style="dim")

        # 时间
        status_text.append(now, style="blue")

        self.layout["status"].update(
            Panel(
                status_text,
                border_style="green",
                padding=(0, 1)
            )
        )

    def add_log(self, message, level="INFO"):
        """添加日志消息"""
        timestamp = datetime.now().strftime("%H:%M:%S")

        # 根据日志级别设置样式
        if level == "INFO":
            style = "white"
            prefix = "[INFO]"
        elif level == "WARNING":
            style = "yellow"
            prefix = "[WARN]"
        elif level == "ERROR":
            style = "red"
            prefix = "[ERR]"
        elif level == "SUCCESS":
            style = "bold green"
            prefix = "[OK]"
        elif level == "DEBUG":
            style = "dim"
            prefix = "[DBG]"
        else:
            style = "white"
            prefix = "[LOG]"

        # 添加新日志
        log_line = Text()
        log_line.append(f"{timestamp} ", style="dim cyan")
        log_line.append(f"{prefix} ", style=style)
        log_line.append(f"{message}\n", style=style)

        self.log_content.append(log_line)

        # 限制日志行数
        lines = str(self.log_content).split('\n')
        if len(lines) > 25:  # 保留最近25行
            self.log_content = Text("\n".join(lines[-25:]) + "\n")

        # 更新日志面板
        self.layout["log_content"].update(
            Panel(
                self.log_content,
                title="[bold yellow]执行日志[/bold yellow]",
                border_style="yellow",
                padding=(1, 1)
            )
        )

    def update_code_execution(self):
        """更新代码执行位置"""
        # 基于进度更新当前执行行
        if self.progress < 10:
            self.current_line = 1
        elif self.progress < 20:
            self.current_line = 3
        elif self.progress < 30:
            self.current_line = 5
        elif self.progress < 40:
            self.current_line = 7
        elif self.progress < 50:
            self.current_line = 9
        elif self.progress < 60:
            self.current_line = 11
        elif self.progress < 70:
            self.current_line = 13
        elif self.progress < 80:
            self.current_line = 15
        elif self.progress < 90:
            self.current_line = 18
        elif self.progress < 95:
            self.current_line = 20
        else:
            self.current_line = 22

        # 更新代码面板
        self.layout["code"].update(
            Panel(
                self.get_highlighted_code(),
                title="[bold blue]代码执行[/bold blue]",
                border_style="blue",
                padding=(0, 1)
            )
        )

    def run(self):
        """运行监控系统"""
        with Live(self.layout, refresh_per_second=10, screen=True):
            self.console.print("[bold cyan]🚀 开始代码执行监控...[/bold cyan]\n")

            # 初始日志
            self.add_log("系统初始化完成", "INFO")
            self.add_log("加载代码文件: process.py", "INFO")
            self.add_log("准备开始执行", "SUCCESS")

            # 模拟执行过程
            for step in range(1, 101):
                time.sleep(0.1)
                self.progress = step

                # 更新代码执行位置
                self.update_code_execution()

                # 触发特定步骤的日志
                if step in [5, 15, 25, 35, 45, 55, 65, 75, 85, 95]:
                    self.add_log(f"执行进度: {step}%", "INFO")

                # 模拟错误和警告
                if step == 30:
                    self.warnings += 1
                    self.add_log("检测到异常数据格式，自动修复中...", "WARNING")
                elif step == 50:
                    self.errors += 1
                    self.add_log("文件写入失败，正在重试...", "ERROR")
                elif step == 80:
                    self.errors = 0  # 错误被修复
                    self.add_log("重试成功，文件写入完成", "SUCCESS")

                # 模拟函数调用日志
                if step == 10:
                    self.add_log("调用 load_data('input.csv')", "DEBUG")
                    self.add_log("正在读取CSV文件...", "INFO")
                elif step == 25:
                    self.add_log("调用 clean_data()", "DEBUG")
                    self.add_log("验证数据格式...", "INFO")
                elif step == 45:
                    self.add_log("调用 analyze()", "DEBUG")
                    self.add_log("运行分析算法...", "INFO")
                elif step == 70:
                    self.add_log("调用 save_results()", "DEBUG")
                    self.add_log("序列化数据...", "INFO")

                # 随机添加性能日志
                if random.random() < 0.2 and step < 95:
                    log_type, template = random.choice([
                        ("INFO", "内存使用: {}MB"),
                        ("INFO", "CPU使用率: {}%"),
                        ("DEBUG", "处理速度: {} records/sec"),
                        ("INFO", "缓存命中率: {}%"),
                    ])
                    value = random.randint(20, 80) if step < 50 else random.randint(60, 95)
                    self.add_log(template.format(value), log_type)

                # 更新状态栏
                self.update_status_bar()

            # 最终状态
            self.add_log("✅ 程序执行成功完成！", "SUCCESS")
            self.add_log(f"总耗时: 10.2秒 | 错误: {self.errors} | 警告: {self.warnings}", "INFO")
            time.sleep(2)


def main():
    """主函数入口"""
    try:
        monitor = CodeMonitor()
        monitor.run()
    except KeyboardInterrupt:
        print("\n[yellow]程序被用户中断[/yellow]")
    except Exception as e:
        print(f"[red]程序执行出错: {e}[/red]")

if __name__ == "__main__":
    main()