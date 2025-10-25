import reflex as rx
import logging
from sqlalchemy import text
from app.utils.password import hash_password


class RegisterState(rx.State):
    error_message: str = ""
    success_message: str = ""

    @rx.event
    async def handle_registration(self, form_data: dict):
        """Handle the registration form submit."""
        self.error_message = ""
        self.success_message = ""
        username = form_data.get("username")
        email = form_data.get("email")
        password = form_data.get("password")
        if not all([username, email, password]):
            self.error_message = "All fields are required."
            return
        try:
            hashed_password = hash_password(password)
            async with rx.asession() as session:
                result = await session.execute(
                    text(
                        'SELECT id FROM "user" WHERE username = :username OR email = :email'
                    ),
                    {"username": username, "email": email},
                )
                if result.scalar_one_or_none() is not None:
                    self.error_message = "Username or email already exists."
                    return
                await session.execute(
                    text(
                        'INSERT INTO "user" (username, email, hashed_password, is_active) VALUES (:username, :email, :password, :is_active)'
                    ),
                    {
                        "username": username,
                        "email": email,
                        "password": hashed_password,
                        "is_active": True,
                    },
                )
                await session.commit()
            self.success_message = "Account created successfully! You can now log in."
            return rx.redirect("/login")
        except Exception as e:
            logging.exception(f"Registration error: {e}")
            self.error_message = "An unexpected error occurred during registration."