from textual.screen import Screen
from textual.widgets import Static
from textual.containers import Vertical

class DashboardView(Screen):
    """Simple dashboard showing a greeting to the user"""

    CSS_PATH = "styles/styles.tcss"

    def __init__(self, username: str):
        super().__init__()
        self.username = username

    def compose(self):
        with Vertical():
            yield Static(f"Hello, {self.username}!", id="greeting")
