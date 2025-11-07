from textual.app import App
from textual.widgets import Footer, Header, Button, Static
from textual.containers import ScrollableContainer



class TimeDisplay(Static):
    pass


class Stopwatch(Static):
    """A simple stopwatch widget."""
    def compose(self):
        yield Button(label="Start", id="start_button", variant="success")
        yield Button(label="Stop", id="stop_button", variant="error")
        yield Button(label="Reset", id="reset_button", variant="warning")
        yield TimeDisplay("00:00:00.00")


class MyApp(App):
    BINDINGS = [
        ("d", "toggle_dark_mode", "Toggle dark mode"),
    ]
    def compose(self):
        """Compose the UI layout."""
        yield Header(show_clock=True)
        yield Footer()
        with ScrollableContainer():
            yield Stopwatch()
            yield Stopwatch()


    





        # action method -> name must start with 'action_'
        def action_toggle_dark_mode():
            self.dark = not self.dark

if __name__ == "__main__":
    MyApp().run()