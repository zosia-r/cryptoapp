from textual.screen import Screen
from textual.widgets import Button, RadioSet, RadioButton, Label, Static
from textual.containers import Vertical, Horizontal

from app.core.report import get_signed_reports
from app.cryptography.rsa import verify_pdf_signature


class VerifyView(Screen):

    CSS_PATH = ["styles/base.tcss", "styles/dashboard.tcss"]

    def __init__(self, username: str):
        super().__init__()
        self.username = username
        self.reports_info = get_signed_reports(username)
        self.selected_index = None

    def compose(self):
        with Vertical(id="main-container"):
            yield Label("Verify report signature", id="title")

            if self.reports_info:
                yield RadioSet(
                    *[
                        RadioButton(
                            f"{r['year']} – report_year_{r['year']}.pdf",
                            id=f"report_{i}"
                        )
                        for i, r in enumerate(self.reports_info)
                    ],
                    id="year_selector"
                )
            else:
                yield Static("No signed reports found.", id="no_records")

            yield Static("", id="error_message")
            yield Static("", id="message")

            with Horizontal(id="button_row"):
                if self.reports_info:
                    yield Button("Verify", id="submit_btn")
                yield Button("Back", id="back_btn")

            yield Static("Cryptography 2025 – Zofia Różańska & Selina Zundel", id="credits")

    def on_radio_set_changed(self, event: RadioSet.Changed):
        self.selected_index = int(event.pressed.id.replace("report_", ""))

    def on_button_pressed(self, event):
        if event.button.id == "back_btn":
                self.app.pop_screen()

        elif event.button.id == "submit_btn":
            if self.selected_index is None:
                self.query_one("#error_message").update("Please select a report.")
                return
            
            self.query_one("#error_message").update("")
            self.query_one("#message").update("")

            report = self.reports_info[self.selected_index]
            ok = verify_pdf_signature(
                self.username,
                report["path"],
                report["sig"]
            )

            if ok:
                self.query_one("#message").update(
                    "✔ Signature is VALID! Report is authentic."
                )
            else:
                self.query_one("#error_message").update(
                    "✖ Signature is INVALID! Report may have been tampered with."
                )
