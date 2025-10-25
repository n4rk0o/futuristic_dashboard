import reflex as rx
from typing import TypedDict
from sqlalchemy import text, func, or_


class Request(TypedDict):
    id: int
    service_type: str
    details: str
    status: str


class RequestHistoryState(rx.State):
    requests: list[Request] = []
    search_query: str = ""
    status_filter: str = "all"

    @rx.event
    async def fetch_requests(self):
        async with rx.asession() as session:
            statement = text("SELECT id, service_type, details, status FROM requests")
            result = await session.execute(statement)
            requests_data = result.fetchall()
            self.requests = [
                {
                    "id": r.id,
                    "service_type": r.service_type,
                    "details": r.details,
                    "status": r.status,
                }
                for r in requests_data
            ]

    @rx.var
    def filtered_requests(self) -> list[Request]:
        query = self.search_query.lower()
        return [
            r
            for r in self.requests
            if (
                self.status_filter == "all" or r["status"].lower() == self.status_filter
            )
            and (
                query == ""
                or query in r["service_type"].lower()
                or query in r["details"].lower()
            )
        ]