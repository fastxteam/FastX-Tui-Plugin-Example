from textual.app import App, ComposeResult
from textual.containers import ScrollableContainer
from textual.widgets import Header, Footer, Static
from textual import events


class ScrollableHelpApp(App):
    """使用Textual的可滚动帮助应用"""

    def compose(self) -> ComposeResult:
        yield Header()
        yield ScrollableContainer(
            Static("你的长内容在这里...你的长内容在这里...你的长内容在这里...你的长内容在这里...你的长内容在这里...你的长内容在这里...你的长内容在这里...你的长内容在这里...你的长内容在这里...你的长内容在这里...你的长内容在这里...你的长内容在这里...你的长内容在这里...你的长内容在这里...你的长内容在这里...你的长内容在这里...你的长内容在这里...你的长内容在这里...你的长内容在这里...你的长内容在这里...你的长内容在这里...你的长内容在这里...你的长内容在这里...你的长内容在这里...你的长内容在这里...你的长内容在这里...你\n\n\\n\n\\n\n\\n\n\\n\n\\n\n\\n\n\\n\n\\n\n\\n\n\\n\n\\n\n\\n\n\\n\n\\n\n\\n\n\\n\n\\n\n\\n\n\\n\n\\n\n\\n\n\\n\n\\n\n\\n\n\\n\n\\n\n\\n\n\\n\n\\n\n\\n\n\\n\n\\n\n\\n\n\\n\n\\n\n\\n\n\\n\n\\n\n\\n\n\\n\n\\n\n\\n\n\\n\n\\n\n\\n\n\\n\n\\n\n\\n\n\\n\n\\n\n\\n\n\\n\n\\n\n\\n\n\\n\n\\n\n\\n\n\\n\n\\n\n\\n\n\\n\n\\n\n\\n\n\\n\n\\n\n\\n\n\\n\n\\n\n\\n\n\\n\n\\n\n\\n\n\\n\n\\n\n\\n\n\\n\n\\n\n\\n\n\\n\n\\n\n\\n\n\\n\n\\n\n\\n\n\\n\n\\n\n\\n\n\\n\n\\n\n\的长内容在这里...你的长内容在这里...你的长内容在这里...你的长内容在这里...你的长内容在这里...你的长内容在这里...你的长内容在这里...你的长内容在这里...你的长内容在这里...\n\n\n"),
            id="help-content"
        )
        yield Footer()

    def on_key(self, event: events.Key):
        if event.key == "q":
            self.exit()


if __name__ == "__main__":
    app = ScrollableHelpApp()
    app.run()