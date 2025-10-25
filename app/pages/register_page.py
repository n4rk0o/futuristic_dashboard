import reflex as rx
from app.states.register_state import RegisterState


def register_page() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon(tag="hexagon", class_name="h-10 w-10 text-cyan-400"),
                rx.el.h2(
                    "Create your NEXUS OS account",
                    class_name="mt-6 text-center text-3xl font-extrabold text-gray-100",
                ),
                class_name="mx-auto w-full max-w-md",
            ),
            rx.cond(
                RegisterState.error_message != "",
                rx.el.div(
                    rx.el.p(RegisterState.error_message),
                    class_name="bg-red-900/50 border border-red-700/50 text-red-300 rounded-lg p-4 my-4",
                ),
                None,
            ),
            rx.cond(
                RegisterState.success_message != "",
                rx.el.div(
                    rx.el.p(RegisterState.success_message),
                    class_name="bg-green-900/50 border border-green-700/50 text-green-300 rounded-lg p-4 my-4",
                ),
                None,
            ),
            rx.el.form(
                rx.el.input(
                    name="username",
                    placeholder="Username",
                    type="text",
                    class_name="w-full px-4 py-2 bg-gray-800 border border-gray-700 rounded-lg text-gray-300 focus:outline-none focus:ring-1 focus:ring-cyan-500 focus:border-cyan-500 placeholder-gray-500",
                ),
                rx.el.input(
                    name="email",
                    placeholder="Email Address",
                    type="email",
                    class_name="w-full px-4 py-2 bg-gray-800 border border-gray-700 rounded-lg text-gray-300 focus:outline-none focus:ring-1 focus:ring-cyan-500 focus:border-cyan-500 placeholder-gray-500",
                ),
                rx.el.input(
                    name="password",
                    placeholder="Password",
                    type="password",
                    class_name="w-full px-4 py-2 bg-gray-800 border border-gray-700 rounded-lg text-gray-300 focus:outline-none focus:ring-1 focus:ring-cyan-500 focus:border-cyan-500 placeholder-gray-500",
                ),
                rx.el.button(
                    "Create Account",
                    type="submit",
                    class_name="w-full flex justify-center py-3 px-4 border border-transparent rounded-lg shadow-sm text-sm font-medium text-white bg-cyan-600 hover:bg-cyan-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-cyan-500 focus:ring-offset-gray-900 transition-colors duration-200",
                ),
                rx.el.a(
                    "Back to Login",
                    href="/login",
                    class_name="font-medium text-cyan-400 hover:text-cyan-300 text-center block mt-4",
                ),
                on_submit=RegisterState.handle_registration,
                reset_on_submit=True,
                class_name="mt-8 space-y-6",
            ),
            class_name="w-full max-w-md space-y-8 p-10 bg-gray-800/50 border border-gray-700/50 rounded-xl shadow-md backdrop-blur-sm",
        ),
        class_name="min-h-screen flex items-center justify-center bg-gray-950 text-gray-300 px-4 sm:px-6 lg:px-8",
    )