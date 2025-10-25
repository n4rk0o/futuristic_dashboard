import reflex as rx
from app.states.callback_state import CallbackState


def callback_page() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon(tag="loader", class_name="h-12 w-12 text-cyan-400 animate-spin"),
            rx.el.h2(
                "Authenticating...",
                class_name="mt-6 text-2xl font-semibold text-gray-100",
            ),
            rx.el.p(
                "Please wait while we log you in.",
                class_name="mt-2 text-sm text-gray-400",
            ),
            rx.cond(
                CallbackState.error_message != "",
                rx.el.div(
                    rx.el.p(CallbackState.error_message),
                    rx.el.a(
                        "Try again",
                        href="/login",
                        class_name="mt-4 font-medium text-cyan-400 hover:text-cyan-300",
                    ),
                    class_name="mt-4 p-4 bg-red-900/50 border border-red-700/50 text-red-300 rounded-lg",
                ),
                None,
            ),
            class_name="text-center",
        ),
        class_name="min-h-screen flex items-center justify-center bg-gray-950",
        on_mount=CallbackState.on_load,
    )