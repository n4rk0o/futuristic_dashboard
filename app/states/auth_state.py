import reflex as rx
from typing import Optional
from app.models.auth_models import User

OAUTH_URL = "/oauth/authorize?response_type=code&client_id=your_client_id&redirect_uri=http://localhost:3000/callback&scope=openid profile email"


class AuthState(rx.State):
    current_user: Optional[str] = None
    user_id: Optional[int] = None
    is_authenticated: bool = False
    access_token: Optional[str] = None

    @rx.var
    def get_current_user(self) -> Optional[str]:
        return self.current_user

    @rx.var
    def user_initial(self) -> str:
        return self.current_user[0].upper() if self.current_user else ""

    @rx.event
    async def check_authentication(self) -> rx.event.EventSpec:
        if not self.is_authenticated:
            return rx.redirect(OAUTH_URL)

    @rx.event
    def login(self, username: str, user_id: int, token: str):
        self.current_user = username
        self.user_id = user_id
        self.access_token = token
        self.is_authenticated = True

    @rx.event
    def logout(self) -> rx.event.EventSpec:
        self.current_user = None
        self.user_id = None
        self.access_token = None
        self.is_authenticated = False
        return rx.redirect("/login")