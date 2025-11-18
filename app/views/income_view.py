from datetime import date
from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Button, Label, Input, Static, Select
from textual.containers import Vertical, Horizontal

from app.core.data_storage import add_income


class IncomeView(Screen):
    CSS_PATH = ["styles/base.tcss"]

    def __init__(self, username: str):
        super().__init__()
        self.username = username

    def compose(self) -> ComposeResult:
        with Vertical():
            yield Static("Add Income", id="title")

            yield Input(placeholder="Amount", id="amount")

            yield Select(
                options=[
                    ("Salary", "salary"),
                    ("Gift", "gift"),
                    ("Freelance", "freelance"),
                    ("Investment", "investment"),
                    ("Other", "other"),
                ],
                id="category",
            )

            yield Input(placeholder="Date (YYYY-MM-DD)", id="date_input")

            yield Static("", id="error_message")
            yield Static("", id="message")

            with Horizontal(id="button_row"):
                yield Button("Submit", id="submit_btn")
                yield Button("Back", id="back_btn")

            yield Static("Cryptography 2025 – Zofia Różańska & Selina Zundel", id="credits")

    def on_mount(self) -> None:
        self.query_one("#amount").focus()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "submit_btn":
            amount = self.query_one("#amount", Input).value.strip()
            category = self.query_one("#category", Select).value
            date_str = self.query_one("#date_input", Input).value.strip()

            error = self.query_one("#error_message", Static)
            msg = self.query_one("#message", Static)

            error.update("")
            msg.update("")

            try:
                float(amount)
            except ValueError:
                error.update("Amount must be a valid number.")
                return

            try:
                date.fromisoformat(date_str)
            except ValueError:
                error.update("Invalid date format. Use YYYY-MM-DD.")
                return

            add_income(self.username, float(amount), category, date_str)
            msg.update("Income added successfully.")

            self.query_one("#amount", Input).value = ""
            self.query_one("#date_input", Input).value = ""
            self.query_one("#amount").focus()

        elif event.button.id == "back_btn":
            self.app.pop_screen()
