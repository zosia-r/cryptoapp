from textual.app import App
from app.views.welcome_view import WelcomeView

class CryptoApp(App):
    """Main Textual application"""
    def on_mount(self):
        self.push_screen(WelcomeView())