from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Button, Input, Static
from textual.containers import Vertical, Horizontal

from app.views.dashboard_view import DashboardView
from app.core.auth import authenticate_user


class LoginView(Screen):
    """Screen for user login"""

    CSS_PATH = "styles/styles.tcss"

    def compose(self) -> ComposeResult:
        with Vertical():
            yield Static("Login", id="title")
            yield Input(placeholder="Username", id="username")
            yield Input(password=True, placeholder="Password", id="password")
            yield Static("", id="error_message")
            with Horizontal(id="button_row"):
                yield Button("Submit", id="submit_btn")
                yield Button("Back", id="back_btn")
            yield Static("Cryptography 2025 – Zofia Różańska & Selina Zundel", id="credits")


    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "submit_btn":
            username = self.query_one("#username", Input).value
            password = self.query_one("#password", Input).value
            if authenticate_user(username, password):
                self.app.push_screen(DashboardView(username))
            else:
                message = self.query_one("#error_message", Static)
                message.update("Incorrect username or password. Try again.")
                self.query_one("#username", Input).value = ""
                self.query_one("#password", Input).value = ""
                self.query_one("#username", Input).focus()
        elif event.button.id == "back_btn":
            self.app.pop_screen()

    
    def on_mount(self) -> None:
        self.query_one("#username").focus()

