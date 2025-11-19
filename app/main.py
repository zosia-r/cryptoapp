from textual.app import App
from app.views.welcome_view import WelcomeView
from app.views.login_view import LoginView
from app.views.register_view import RegisterView
from app.views.dashboard_view import DashboardView


class CryptoApp(App):
    """Main Textual application"""

    def on_mount(self):
        # Register screens
        self.install_screen(WelcomeView(), "welcome")
        #self.install_screen(LoginView(), "login")
        #self.install_screen(RegisterView(), "register")
        #self.install_screen(DashboardView("zosia"), "dashboard")

        # Show welcome first
        self.push_screen("welcome")


if __name__ == "__main__":
    CryptoApp().run()
