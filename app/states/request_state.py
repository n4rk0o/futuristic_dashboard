import logging
import os
from typing import TypedDict
import reflex as rx
import requests
from sqlalchemy import text


class Request(TypedDict):
    id: int
    service_type: str
    details: str
    status: str


class Service(TypedDict):
    id: int
    name: str


class RequestState(rx.State):
    services: list[str] = []
    form_data: dict = {}
    error_message: str = ""

    async def _create_tables_if_not_exist(self, asession):
        await asession.execute(
            text(
                "CREATE TABLE IF NOT EXISTS services (id SERIAL PRIMARY KEY, name VARCHAR);"
            )
        )
        await asession.execute(
            text(
                "CREATE TABLE IF NOT EXISTS requests (id SERIAL PRIMARY KEY, service_type VARCHAR, details TEXT, status VARCHAR);"
            )
        )
        result = await asession.execute(text("SELECT COUNT(*) FROM services"))
        if result.scalar_one() == 0:
            await asession.execute(
                text(
                    "INSERT INTO services (name) VALUES ('Data Analysis'), ('Model Training'), ('Resource Provisioning');"
                )
            )
        await asession.commit()

    @rx.event
    async def on_load(self):
        self.error_message = ""
        try:
            async with rx.asession() as asession:
                await self._create_tables_if_not_exist(asession)
                result = await asession.execute(text("SELECT name FROM services"))
                services_result = result.all()
                self.services = [row[0] for row in services_result]
        except Exception as e:
            logging.exception(f"Database error: {e}")
            self.error_message = "Could not connect to the database or load services."

    @rx.event
    async def handle_submit(self, form_data: dict):
        self.form_data = form_data
        self.error_message = ""
        try:
            api_url = os.getenv("API_URL", "https://api.example.com/requests")
            response = requests.post(api_url, json=form_data)
            response.raise_for_status()
            api_response = response.json()
            request_id = api_response.get("request_id", "N/A")
            async with rx.asession() as asession:
                await asession.execute(
                    text(
                        "INSERT INTO requests (service_type, details, status) VALUES (:service_type, :details, :status)"
                    ),
                    {
                        "service_type": form_data["service_type"],
                        "details": form_data["details"],
                        "status": "submitted",
                    },
                )
                await asession.commit()
            return rx.toast.info(f"Request submitted successfully! ID: {request_id}")
        except requests.exceptions.RequestException as e:
            logging.exception(f"API Error: {e}")
            self.error_message = "Failed to submit request to the API."
            return rx.toast.error("API submission failed. Please try again later.")
        except Exception as e:
            logging.exception(f"Database/Form Error: {e}")
            self.error_message = "An unexpected error occurred."
            return rx.toast.error("An unexpected error occurred.")