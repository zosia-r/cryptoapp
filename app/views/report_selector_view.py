from textual.screen import Screen
from textual.widgets import Button, RadioSet, RadioButton, Label, Static
from textual.containers import Vertical, Horizontal
from textual.message import Message
import asyncio

from app.core.report import ReportGenerator, get_years_for_user


class ReportSelectorView(Screen):

    CSS_PATH = ["styles/base.tcss", "styles/dashboard.tcss"]

    class ReportGenerated(Message):
        def __init__(self, pdf_path: str):
            super().__init__()
            self.pdf_path = pdf_path

    def __init__(self, username: str):
        super().__init__()
        self.username = username
        self.years_info = get_years_for_user(self.username)
        self.selected_year = None

    def compose(self):
        with Vertical(id="dialog"):
            yield Label("Select year to generate report:", id="title")
            yield RadioSet(
                *[
                    RadioButton(f"{year}: {count} records", id=f"year_{year}")
                    for year, count in self.years_info.items()
                ],
                id="year_selector"
            )
            yield Static("", id="error_message")
            yield Static("", id="message")
            with Horizontal(id="button_row"):
                yield Button("Submit", id="submit_btn")
                yield Button("Back", id="back_btn")
            yield Static("Cryptography 2025 – Zofia Różańska & Selina Zundel", id="credits")

    def on_radio_set_changed(self, event: RadioSet.Changed):
        self.selected_year = int(event.pressed.id.replace("year_", ""))

    def on_button_pressed(self, event: Button.Pressed):
        match event.button.id:
            case "back_btn":
                self.app.pop_screen()
            case "submit_btn":
                if self.selected_year is None:
                    self.query_one("#error_message", Static).update("Please select a year!")
                    return
                
                self.query_one("#error_message", Static).update("")
                message_widget = self.query_one("#message", Static)
                message_widget.update("Generating report...")
                asyncio.create_task(self.generate_report_async())

    async def generate_report_async(self):
        try:
            generator = ReportGenerator(self.username, self.selected_year)
            pdf_path = await asyncio.to_thread(generator.generate_pdf)
        
            message_widget = self.query_one("#message", Static)
            message_widget.update(f"Report generated successfully: {pdf_path}")
        
            await asyncio.sleep(2)
        
            self.app.pop_screen()
        except Exception as e:
            self.query_one("#error_message", Static).update(f"Error generating report: {e}")
