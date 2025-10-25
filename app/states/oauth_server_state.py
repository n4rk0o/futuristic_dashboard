import logging
import time
from authlib.oauth2.rfc6749 import (
    AuthorizationCodeGrant as _AuthorizationCodeGrant,
    RefreshTokenGrant as _RefreshTokenGrant,
    OAuth2Error,
)
from authlib.oauth2.rfc6750 import BearerTokenValidator
from authlib.oauth2.rfc7636 import CodeChallenge
import reflex as rx
from sqlalchemy import text
from app.models.auth_models import (
    User,
    OAuth2Token,
    OAuth2Client,
    OAuth2AuthorizationCode,
)
from authlib.oauth2.rfc6749 import (
    AuthorizationCodeGrant as _AuthorizationCodeGrant,
    RefreshTokenGrant as _RefreshTokenGrant,
)
from authlib.oauth2.rfc7636 import CodeChallenge
import reflex as rx
from sqlalchemy import text
from app.models.auth_models import OAuth2AuthorizationCode


class AuthorizationCodeGrant(_AuthorizationCodeGrant):
    async def save_authorization_code(self, code, request):
        async with rx.asession() as session:
            auth_code = OAuth2AuthorizationCode(
                code=code,
                client_id=request.client.client_id,
                redirect_uri=request.redirect_uri,
                scope=request.scope,
                user_id=request.user.id,
                code_challenge=request.data.get("code_challenge"),
                code_challenge_method=request.data.get("code_challenge_method"),
            )
            session.add(auth_code)
            await session.commit()
        return auth_code

    async def query_authorization_code(self, code, client):
        async with rx.asession() as session:
            result = await session.execute(
                text("SELECT * FROM oauth2authorizationcode WHERE code = :code"),
                {"code": code},
            )
            auth_code = result.fetchone()
            if auth_code:
                return auth_code
        return None

    async def delete_authorization_code(self, authorization_code):
        async with rx.asession() as session:
            await session.execute(
                text("DELETE FROM oauth2authorizationcode WHERE code = :code"),
                {"code": authorization_code.code},
            )
            await session.commit()

    async def authenticate_user(self, authorization_code):
        async with rx.asession() as session:
            result = await session.execute(
                text('SELECT * FROM "user" WHERE id = :id'),
                {"id": authorization_code.user_id},
            )
            return result.fetchone()


class RefreshTokenGrant(_RefreshTokenGrant):
    async def authenticate_refresh_token(self, refresh_token):
        async with rx.asession() as session:
            result = await session.execute(
                text("SELECT * FROM oauth2token WHERE refresh_token = :refresh_token"),
                {"refresh_token": refresh_token},
            )
            token = result.fetchone()
            if token:
                return token
        return None

    async def authenticate_user(self, credential):
        async with rx.asession() as session:
            result = await session.execute(
                text('SELECT * FROM "user" WHERE id = :id'), {"id": credential.user_id}
            )
            return result.fetchone()

    async def revoke_old_credential(self, credential):
        async with rx.asession() as session:
            credential.revoked = True
            session.add(credential)
            await session.commit()