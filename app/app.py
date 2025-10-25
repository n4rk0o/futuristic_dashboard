import reflex as rx
import os
from app.components.header import dashboard_header
from app.components.main_content import main_content
from app.components.right_sidebar import right_sidebar
from app.components.sidebar import sidebar
from app.pages.requests_page import requests_page
from app.pages.requests_history_page import requests_history_page
from app.states.dashboard_state import DashboardState
from app.oauth import userinfo_endpoint


def index() -> rx.Component:
    return rx.el.div(
        sidebar(),
        rx.el.div(
            dashboard_header(),
            rx.el.div(
                rx.match(
                    DashboardState.active_nav,
                    ("Dashboard", main_content()),
                    ("Requests", requests_page()),
                    ("Requests History", requests_history_page()),
                    main_content(),
                ),
                right_sidebar(),
                class_name="flex flex-1 overflow-hidden",
            ),
            class_name="flex flex-col flex-1 overflow-hidden",
        ),
        rx.cond(
            DashboardState.mobile_sidebar_open,
            rx.el.div(
                on_click=DashboardState.toggle_mobile_sidebar,
                class_name="fixed inset-0 bg-black/50 z-30 md:hidden",
            ),
            None,
        ),
        class_name="flex h-screen bg-gray-950 text-gray-300 relative",
        on_mount=[DashboardState.update_time, AuthState.check_authentication],
    )


import logging
from authlib.oauth2.rfc6749.errors import OAuth2Error
from app.states.auth_state import AuthState
from app.oauth import create_oauth_server
from app.pages.login_page import login_page
from app.pages.callback_page import callback_page
from app.pages.register_page import register_page

app = rx.App(
    theme=rx.theme(appearance="light"),
    stylesheets=[
        "https://cdnjs.cloudflare.com/ajax/libs/feather-icons/4.29.0/feather.min.js"
    ],
)
app.add_page(index)
app.add_page(login_page, route="/login")
app.add_page(register_page, route="/register")
app.add_page(callback_page, route="/callback")
from fastapi import Request, Response


async def token_endpoint(request: Request):
    try:
        oauth_server = create_oauth_server()
        return await oauth_server.create_token_response(request)
    except OAuth2Error as e:
        logging.exception(f"OAuth2 error in token endpoint: {e}")
        return Response(
            e.get_body(), status_code=e.status_code, headers=e.get_headers()
        )


async def auth_endpoint(request: Request):
    from sqlalchemy import text

    async with rx.asession() as session:
        result = await session.execute(text('SELECT * FROM "user" LIMIT 1'))
        user = result.fetchone()
        if not user:
            await session.execute(
                text(
                    'INSERT INTO "user" (username, email, hashed_password) VALUES (:username, :email, :password)'
                ),
                {
                    "username": "demo_user",
                    "email": "demo@example.com",
                    "password": "demo",
                },
            )
            await session.commit()
            result = await session.execute(text('SELECT * FROM "user" LIMIT 1'))
            user = result.fetchone()
    grant_user = user
    try:
        oauth_server = create_oauth_server()
        return await oauth_server.create_authorization_response(
            request, grant_user=grant_user
        )
    except OAuth2Error as e:
        logging.exception(f"OAuth2 error in auth endpoint: {e}")
        return Response(
            e.get_body(), status_code=e.status_code, headers=e.get_headers()
        )


from fastapi import FastAPI

api = FastAPI()
api.add_api_route("/oauth/token", token_endpoint, methods=["POST"])
api.add_api_route("/oauth/authorize", auth_endpoint, methods=["GET", "POST"])
api.add_api_route("/oauth/userinfo", userinfo_endpoint, methods=["GET"])
app.api_transformer = api