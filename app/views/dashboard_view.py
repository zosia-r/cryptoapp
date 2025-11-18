from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Button, Static
from textual.containers import Vertical, Horizontal

class DashboardView(Screen):
    CSS_PATH = ["styles/base.tcss", "styles/dashboard.tcss"]

    def __init__(self, username: str):
        super().__init__()
        self.username = username

    def compose(self) -> ComposeResult:
        with Vertical(id="main_container"):
            with Horizontal(id="top_bar"):
                yield Static(f"Hello, {self.username}", id="welcome_text")
                yield Button("Edit Profile", id="edit_profile_btn")
                yield Button("Logout", id="logout_btn")

            with Vertical(id="dashboard_container"):
                with Horizontal(classes="dashboard_row", id="dashboard_row1"):
                    yield Button("Add Expense", classes="dashboard_button", id="add_expense_btn")
                    yield Button("Add Income", classes="dashboard_button", id="add_income_btn")
                with Horizontal(classes="dashboard_row", id="dashboard_row2"):
                    yield Button("Generate Report", classes="dashboard_button", id="report_btn")
                    yield Button("Check Report", classes="dashboard_button", id="check_report_btn")

                yield Static("Cryptography 2025 – Zofia Różańska & Selina Zundel", id="credits")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        match event.button.id:
            case "add_expense_btn":
                self.app.push_screen("add_expense")
            case "add_income_btn":
                self.app.push_screen("add_income")
            case "edit_profile_btn":
                self.app.push_screen("edit_profile")
            case "report_btn":
                self.app.push_screen("report")
            case "check_report_btn":
                self.app.push_screen("check_report")
            case "logout_btn":
                self.app.pop_screen()
