import reflex as rx
import httpx
import logging
from app.states.auth_state import AuthState


class CallbackState(rx.State):
    error_message: str = ""

    @rx.event
    async def on_load(self):
        code = self.router.page.params.get("code")
        if not code:
            self.error_message = "Authorization code not found."
            return
        try:
            token_url = "http://localhost:8000/oauth/token"
            data = {
                "grant_type": "authorization_code",
                "code": code,
                "client_id": "your_client_id",
                "redirect_uri": "http://localhost:3000/callback",
            }
            async with httpx.AsyncClient() as client:
                response = await client.post(token_url, data=data)
                response.raise_for_status()
                token_data = response.json()
            access_token = token_data["access_token"]
            userinfo_url = "http://localhost:8000/oauth/userinfo"
            headers = {"Authorization": f"Bearer {access_token}"}
            async with httpx.AsyncClient() as client:
                user_response = await client.get(userinfo_url, headers=headers)
                user_response.raise_for_status()
                user_data = user_response.json()
            auth_state = await self.get_state(AuthState)
            auth_state.login(
                username=user_data["name"], user_id=user_data["sub"], token=access_token
            )
            return rx.redirect("/")
        except httpx.HTTPStatusError as e:
            logging.exception(f"HTTP error during token exchange: {e.response.text}")
            self.error_message = (
                f"Failed to authenticate: {e.response.status_code} - {e.response.text}"
            )
        except Exception as e:
            logging.exception(f"Callback error: {e}")
            self.error_message = "An unexpected error occurred during authentication."