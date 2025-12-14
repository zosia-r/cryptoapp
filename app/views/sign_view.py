from textual.screen import Screen
from textual.widgets import Button, Input, Label, Static, RadioSet, RadioButton
from textual.containers import Vertical, Horizontal

from app.cryptography.rsa import sign_pdf

from app.core.report import get_unsigned_reports

class SignView(Screen):

    CSS_PATH = ["styles/base.tcss", "styles/dashboard.tcss"]

    def __init__(self, username: str):
        super().__init__()
        self.username = username
        self.selected_year = None
        self.reports_info = get_unsigned_reports(self.username)
        self.password = ""

    def compose(self):
        with Vertical(id="main-container"):
            yield Label("Select year to sign:", id="title")
            if self.reports_info:
                yield RadioSet(
                    *[
                        RadioButton(f"{report['year']}: {report['filename']}", id=f"year_{report['year']}")
                        for report in self.reports_info
                    ],
                    id="year_selector"
                )
                yield Input(placeholder="Password", password=True, id="password")
            else:
                yield Static("No unsigned reports found for this user.", id="no_records")
            
            yield Static("", id="error_message")
            yield Static("", id="message")
            with Horizontal(id="button_row"):
                if self.reports_info:
                    yield Button("Submit", id="submit_btn")
                yield Button("Back", id="back_btn")
            yield Static("Cryptography 2025 – Zofia Różańska & Selina Zundel", id="credits")

    def on_radio_set_changed(self, event: RadioSet.Changed):
        self.selected_year = int(event.pressed.id.removeprefix("year_"))

    def on_button_pressed(self, event):
        if event.button.id == "back_btn":
            self.app.pop_screen()

        elif event.button.id == "submit_btn":
            if self.selected_year is None:
                    self.query_one("#error_message", Static).update("Please select a year!")
                    return
            
            self.password = self.query_one("#password").value
            if not self.password:
                self.query_one("#error_message", Static).update("Please enter your password!")
                return
            
            self.query_one("#error_message").update("")

            try:
                reports_by_year = {
                    r["year"]: r for r in get_unsigned_reports(self.username)
                }
                pdf_path = reports_by_year[self.selected_year]["path"]

                signature_path = sign_pdf(self.username, pdf_path, self.password)

                self.query_one("#message").update(f"Report signed successfully: {signature_path}")
            
            except Exception as e:
                self.query_one("#error_message").update(f"Error signing report: {str(e)}")
