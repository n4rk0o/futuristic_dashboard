import reflex as rx
from app.states.dashboard_state import DashboardState
from app.states.auth_state import AuthState


def user_menu() -> rx.Component:
    return rx.el.div(
        rx.el.button(
            rx.cond(
                AuthState.current_user,
                rx.el.div(
                    AuthState.user_initial,
                    class_name="w-8 h-8 rounded-full bg-cyan-500 flex items-center justify-center text-white font-bold",
                ),
                rx.el.div(class_name="w-8 h-8 rounded-full bg-gray-700"),
            ),
            id="user-menu-button",
            aria_expanded="false",
            aria_haspopup="true",
        ),
        class_name="relative ml-3",
    )


def dashboard_header() -> rx.Component:
    return rx.el.header(
        rx.el.div(
            rx.el.button(
                rx.icon(tag="menu", class_name="size-6"),
                on_click=DashboardState.toggle_mobile_sidebar,
                class_name="p-2 text-gray-400 hover:text-gray-200 md:hidden mr-4",
            ),
            rx.el.div(
                rx.icon(
                    tag="search",
                    class_name="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-500 pointer-events-none",
                ),
                rx.el.input(
                    placeholder="Search systems...",
                    class_name="w-full pl-10 pr-4 py-2 bg-gray-800 border border-gray-700 rounded-lg text-gray-300 focus:outline-none focus:ring-1 focus:ring-cyan-500 focus:border-cyan-500 placeholder-gray-500",
                ),
                class_name="relative flex-grow max-w-xs hidden sm:block",
            ),
            class_name="flex items-center",
        ),
        rx.el.div(
            rx.el.button(
                rx.icon(tag="bell", class_name="text-gray-400 hover:text-gray-200"),
                class_name="p-2 rounded-full hover:bg-gray-800",
            ),
            rx.el.button(
                rx.icon(tag="moon", class_name="text-gray-400 hover:text-gray-200"),
                class_name="p-2 rounded-full hover:bg-gray-800",
            ),
            rx.el.p(
                rx.cond(
                    AuthState.current_user, "Welcome, " + AuthState.current_user, ""
                ),
                class_name="text-sm text-gray-300 hidden sm:block",
            ),
            rx.el.button(
                "Logout",
                on_click=AuthState.logout,
                class_name="ml-4 px-3 py-1.5 text-xs font-medium text-gray-300 bg-gray-700 rounded-md hover:bg-gray-600",
            ),
            user_menu(),
            class_name="flex items-center space-x-1 sm:space-x-3",
        ),
        class_name="sticky top-0 z-30 flex items-center justify-between p-4 border-b border-gray-700/50 bg-gray-950/80 backdrop-blur-md",
    )