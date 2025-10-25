import reflex as rx
from app.states.request_state import RequestState


def requests_page() -> rx.Component:
    return rx.el.div(
        rx.el.h2(
            rx.icon(
                tag="file-text", class_name="mr-2 text-cyan-400 hidden sm:inline-block"
            ),
            "Create New Request",
            class_name="text-lg sm:text-xl font-semibold text-gray-200 flex items-center mb-6",
        ),
        rx.cond(
            RequestState.error_message != "",
            rx.el.div(
                rx.el.p(RequestState.error_message),
                class_name="bg-red-900/50 border border-red-700/50 text-red-300 rounded-lg p-4 mb-6",
            ),
            None,
        ),
        rx.el.form(
            rx.el.div(
                rx.el.label(
                    "Service Type",
                    html_for="service_type",
                    class_name="block text-sm font-medium text-gray-400 mb-2",
                ),
                rx.el.select(
                    rx.foreach(
                        RequestState.services,
                        lambda service: rx.el.option(service, value=service),
                    ),
                    name="service_type",
                    id="service_type",
                    class_name="w-full pl-4 pr-10 py-2 bg-gray-800 border border-gray-700 rounded-lg text-gray-300 focus:outline-none focus:ring-1 focus:ring-cyan-500 focus:border-cyan-500",
                ),
                class_name="mb-4",
            ),
            rx.el.div(
                rx.el.label(
                    "Details",
                    html_for="details",
                    class_name="block text-sm font-medium text-gray-400 mb-2",
                ),
                rx.el.textarea(
                    name="details",
                    id="details",
                    placeholder="Provide detailed information about your request...",
                    class_name="w-full h-32 px-4 py-2 bg-gray-800 border border-gray-700 rounded-lg text-gray-300 focus:outline-none focus:ring-1 focus:ring-cyan-500 focus:border-cyan-500 placeholder-gray-500",
                ),
                class_name="mb-6",
            ),
            rx.el.button(
                "Submit Request",
                type="submit",
                class_name="px-6 py-3 font-medium text-white bg-cyan-600 hover:bg-cyan-700 rounded-lg focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-gray-950 focus:ring-cyan-500 transition-colors duration-200 disabled:opacity-50",
            ),
            on_submit=RequestState.handle_submit,
            reset_on_submit=True,
            class_name="bg-gray-800/50 border border-gray-700/50 rounded-xl p-6 shadow-md backdrop-blur-sm",
        ),
        on_mount=RequestState.on_load,
        class_name="p-4 sm:p-6 flex-1 overflow-y-auto",
    )