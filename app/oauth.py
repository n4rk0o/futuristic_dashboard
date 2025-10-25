import logging
import time
import reflex as rx
from authlib.oauth2.rfc6749 import AuthorizationServer, ResourceProtector
from authlib.oauth2.rfc6750 import BearerTokenValidator
from sqlalchemy import text
from app.models.auth_models import OAuth2Token
from app.states.oauth_server_state import AuthorizationCodeGrant, RefreshTokenGrant


async def query_client(client_id: str):
    async with rx.asession() as session:
        result = await session.execute(
            text("SELECT * FROM oauth2client WHERE client_id = :client_id"),
            {"client_id": client_id},
        )
        return result.fetchone()


from fastapi import Request


async def save_token(token: dict, request: Request):
    client = request.scope["client"]
    async with rx.asession() as session:
        if request.scope.get("user"):
            user_id = request.scope["user"].id
        else:
            result = await session.execute(
                text("SELECT user_id FROM oauth2token WHERE id = :id"),
                {"id": request.credential.id},
            )
            user_id = result.scalar_one()
        db_token = OAuth2Token(
            user_id=user_id,
            client_id=client.client_id,
            token_type=token["token_type"],
            access_token=token["access_token"],
            refresh_token=token.get("refresh_token"),
            scope=token["scope"],
            expires_in=token["expires_in"],
            issued_at=token["issued_at"],
        )
        session.add(db_token)
        await session.commit()


def create_oauth_server() -> AuthorizationServer:
    server = AuthorizationServer()
    server.query_client = query_client
    server.save_token = save_token
    server.register_grant(AuthorizationCodeGrant)
    server.register_grant(RefreshTokenGrant)
    return server


class MyBearerTokenValidator(BearerTokenValidator):
    async def authenticate_token(self, token_string: str):
        async with rx.asession() as session:
            result = await session.execute(
                text("SELECT * FROM oauth2token WHERE access_token = :access_token"),
                {"access_token": token_string},
            )
            return result.fetchone()

    def token_revoked(self, token) -> bool:
        return token.revoked


require_oauth = ResourceProtector()
require_oauth.register_token_validator(MyBearerTokenValidator())
from fastapi import Response, HTTPException


async def userinfo_endpoint(request: Request):
    try:
        token = require_oauth.validate_request(scopes=[], request=request)
    except OAuth2Error as e:
        logging.exception(f"OAuth2 validation error in userinfo_endpoint: {e}")
        raise HTTPException(
            status_code=e.status_code,
            detail=e.description,
            headers={"WWW-Authenticate": "Bearer"},
        )
    async with rx.asession() as session:
        result = await session.execute(
            text('SELECT * FROM "user" WHERE id = :user_id'), {"user_id": token.user_id}
        )
        user = result.fetchone()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return {"sub": user.id, "name": user.username, "email": user.email}