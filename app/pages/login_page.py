import reflex as rx

OAUTH_URL = "/oauth/authorize?response_type=code&client_id=your_client_id&redirect_uri=http://localhost:3000/callback&scope=openid profile email"


def login_page() -> rx.Component:
    """A page to redirect the user to the OAuth provider."""
    return rx.el.div(
        rx.el.div(
            rx.icon(tag="loader", class_name="h-12 w-12 text-cyan-400 animate-spin"),
            rx.el.h2(
                "Redirecting to login...",
                class_name="mt-6 text-2xl font-semibold text-gray-100",
            ),
            rx.el.p(
                "Please wait while we prepare the authentication service.",
                class_name="mt-2 text-sm text-gray-400",
            ),
            class_name="text-center",
        ),
        class_name="min-h-screen flex items-center justify-center bg-gray-950",
        on_mount=rx.redirect(OAUTH_URL),
    )