import time
from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Button, Label, Input, Static
from textual.containers import Vertical, Horizontal
from app.core.auth import register_user, is_strong_password
from app.views.login_view import LoginView

class RegisterView(Screen):
    CSS_PATH = "styles/styles.tcss"

    def compose(self) -> ComposeResult:
        with Vertical():
            yield Static("Register", id="title")
            yield Input(placeholder="Username", id="username")
            yield Input(password=True, placeholder="Password", id="password")
            yield Input(password=True, placeholder="Confirm Password", id="confirm_password")
            yield Static("", id="error_message")
            yield Static("", id="message")
            with Horizontal(id="button_row"):
                yield Button("Submit", id="submit_btn")
                yield Button("Back", id="back_btn")
            yield Static("Cryptography 2025 – Zofia Różańska & Selina Zundel", id="credits")

    def on_mount(self) -> None:
        self.query_one("#username").focus()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "submit_btn":
            username = self.query_one("#username", Input).value.strip()
            password = self.query_one("#password", Input).value.strip()
            confirm = self.query_one("#confirm_password", Input).value.strip()
            error_message = self.query_one("#error_message", Static)
            message = self.query_one("#message", Static)

            if password != confirm:
                error_message.update("Passwords do not match.")
                self.query_one("#password", Input).value = ""
                self.query_one("#confirm_password", Input).value = ""
                self.query_one("#password", Input).focus()
            elif not is_strong_password(password):
                error_message.update("Password is too weak. Min 8 chars, 1 uppercase, 1 number and 1 special character.")
                self.query_one("#password", Input).value = ""
                self.query_one("#confirm_password", Input).value = ""
                self.query_one("#password", Input).focus()
            elif not register_user(username, password):
                error_message.update("Username already exists.")
                self.query_one("#username", Input).value = ""
                self.query_one("#username", Input).focus()
            else:
                error_message.update("")
                message.update("Registration successful!")
                self.set_timer(2, lambda: self.app.push_screen(LoginView()))


        elif event.button.id == "back_btn":
            self.app.pop_screen()
