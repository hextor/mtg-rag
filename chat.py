from textual.app import App, ComposeResult
from textual.widgets import Input, MarkdownViewer, Static, Label, Pretty
from textual.containers import VerticalScroll, Container
from chroma import InputPrompt

class UserMessage(Static):
    def __init__(self, text: str):
        super().__init__(text)
        self.add_class("user")


class ChatApp(App):
    CSS = """

    #chat {
        height: 1fr;
        padding: 1;
    }

    #input-bar {
        dock: bottom;
        padding: 1;
        background: $surface;
    }

    Input {
        width: 100%;
    }

    .user {
        background: $accent-darken-1;
        padding: 1;
        margin: 1 0;
    }

    MarkdownViewer {
        height: auto;
        background: $boost;
        margin: 1 0;
        padding: 1;
    }
    """

    def compose(self) -> ComposeResult:
        yield VerticalScroll(id="chat")
        yield Label("MTG Oracle")
        yield Input(
            placeholder="Type a message and press Enter…",
            id="input"
        )

    def on_input_submitted(self, event: Input.Submitted) -> None:
        chat = self.query_one("#chat", VerticalScroll)
        text = event.value.strip()

        if not text:
            return

        # User message
        chat.mount(UserMessage(f"You: {text}"))
        event.input.value = ""
        chat.scroll_end()

        response_markdown = InputPrompt(f"{text}")

        markdown_viewer = MarkdownViewer(
            response_markdown,
            show_table_of_contents=True,
        )

        chat.mount(markdown_viewer)
        chat.scroll_end()