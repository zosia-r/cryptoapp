from datetime import datetime
from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Header, Button, Label, Static
from textual.containers import VerticalScroll, Horizontal
from app.views.login_view import LoginView

ASCII_ART = r"""
  ____                  _          _                
 / ___|_ __ _   _ _ __ | |_ ___   / \   _ __  _ __  
| |   | '__| | | | '_ \| __/ _ \ / _ \ | '_ \| '_ \ 
| |___| |  | |_| | |_) | || (_) / ___ \| |_) | |_) |
 \____|_|   \__, | .__/ \__\___/_/   \_\ .__/| .__/ 
            |___/|_|                   |_|   |_|    
"""

class WelcomeView(Screen):
    CSS_PATH = "styles/welcome_view.tcss"

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with VerticalScroll():
            yield Static(ASCII_ART, id="title")
            yield Label("Manage your expenses. Securely.", id="subtitle")
            yield Label(f"Date: {datetime.now().strftime('%d %b %Y')}", id="date")
            with Horizontal(id="button_row"):
                yield Button("Login", id="login_btn")
                yield Button("Register", id="register_btn")
            yield Static("Cryptography 2025 – Zofia Różańska & Selina Zundel", id="credits")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "login_btn":
            self.app.push_screen(LoginView())
        elif event.button.id == "register_btn":
            self.app.push_screen("register")
