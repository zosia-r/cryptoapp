from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Button, Static
from textual.containers import Vertical, Horizontal

from app.views.income_view import IncomeView
from app.views.expense_view import ExpenseView
from app.views.report_selector_view import ReportSelectorView
from app.views.sign_view import SignView

class DashboardView(Screen):
    CSS_PATH = ["styles/base.tcss", "styles/dashboard.tcss"]

    def __init__(self, username: str, encryption_key: bytes):
        super().__init__()
        self.username = username
        self.encryption_key = encryption_key

    def compose(self) -> ComposeResult:
        with Vertical(id="main_container"):
            with Horizontal(id="top_bar"):
                yield Static(f"Hello, {self.username}", id="welcome_text")
                yield Button("Logout", id="logout_btn")

            with Vertical(id="dashboard_container"):
                with Horizontal(classes="dashboard_row", id="dashboard_row1"):
                    yield Button("Add Expense", classes="dashboard_button", id="add_expense_btn")
                    yield Button("Add Income", classes="dashboard_button", id="add_income_btn")
                with Horizontal(classes="dashboard_row", id="dashboard_row2"):
                    yield Button("Generate Report", classes="dashboard_button", id="report_btn")
                with Horizontal(classes="dashboard_row", id="dashboard_row3"):
                    yield Button("Sign Report", classes="dashboard_button", id="sign_report_btn")    
                    yield Button("Check Report", classes="dashboard_button", id="check_report_btn")

                yield Static("Cryptography 2025 – Zofia Różańska & Selina Zundel", id="credits")

    def on_mount(self):
        self.query_one("#add_expense_btn").focus()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        match event.button.id:
            case "add_expense_btn":
                self.app.push_screen(ExpenseView(username=self.username, encryption_key=self.encryption_key))
            case "add_income_btn":
                self.app.push_screen(IncomeView(username=self.username, encryption_key=self.encryption_key))
            case "report_btn":
                self.app.push_screen(ReportSelectorView(username=self.username, encryption_key=self.encryption_key))
            case "sign_report_btn":
                self.app.push_screen(SignView(username=self.username))
            case "check_report_btn":
                pass #TODO: implement check report functionality
            case "logout_btn":
                self.app.pop_screen()
