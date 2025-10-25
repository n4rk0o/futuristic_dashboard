import reflex as rx
from app.states.request_history_state import RequestHistoryState, Request


def request_row(request: Request) -> rx.Component:
    return rx.el.tr(
        rx.el.td(request["id"], class_name="px-4 py-3 text-sm text-gray-300"),
        rx.el.td(request["service_type"], class_name="px-4 py-3 text-sm text-gray-300"),
        rx.el.td(
            request["details"],
            class_name="px-4 py-3 text-sm text-gray-300 max-w-xs truncate",
        ),
        rx.el.td(
            rx.el.span(
                request["status"],
                class_name=rx.match(
                    request["status"].lower(),
                    (
                        "submitted",
                        "px-2 py-1 text-xs font-medium text-yellow-300 bg-yellow-900/50 rounded-full",
                    ),
                    (
                        "in progress",
                        "px-2 py-1 text-xs font-medium text-blue-300 bg-blue-900/50 rounded-full",
                    ),
                    (
                        "completed",
                        "px-2 py-1 text-xs font-medium text-green-300 bg-green-900/50 rounded-full",
                    ),
                    (
                        "failed",
                        "px-2 py-1 text-xs font-medium text-red-300 bg-red-900/50 rounded-full",
                    ),
                    "px-2 py-1 text-xs font-medium text-gray-300 bg-gray-700 rounded-full",
                ),
            ),
            class_name="px-4 py-3 text-sm",
        ),
        class_name="border-b border-gray-700/50 hover:bg-gray-800/50",
    )


def requests_history_page() -> rx.Component:
    return rx.el.main(
        rx.el.div(
            rx.el.h2(
                rx.icon(
                    tag="history",
                    class_name="mr-2 text-cyan-400 hidden sm:inline-block",
                ),
                "Requests History",
                class_name="text-lg sm:text-xl font-semibold text-gray-200 flex items-center mb-6",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.input(
                        placeholder="Search by service or details...",
                        on_change=RequestHistoryState.set_search_query,
                        class_name="w-full max-w-xs pl-4 pr-4 py-2 bg-gray-800 border border-gray-700 rounded-lg text-gray-300 focus:outline-none focus:ring-1 focus:ring-cyan-500 focus:border-cyan-500 placeholder-gray-500",
                    ),
                    rx.el.select(
                        rx.el.option("All Statuses", value="all"),
                        rx.el.option("Submitted", value="submitted"),
                        rx.el.option("In Progress", value="in progress"),
                        rx.el.option("Completed", value="completed"),
                        rx.el.option("Failed", value="failed"),
                        on_change=RequestHistoryState.set_status_filter,
                        default_value="all",
                        class_name="pl-4 pr-10 py-2 bg-gray-800 border border-gray-700 rounded-lg text-gray-300 focus:outline-none focus:ring-1 focus:ring-cyan-500 focus:border-cyan-500",
                    ),
                    class_name="flex items-center space-x-4 mb-4",
                ),
                rx.el.div(
                    rx.el.table(
                        rx.el.thead(
                            rx.el.tr(
                                rx.el.th(
                                    "ID",
                                    class_name="px-4 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider",
                                ),
                                rx.el.th(
                                    "Service Type",
                                    class_name="px-4 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider",
                                ),
                                rx.el.th(
                                    "Details",
                                    class_name="px-4 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider",
                                ),
                                rx.el.th(
                                    "Status",
                                    class_name="px-4 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider",
                                ),
                            )
                        ),
                        rx.el.tbody(
                            rx.foreach(
                                RequestHistoryState.filtered_requests, request_row
                            )
                        ),
                        class_name="min-w-full divide-y divide-gray-700/50",
                    ),
                    class_name="bg-gray-800/50 border border-gray-700/50 rounded-xl shadow-md backdrop-blur-sm overflow-x-auto",
                ),
            ),
            class_name="p-4 sm:p-6 flex-1 overflow-y-auto",
        ),
        on_mount=RequestHistoryState.fetch_requests,
    )